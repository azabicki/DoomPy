import streamlit as st
import functions.utils as ut
import functions.rules_traits as rules_tr


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
    c_move, c_hand, c_disc = st.columns(3)
    with c_move:
        st.selectbox(
            "move_from_" + str(p),
            ("move to ...", "b", "b", "b"),
            label_visibility="collapsed",
        )

    with c_hand:
        st.button("to hand", key="hand_" + str(p), use_container_width=True)

    with c_disc:
        st.button("discard", key="discard_" + str(p), use_container_width=True)


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
        # columns
        c_trait = st.columns([1, 6, 1, 1])

        # get trait name
        trait = traits_df.loc[trait_idx].trait

        # trait checkbox
        with c_trait[0]:
            st.checkbox(
                trait,
                value=False,
                key=f"tp_{p}_{trait_idx}",
                on_change=update_selected_trait,
                args=(p, trait_idx),
                label_visibility="collapsed",
            )

        # traits name
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

        # color
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

        # face value
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


# -----
def update_selected_trait(p, t):
    for trait_idx in st.session_state.plr["trait_pile"][p]:
        if t == trait_idx:
            st.session_state[f"tp_{p}_{trait_idx}"] = True
            st.session_state.plr["trait_selected"][p]
        else:
            st.session_state[f"tp_{p}_{trait_idx}"] = False
