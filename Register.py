import streamlit as st
import time
import re

st.header("Register User")
# Create a form for user registration
st.session_state = True
st.write("\n")
with st.form('register',clear_on_submit=True):

    first_name = st.text_input('First Name')
    if first_name == "":
        st.write("Enter First Name")
        st.session_state = False

    middle_name = st.text_input('Middle Name')

    last_name = st.text_input('Last Name')
    if last_name == "":
        st.write("Enter Last Name")
        st.session_state = False

    email = st.text_input('Email')
    if email != "":
        if not re.search("\w*@\w*.com",email):
            st.write("Invalid email format")
            st.session_state = False
    elif email == "":
        st.write("Enter Email")
        st.session_state = False

    password1 = st.text_input('Password', type='password')
    if len(password1) <= 7:
        st.write("Please enter atleast 8 characters in password")
        st.session_state.disabled = False
    
    password2 = st.text_input('Confirm Password', type='password')
    if password1 != password2:
        st.write(f"Passwords do not match! Please try again.")
        st.session_state = False
    
    submitted = st.form_submit_button("Submit",disabled=st.session_state)



    