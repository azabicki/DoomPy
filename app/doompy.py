import streamlit as st
import functions.sidebar as sidebar
import functions.variables as vars

st.set_page_config(layout="wide")  # need to be first 'st' command !!!

# init variables
vars.init_vars()
vars.start_game()

# create sidebar
sidebar.create()
sidebar.style()

st.divider()
st.session_state
