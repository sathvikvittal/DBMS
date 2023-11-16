import streamlit as st
import pandas as pd
from sqlconfig import connect
import uuid

if 'user' in st.session_state:
    user = st.session_state.user
    con = connect()
    cursor = con.cursor()
    cursor.execute(f'select * from (select * from orders where user_id = "{user}") T')
    orders = cursor.fetchall()
    df = pd.DataFrame(orders,columns=['Order_ID','Product_ID','User_ID','Address','Mode Of Payment','Quantity'])
    df.drop(["User_ID"],axis=1,inplace=True)
    st.write(df)

    pid = st.selectbox("Select Product To Review: ",df['Product_ID'])
    rating = st.number_input("Rate The product on a Scale of 5",min_value=1,max_value=5,step=1)
    review = st.text_input("Enter Review: ")
    submit = st.button("Submit Review",type='primary')
    if submit and review!="":
        cursor.execute(f'Select * from review where product_id="{pid}" and user_id="{user}"')
        if(len(cursor.fetchall()) == 0):
            rid = str(uuid.uuid4().hex[:20].upper())
            cursor.execute(f"Insert into review values('{rid}','{pid}','{user}','{rating}','{review}')")
            con.commit()
            st.success("Review Added Successfully")
        else:
            st.error("You have already Reviewed this order")
    elif submit and review == "":
        st.error("Comments Cannot be Empty")

