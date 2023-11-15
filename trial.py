import streamlit as st

def main():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    # Sidebar navigation
    st.sidebar.title('Navigation')
    pages = ['Home', 'Page 1', 'Page 2']
    selected_page = st.sidebar.selectbox('Select Page', pages)

    # Update page based on user selection
    if selected_page.lower() != st.session_state.page:
        st.session_state.page = selected_page.lower()

    # Render selected page
    if st.session_state.page == 'home':
        render_home()
    elif st.session_state.page == 'page 1':
        render_page_1()
    elif st.session_state.page == 'page 2':
        render_page_2()

def render_home():
    st.title('Home Page')
    st.write('Welcome to the home page.')

def render_page_1():
    st.title('Page 1')
    st.write('This is Page 1.')

def render_page_2():
    st.title('Page 2')
    st.write('This is Page 2.')

if __name__ == '__main__':
    main()