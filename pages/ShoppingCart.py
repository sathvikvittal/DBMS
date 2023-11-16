import streamlit as st
from sqlconfig import connect
import pandas as pd
import uuid

st.session_state.page=1
if 'conf' not in st.session_state:
    st.session_state.conf = False

if 'user' in st.session_state:
    user = st.session_state.user
    con = connect()
    cursor = con.cursor()
    cursor.execute(f'select s.product_id,s.qty,p.product_name,p.price from shopping_cart s join product p on s.product_id = p.product_id where s.user_id = "{user}" ')
    cart = cursor.fetchall()
    df = pd.DataFrame(cart,columns=['Product_id','Qty','Product Name','Price per Unit'])
    # df['Total Amount'] = df['Qty']*df['Price per unit']

    def dataframe_with_selections(df):
        df_with_selections = df.copy()
        df_with_selections.insert(0, "Select", False)

        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(
            df_with_selections,
            hide_index=True,
            column_config={"Select": st.column_config.CheckboxColumn(required=True)},
            disabled=df.columns,
        )

        # Filter the dataframe using the temporary column, then drop the column
        selected_rows = edited_df[edited_df.Select]
        return selected_rows.drop('Select', axis=1)

    
    selection = dataframe_with_selections(df)
    st.write("Your selection:")
    st.write(selection)

    delete = st.button("Delete Selected")
    if delete:
        for i in selection['Product_id'].values:
            cursor.execute(f'delete from shopping_cart where product_id="{i}" and user_id = "{user}"')
            con.commit()
        st.rerun()
    
    def clicked():
        st.session_state.conf = True

    st.button("Buy Selected",type='primary',on_click=clicked)


    if st.session_state.conf:
        total = 0
        qty = selection['Qty'].values
        ppu = selection['Price per Unit'].values
        for i in range(len(qty)):
            total+=float(qty[i]*ppu[i])
        
        st.subheader(f"Total Price: {total}")
        payment_mode = st.selectbox("Select Payment Mode",('Cash on Delivery','UPI','Credit/Debit Card'))

        if st.button('Confirm',type='primary'):
            orderid = str(uuid.uuid4().hex[:20].upper())
            cursor.execute(f'select addr from user where user_id = "{user}"')
            addr = cursor.fetchall()[0][0]
            for i in selection['Product_id'].values:
                qty = selection[selection['Product_id']==i]['Qty'].values[0]
                try:
                    cursor.execute(f'Insert into orders values("{orderid}","{i}","{user}","{addr}","{payment_mode}","{qty}");')
                except:
                    st.error("Error: Qty greater than available")
                else:
                    con.commit()

else:
    st.write("Please Login to View Your Shopping Cart")