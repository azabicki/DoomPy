import streamlit as st
import numpy as np
import functions.utils as ut
import functions.actions as act
import functions.updates as update
import functions.rules_traits as rules_tr
import functions.rules_attachment as rules_at
import functions.rules_trait_pile as rules_tp
import functions.rules_worlds_end as rules_we


# ScoreBoard ------------------------------------------------------------------
def score_board(p):
    # upper row --------------------------------
    c_dom1, c_dom2, c_name, c_gp_txt, c_gp = st.columns(
        [1, 1, 3.5, 1, 0.6], gap="small"
    )
    # ----- dominant star 1 -----
    with c_dom1:
        n_dom = update.count_dominants(p)
        if n_dom == 0:
            st.markdown(
                ut.img2html(
                    st.session_state.images["no_star"],
                    div="div_score_upper",
                    cls="star",
                ),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                ut.img2html(
                    st.session_state.images["star"], div="div_score_upper", cls="star"
                ),
                unsafe_allow_html=True,
            )

    # ----- dominant star 2 -----
    with c_dom2:
        if n_dom <= 1:
            st.markdown(
                ut.img2html(
                    st.session_state.images["no_star"],
                    div="div_score_upper",
                    cls="star",
                ),
                unsafe_allow_html=True,
            )
        elif n_dom == 2:
            st.markdown(
                ut.img2html(
                    st.session_state.images["star"], div="div_score_upper", cls="star"
                ),
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                ut.img2html(
                    st.session_state.images["heroic_star"],
                    div="div_score_upper",
                    cls="star",
                ),
                unsafe_allow_html=True,
            )

    # ----- name -----
    with c_name:
        if st.session_state["1st_player"] == p:
            name_str = """
                <div class="div_score_upper">
                <div class="div_yCenter">
                <p style="
                    color: {color};
                    font-size: 40px;
                    font-weight: bold;
                    text-align: center;
                ">
                {name}
                </p></div></div>""".format(
                color=st.session_state.cfg["font_color_1st_player"],
                name=st.session_state.plr["name"][p],
            )
        else:
            name_str = """
                <div class="div_score_upper">
                <div class="div_yCenter">
                <p style="
                    font-size: 40px;
                    font-weight: bold;
                    text-align: center;
                ">
                {name}
                </p></div></div>""".format(
                name=st.session_state.plr["name"][p]
            )
        st.markdown(name_str, unsafe_allow_html=True)

    # ----- gene pool string -----
    with c_gp_txt:
        gp_txt_str = """
            <div class="div_score_upper">
            <div class="div_yCenter">
            <p style="
                color: {color};
                font-size: 12px;
                font-weight: bold;
                text-align: right;
            ">
            gene<br>pool
            </p></div></div>""".format(
            color=st.session_state.cfg["font_color_genes"]
        )
        st.markdown(gp_txt_str, unsafe_allow_html=True)

    # ----- gene pool -----
    with c_gp:
        gp_str = """
            <div class="div_score_upper">
            <div class="div_yCenter">
            <p style="
                color: {color};
                font-size: 40px;
                font-weight: bold;
                text-align: left
            ">
            {gp}
            </p></div></div>""".format(
            color=st.session_state.cfg["font_color_genes"],
            gp=st.session_state.plr["genes"][p],
        )
        st.markdown(gp_str, unsafe_allow_html=True)

    # lower row --------------------------------
    ut.h_spacer(1)
    c_col1, c_col2, c_col3, c_pnts, c_sub1, c_sub2, c_sub3, c_sub4 = st.columns(
        [1, 1, 1, 5, 1.2, 1, 1.2, 1], gap="small"
    )
    # ----- color count -----
    with c_col1:
        cnt_b = """
            <div class="div_points">
            <div class="div_yCenter">
            <p class="points" style="
                color: {color};
                text-align: right
            ">
            {cnt}
            </p></div></div>""".format(
            color=st.session_state.cfg["color_blue"],
            cnt=st.session_state.plr["n_tp"][p]["b"],
        )
        st.markdown(cnt_b, unsafe_allow_html=True)

        cnt_p = """
            <div class="div_points">
            <div class="div_yCenter">
            <p class="points" style="
                color: {color};
                text-align: right
            ">
            {cnt}
            </p></div></div>""".format(
            color=st.session_state.cfg["color_purple"],
            cnt=st.session_state.plr["n_tp"][p]["p"],
        )
        st.markdown(cnt_p, unsafe_allow_html=True)

    with c_col2:
        cnt_g = """
            <div class="div_points">
            <div class="div_yCenter">
            <p class="points" style="
                color: {color};
                text-align: center
            ">
            {cnt}
            </p></div></div>""".format(
            color=st.session_state.cfg["color_green"],
            cnt=st.session_state.plr["n_tp"][p]["g"],
        )
        st.markdown(cnt_g, unsafe_allow_html=True)

        cnt_r = """
            <div class="div_points">
            <div class="div_yCenter">
            <p class="points" style="
                color: {color};
                text-align: center
            ">
            {cnt}
            </p></div></div>""".format(
            color=st.session_state.cfg["color_red"],
            cnt=st.session_state.plr["n_tp"][p]["r"],
        )
        st.markdown(cnt_r, unsafe_allow_html=True)

    with c_col3:
        cnt_c = """
            <div class="div_points">
            <div class="div_yCenter">
            <p class="points" style="
                color: {color};
                text-align: left
            ">
            {cnt}
            </p></div></div>""".format(
            color=st.session_state.cfg["color_colorless"],
            cnt=st.session_state.plr["n_tp"][p]["c"],
        )
        st.markdown(cnt_c, unsafe_allow_html=True)

        cnt_total = """
            <div class="div_points">
            <div class="div_yCenter">
            <p class="points" style="
                tesxt-align: left
            ">
            {cnt}
            </p></div></div>""".format(
            cnt=st.session_state.plr["n_tp"][p]["sb"],
        )
        st.markdown(cnt_total, unsafe_allow_html=True)

    # ----- points -----
    with c_pnts:
        pnt_str = """
            <div class="div_points_total">
            <div class="div_yCenter">
            <p class="points_total" style="
                color: {color}
            ">
            {gp}
            </p></div></div>""".format(
            color=st.session_state.cfg["font_color_total_score"],
            gp=st.session_state.plr["points"][p]["total"],
        )
        st.markdown(pnt_str, unsafe_allow_html=True)

    # ----- sub-points -----
    with c_sub1:
        st.markdown(
            ut.img2html(
                st.session_state.images["blank_sb"], div="div_points", cls="score_icons"
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            ut.img2html(
                st.session_state.images["drops_sb"], div="div_points", cls="score_icons"
            ),
            unsafe_allow_html=True,
        )

    with c_sub2:
        pnt_f = """
            <div class="div_points">
            <div class="div_yCenter">
            <p class="points" style="
                text-align: left
            ">
            {pnt}
            </p></div></div>""".format(
            pnt=st.session_state.plr["points"][p]["face"],
        )
        st.markdown(pnt_f, unsafe_allow_html=True)

        pnt_d = """
            <div class="div_points">
            <div class="div_yCenter">
            <p class="points" style="
                text-align: left
            ">
            {pnt}</p></div></div>""".format(
            pnt=st.session_state.plr["points"][p]["drops"],
        )
        st.markdown(pnt_d, unsafe_allow_html=True)

    with c_sub3:
        st.markdown(
            ut.img2html(
                st.session_state.images["worlds_end_sb"],
                div="div_points",
                cls="score_icons",
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            ut.img2html(
                st.session_state.images["MOL_sb"], div="div_points", cls="score_icons"
            ),
            unsafe_allow_html=True,
        )

    with c_sub4:
        pnt_we = """
            <div class="div_points">
            <div class="div_yCenter">
            <p class="points" style="
                text-align: left
            ">
            {pnt}
            </p></div></div>""".format(
            pnt=st.session_state.plr["points"][p]["worlds_end"],
        )
        st.markdown(pnt_we, unsafe_allow_html=True)

        pnt_m = """
            <div class="div_points">
            <div class="div_yCenter">
            <p class="points" style="
                text-align: left
            ">
            {pnt}
            </p></div></div>""".format(
            pnt=st.session_state.plr["points"][p]["MOL"],
        )
        st.markdown(pnt_m, unsafe_allow_html=True)


# Control Buttons -------------------------------------------------------------
def controls(p):
    c_move, c_hand, c_disc = st.columns([0.4, 0.3, 0.3])
    with c_move:
        mv_options = ["move to"] + [
            j for i, j in enumerate(st.session_state.plr["name"]) if i != p
        ]

        st.selectbox(
            "move_from_" + str(p),
            mv_options,
            index=mv_options.index(st.session_state[f"move_to_{p}"]),
            key=f"move_to_{p}",
            on_change=act.move_trait,
            args=(p,),
            label_visibility="collapsed",
        )

    with c_hand:
        st.button(
            "to hand",
            key="hand_" + str(p),
            on_click=act.remove_trait,
            args=(p, "hand"),
            use_container_width=True,
        )

    with c_disc:
        st.button(
            "discard",
            key="discard_" + str(p),
            on_click=act.remove_trait,
            args=(p, "discard"),
            use_container_width=True,
        )


# Trait Pile ------------------------------------------------------------------
def trait_pile(p):
    # shorten df's
    status_df = st.session_state.df["status_df"]
    traits_df = st.session_state.df["traits_df"]
    catastrophes_df = st.session_state.df["catastrophes_df"]
    plr = st.session_state.plr
    worlds_end = st.session_state.worlds_end

    # first, scan trait pile for any effects by any traits, like protecting
    # other traits...
    rules_tr.permanent_effects(plr["trait_pile"][p])

    # --- loop traits in trait pile -------------------------------------------
    for trait_idx in plr["trait_pile"][p]:
        # get trait name
        trait = traits_df.loc[trait_idx].trait

        # columns
        c_trait = st.columns([1, 4, 1, 1, 1, 1, 1, 1])
        # c_trait = st.columns(7)

        # ----- trait checkbox -------------
        with c_trait[0]:
            st.checkbox(
                trait,
                value=False,
                key=f"tp_{p}_{trait_idx}",
                on_change=update.selected_trait,
                args=(p, trait_idx),
                label_visibility="collapsed",
            )

        # ----- traits name -------------
        with c_trait[1]:
            if traits_df.loc[trait_idx].dominant == 1:
                name_str = """<p style="
                color:{color};
                font-weight: bold;
                text-align:left;
                ">{trait}</p>""".format(
                    color=st.session_state.cfg["font_color_dominant"],
                    trait=trait,
                )
            else:
                name_str = "{trait}".format(trait=trait)
            st.markdown(name_str, unsafe_allow_html=True)

        # ----- color -------------
        with c_trait[2]:
            # get color
            color = traits_df.loc[trait_idx].color
            cc = "c" if "colorless" in color.lower() else ""
            cb = "b" if "blue" in color.lower() else ""
            cg = "g" if "green" in color.lower() else ""
            cp = "p" if "purple" in color.lower() else ""
            cr = "r" if "red" in color.lower() else ""

            # check if color changed
            X = (
                "X"
                if status_df.loc[trait_idx].color.lower()
                != traits_df.loc[trait_idx].color.lower()
                else ""
            )
            st.markdown(
                ut.img2html(
                    st.session_state.images[cc + cb + cg + cp + cr + X],
                    div="div_icons",
                    cls="icons",
                ),
                unsafe_allow_html=True,
            )

        # ----- face value -------------
        with c_trait[3]:
            trait_face = traits_df.loc[trait_idx].face
            status_face = status_df.loc[trait_idx].face

            X = "X" if trait_face != status_face else ""
            face_string = (
                trait_face if isinstance(trait_face, str) else str(int(trait_face))
            )
            st.markdown(
                ut.img2html(
                    st.session_state.images[face_string + X],
                    div="div_icons",
                    cls="icons",
                ),
                unsafe_allow_html=True,
            )

        # ---------- STATE_icons -> current drop/attachment effects  ----------
        # ----- seperator -------------
        with c_trait[4]:
            sep_str = """
                <div class="div_icons">
                <div class="div_yCenter">
                <p style="
                    text-align: center;
                    font-size: 20px;
                ">
                |
                </p></div></div>"""
            st.markdown(sep_str, unsafe_allow_html=True)

        # (running) index for next columns
        next_col = 4

        # ----- *new* color -------------
        cur_color = status_df.loc[trait_idx].color.lower()
        if cur_color != traits_df.loc[trait_idx].color.lower():
            next_col += 1
            with c_trait[next_col]:
                # find current color
                cc = "c" if "colorless" in cur_color.lower() else ""
                cb = "b" if "blue" in cur_color.lower() else ""
                cg = "g" if "green" in cur_color.lower() else ""
                cp = "p" if "purple" in cur_color.lower() else ""
                cr = "r" if "red" in cur_color.lower() else ""

                # change to 'causing' color-icon
                if any(
                    col in status_df.loc[trait_idx].effects_traits_WE
                    for col in cur_color.split("_")
                ):
                    X = "WE"
                elif status_df.loc[trait_idx].attachment != "none":
                    X = "AT"
                else:
                    X = ""

                # add new color icon
                st.markdown(
                    ut.img2html(
                        st.session_state.images[cc + cb + cg + cp + cr + X],
                        div="div_icons",
                        cls="icons",
                    ),
                    unsafe_allow_html=True,
                )

        # ----- drop value -------------
        cur_drops = status_df.loc[trait_idx].drops
        if traits_df.loc[trait_idx].drops == 1:
            # drop icon
            next_col += 1
            with c_trait[next_col]:
                st.markdown(
                    ut.img2html(
                        st.session_state.images["drops"],
                        div="div_icons",
                        cls="icons",
                    ),
                    unsafe_allow_html=True,
                )

            # value icon
            next_col += 1
            with c_trait[next_col]:
                if np.isnan(cur_drops):
                    # add question mark as long as no drop value is calculated
                    drop_string = "question_mark"
                else:
                    # check if values are higher/lower than drop icons exist
                    if int(cur_drops) > 20:
                        drop_string = "20+"
                    elif int(cur_drops) < -20:
                        drop_string = "-20-"
                    else:
                        drop_string = str(int(cur_drops))

                st.markdown(
                    ut.img2html(
                        st.session_state.images[drop_string],
                        div="div_icons",
                        cls="icons",
                    ),
                    unsafe_allow_html=True,
                )

        # maybe add the following icons if i find a good way to do that
        if 1 == 2:
            # ----- has attachment -------------
            if status_df.loc[trait_idx].attachment != "none":
                next_col += 1
                with c_trait[next_col]:
                    st.markdown(
                        ut.img2html(
                            st.session_state.images["attachment"],
                            div="div_icons",
                            cls="icons",
                        ),
                        unsafe_allow_html=True,
                    )

            # ----- noFX -------------
            if (
                status_df.loc[trait_idx].inactive
                and "inactive" not in status_df.loc[trait_idx].effects_WE.lower()
            ):
                next_col += 1
                with c_trait[next_col]:
                    st.markdown(
                        ut.img2html(
                            st.session_state.images["noFX"],
                            div="div_icons",
                            cls="icons",
                        ),
                        unsafe_allow_html=True,
                    )

            # ----- noRemove -------------
            if status_df.loc[trait_idx].no_remove:
                next_col += 1
                with c_trait[next_col]:
                    st.markdown(
                        ut.img2html(
                            st.session_state.images["noRemove"],
                            div="div_icons",
                            cls="icons",
                        ),
                        unsafe_allow_html=True,
                    )

            # ----- noDiscard -------------
            if status_df.loc[trait_idx].no_discard:
                next_col += 1
                with c_trait[next_col]:
                    st.markdown(
                        ut.img2html(
                            st.session_state.images["noDiscard"],
                            div="div_icons",
                            cls="icons",
                        ),
                        unsafe_allow_html=True,
                    )

            # ----- noSteal -------------
            if status_df.loc[trait_idx].no_steal:
                next_col += 1
                with c_trait[next_col]:
                    st.markdown(
                        ut.img2html(
                            st.session_state.images["noSteal"],
                            div="div_icons",
                            cls="icons",
                        ),
                        unsafe_allow_html=True,
                    )

            # ----- noSwap -------------
            if status_df.loc[trait_idx].no_swap:
                next_col += 1
                with c_trait[next_col]:
                    st.markdown(
                        ut.img2html(
                            st.session_state.images["noSwap"],
                            div="div_icons",
                            cls="icons",
                        ),
                        unsafe_allow_html=True,
                    )

            # ----- if WORLDS END effects this trait -------------
            if status_df.loc[trait_idx].effects_WE != "none":
                next_col += 1
                with c_trait[next_col]:
                    st.markdown(
                        ut.img2html(
                            st.session_state.images["worlds_end"],
                            div="div_icons",
                            cls="icons",
                        ),
                        unsafe_allow_html=True,
                    )

                if "face" in status_df.loc[trait_idx].effects_WE.lower():
                    we_face_string = str(int(status_df.loc[trait_idx].face))
                    next_col += 1
                    with c_trait[next_col]:
                        st.markdown(
                            ut.img2html(
                                st.session_state.images[we_face_string],
                                div="div_icons",
                                cls="icons",
                            ),
                            unsafe_allow_html=True,
                        )

                if "inactive" in status_df.loc[trait_idx].effects_WE.lower():
                    next_col += 1
                    with c_trait[next_col]:
                        st.markdown(
                            ut.img2html(
                                st.session_state.images["noFX"],
                                div="div_icons",
                                cls="icons",
                            ),
                            unsafe_allow_html=True,
                        )

        # ---------- TRAIT specific aditional rows ----------------------------
        # ----- SLEEPY may affect gene pool ?!?!  -------------
        if traits_df.loc[trait_idx].trait == "Sleepy":
            c_slp = st.columns([0.4, 0.8, 0.99])
            with c_slp[1]:
                st.write("gene effect:")
            with c_slp[2]:
                # create spinbox
                st.number_input(
                    "Sleepy",
                    min_value=-5,
                    max_value=5,
                    step=1,
                    value=st.session_state.game["sleepy_spinbox"][p],
                    on_change=update.sleepy,
                    args=(p,),
                    key="sleepy_input",
                    label_visibility="collapsed",
                )

        # ----- ATTACHMENT combobox if trait is attachment --------------------
        if traits_df.loc[trait_idx].attachment == 1:
            c_atch = st.columns([0.2, 0.6, 0.99])
            with c_atch[1]:
                st.write("attach to:")
            with c_atch[2]:
                # filter only non-attachment-traits and check if this is already attached to a trait
                traits_filtered_idx = [None] + rules_at.filter_attachables(trait_idx, p)
                traits_filtered_str = [" ... "] + [
                    traits_df.loc[idx].trait
                    for idx in traits_filtered_idx
                    if idx is not None
                ]

                # check if already attached to host
                if status_df.loc[trait_idx].host == "none":
                    sbox_index = 0
                else:
                    cur_host = status_df.loc[trait_idx].host
                    sbox_index = traits_filtered_idx.index(cur_host)

                # create selectbox
                st.selectbox(
                    f"attach_{p}_{trait_idx}",
                    traits_filtered_str,
                    index=sbox_index,
                    label_visibility="collapsed",
                    key=f"attchmnt_{trait_idx}",
                    on_change=act.attach_to,
                    args=(
                        p,
                        trait_idx,
                        "event",
                        dict(zip(traits_filtered_str, traits_filtered_idx)),
                    ),
                )

        # ----- WORLDS_END combobox if trait has worlds end effect ------------
        if isinstance(traits_df.loc[trait_idx].worlds_end_task, str):
            c_we = st.columns([0.2, 0.6, 0.99])
            with c_we[1]:
                st.write("Worlds End:")
            with c_we[2]:
                # get task what to do at worlds end
                twe_effect = rules_tr.traits_WE_tasks(trait_idx)

                # set state depending on 'played' catastrophes
                state = (
                    False
                    if sum(i is None for i in st.session_state.catastrophe["played"])
                    == 0
                    else True
                )

                # check if effect already selected
                if status_df.loc[trait_idx].traits_WE == "none":
                    sbox_index = 0
                else:
                    cur_effect = status_df.loc[trait_idx].traits_WE
                    sbox_index = twe_effect.index(cur_effect)

                # create selectbox
                st.selectbox(
                    f"traits_WE_{trait_idx}",
                    twe_effect,
                    index=sbox_index,
                    label_visibility="collapsed",
                    key=f"twe_{trait_idx}",
                    on_change=act.traits_world_end,
                    args=(p, trait_idx),
                    disabled=state,
                )

        # ----- manual DROP points spinbox ------------------------------------
        cur_drop_eff = traits_df.loc[trait_idx].drop_effect
        if (
            isinstance(cur_drop_eff, str)
            and not isinstance(traits_df.loc[trait_idx].worlds_end_task, str)
            and (
                "own_hand" in traits_df.loc[trait_idx].drop_effect
                or "discarded" in traits_df.loc[trait_idx].drop_effect
            )
        ):
            c_we = st.columns([0.2, 0.6, 0.99])
            with c_we[1]:
                st.write("Drop of Life:")
            with c_we[2]:
                # set state depending on 'played' worlds end
                state = False if worlds_end["played"] != "none" else True

                # fill spinbox, depending on drops_status
                if not np.isnan(status_df.loc[trait_idx].drops):
                    dp = int(status_df.loc[trait_idx].drops)
                else:
                    dp = 0

                st.number_input(
                    f"drops_{trait_idx}",
                    min_value=-20,
                    max_value=20,
                    step=1,
                    value=dp,
                    key=f"drop_{trait_idx}",
                    on_change=act.manual_drops,
                    args=(trait_idx,),
                    label_visibility="collapsed",
                    disabled=state,
                )

    # *********** special, individual cases *** !!! ***************************
    # Some Drop-of-Life-Effects are affecting other players! hence, effects of
    # these traits need to be shown on each other players trait pile, allowing
    # to enter individual drop values
    st.divider()
    # call function to insert special-effects from various traits
    rules_tp.special_trait_effects(p)

    # --- NEOTENY needs to stay here ------------------------------------------
    # --- because 'create_trait_pile' needs to be run once checkbox is clicked
    neoteny_idx = traits_df.index[traits_df.trait == "Neoteny"].tolist()
    if neoteny_idx != []:
        neoteny_effect = status_df.loc[neoteny_idx[0]].effects
        if (worlds_end["played"] != "none") and (
            all(neoteny_idx[0] not in tp for tp in plr["trait_pile"])
        ):
            # only if no one has it or this player has it
            if neoteny_effect == "none" or neoteny_effect == str(p):
                # columns
                c_trait = st.columns([2, 3, 2])

                # add trait
                with c_trait[0]:
                    name_str = """<p style="
                        color:{color};
                        font-weight: bold;
                        text-align:left;
                        ">NEOTENY</p>""".format(
                        color=st.session_state.cfg["color_blue"],
                    )
                    st.markdown(name_str, unsafe_allow_html=True)

                # not in this hand
                # if not st.session_state[f"neoteny_{p}"]:
                if st.session_state.game["neoteny_checkbutton"][p] == 0:
                    with c_trait[1]:
                        st.checkbox(
                            "on hand?",
                            value=False,
                            key=f"neoteny_{p}",
                            on_change=update.traits_current_status,
                            args=("neoteny", p),
                            label_visibility="visible",
                        )

                # if is this hand
                else:
                    with c_trait[1]:
                        st.checkbox(
                            "got it!",
                            value=True,
                            key=f"neoteny_{p}",
                            on_change=update.traits_current_status,
                            args=("neoteny", p),
                            label_visibility="visible",
                        )

                    with c_trait[2]:
                        st.markdown(
                            ut.img2html_doubles(
                                [
                                    st.session_state.images["drops"],
                                    st.session_state.images["4"],
                                ],
                                cls="Xtra_icons",
                            ),
                            unsafe_allow_html=True,
                        )

    # *************************************************************************
    # ------ worlds end -> manual entries -------------------------------------
    # if worlds_end["played"] != "none":
    if worlds_end["played"] != "none":
        st.divider()

        # get world's end name & index
        we = worlds_end["played"]
        we_idx = catastrophes_df[catastrophes_df["name"] == we].index.values[0]
        we_type = catastrophes_df.loc[we_idx].worlds_end_type

        # columns
        c_we = st.columns([1, 3, 1])

        # WE_icons
        with c_we[0]:
            st.markdown(
                ut.img2html(
                    st.session_state.images["catastrophe_WE"],
                    div="div_WE_icons_L",
                    cls="WE_icons",
                ),
                unsafe_allow_html=True,
            )
        with c_we[2]:
            st.markdown(
                ut.img2html(
                    st.session_state.images["catastrophe_WE"],
                    div="div_WE_icons_R",
                    cls="WE_icons",
                ),
                unsafe_allow_html=True,
            )

        # WE name & effect
        with c_we[1]:
            we_str = """
                <div class="div_WE">
                <div class="div_yCenter">
                <p class="WE" style="
                    color:{color};
                ">
                {we}
                </p></div></div>""".format(
                color=st.session_state.cfg["font_color_total_score"],
                we=we,
            )
            st.markdown(we_str, unsafe_allow_html=True)

            # WE_EFFECTS
            if we_type == "hand" or we_type == "draw":
                # create spinbox
                st.number_input(
                    "we_points",
                    min_value=-30,
                    max_value=30,
                    step=1,
                    value=plr["points_WE_effect"][p],
                    on_change=act.manual_we,
                    args=(p,),
                    key=f"we_points_{p}",
                    label_visibility="collapsed",
                )

            elif we_type == "calculate":
                we_points = (
                    rules_we.calc_WE_points(p) if worlds_end["played"] != "none" else 0
                )
                st.markdown(
                    ut.img2html(
                        st.session_state.images[str(we_points)],
                        div="div_WE_points",
                        cls="WE_icons",
                    ),
                    unsafe_allow_html=True,
                )


# MOLs ------------------------------------------------------------------------
def MOLs(p):
    # shorten df's
    MOLs_df = st.session_state.df["MOLs_df"]
    MOLs = st.session_state.MOLs
    plr = st.session_state.plr

    # create MOL select_boxes
    for m in range(MOLs["n"][p]):
        m_idx = MOLs["played"][p][m]

        # check if spinbox need to be drawn
        if MOLs["played"][p][m] is not None and (
            "hand" in MOLs_df.loc[m_idx].MOL_type.lower()
            or "draw" in MOLs_df.loc[m_idx].MOL_type.lower()
        ):
            spin = True
            c_l, c_r = st.columns([3, 2])
        else:
            spin = False
            c_l, c_r = st.columns([7, 1])

        # MOL selectbox
        with c_l:
            pos_MOLs = ["... MOL #{}".format(m + 1)] + MOLs_df.MOL.values.tolist()

            st.selectbox(
                f"MOL_{p}_{m}",
                list(range(len(pos_MOLs))),
                format_func=lambda x: pos_MOLs[x],
                index=st.session_state[f"MOL_{p}_{m}"],
                key=f"MOL_{p}_{m}",
                label_visibility="collapsed",
                on_change=act.select_MOL,
                args=(p, m),
            )

        # points/icons
        with c_r:
            if m_idx is None:
                st.markdown(
                    ut.img2html(
                        st.session_state.images["question_mark"],
                        div="div_MOL",
                        cls="MOL",
                    ),
                    unsafe_allow_html=True,
                )
            elif spin:
                # create spinbox
                st.number_input(
                    f"mol_points_{p}_{m}",
                    min_value=-30,
                    max_value=30,
                    step=1,
                    value=st.session_state[f"mol_points_{p}_{m}"],
                    on_change=act.manual_MOL,
                    args=(p, m),
                    key=f"mol_points_{p}_{m}",
                    label_visibility="collapsed",
                )
            else:
                st.markdown(
                    ut.img2html(
                        st.session_state.images[str(plr["points_MOL"][p][m])],
                        div="div_MOL",
                        cls="MOL",
                    ),
                    unsafe_allow_html=True,
                )
