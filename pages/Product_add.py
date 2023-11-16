import streamlit as st
import time
import mysql.connector
import re
from sqlconfig import connect
from streamlit_extras.switch_page_button import switch_page
import os
from PIL import Image

conn = connect()
cursor = conn.cursor()

if 'user' in st.session_state and 'admin' in st.session_state and st.session_state["admin"] == "True":
    st.header(":red[Add Products]")
    st.session_state.dis = False
    st.write("\n")

    prod_id = st.text_input("Prod ID")
    if prod_id == "":
        st.warning("Enter Prod ID")
        st.session_state.dis = True

    prod_name = st.text_input('Product Name')
    if prod_name == "":
        st.warning("Enter Product Name")
        st.session_state.dis = True

    quantity = st.number_input('Quantity',step=1,min_value=0)
    if not quantity:
        st.warning("Enter Quantity available in Stock")
        st.session_state.dis = True

    price = st.number_input('Price',step=1,min_value=0)
    if not price:
        st.warning("Enter the price of the product")
        st.session_state.dis = True

    descr = st.text_input('Product Description')
    if descr == "":
        st.warning("Enter details about product")
        st.session_state.dis = True

    category = st.text_input('Category')
    if category == "":
        st.warning("Enter Category")
        st.session_state.dis = True
    
    uploaded_file = st.file_uploader(label="Upload Image", type=["jpg"])
    if uploaded_file is not None:
        with open(os.path.join("../images/", f"{prod_id}.jpg"), "wb") as f:
            f.write(uploaded_file.getbuffer())
        image = Image.open(uploaded_file)
        st.image(image)

        
    submitted = st.button("Register",disabled=st.session_state.dis)

    if submitted:
        cursor.execute(f"SELECT * FROM (SELECT * FROM PRODUCT WHERE PRODUCT_ID = '{prod_id}')")
        if cursor.fetchall():
            st.error("This ID already exists, please use a different ID.")
        else:
            cursor.execute(f"""INSERT INTO PRODUCT(PRODUCT_ID,SELLER_ID,PRODUCT_NAME,QTY,PRICE,DETAILS,CATEGORY)
                        VALUES('{prod_id}','{st.session_state.user}','{prod_name}',{quantity},{price},'{descr}','{category}')
                        ;
                        """)
            conn.commit()
            time.sleep(2)
            st.rerun()
            