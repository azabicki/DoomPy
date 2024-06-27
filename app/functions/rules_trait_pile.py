import streamlit as st
import functions.utils as ut


# single_trait_functions ######################################################
# --- AMATOXINS ---------------------------------------------------------------
def amatoxins(
    trait_idx: int,
    trait_name: str,
) -> int:
    # shorten df's
    status_df = st.session_state.df["status_df"]

    # columns
    c_trait = st.columns(3)

    # add trait
    with c_trait[0]:
        name_str = """<p style="
            color:{color};
            font-weight: bold;
            text-align:left;
            ">{trait_name}</p>""".format(
            color=st.session_state.cfg["color_purple"],
            trait_name=trait_name.upper(),
        )
        st.markdown(name_str, unsafe_allow_html=True)

    # add effect
    with c_trait[1]:
        effect_str = """<p style="
            text-align:right;
            ">discarded</p>"""
        st.markdown(effect_str, unsafe_allow_html=True)

    # add effect/?/drop icons
    # check if worlds end effect was chosen
    traits_WE = status_df.loc[trait_idx].traits_WE
    if traits_WE == "none":
        with c_trait[2]:
            st.markdown(
                ut.img2html_doubles(
                    [
                        st.session_state.images["bgpr"],
                        st.session_state.images["question_mark"],
                    ],
                    cls="Xtra_icons",
                ),
                unsafe_allow_html=True,
            )
    else:
        WE_drops = str(int(traits_WE) * -2)
        with c_trait[2]:
            # change ?/drop icon
            st.markdown(
                ut.img2html_triples(
                    [
                        st.session_state.images["bgpr"],
                        st.session_state.images["drops"],
                        st.session_state.images[WE_drops],
                    ],
                    cls="Xtra_icons",
                ),
                unsafe_allow_html=True,
            )

        print(["trait_effects", "amatoxins"], trait_idx, int(traits_WE), WE_drops)


# --- PROWLER -----------------------------------------------------------------
def prowler(
    p: int,
    trait_idx: int,
    trait_name: str,
) -> int:
    # shorten df's
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr

    # columns
    c_trait = st.columns(3)

    # add trait
    with c_trait[0]:
        name_str = """<p style="
            color:{color};
            font-weight: bold;
            text-align:left;
            ">{trait_name}</p>""".format(
            color=st.session_state.cfg["color_purple"],
            trait_name=trait_name.upper(),
        )
        st.markdown(name_str, unsafe_allow_html=True)

    # add effect
    with c_trait[1]:
        effect_str = """<p style="
            text-align:right;
            ">less</p>"""
        st.markdown(effect_str, unsafe_allow_html=True)

    with c_trait[2]:
        WE_drops = status_df.loc[trait_idx].effects.split()
        st.markdown(
            ut.img2html_triples(
                [
                    st.session_state.images["bgpr"],
                    st.session_state.images["drops"],
                    st.session_state.images[WE_drops[p]],
                ],
                cls="Xtra_icons",
            ),
            unsafe_allow_html=True,
        )

    print(["trait_effects", "prowler"], trait_idx, plr["name"][p], WE_drops[p])


# --- SHINY -------------------------------------------------------------------
def shiny(p: int, trait_idx: int) -> int:
    # shorten df's
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr

    # columns
    c_trait = st.columns(3)

    # add trait
    with c_trait[0]:
        name_str = """<p style="
            color:{color};
            font-weight: bold;
            text-align:left;
            ">SHINY</p>""".format(
            color=st.session_state.cfg["color_green"],
        )
        st.markdown(name_str, unsafe_allow_html=True)

    # add effect
    with c_trait[1]:
        effect_str = """<p style="
            text-align:right;
            ">punishes</p>"""
        st.markdown(effect_str, unsafe_allow_html=True)

    with c_trait[2]:
        shiny_dp = status_df.loc[trait_idx].effects.split()
        st.markdown(
            ut.img2html_triples(
                [
                    st.session_state.images["c"],
                    st.session_state.images["drops"],
                    st.session_state.images[shiny_dp[p]],
                ],
                cls="Xtra_icons",
            ),
            unsafe_allow_html=True,
        )

    print(["trait_effects", "shiny"], trait_idx, plr["name"][p], shiny_dp[p])


# --- SPORES ------------------------------------------------------------------
def spores(
    p: int,
    spores_effect: str,
    trait_idx: str,
) -> int:
    # shorten df's
    plr = st.session_state.plr

    # check if more players are affected
    if "_" in spores_effect:
        spores_effect = spores_effect.split("_")

    # print Spores effects if this player is affected
    n_genes = sum(str(p) == i for i in spores_effect)
    if n_genes > 0:
        # columns
        c_trait = st.columns(3)

        # add trait
        with c_trait[0]:
            name_str = """<p style="
                color:{color};
                font-weight: bold;
                text-align:left;
                ">SPORES</p>""".format(
                color=st.session_state.cfg["color_green"],
            )
            st.markdown(name_str, unsafe_allow_html=True)

        # add effect
        with c_trait[1]:
            effect_str = """<p style="
                text-align:right;
                ">adds</p>"""
            st.markdown(effect_str, unsafe_allow_html=True)

        # add gene_pool icon
        with c_trait[2]:
            st.markdown(
                ut.img2html_doubles(
                    [
                        st.session_state.images["gene_pool"],
                        st.session_state.images[str(n_genes)],
                    ],
                    cls="Xtra_icons",
                ),
                unsafe_allow_html=True,
            )

        print(["trait_effects", "spores"], trait_idx, n_genes, plr["name"][p])


