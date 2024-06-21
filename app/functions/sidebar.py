import streamlit as st
import functions.actions as act
import functions.utils as ut


# -----------------------------------------------------------------------------
def create():
    # Next Game ----------------------------------------
    next_game()

    # 1st player ----------------------------------------
    first_player()

    # Traits ----------------------------------------
    trait_deck()

    # Ages ----------------------------------------
    catastrophes()

    # Worlds End ----------------------------------------
    worlds_end()

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
                st.session_state.game["n_player"] = st.number_input(
                    "Players",
                    min_value=2,
                    max_value=6,
                    step=1,
                    value=st.session_state.game["n_player"],
                )
            with c_gp:
                st.session_state.game["n_genes"] = st.number_input(
                    "Gene Pool",
                    min_value=1,
                    max_value=10,
                    step=1,
                    value=st.session_state.game["n_genes"],
                )
            with c_cat:
                st.session_state.game["n_catastrophes"] = st.number_input(
                    "Catastrophes",
                    min_value=1,
                    max_value=6,
                    step=1,
                    value=st.session_state.game["n_catastrophes"],
                )
            with c_mol:
                st.session_state.game["n_MOLs"] = st.number_input(
                    "MOLs",
                    min_value=1,
                    max_value=4,
                    step=1,
                    value=st.session_state.game["n_MOLs"],
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
                act.start_game(what="next_game")


# -----------------------------------------------------------------------------
def first_player():
    with st.sidebar.container(border=True):
        st.markdown("**First Player**")
        st.selectbox(
            "first player",
            list(range(st.session_state.game["n_player"])),
            format_func=lambda x: st.session_state.plr["name"][x],
            key="1st_player",
            label_visibility="collapsed",
        )


# -----------------------------------------------------------------------------
def trait_deck():
    def create_btn(p):
        st.button(
            st.session_state.plr["name"][p],
            use_container_width=True,
            on_click=act.play_trait,
            args=(p,),
        )

    with st.sidebar.container(border=True):
        st.markdown("**Who Plays Which Trait**")

        # trait select box
        st.selectbox(
            "select trait",
            st.session_state.deck,
            format_func=lambda x: st.session_state.deck_str[x],
            index=None,
            placeholder="search trait...",
            label_visibility="collapsed",
            key="trait2play",
        )

        # player buttons
        c11, c12 = st.columns(2)
        with c11:
            create_btn(0)

        with c12:
            create_btn(1)

        if st.session_state.game["n_player"] == 3:
            create_btn(2)

        if st.session_state.game["n_player"] >= 4:
            c21, c22 = st.columns(2)
            with c21:
                create_btn(2)
            with c22:
                create_btn(3)

        if st.session_state.game["n_player"] == 5:
            create_btn(4)

        if st.session_state.game["n_player"] >= 6:
            c31, c32 = st.columns(2)
            with c31:
                create_btn(4)
            with c32:
                create_btn(5)


# -----------------------------------------------------------------------------
def catastrophes():
    catastrophes_df = st.session_state.df["catastrophes_df"]
    catastrophe = st.session_state.catastrophe

    with st.sidebar.container(border=True):
        st.markdown("**Catastrophes**")

        # catastrophe select box ---------------------------
        for c in range(st.session_state.game["n_catastrophes"]):
            pos_cat_values = [" catastrophe {}...".format(c + 1)] + catastrophes_df.loc[
                catastrophe["possible"][c]
            ].name.values.tolist()

            if c == 0 or catastrophe["played"][c - 1] is not None:
                state = False
            else:
                state = True

            st.selectbox(
                f"catastrophe_{c}",
                list(range(len(pos_cat_values))),
                format_func=lambda x: pos_cat_values[x],
                index=st.session_state[f"catastrophe_{c}"],
                key=f"catastrophe_{c}",
                label_visibility="collapsed",
                disabled=state,
                on_change=act.catastrophe,
                args=(c, pos_cat_values),
            )


# -----------------------------------------------------------------------------
def worlds_end():
    with st.sidebar.container(border=True):
        st.markdown("**World's End**")
