import streamlit as st
import numpy as np
import functions.rules_attachment as rules_at
import functions.rules_traits as rules_tr
import functions.rules_worlds_end as rules_we
import functions.rules_drop as rules_dr
import functions.rules_MOL as rules_mol


# -----------------------------------------------------------------------------
def all() -> None:
    # shorten df's
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr

    # first: resolve all effects on traits, then: update n_TP (count) &
    for p in range(st.session_state.game["n_player"]):
        # get  player's trait pile
        tp = plr["trait_pile"][p]

        # resolve all effects on traits --------------------
        for trait_idx in tp:
            # 1: attachment effect
            rules_at.apply_effects(trait_idx)

            # 2: traits WE effect(s)
            rules_tr.apply_traits_WE_effects(trait_idx)

            # 3: worlds end effect
            rules_we.apply_WE_effects(trait_idx)

        # update n_tp --------------------
        # colors
        for col in ["blue", "green", "purple", "red", "colorless"]:
            plr["n_tp"][p][col[0]] = sum(
                col in color.lower() for color in status_df.iloc[tp].color.tolist()
            )

        # total
        plr["n_tp"][p]["t"] = len(tp) + plr["n_tp"][p]["xtra"]

        # scoreboard
        if plr["n_tp"][p]["xtra"] == 0:
            txt = "\u2211" + str(len(tp))
        else:
            txt = str(len(tp)) + "+" + str(plr["n_tp"][p]["xtra"])
        plr["n_tp"][p]["sb"] = txt

    # # update stuff
    # stars()
    genes()
    scoring()

    # save df's
    st.session_state.df["status_df"] = status_df
    st.session_state.plr = plr




# -----------------------------------------------------------------------------
def genes() -> None:
    # shorten df's
    status_df = st.session_state.df["status_df"]
    traits_df = st.session_state.df["traits_df"]
    catastrophes_df = st.session_state.df["catastrophes_df"]
    plr = st.session_state.plr

    # init vars
    diff_genes = [0] * st.session_state.game["n_player"]

    # loop players and calculate +- genes of all played traits ----------------
    for p in range(st.session_state.game["n_player"]):
        # loop traits in trait_pile
        for trait_idx in plr["trait_pile"][p]:
            # continue to next trait in tp if current trait is inactive
            if status_df.loc[trait_idx].inactive:
                continue

            # get gene effect of this card
            who = traits_df.loc[trait_idx].gene_pool_target
            effect = traits_df.loc[trait_idx].gene_pool_effect
            rule = traits_df.loc[trait_idx].gene_pool_rule

            # if there is an effect and no restrictions
            if isinstance(who, str) and not isinstance(rule, str):
                match who:
                    case "all":
                        diff_genes = [i + int(effect) for i in diff_genes]
                    case "self":
                        diff_genes[p] += int(effect)
                    case "opponents":
                        diff_genes = [
                            g + int(effect) if i != p else g
                            for i, g in enumerate(diff_genes)
                        ]

                # log
                print(
                    ["genes", "trait"],
                    plr["name"][p],
                    traits_df.loc[trait_idx].trait,
                    trait_idx,
                    int(effect),
                    who,
                    diff_genes,
                )

    # check for special effects by specific traits ----------------------------
    # ----- Denial --------------
    dnl_idx = traits_df.index[traits_df.trait == "Denial"].tolist()
    if dnl_idx != []:
        dnl_effect = status_df.loc[dnl_idx[0]].effects
        if dnl_effect != "none":
            # find player
            dnl_in = [dnl_idx[0] in tp for tp in plr["trait_pile"]]
            dnl_p = dnl_in.index(True)

            if dnl_effect == "The Four Horsemen":
                # log
                print(
                    ["genes", "denial_t4h"],
                    dnl_idx[0],
                    plr["name"][dnl_p],
                    dnl_effect,
                    diff_genes,
                )
            else:
                # reverse effect
                reverse_effect = (
                    catastrophes_df[
                        catastrophes_df.name == dnl_effect
                    ].gene_pool.values[0]
                    * -1
                )
                diff_genes[dnl_p] += int(reverse_effect)

                # log
                print(
                    ["genes", "denial"],
                    dnl_idx[0],
                    plr["name"][dnl_p],
                    dnl_effect,
                    diff_genes,
                )

    # ----- Sleepy --------------
    slp_idx = traits_df.index[traits_df.trait == "Sleepy"].tolist()
    if slp_idx != []:
        slp_eff = [i for i in st.session_state.game["sleepy_spinbox"]]
        diff_genes = [diff_genes[x] + slp_eff[x] for x in range(len(diff_genes))]
        if any(slp_eff):
            p = [i for i, e in enumerate(slp_eff) if e != 0]
            print(["genes", "sleepy"], plr["name"][p[0]], slp_eff[p[0]], diff_genes)

    # ----- Spores ---------------
    sprs_idx = traits_df.index[traits_df.trait == "Spores"].tolist()
    if sprs_idx != []:
        sprs_eff = status_df.loc[sprs_idx[0]].effects
        if sprs_eff != "none":
            # check if more players are affected
            if "_" in sprs_eff:
                sprs_eff = sprs_eff.split("_")

            # apply effects
            for eff in sprs_eff:
                p = int(eff)
                diff_genes[p] += 1

                # log
                print(["genes", "spores"], sprs_idx[0], plr["name"][p], diff_genes)

    # check what catastrophes were played already -----------------------------
    for c in range(st.session_state.game["n_catastrophes"]):
        # get card & effect
        c_idx = st.session_state.catastrophe["played"][c]

        # check if catastrophe was played
        if c_idx is not None:
            c_str = catastrophes_df.loc[c_idx, "name"]
            # get effect and apply it
            effect = int(catastrophes_df.loc[c_idx].gene_pool)
            diff_genes = [i + effect for i in diff_genes]

            # log
            print(["genes", "catastrophe"], c_str, effect, diff_genes)

    # update gene values ------------------------------------------------------
    for p in range(st.session_state.game["n_player"]):
        new_gp = st.session_state.game["n_genes"] + diff_genes[p]
        if new_gp > 8:
            plr["genes"][p] = 8
        elif new_gp < 1:
            plr["genes"][p] = 1
        else:
            plr["genes"][p] = new_gp

    # log - if genes are effected
    if any(i > 0 for i in diff_genes):
        print(
            ["genes", "total_effect"],
            diff_genes,
            [plr["genes"][i] for i in range(st.session_state.game["n_player"])],
        )

    # save df's
    st.session_state.plr = plr


