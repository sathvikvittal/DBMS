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
    st.header(":red[User not logged in]")
    time.sleep(5)
    switch_page("Login")
else:
    logout = st.button("Logout")
    if logout:
        del(st.session_state.user)

        logout = False
        time.sleep(1)
        switch_page("Login")
    st.session_state.dis = False
    sql_query=''
    query = ''
    if 'admin' in st.session_state:
        type1 = "SELLER"
        
    else:
        type1 = "USER"

    sql_query = f"""
    SELECT * FROM (SELECT * FROM {type1} WHERE {type1}_ID = '{st.session_state.user}') T
    """
    cursor.execute(sql_query)
    query = cursor.fetchone()

    st.header(":red[Your Profile]")
    
    print(query)
    choice = st.selectbox("Pick one", ["Edit Password", "Edit User details"])
    if choice == "Edit User details":
        st.text_input("Your username : ",value=query[0],disabled=True)

        first_name = st.text_input("Your First Name : ",value=query[1])
        middle_name = st.text_input("Your Middle Name : ",value=query[2])
        last_name = st.text_input("Your First Name : ",value=query[3])
        st.text_input("Your emailId : ",value=query[6],disabled=True)
        if type1 == "USER":
            phone_number = st.number_input("Your Phone Number : ",value=query[7])
            adr = st.text_input("Your Address : ",value=query[8])
        else:
            shop_name = st.text_input("Your Shop Name : ",value=query[6])
    
    else:
        pass1 =  st.text_input("Enter Old Password ",type='password')
        pass2 =  st.text_input("Enter New Password ",type='password')
        if len(pass2)<8:
            st.session_state.dis = True
            st.warning("Please enter atleast 8 characters in password")
        pass3 =  st.text_input("Re-enter New Password ",type='password')

        if pass3 != pass2:
            st.session_state.dis = True
            st.warning("Password does not match")

    submitted = st.button("Update",disabled=st.session_state.dis)

    if submitted:
        if choice == 'Edit Password':
            if type1 == 'SELLER':
                cursor.callproc("UpdatePassSeller",(f"'{pass2}'",f"'{st.session_state.user}'"))
            cursor.execute(f"""
                UPDATE {type1} SET PASSWD = '{pass2}' WHERE {type1}_ID = '{st.session_state.user}'
            """)
            st.success("Updated successfully")
            con.commit()
        else:
            if type1 == "SELLER":
                cursor.execute(f"""
                    UPDATE {type1} SET FIRSTNAME = '{first_name}',MIDDLENAME = '{middle_name}',
                    LASTNAME = '{last_name}',SHOP_NAME = '{shop_name}' WHERE {type1}_ID = '{st.session_state.user}' 
                """)
                
            else:
                cursor.execute(f"""
                    UPDATE {type1} SET FIRSTNAME = '{first_name}',MIDDLENAME = '{middle_name}',
                    LASTNAME = '{last_name}',ADDR = '{adr}',PHONENO = {phone_number} WHERE {type1}_ID = '{st.session_state.user}' 
                """)
            st.success("Updated successfully")
            con.commit()
        time.sleep(0.75)
        st.rerun()
            