# --- VIRAL -------------------------------------------------------------------
def viral(
    p: int,
    trait_idx: int,
    trait_name: str,
) -> int:
    # shorten df's
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr

    # columns
    c_trait = st.columns(3)

    # add trait
    with c_trait[0]:
        name_str = """<p style="
            color:{color};
            font-weight: bold;
            text-align:left;
            ">{trait_name}</p>""".format(
            color=st.session_state.cfg["color_purple"],
            trait_name=trait_name.upper(),
        )
        st.markdown(name_str, unsafe_allow_html=True)

    # add effect
    with c_trait[1]:
        effect_str = """<p style="
            text-align:right;
            ">punishes</p>"""
        st.markdown(effect_str, unsafe_allow_html=True)

    # check if worlds end effect was chosen
    trait_WE = status_df.loc[trait_idx].traits_WE
    if trait_WE == "none":
        with c_trait[2]:
            st.markdown(
                ut.img2html(
                    st.session_state.images["question_mark"],
                    div="div_icons",
                    cls="icons",
                ),
                unsafe_allow_html=True,
            )
    else:
        WE_drops = status_df.loc[trait_idx].effects.split()

        # change effect/?/drop icon
        with c_trait[2]:
            st.markdown(
                ut.img2html_triples(
                    [
                        st.session_state.images[trait_WE[0]],
                        st.session_state.images["drops"],
                        st.session_state.images[WE_drops[p]],
                    ],
                    cls="Xtra_icons",
                ),
                unsafe_allow_html=True,
            )

        print(
            ["trait_effects", "viral"],
            trait_idx,
            trait_WE,
            plr["name"][p],
            WE_drops[p],
        )


# checking for specific traits ################################################
# - if they are played, run the respective function
def special_trait_effects(p: int) -> int:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr

    # --- AMATOXINS --- add passively Amatoxins to this trait pile ------------
    amatoxins_idx = traits_df.index[traits_df.trait == "Amatoxins"].tolist()
    if (
        amatoxins_idx != []
        and any([amatoxins_idx[0] in tp for tp in plr["trait_pile"]])
        and amatoxins_idx[0] not in plr["trait_pile"][p]
    ):
        amatoxins(amatoxins_idx[0], "Amatoxins")

    # --- PROWLER --- add passively Prowler to this trait pile ----------------
    prowler_idx = traits_df.index[traits_df.trait == "Prowler"].tolist()
    if (
        prowler_idx != []
        and any([prowler_idx[0] in tp for tp in plr["trait_pile"]])
        and prowler_idx[0] not in plr["trait_pile"][p]
    ):
        prowler(p, prowler_idx[0], "Prowler")

    # --- SHINY --- add passively Shiny to this trait pile --------------------
    shiny_idx = traits_df.index[traits_df.trait == "Shiny"].tolist()
    if (
        shiny_idx != []
        and any([shiny_idx[0] in tp for tp in plr["trait_pile"]])
        and shiny_idx[0] not in plr["trait_pile"][p]
    ):
        shiny(p, shiny_idx[0])

    # --- SPORES --- add passively Viral to this trait pile -------------------
    spores_idx = traits_df.index[traits_df.trait == "Spores"].tolist()
    if spores_idx != []:
        spores_effect = status_df.iloc[spores_idx[0]].effects
        if spores_effect != "none":
            spores(p, spores_effect, spores_idx[0])

    # --- VIRAL --- add passively Viral to this trait pile --------------------
    viral_idx = traits_df.index[traits_df.trait == "Viral"].tolist()
    if (
        viral_idx != []
        and any([viral_idx[0] in tp for tp in plr["trait_pile"]])
        and viral_idx[0] not in plr["trait_pile"][p]
    ):
        viral(p, viral_idx[0], "Viral")

    # --- OPPOSABLE THUMBS --- copy first traits effects, if listed here ------
    oppo_idx = traits_df.index[traits_df.trait == "Opposable Thumbs"].tolist()
    if (
        oppo_idx != []
        and any(oppo_idx[0] in tp for tp in plr["trait_pile"])
        and oppo_idx[0] not in plr["trait_pile"][p]
    ):

        oppo_at = [i for i, tp in enumerate(plr["trait_pile"]) if oppo_idx[0] in tp][0]
        first_D = [
            traits_df.loc[i].trait
            for i in plr["trait_pile"][oppo_at]
            if (traits_df.loc[i].dominant == 1 and i != oppo_idx[0])
        ][0]
        match first_D:
            case "Amatoxins":
                amatoxins(oppo_idx[0], "Opp. Thumbs")

            case "Prowler":
                prowler(p, oppo_idx[0], "Opp. Thumbs")

            case "Viral":
                viral(p, oppo_idx[0], "Opp. Thumbs")
