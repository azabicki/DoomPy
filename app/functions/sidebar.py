import streamlit as st
import functions.variables as vars
import functions.utils as ut


# -----------------------------------------------------------------------------
def create():
    # Next Game ----------------------------------------
    next_game()

    # 1st player ----------------------------------------
    with st.sidebar.container(border=True):
        st.selectbox(
            "**first player**",
            list(range(st.session_state.game["n_player"])),
            format_func=lambda x: st.session_state.plr["name"][x],
            key="1st_player",
        )

    # Traits ----------------------------------------
    with st.sidebar.container(border=True):
        st.markdown("**who plays a trait**")
        st.selectbox(
            "**select trait**",
            st.session_state.deck,
            format_func=lambda x: st.session_state.deck_str[x],
            index=None,
            placeholder="search trait...",
            label_visibility="collapsed",
            key="trait2play",
        )

    # Ages ----------------------------------------
    with st.sidebar.container(border=True):
        st.markdown("**Catastrophes**")
        st.markdown("**World's End**")

    # Options ----------------------------------------
    with st.sidebar.container(border=True):
        st.markdown("_some options..._")

    with st.sidebar.container(border=True):
        # config ----------------------------------------
        st.markdown("current game:")
        st.markdown(
            "{np}p / {ng}g / {nc}c / {nm}m".format(
                np=st.session_state.game["n_player"],
                ng=st.session_state.game["n_genes"],
                nc=st.session_state.game["n_catastrophes"],
                nm=st.session_state.game["n_MOLs"],
            )
        )


# -----------------------------------------------------------------------------
def next_game():
    with st.sidebar.popover("Next Game", use_container_width=False):
        with st.form("form_next_game", border=False):
            # settings
            st.markdown("##### Start with:")
            c_plr, c_gp, c_cat, c_mol = st.columns(4)
            with c_plr:
                st.session_state.next["n_player"] = st.number_input(
                    "Players",
                    min_value=2,
                    max_value=6,
                    step=1,
                    value=st.session_state.next["n_player"],
                )
            with c_gp:
                st.session_state.next["n_genes"] = st.number_input(
                    "Gene Pool",
                    min_value=1,
                    max_value=10,
                    step=1,
                    value=st.session_state.next["n_genes"],
                )
            # c_cat, c_mol = st.columns(2)
            with c_cat:
                st.session_state.next["n_catastrophes"] = st.number_input(
                    "Catastrophes",
                    min_value=1,
                    max_value=6,
                    step=1,
                    value=st.session_state.next["n_catastrophes"],
                )
            with c_mol:
                st.session_state.next["n_MOLs"] = st.number_input(
                    "MOLs",
                    min_value=1,
                    max_value=4,
                    step=1,
                    value=st.session_state.next["n_MOLs"],
                )

            # names
            ut.h_spacer(2)
            st.markdown("##### Play with:")
            st.markdown("according to the seating order at the table !")
            for n in range(0, st.session_state.cfg["max_player"], 3):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.session_state.cfg["names"][n] = st.text_input(
                        f"Player {n+1}",
                        value=st.session_state.cfg["names"][n],
                        max_chars=None,
                    )
                with c2:
                    st.session_state.cfg["names"][n + 1] = st.text_input(
                        f"Player {n+2}",
                        value=st.session_state.cfg["names"][n + 1],
                        max_chars=None,
                    )
                with c3:
                    st.session_state.cfg["names"][n + 2] = st.text_input(
                        f"Player {n+3}",
                        value=st.session_state.cfg["names"][n + 2],
                        max_chars=None,
                    )

            # button
            ut.h_spacer(2)
            if st.form_submit_button("start game", use_container_width=True):
                vars.start_game(what="next_game")


# -----------------------------------------------------------------------------
def style():
    css = """
    <style>
        [data-testid="stSidebar"]{
            min-width: 280px;
            max-width: 280px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
