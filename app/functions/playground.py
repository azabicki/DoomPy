import streamlit as st
import functions.utils as ut


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
                name=st.session_state.plr["name"][p]
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
        st.image(image=st.session_state.images["worlds_end_sb"], use_column_width="always")
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


print(st.session_state.plr["n_tp"][0]["sb"])


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
        st.button("discrad", key="discard_" + str(p), use_container_width=True)


# Trait Pile ------------------------------------------------------------------
def trait_pile(p):
    st.write("trait pile")


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
