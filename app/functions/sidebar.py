import streamlit as st


# -----------------------------------------------------------------------------
def create():
    # Next Game ----------------------------------------
    with st.sidebar.popover("Next Game", use_container_width=False):
        st.markdown("##### Settings")
        c_plr, c_gp = st.columns(2)
        with c_plr:
            st.session_state.options["n_player"] = st.number_input(
                "players",
                min_value=2,
                max_value=6,
                step=1,
                value=st.session_state.cfg["n_player"],
            )
        with c_gp:
            st.number_input(
                "gene pool",
                min_value=1,
                max_value=10,
                step=1,
                value=st.session_state.cfg["n_genes"],
            )
        c_cat, c_mol = st.columns(2)
        with c_cat:
            st.number_input(
                "catastrophes",
                min_value=1,
                max_value=6,
                step=1,
                value=st.session_state.cfg["n_catastrophes"],
            )
        with c_mol:
            st.number_input(
                "MOLs",
                min_value=1,
                max_value=4,
                step=1,
                value=st.session_state.cfg["n_MOLs"],
            )

        st.divider()
        st.markdown("##### Names - keep order !")
        for n in range(st.session_state.options["n_player"]):
            st.session_state.cfg["names"][n] = st.text_input(
                f"Player {n+1}", value=st.session_state.cfg["names"][n], max_chars=None
            )
        st.divider()
        st.button("start game", use_container_width=True)

    # 1st player ----------------------------------------
    st.sidebar.divider()
    st.sidebar.selectbox("**first player**",
                         list(range(st.session_state.game["n_player"])),
                         format_func=lambda x: st.session_state.plr["name"][x],
                         key="1st_player"
                         )

    # Traits ----------------------------------------
    st.sidebar.divider()
    st.sidebar.markdown("**who plays which trait**")
    st.sidebar.selectbox(
        "**select trait**",
        st.session_state.deck,
        format_func=lambda x: st.session_state.deck_str[x],
        index=None,
        placeholder="search trait...",
        label_visibility="collapsed",
        key="trait2play",
    )

    # Ages ----------------------------------------
    st.sidebar.divider()
    st.sidebar.markdown("**Catastrophes**")
    st.sidebar.markdown("**World's End**")

    # Options ----------------------------------------
    st.sidebar.divider()
    st.sidebar.markdown("_some options..._")


# -----------------------------------------------------------------------------
def style():
    css = """
    <style>
        [data-testid="stSidebar"]{
            min-width: 250px;
            max-width: 250px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
