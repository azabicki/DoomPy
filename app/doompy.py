import streamlit as st
import functions.utils as ut
import functions.actions as act
import functions.playground as pg
import functions.variables as vars
import functions.sidebar as sidebar

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
        with st.container(border=True):
            pg.score_board(p)

            st.divider()
            pg.controls(p)
            pg.trait_pile(p)

            st.divider()
            st.markdown("Meaning(s) of Life")
            pg.MOLs(p)
