import streamlit as st
import time
import mysql.connector
import re
from sqlconfig import connect

conn = connect()
cursor = conn.cursor()

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

descr = st.text_input('Product Description')
if descr == "":
    st.warning("Enter details about product")
    st.session_state.dis = True

category = st.text_input('Category')
if category == "":
    st.warning("Enter Category")
    st.session_state.dis = True
    
submitted = st.button("Register",disabled=st.session_state.dis)