# -----------------------------------------------------------------------------
def scoring() -> None:
    # shorten df's
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr

    # first, calculate all scores
    p_worlds_end = []
    p_face = []
    p_drop = []
    p_MOL = []
    total = []
    for p in range(st.session_state.game["n_player"]):
        # get cards
        trait_pile = plr["trait_pile"][p]

        # calculate world's end points
        p_worlds_end.append(
            rules_we.calc_WE_points(p)
            if st.session_state.worlds_end["played"] != "none"
            else 0
        )

        # calculate face value
        p_face.append(
            int(
                sum(
                    [
                        status_df.loc[trait_idx].face
                        for trait_idx in trait_pile
                        if not isinstance(status_df.loc[trait_idx].face, str)
                    ]
                )
            )
        )

        # calculate drops points
        p_drop.append(rules_dr.drop_points(p))

        # calculate MOL points
        p_MOL.append(calc_MOLs(p))

        # calculate total score
        total.append(p_face[p] + p_drop[p] + p_worlds_end[p] + p_MOL[p])

    # calculate RANK
    r_face = [sorted(p_face, reverse=True).index(x) + 1 for x in p_face]
    r_drop = [sorted(p_drop, reverse=True).index(x) + 1 for x in p_drop]
    r_WE = [sorted(p_worlds_end, reverse=True).index(x) + 1 for x in p_worlds_end]
    r_MOL = [sorted(p_MOL, reverse=True).index(x) + 1 for x in p_MOL]
    r_total = [sorted(total, reverse=True).index(x) + 1 for x in total]
    add = {
        1: "\u02e2\u1d57",
        2: "\u207f\u1d48",
        3: "\u02b3\u1d48",
        4: "\u1d57\u02b0",
        5: "\u1d57\u02b0",
        6: "\u1d57\u02b0",
    }

    # show current scoring according to setting
    for p in range(st.session_state.game["n_player"]):
        # update points
        if st.session_state.game["points_onoff"] == "on":
            plr["points"][p]["face"] = p_face[p]
            plr["points"][p]["drops"] = p_drop[p]
            plr["points"][p]["worlds_end"] = p_worlds_end[p]
            plr["points"][p]["MOL"] = p_MOL[p]
            plr["points"][p]["total"] = total[p]
        elif st.session_state.game["points_onoff"] == "rank":
            plr["points"][p]["face"] = str(r_face[p]) + add[r_face[p]]
            plr["points"][p]["drops"] = str(r_drop[p]) + add[r_drop[p]]
            plr["points"][p]["worlds_end"] = str(r_WE[p]) + add[r_WE[p]]
            plr["points"][p]["MOL"] = str(r_MOL[p]) + add[r_MOL[p]]
            plr["points"][p]["total"] = str(r_total[p]) + add[r_total[p]]
        else:
            plr["points"][p]["face"] = "\u2736"
            plr["points"][p]["drops"] = "\u2736"
            plr["points"][p]["worlds_end"] = "\u2736"
            plr["points"][p]["MOL"] = "\u2736"
            plr["points"][p]["total"] = "\u2736"

        # log
        print(
            ["scoring", "update"],
            plr["name"][p],
            p_face[p],
            p_drop[p],
            p_worlds_end[p],
            p_MOL[p],
            total[p],
        )

    # save df's
    st.session_state.plr = plr


