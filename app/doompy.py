import streamlit as st
import functions.utils as ut
import functions.sidebar as sidebar
import functions.variables as vars
import functions.actions as act
import functions.playground as pg

st.set_page_config(layout="wide")  # need to be first 'st' command !!!
ut.style()

# init variables
vars.init_vars()

# first time starting a game
if st.session_state.booting:
    st.session_state.booting = False
    act.start_game()

# create sidebar
sidebar.create()

# content
cols = st.columns(st.session_state.game["n_player"])
for p, col in enumerate(cols):
    with col:
        st.write(st.session_state.plr["name"][p])
        with st.container(border=True):
            st.write("scoreboard")

        with st.container(border=True):
            st.write("traitpile")

        with st.container(border=True):
            st.write("MOLs")
            pg.MOLs(p)

st.divider()
st.session_state
