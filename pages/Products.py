import streamlit as st
import mysql.connector
import pandas as pd
from PIL import Image
from sqlconfig import connect
import time
import os
con = connect()
cursor = con.cursor()

# Query all products from the database
image_path = os.path.join(os.getcwd(),'images')

# df = pd.DataFrame(products, columns=['ID','Seller', 'Name','Qty', 'Price', 'Description','Category'])

# con.close()

def p1():
    st.header(f':red[Our Products]',divider='red')
    name = st.text_input('Search')

    cursor.execute('Select distinct category from product')
    all_cat= cursor.fetchall()
    all_cat = [i[0] for i in all_cat]
    all_cat.insert(0,"Any")

    category = st.selectbox("Filter By Category",all_cat)
    sort = st.selectbox("Sort by price",['Any','Ascending','Descending'])

    #get filtered procduct list
    query = 'select * from product'
    if(name != ""):
        if(" where " not in query):
            query+=" where "
        query+=f'product_name like \"%{name}%\"'

    if(category != "Any"):
        if(" where " not in query):
            query+=" where "
        else:
            query+=" and "
        query+=f'category="{category}"'
    
    if(sort == 'Ascending'):
        query+=f" order by price"
    elif sort == 'Descending':
        query+=f' order by price DESC'
    
    print(query)
    cursor.execute(query)
    products = cursor.fetchall()

    for i, (id,seller, name,qty, price,desc,cat) in enumerate(products):
        st.image(Image.open(f'{image_path}/{id}.jpg'), caption=f'{name}', use_column_width=True)
        st.write(f':red[Rs.{price}]')
        button_label = f'View Details'
        if st.button(button_label,id):
            st.session_state.page = 2
            st.session_state.product = [id,seller,name,qty,price,desc,cat]
            # switch_page('Register')
            st.experimental_rerun()
        st.divider()

def p2():
    cursor.execute(f'select shop_name from seller where seller_id = "{st.session_state.product[1]}"')
    seller = cursor.fetchall()[0][0]
    st.header(f':red[{st.session_state.product[2]}]',divider='red')
    st.image(Image.open(f'{image_path}/{st.session_state.product[0]}.jpg'), caption=f'{st.session_state.product[2]}', use_column_width=True)
    st.write(f':red[By]: {seller}')
    st.write(f':red[Price:] {st.session_state.product[4]}')
    st.write(f':red[Available Qty]: {st.session_state.product[3]}')
    st.write(':red[Details:]')
    st.write(f':white[{st.session_state.product[5]}]')
    cursor.execute(f'Select * from (Select * from review where product_id = "{st.session_state.product[0]}") T')
    reviews = cursor.fetchall()
    df = pd.DataFrame(reviews , columns=['rid','pid','buyer','rating','comment'])
    cursor.execute(f"Select AVG(Rating) from Review Group by product_id having product_id = '{st.session_state.product[0]}'")
    res = cursor.fetchall()
    avg_rat = 0
    if len(res)>0:
        avg_rat = float(res[0][0])
        round(avg_rat,2)

    st.write(f':red[Average Rating:] {avg_rat}')
    df.drop(['rid','pid'],axis=1,inplace=True)
    st.table(df)

    qty = int(st.number_input("Enter Purchase Quantity",min_value=1,step = 1,max_value=st.session_state.product[3]))
    add = st.button("Add to Cart",type='primary')
    if add and 'user' in st.session_state:
        if(qty <= 0):
            st.error("Qty Cannot be 0 or negative")
        else:
            try:
                cursor.execute(f'insert into shopping_cart values("{st.session_state.user}","{st.session_state.product[0]}","{qty}")')
            except mysql.connector.errors.IntegrityError:
                st.error("Product Already in cart")
            else:
                con.commit()
                st.success("Product Added to Cart")
                time.sleep(1)
                st.session_state.page=1
            
    elif add:
        st.error("Please Login to Access Cart")



def main():
    if 'page' not in st.session_state or st.session_state.page == 1:
        p1()
    
    elif st.session_state.page == 2:
        p2()

if __name__ == '__main__':
    main()