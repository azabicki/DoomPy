import streamlit as st
import numpy as np
import functions.rules_attachment as rules_at
import functions.rules_traits as rules_tr
import functions.rules_worlds_end as rules_we


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
    # genes()
    # scoring()

    # save df's
    st.session_state.df["status_df"] = status_df
    st.session_state.plr = plr


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

            # save df's
            st.session_state.df["traits_df"] = traits_df
            st.session_state.df["status_df"] = status_df
            st.session_state.plr = plr

            # update
            all()
