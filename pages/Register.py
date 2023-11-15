import streamlit as st
import time
import mysql.connector
import re
from sqlconfig import connect

con = connect()
cursor = con.cursor()

st.header(":red[Register User]")
# Create a form for user registration
st.session_state.dis = False
st.write("\n")

user_name = st.text_input('User/Seller name')
if user_name == "":
    st.warning("Enter User Name")
    st.session_state.dis = True

first_name = st.text_input('First Name')
if first_name == "":
    st.warning("Enter First Name")
    st.session_state.dis = True

middle_name = st.text_input('Middle Name')

last_name = st.text_input('Last Name')
if last_name == "":
    st.warning("Enter Last Name")
    st.session_state.dis = True

email = st.text_input('Email')
if email != "":
    if not re.search("\w*@\w*.com",email):
        st.warning("Invalid email format")
        st.session_state.dis = True
elif email == "":
    st.session_state.dis = True
    st.warning("Enter Email")

password1 = st.text_input('Password', type='password')
if len(password1) <= 7:
    st.session_state.dis = True
    st.warning("Please enter atleast 8 characters in password")


password2 = st.text_input('Confirm Password', type='password')
if password1 != password2:
    st.session_state.dis = True
    st.warning("Passwords do not match! Please try again")

choice = st.selectbox("Pick one", ["Seller", "User"])
if choice == "User":
    phone = st.text_input("Phone Number")
    if phone == "":
        st.warning("Enter Phone number")
        st.session_state.dis = True
    address = st.text_input("Address")
    if address == "":
        st.warning("Enter Address")
        st.session_state.dis = True
else:
    shop_name =  st.text_input("Shop Name")
    if shop_name == "":
        st.warning("Enter Shop Name")
        st.session_state.dis = True

submitted = st.button("Register",disabled=st.session_state.dis)

if submitted:
    # Add the data to database here
    hi = True
    cursor.execute(f"SELECT * FROM {choice} WHERE {choice}_ID = {user_name}")
    if cursor.fetchall():
        st.error("This ID already exists, please use a different ID.")
    else:
        cursor.execute(f"SELECT * FROM {choice} WHERE EMAIL = {email}")
        if cursor.fetchall():
            st.error("This email is already registered with another account.")
        else:
            if choice == 'Seller':
                query = f"""INSERT INTO seller (SELLER_ID,FIRSTNAME,MIDDLENAME,LASTNAME,EMAIL,PASSWORD,SHOP_NAME
                ) VALUES ('{user_name}','{first_name}','{middle_name}','{last_name}','{email}','{password1}','{shop_name}'
                ); """
                print(query)
                cursor.execute(query)
                con.commit()
            else:
                query = f"""INSERT INTO User (USERNAME,FIRSTNAME,MIDDLENAME,LASTNAME,PASSWORD,EMAIL,PHONE,ADDRESS)
                VALUES ('{user_name}','{first_name}','{middle_name}','{last_name}','{password1}','{email}','{phone}','{address}'
                ); """
                print(query)
                cursor.execute(query)
                con.commit()
        
        time.sleep(1)
        st.rerun()
        st.success('Registration Successful')