import streamlit as st
import pandas as pd
from sqlconfig import connect

if 'user' in st.session_state:
    user = st.session_state.user
    con = connect()
    cursor = con.cursor()
    cursor.execute(f'select * from (select * from orders where user_id = "{user}") T')
    orders = cursor.fetchall()
    df = pd.DataFrame(orders,columns=['Order_ID','Product_ID','User_ID','Address','Mode Of Payment','Quantity'])
    df.drop(["User_ID"],axis=1,inplace=True)

    st.write(df)

