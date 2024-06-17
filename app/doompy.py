import streamlit as st
import functions.sidebar as sidebar
import functions.variables as vars
import functions.actions as act

st.set_page_config(layout="wide")  # need to be first 'st' command !!!

# init variables
vars.init_vars()

# first time starting a game
if st.session_state.booting:
    st.session_state.booting = False
    act.start_game()

# create sidebar
sidebar.create()
sidebar.style()

# content
st.divider()
st.session_state
