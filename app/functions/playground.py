import streamlit as st
import numpy as np
import functions.utils as ut
import functions.actions as act
import functions.updates as update
import functions.rules_traits as rules_tr
import functions.rules_attachment as rules_at


# ScoreBoard ------------------------------------------------------------------
def score_board(p):
    # upper row --------------------------------
    c_dom1, c_dom2, c_name, c_gp_txt, c_gp = st.columns([1, 1, 3, 1, 1], gap="small")
    # ----- dominant star 1 -----
    with c_dom1:
        # str_1 = """<div class="parent-div"><div class="text-div"><img
        # src="{image}"
        # alt="star"
        # class="img_center"/></div></div>""".format(
        #     image=st.session_state.images["no_star"]
        # )
        # st.markdown(str_1, unsafe_allow_html=True)
        st.image(image=st.session_state.images["no_star"], use_column_width="always")

    # ----- dominant star 2 -----
    with c_dom2:
        st.image(image=st.session_state.images["no_star"], use_column_width="always")

    # ----- name -----
    with c_name:
        if st.session_state["1st_player"] == p:
            name_str = """<div class="parent-div"><div class="text-div"><p style="
            color:{color};
            font-size: 40px;
            font-weight: bold;
            text-align:center;
            ">{name}</p></div></div>""".format(
                color=st.session_state.cfg["font_color_1st_player"],
                name=st.session_state.plr["name"][p],
            )
        else:
            name_str = """<div class="parent-div"><div class="text-div"><p style="
            font-size: 40px;
            font-weight: bold;
            text-align:center;
            ">{name}</p></div></div>""".format(
                name=st.session_state.plr["name"][p]
            )
        st.markdown(name_str, unsafe_allow_html=True)

    # ----- gene pool string -----
    with c_gp_txt:
        gp_txt_str = """<div class="parent-div"><div class="text-div"><p style="
        color:{color};
        font-size: 14px;
        text-align:right;
        ">gene<br>pool</p></div></div>""".format(
            color=st.session_state.cfg["font_color_genes"]
        )
        st.markdown(gp_txt_str, unsafe_allow_html=True)

    # ----- gene pool -----
    with c_gp:
        gp_str = """<div class="parent-div"><div class="text-div"><p style="
        color:{color};
        font-size: 40px;
        font-weight: bold;
        text-align: left
        ">{gp}</p></div></div>""".format(
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
        cnt_b = """<div class="clr-cnt-div"><div class="text-div">
            <p class="clr-cnt" style="color:{color}; text-align:right">
            {cnt}</p></div></div>""".format(
            color=st.session_state.cfg["color_blue"],
            cnt=st.session_state.plr["n_tp"][p]["b"],
        )
        st.markdown(cnt_b, unsafe_allow_html=True)

        cnt_p = """<div class="clr-cnt-div"><div class="text-div">
            <p class="clr-cnt" style="color:{color}; text-align:right">
            {cnt}</p></div></div>""".format(
            color=st.session_state.cfg["color_purple"],
            cnt=st.session_state.plr["n_tp"][p]["p"],
        )
        st.markdown(cnt_p, unsafe_allow_html=True)

    with c_col2:
        cnt_g = """<div class="clr-cnt-div"><div class="text-div">
            <p class="clr-cnt" style="color:{color}; text-align:center">
            {cnt}</p></div></div>""".format(
            color=st.session_state.cfg["color_green"],
            cnt=st.session_state.plr["n_tp"][p]["g"],
        )
        st.markdown(cnt_g, unsafe_allow_html=True)

        cnt_r = """<div class="clr-cnt-div"><div class="text-div">
            <p class="clr-cnt" style="color:{color}; text-align:center">
            {cnt}</p></div></div>""".format(
            color=st.session_state.cfg["color_red"],
            cnt=st.session_state.plr["n_tp"][p]["r"],
        )
        st.markdown(cnt_r, unsafe_allow_html=True)

    with c_col3:
        cnt_c = """<div class="clr-cnt-div"><div class="text-div">
            <p class="clr-cnt" style="color:{color}; text-align:left">
            {cnt}</p></div></div>""".format(
            color=st.session_state.cfg["color_colorless"],
            cnt=st.session_state.plr["n_tp"][p]["c"],
        )
        st.markdown(cnt_c, unsafe_allow_html=True)

        cnt_total = """<div class="clr-cnt-div"><div class="text-div">
            <p class="clr-cnt" style="text-align:left">
            {cnt}</p></div></div>""".format(
            cnt=st.session_state.plr["n_tp"][p]["sb"],
        )
        st.markdown(cnt_total, unsafe_allow_html=True)

    # ----- points -----
    with c_pnts:
        pnt_str = """<div class="ttl-scr-div"><div class="text-div"><p style="
        color:{color};
        font-size: 80px;
        font-weight: bold;
        text-align: center
        ">{gp}</p></div></div>""".format(
            color=st.session_state.cfg["font_color_total_score"],
            gp=st.session_state.plr["points"][p]["total"],
        )
        st.markdown(pnt_str, unsafe_allow_html=True)

    # ----- sub-points -----
    with c_sub1:
        st.image(image=st.session_state.images["blank_sb"], use_column_width="always")
        st.image(image=st.session_state.images["drops_sb"], use_column_width="always")

    with c_sub3:
        st.image(
            image=st.session_state.images["worlds_end_sb"], use_column_width="always"
        )
        st.image(image=st.session_state.images["MOL_sb"], use_column_width="always")

    with c_sub2:
        pnt_f = """<div class="clr-cnt-div"><div class="text-div">
            <p class="clr-cnt" style="text-align:left">
            {pnt}</p></div></div>""".format(
            pnt=st.session_state.plr["points"][p]["face"],
        )
        st.markdown(pnt_f, unsafe_allow_html=True)

        pnt_d = """<div class="clr-cnt-div"><div class="text-div">
            <p class="clr-cnt" style="text-align:left">
            {pnt}</p></div></div>""".format(
            pnt=st.session_state.plr["points"][p]["drops"],
        )
        st.markdown(pnt_d, unsafe_allow_html=True)

    with c_sub4:
        pnt_we = """<div class="clr-cnt-div"><div class="text-div">
            <p class="clr-cnt" style="text-align:left">
            {pnt}</p></div></div>""".format(
            pnt=st.session_state.plr["points"][p]["worlds_end"],
        )
        st.markdown(pnt_we, unsafe_allow_html=True)

        pnt_m = """<div class="clr-cnt-div"><div class="text-div">
            <p class="clr-cnt" style="text-align:left">
            {pnt}</p></div></div>""".format(
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

    # first, scan trait pile for any effects by any traits, like protecting
    # other traits...
    rules_tr.permanent_effects(st.session_state.plr["trait_pile"][p])

    # --- loop traits in trait pile -------------------------------------------
    for trait_idx in st.session_state.plr["trait_pile"][p]:
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
            st.image(
                image=st.session_state.images[cc + cb + cg + cp + cr + X],
                use_column_width="always",
            )

        # ----- face value -------------
        with c_trait[3]:
            trait_face = traits_df.loc[trait_idx].face
            status_face = status_df.loc[trait_idx].face

            X = "X" if trait_face != status_face else ""
            face_string = (
                trait_face if isinstance(trait_face, str) else str(int(trait_face))
            )
            st.image(
                image=st.session_state.images[face_string + X],
                use_column_width="always",
            )

        # ---------- STATE_icons -> current drop/attachment effects  ----------
        # ----- seperator -------------
        with c_trait[4]:
            st.markdown("**|**")

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
                    next_col += 1  # is this NEEDED ????
                    X = "AT"
                else:
                    X = ""

                # add new color icon
                st.image(
                    image=st.session_state.images[cc + cb + cg + cp + cr + X],
                    use_column_width="always",
                )

        # ----- drop value -------------
        cur_drops = status_df.loc[trait_idx].drops
        if traits_df.loc[trait_idx].drops == 1:
            # drop icon
            next_col += 1
            with c_trait[next_col]:
                st.image(
                    image=st.session_state.images["drops"],
                    use_column_width="always",
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

                st.image(
                    image=st.session_state.images[drop_string],
                    use_column_width="always",
                )

        # maybe add the following icons if i find a good way to do that
        if 1 == 2:
            # ----- has attachment -------------
            if status_df.loc[trait_idx].attachment != "none":
                next_col += 1
                with c_trait[next_col]:
                    st.image(
                        image=st.session_state.images["attachment"],
                        use_column_width="always",
                    )

            # ----- noFX -------------
            if (
                status_df.loc[trait_idx].inactive
                and "inactive" not in status_df.loc[trait_idx].effects_WE.lower()
            ):
                next_col += 1
                with c_trait[next_col]:
                    st.image(
                        image=st.session_state.images["noFX"],
                        use_column_width="always",
                    )

            # ----- noRemove -------------
            if status_df.loc[trait_idx].no_remove:
                next_col += 1
                with c_trait[next_col]:
                    st.image(
                        image=st.session_state.images["noRemove"],
                        use_column_width="always",
                    )

            # ----- noDiscard -------------
            if status_df.loc[trait_idx].no_discard:
                next_col += 1
                with c_trait[next_col]:
                    st.image(
                        image=st.session_state.images["noDiscard"],
                        use_column_width="always",
                    )

            # ----- noSteal -------------
            if status_df.loc[trait_idx].no_steal:
                next_col += 1
                with c_trait[next_col]:
                    st.image(
                        image=st.session_state.images["noSteal"],
                        use_column_width="always",
                    )

            # ----- noSwap -------------
            if status_df.loc[trait_idx].no_swap:
                next_col += 1
                with c_trait[next_col]:
                    st.image(
                        image=st.session_state.images["noSwap"],
                        use_column_width="always",
                    )

            # ----- if WORLDS END effects this trait -------------
            if status_df.loc[trait_idx].effects_WE != "none":
                next_col += 1
                with c_trait[next_col]:
                    st.image(
                        image=st.session_state.images["worlds_end"],
                        use_column_width="always",
                    )

                if "face" in status_df.loc[trait_idx].effects_WE.lower():
                    we_face_string = str(int(status_df.loc[trait_idx].face))
                    next_col += 1
                    with c_trait[next_col]:
                        st.image(
                            image=st.session_state.images[we_face_string],
                            use_column_width="always",
                        )

                if "inactive" in status_df.loc[trait_idx].effects_WE.lower():
                    next_col += 1
                    with c_trait[next_col]:
                        st.image(
                            image=st.session_state.images["noFX"],
                            use_column_width="always",
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
            c_slp = st.columns([0.4, 0.8, 0.99])
            with c_slp[1]:
                st.write("attach to:")
            with c_slp[2]:
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

                # create combobox
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
                    f"traits_WE_{p}_{trait_idx}",
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
                state = (
                    False if st.session_state.worlds_end["played"] != "none" else True
                )

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


# MOLs ------------------------------------------------------------------------
def MOLs(p):
    st.markdown("Meaning(s) of Life")
    for m in range(st.session_state.game["n_MOLs"]):
        st.selectbox(
            "MOL_" + str(p) + "_" + str(m),
            st.session_state.deck,
            format_func=lambda x: st.session_state.deck_str[x],
            index=None,
            placeholder="MOL #" + str(m + 1),
            label_visibility="collapsed",
            disabled=False if m == 0 else True,
        )