# -----------------------------------------------------------------------------
def calc_MOLs(p: int) -> None:
    # shorten df's
    MOLs = st.session_state.MOLs
    plr = st.session_state.plr
    MOLs_df = st.session_state.df["MOLs_df"]

    p_MOL = 0
    for m in range(st.session_state.MOLs["n"][p]):
        # calculate, if MOL is selected
        if MOLs["played"][p][m] is not None:
            # calculate points
            p_MOL_m = rules_mol.calc_MOL_points(p, m)

            # update sum of MOL points
            p_MOL += p_MOL_m

            # log
            print(
                ["MOLs", "MOL_points"],
                plr["name"][p],
                MOLs_df.loc[MOLs["played"][p][m]].MOL,
                MOLs["played"][p][m],
                p_MOL_m,
            )

        # update points_icon of MOL
        if MOLs["played"][p][m] is not None and st.session_state.game["points_onoff"] == "on":
            plr["points_MOL"][p][m] = p_MOL_m
        else:
            plr["points_MOL"][p][m] = 0

    return p_MOL


# -----------------------------------------------------------------------------
def sleepy(p):
    st.session_state.game["sleepy_spinbox"][p] = st.session_state.sleepy_input
    all()


# -----------------------------------------------------------------------------
def selected_trait(p, t):
    for trait_idx in st.session_state.plr["trait_pile"][p]:
        if t == trait_idx:
            st.session_state[f"tp_{p}_{trait_idx}"] = True
            st.session_state.plr["trait_selected"][p] = t
        else:
            st.session_state[f"tp_{p}_{trait_idx}"] = False


# -----------------------------------------------------------------------------
def traits_current_status(todo: str, *args) -> None:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr

    # space for various effects which may affect traits in certain situations
    # (like Neoteny...)
    match todo:
        # 'reset' routine to reset traits status_df_row to initial state
        case "reset":
            trait = args[0]
            reset_rule = args[-1]

            # backup current state
            bkp = status_df.loc[trait].copy()

            # reset trait
            true_color = traits_df.loc[trait].color
            true_face = traits_df.loc[trait].face

            status_df.loc[trait, "color"] = true_color
            status_df.loc[trait, "face"] = true_face
            status_df.loc[trait, "drops"] = np.nan
            status_df.loc[trait, "host"] = "none"
            status_df.loc[trait, "attachment"] = "none"
            status_df.loc[trait, "inactive"] = False
            status_df.loc[trait, "no_remove"] = False
            status_df.loc[trait, "no_discard"] = False
            status_df.loc[trait, "no_steal"] = False
            status_df.loc[trait, "no_swap"] = False
            status_df.loc[trait, "effects"] = "none"
            status_df.loc[trait, "effects_attachment"] = "none"
            status_df.loc[trait, "effects_traits_WE"] = "none"
            status_df.loc[trait, "effects_WE"] = "none"
            status_df.loc[trait, "traits_WE"] = "none"

            # apply rule after resetting
            match reset_rule:
                case "keep_trait_effect":
                    status_df.loc[trait, "effects"] = bkp.effects

            # log
            print(["update_trait_status", "reset"], traits_df.loc[trait].trait, trait)

            # save df's
            st.session_state.df["traits_df"] = traits_df
            st.session_state.df["status_df"] = status_df
            st.session_state.plr = plr

        # Neoteny-Checkbox is clicked somewhere
        case "neoteny":
            neoteny_idx = traits_df.index[traits_df.trait == "Neoteny"].tolist()[0]
            p = args[0]

            # update current player
            st.session_state.game["neoteny_checkbutton"][p] = (
                1 if st.session_state[f"neoteny_{p}"] else 0
            )

            # set other player to 0
            for i in range(st.session_state.game["n_player"]):
                if i != p:
                    st.session_state.game["neoteny_checkbutton"][i] = 0

            # update 'cur_effect'
            if not any([i for i in st.session_state.game["neoteny_checkbutton"]]):
                status_df.loc[neoteny_idx, "effects"] = "none"
                print(["update_trait_status", "neoteny_no_one"])
            else:
                status_df.loc[neoteny_idx, "effects"] = str(p)
                print(["update_trait_status", "neoteny_that_one"], plr["name"][p])

            # update
            all()


# -----------------------------------------------------------------------------
def count_dominants(p):
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    plr = st.session_state.plr

    # number of dominant traits
    n_dominant = np.nansum(
        [traits_df.loc[trait_idx].dominant for trait_idx in plr["trait_pile"][p]]
    )

    # check special cases
    Epic_idx = traits_df.index[traits_df.trait == "Epic"].tolist()
    if Epic_idx != [] and Epic_idx[0] in plr["trait_pile"][p]:
        n_dominant = 2
        print(["stars", "epic"], plr["name"][p])

    return n_dominant
