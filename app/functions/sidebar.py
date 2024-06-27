import streamlit as st
import functions.actions as act
import functions.utils as ut
import functions.updates as update


# -----------------------------------------------------------------------------
def create():
    st.sidebar.image(
        "app/logo.png",
        use_column_width="always",
    )
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
    options()


# -----------------------------------------------------------------------------
def next_game():
    with st.sidebar.popover("New Game", use_container_width=True):
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
            ut.h_spacer(1)
            st.markdown("**IMPORTANT:** according to the seating order at the table !")

            # button
            ut.h_spacer(1)
            if st.form_submit_button("Start New Game", use_container_width=True):
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
            pos_cat_strings = [
                " catastrophe {}...".format(c + 1)
            ] + catastrophes_df.loc[catastrophe["possible"][c]].name.values.tolist()

            if c == 0 or catastrophe["played"][c - 1] is not None:
                state = False
            else:
                state = True

            if catastrophe["played"][c] is None:
                actual_index = 0
            else:
                actual_index = (
                    catastrophe["possible"][c].index(catastrophe["played"][c]) + 1
                )

            st.selectbox(
                f"catastrophe_{c}",
                list(range(len(pos_cat_strings))),
                format_func=lambda x: pos_cat_strings[x],
                index=actual_index,
                key=f"catastrophe_{c}",
                label_visibility="collapsed",
                disabled=state,
                on_change=act.select_catastrophe,
                args=(c, pos_cat_strings),
            )


# -----------------------------------------------------------------------------
def worlds_end():
    catastrophes_df = st.session_state.df["catastrophes_df"]
    status_df = st.session_state.df["status_df"]
    traits_df = st.session_state.df["traits_df"]
    catastrophe = st.session_state.catastrophe
    plr = st.session_state.plr

    with st.sidebar.container(border=True):
        st.markdown("**World's End**")

        # world's end select box ---------------------------
        played_catastrophes = [
            catastrophes_df.loc[catastrophe["played"][i], "name"]
            for i in range(st.session_state.game["n_catastrophes"])
            if catastrophe["played"][i] is not None
        ]

        # enable worlds_end-combobox and select last entry
        if len(played_catastrophes) == st.session_state.game["n_catastrophes"]:
            state_we = False
            if st.session_state["selected_worlds_end"] is None:
                st.session_state["selected_worlds_end"] = (
                    st.session_state.game["n_catastrophes"] - 1
                )
        else:
            state_we = True

        st.selectbox(
            "worlds_end",
            list(range(len(played_catastrophes))),
            format_func=lambda x: played_catastrophes[x],
            index=st.session_state["selected_worlds_end"],
            placeholder="...",
            key="selected_worlds_end",
            label_visibility="collapsed",
            disabled=state_we,
        )

        # world's end button ---------------------------
        if (state_we is True) or any(
            [
                status_df.loc[trait_idx].traits_WE == "none"
                for tp in plr["trait_pile"]
                for trait_idx in tp
                if isinstance(traits_df.loc[trait_idx].worlds_end_task, str)
            ]
        ):
            # disable WE_button
            state = True
        else:
            # enable WE_button
            state = False
            # log
            print(["worlds_end", "button_ready"])

        st.button(
            "do WORLD'S END !!!",
            disabled=state,
            on_click=act.worlds_end_GO,
            args=(played_catastrophes,),
            use_container_width=True,
        )


# -----------------------------------------------------------------------------
def options():
    with st.sidebar.container(border=True):
        pnt_opt = ["visible", "only rank", "hidden"]
        st.radio(
            "How to display Points?",
            list(range(len(pnt_opt))),
            format_func=lambda x: pnt_opt[x],
            index=st.session_state["points_onoff"],
            key="points_onoff",
            on_change=update.all,
        )

    with st.sidebar.container(border=True):
        # st.markdown("**Options**")
        st.markdown(
            """
        **Hi there,**


        hope you have fun playing [_Doomlings_](https://doomlings.com) and maybe
        could even make use of this **Live Scoring** tool!

        If you find any bugs or space for improvement, just let me know! You
        can open an [issue](https://github.com/azabicki/DoomPy/issues) in the
        [_GITHUB repo_](https://github.com/azabicki/DoomPy), or drop me an
        [_eMail_](azabicki@posteo.de).
        """
        )
