import streamlit as st
import streamlit as st
import time
import mysql.connector
import re
from sqlconfig import connect
from streamlit_extras.switch_page_button import switch_page
import os
from PIL import Image

con = connect()
cursor = con.cursor()

if 'user' not in st.session_state:
    st.write("User not logged in")
    time.sleep(5)
    switch_page("Login")
else:
    st.session_state.dis = False
    if 'admin' in st.session_state:
        type1 = "SELLER"
    else:
        type1 = "USER"
    st.header(":red[Your Profile]")
    cursor.execute(f"""
    SELECT * FROM (SELECT * FROM {type1} WHERE {type1}_ID = '{st.session_state.user}') T
    """)
    query = cursor.fetchone()
    choice = st.selectbox("Pick one", ["Edit Password", "Edit User details"])
    if choice == "Edit User details":
        st.text_area("Your username : ",placeholder=query[0],disabled=True)

        first_name = st.text_area("Your First Name : ",placeholder=query[1])
        middle_name = st.text_area("Your Middle Name : ",placeholder=query[2])
        last_name = st.text_area("Your First Name : ",placeholder=query[3])
        st.text_area("Your emailId : ",placeholder=query[5],disabled=True)
        if type1 == "USER":
            phone_number = st.number_input("Your Phone Number : ",placeholder=query[6])
            adr = st.text_area("Your Address : ",placeholder=query[7])
        else:
            shop_name = st.text_area("Your Shop Name : ",placeholder=query[6])
    
    else:
        pass1 =  st.text_area("Enter Old Password ",type='password')
        pass2 =  st.text_area("Enter New Password ",type='password')
        if len(pass2)<8:
            st.session_state.dis = True
            st.warning("Please enter atleast 8 characters in password")
        pass3 =  st.text_area("Re-enter New Password ",type='password')

        if pass3 != pass2:
            st.session_state.dis = True
            st.warning("Password does not match")

    submitted = st.button("Register",disabled=st.session_state.dis)

    if submitted:
        if choice == 'Edit Password':
            cursor.execute(f"""
                UPDATE {type1} SET PASSWD = '{pass2}' WHERE {type1}_ID = '{st.session_state.user}'
            """)
            con.commit()
        else:
            if type1 == "SELLER":
                cursor.execute(f"""
                    UPDATE {type1} SET FIRST_NAME = '{first_name}',MIDDLE_NAME = '{middle_name}',
                    LAST_NAME = '{last_name}',SHOP_NAME = '{shop_name}' WHERE {type1}_ID = '{st.session_state.user}' 
                """)
            else:
                cursor.execute(f"""
                    UPDATE {type1} SET FIRST_NAME = '{first_name}',MIDDLE_NAME = '{middle_name}',
                    LAST_NAME = '{last_name}',ADDR = '{adr}',PHONENO = {phone_number} WHERE {type1}_ID = '{st.session_state.user}' 
                """)
            con.commit()
        
        switch_page("Profile")
            