import streamlit as st
from sqlconfig import connect
import time
from streamlit_extras.switch_page_button import switch_page


con = connect()
cursor = con.cursor()
st.header(':red[Login]')

option = st.selectbox(
    'Login as Seller/User?',
    ( 'User','Seller'))
placeholder=st.empty()
with st.form('login',clear_on_submit=True):
    st.markdown("Enter your credentials")
    username = st.text_input('Username')
    passwd = st.text_input('Password',type='password')
    submit = st.form_submit_button("Login")

    if(submit and option == 'Seller'):
        cursor.execute(f'Select passwd,shop_name from seller where seller_id = "{username}"')
        user = cursor.fetchall()
        print(user)
        if(len(user)>0):
            actual_passwd = user[0][0]
            if(actual_passwd == passwd):
                st.success('Logged In Successfully')
                time.sleep(1.5)
                st.session_state.admin = 'True'
                switch_page('MainPage')
            else:
                st.error("Invalid Username/Password")
        else:
            st.error("Invalid Username/Password")
    
    if(submit and option == 'User'):
        cursor.execute(f'Select passwd,firstname from USER where user_id = "{username}"')
        user = cursor.fetchall()
        print(user)
        if(len(user)>0):
            actual_passwd = user[0][0]
            if(actual_passwd == passwd):
                st.success('Logged In Successfully')
                time.sleep(1.5)
                switch_page('MainPage')
            else:
                st.error("Invalid Username/Password")
        else:
            st.error("Invalid Username/Password")




        