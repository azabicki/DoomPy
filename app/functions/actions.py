import bisect
import streamlit as st
import numpy as np
import functions.updates as update
import functions.variables as vars
import functions.rules_play as rules_pl
import functions.rules_attachment as rules_at
import functions.rules_remove as rules_re


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

    # save df's
    st.session_state.df["traits_df"] = traits_df
    st.session_state.df["status_df"] = status_df
    st.session_state.plr = plr
    st.session_state.deck = deck

    # update
    update.all()

    return 1


# -----------------------------------------------------------------------------
def move_trait(from_: int) -> None:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr

    # get card, its attachment & target
    trait_idx = plr["trait_selected"][from_]

    if not np.isnan(trait_idx):
        if traits_df.loc[trait_idx].attachment == 1:
            attachment = trait_idx
            trait_idx = status_df.loc[attachment, "host"]
            trait_idx = np.nan if trait_idx == 'none' else trait_idx
        else:
            attachment = status_df.loc[trait_idx].attachment

    sbox_str = st.session_state[f"move_to_{from_}"]
    if sbox_str != "move to":
        to = [i for i in plr["name"]].index(sbox_str)

    # clear selectbox
    st.session_state[f"move_to_{from_}"] = "move to"

    if sbox_str == "move to":
        print("___ move: ", from_, " -> ...")
    else:
        print("___ move: ", from_, " -> ", to)

    print("___ move idx: ", trait_idx)
    if not np.isnan(trait_idx):
        print("___ attachment: ", attachment)

    # return, if no target selected
    if sbox_str == "move to":
        print(["move", "error_move_to"])
        return

    # return, if no trait selected
    if np.isnan(trait_idx):
        # cbox_move_to.current(0)
        print(["move", "error_no_trait"])
        return

    # log
    add_txt = (
        "(and its attachment '{}' (id:{}))".format(
            traits_df.loc[attachment].trait, attachment
        )
        if attachment != "none"
        else ""
    )
    print(
        ["move", "move_to"],
        traits_df.loc[trait_idx].trait,
        trait_idx,
        add_txt,
        plr["name"][from_],
        plr["name"][to],
    )

    # remove traits(s) from 'giving' player - update trait_pile - check
    # remove_rules - clear trait selection
    plr["trait_pile"][from_].remove(trait_idx)
    if attachment != "none":
        plr["trait_pile"][from_].remove(attachment)

    rules_re.check_trait(trait_idx, from_, "different_trait_pile")

    plr["trait_selected"][from_] = np.nan
    st.session_state[f"tp_{from_}_{trait_idx}"] = False

    # add to 'receiving' players traits
    bisect.insort_left(plr["trait_pile"][to], trait_idx)
    if attachment != "none":
        bisect.insort_left(plr["trait_pile"][to], attachment)

    # update
    update.all()


# -----------------------------------------------------------------------------
def attach_to(
    from_: int, attachment_idx: int, event: int, possible_hosts: list
) -> None:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]

    # get host_data from event_data
    host = st.session_state[f"attchmnt_{attachment_idx}"]
    host_idx = possible_hosts[host]
    attachment = traits_df.loc[attachment_idx].trait

    # return, if clicked on current host
    old_host_idx = status_df[
        status_df["attachment"] == attachment_idx
    ].index.values.tolist()
    if host_idx in old_host_idx:
        print(["attach_to", "error_current_host"])
        return

    # log
    if host == " ... ":
        if len(old_host_idx) == 0:
            print(["attach_to", "still_detached"], attachment, attachment_idx)
        else:
            print(["attach_to", "detached"], attachment, attachment_idx)
    else:
        print(
            ["attach_to", "attached"],
            st.session_state.plr["name"][from_],
            attachment,
            attachment_idx,
            host,
            host_idx,
        )

    # update old_host, where attachment was removed from
    if old_host_idx:
        print(
            ["attach_to", "change_host"],
            traits_df.loc[old_host_idx[0]].trait,
            old_host_idx[0],
        )
        update.traits_current_status("reset", old_host_idx[0], [])

    # check if attachment is set back to "..." (idx=0)
    if host_idx is None:
        # reset host='none' to status_row of attachment
        status_df.loc[attachment_idx, "host"] = "none"
    else:
        # update status of attachment/host - saving idx's of each other
        status_df.loc[attachment_idx, "host"] = host_idx
        status_df.loc[host_idx, "attachment"] = attachment_idx

    # save df's
    st.session_state.df["traits_df"] = traits_df
    st.session_state.df["status_df"] = status_df

    # update
    update.all()


# -----------------------------------------------------------------------------
def btn_clear_trait_search():
    st.session_state.trait2play = None
