import bisect
import streamlit as st
import functions.variables as vars
import functions.rules_play as rules_pl
import functions.rules_attachment as rules_at


# -----------------------------------------------------------------------------
def start_game(what: str = "boot"):
    print(f"starting game by '{what}'")

    # reset variables ---------------------------------------------------------
    vars.reset_variables()

    # clear traits listbox ----------------------------------------------------
    btn_clear_trait_search()


# -----------------------------------------------------------------------------
def play_trait(to: int) -> int:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr
    deck = st.session_state.deck

    # return, if no trait selected
    if st.session_state.trait2play is None:
        print("exit no card")
        return 0

    # get card
    trait_idx = st.session_state.trait2play
    trait = st.session_state.df["traits_df"].loc[trait_idx].trait

    # return, if any trait specific requirements are not met
    if rules_pl.check_requirement(trait_idx, to):
        print("exit requirement")
        return 0

    # return, if player already has two dominants
    if traits_df.loc[trait_idx].dominant == 1:
        if (
            sum([1 for t in plr["trait_pile"][to] if traits_df.loc[t].dominant == 1])
            >= 2
        ):
            # check if HEROIC is born during 'Birth of a Hero'
            heroic_idx = traits_df.index[traits_df.trait == "Heroic"].tolist()
            if heroic_idx != []:
                heroic_is_born = status_df.loc[heroic_idx[0], "effects"]
            else:
                heroic_is_born = False

            # no hero, then return
            if heroic_is_born and trait_idx == heroic_idx[0]:
                print(["play", "heroic"])
            else:
                print(["play", "error_2dominants"], plr["name"][to])
                return 0

    # return, if attachment does not have any trait to attach to
    if traits_df.loc[trait_idx].attachment == 1:
        attachables = rules_at.filter_attachables(trait_idx, to)
        if len(attachables) == 0:
            print(["play", "error_no_attachables"], plr["name"][to])
            return 0

    # log
    print(["play", "play"], plr["name"][to], trait, trait_idx)

    # check for rules/effects to apply when playing this trait
    rules_pl.play_effect(trait_idx, to)

    # add to players traits & update trait_pile
    bisect.insort_left(plr["trait_pile"][to], trait_idx)

    # remove from deck & update deck_listbox
    deck.remove(trait_idx)
    btn_clear_trait_search()

    # shorten df's
    st.session_state.df["traits_df"] = traits_df
    st.session_state.df["status_df"] = status_df
    st.session_state.plr = plr
    st.session_state.deck = deck

    # update
#    update_all()

    return 1


# -------
def btn_clear_trait_search():
    st.session_state.trait2play = None
