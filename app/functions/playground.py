import streamlit as st


# ScoreBoard ------------------------------------------------------------------
def score_board(p):

    # upper row
    c_dom1, c_dom2, c_name, c_gp_txt, c_gp = st.columns([1, 1, 3, 1, 1])
    print(st.session_state.images["no_star"])
    with c_dom1:
        str_1 = """<div class="parent-div"><div class="text-div"><img
        src="{image}"
        alt="star"
        class="img_center"/></div></div>""".format(
            image=st.session_state.images["no_star"]
        )
        st.markdown(str_1, unsafe_allow_html=True)

    with c_dom2:
        str_2 = """<div class="parent-div"><div class="text-div"><img
        src="star.png"
        alt="star"
        class="img_center"/></div></div>"""
        st.markdown(str_2, unsafe_allow_html=True)

    with c_name:
        if st.session_state["1st_player"] == p:
            name_col = st.session_state.cfg["font_color_1st_player"]
        else:
            name_col = "#000000"

        name_str = """<div class="parent-div"><div class="text-div"><p style="
        color:{color};
        font-size: 40px;
        font-weight: bold;
        text-align:center;
        ">{name}</p></div></div>""".format(
            color=name_col, name=st.session_state.plr["name"][p]
        )
        st.markdown(name_str, unsafe_allow_html=True)

    with c_gp_txt:
        gp_txt_str = """<div class="parent-div"><div class="text-div"><p style="
        color:{color};
        text-align:right;
        ">gene<br>pool</p></div></div>""".format(
            color=st.session_state.cfg["font_color_genes"]
        )
        st.markdown(gp_txt_str, unsafe_allow_html=True)

    with c_gp:
        gp_str = """<div class="parent-div"><div class="text-div"><p style="
        color:{color};
        font-size: 40px;
        text-align: left
        ">{gp}</p></div></div>""".format(
            color=st.session_state.cfg["font_color_genes"], gp=5
        )
        st.markdown(gp_str, unsafe_allow_html=True)

    # lower row


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
