import streamlit as st
import bisect
import numpy as np
import functions.updates as update
import functions.variables as vars
import functions.rules_MOL as rules_mol
import functions.rules_play as rules_pl
import functions.rules_remove as rules_re
import functions.rules_traits as rules_tr
import functions.rules_attachment as rules_at


# -----------------------------------------------------------------------------
def start_game(what: str = "boot"):
    print(f"starting game by '{what}'")

    # reset variables ---------------------------------------------------------
    vars.reset_variables()

    # clear traits listbox ----------------------------------------------------
    clear_trait_search()


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
    clear_trait_search()

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
            trait_idx = np.nan if trait_idx == "none" else trait_idx
        else:
            attachment = status_df.loc[trait_idx].attachment

    sbox_str = st.session_state[f"move_to_{from_}"]
    if sbox_str != "move to":
        to = [i for i in plr["name"]].index(sbox_str)

    # clear selectbox
    st.session_state[f"move_to_{from_}"] = "move to"

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
# def remove_trait(from_: int, where_to: str, *args) -> None:
def remove_trait(from_: int, where_to: str, *args) -> None:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr
    deck = st.session_state.deck

    # get card & its attachment
    trait_idx = plr["trait_selected"][from_]

    if not np.isnan(trait_idx):
        if traits_df.loc[trait_idx].attachment == 1:
            attachment = trait_idx
            trait_idx = status_df.loc[attachment, "host"]
            trait_idx = np.nan if trait_idx == "none" else trait_idx
        else:
            attachment = status_df.loc[trait_idx].attachment

    # return, if no trait selected
    if np.isnan(trait_idx):
        print(["remove", "error_no_trait"])
        return

    # log
    if where_to == "hand":
        print(
            ["remove", "hand"],
            plr["name"][from_],
            traits_df.loc[trait_idx].trait,
            trait_idx,
        )
    else:
        print(
            ["remove", "discard"],
            plr["name"][from_],
            traits_df.loc[trait_idx].trait,
            trait_idx,
        )
    if attachment != "none":
        print(
            ["remove", "discard_attachment"],
            traits_df.loc[attachment].trait,
            attachment,
        )

    # remove card(s) from player & clear player trait selection
    plr["trait_pile"][from_].remove(trait_idx)
    if attachment != "none":
        plr["trait_pile"][from_].remove(attachment)
    plr["trait_selected"][from_] = np.nan

    # add to deck traits & update deck_listbox
    bisect.insort_left(deck, trait_idx)
    if attachment != "none":
        bisect.insort_left(deck, attachment)

    # check, if this trait has a special "remove-rule",
    # which may be needed for "status_updating"
    remove_rule = rules_re.check_trait(trait_idx, from_, where_to)

    # reset current status of card(s)
    update.traits_current_status("reset", trait_idx, remove_rule)
    if attachment != "none":
        update.traits_current_status("reset", attachment, [])

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

    # update
    update.all()


# -----------------------------------------------------------------------------
def traits_world_end(from_: int, trait_idx: int) -> None:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]

    # get index of WE_effect
    effect = st.session_state[f"twe_{trait_idx}"]
    effect_idx = rules_tr.traits_WE_tasks(trait_idx).index(effect)

    # log
    if effect_idx == 0:
        print(["traits_WE", "reset"], traits_df.loc[trait_idx].trait, trait_idx)
    else:
        print(
            ["traits_WE", "set"], traits_df.loc[trait_idx].trait, trait_idx, effect
        )

    # set traits_WE-effect to status_df of trait
    if effect_idx == 0:
        status_df.loc[trait_idx, "traits_WE"] = "none"
    else:
        status_df.loc[trait_idx, "traits_WE"] = effect

    # apply traits_WE-effects and update status of traits in this trait pile
    rules_tr.assign_traits_WE_effects(trait_idx, st.session_state.plr["trait_pile"][from_])

    # update
    update.all()


# -----------------------------------------------------------------------------
def manual_drops(trait: int) -> None:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]

    # change value according to button
    value = st.session_state[f"drop_{trait}"]

    # save value in status_df
    status_df.loc[trait, "drops"] = value

    # log
    print(["scoring", "manual_drops"], traits_df.iloc[trait].trait, trait, value)

    # update all
    update.all()


# -----------------------------------------------------------------------------
def manual_MOL(p: int, m: int) -> None:
    # shorten df's
    plr = st.session_state.plr

    # change value according to button
    value = st.session_state[f"mol_points_{p}_{m}"]

    # save current value
    plr["points_MOL"][p][m] = value

    # update all
    update.all()


# -----------------------------------------------------------------------------
def manual_we(p: int) -> None:
    # shorten df's
    plr = st.session_state.plr

    # change value according to button
    value = st.session_state[f"we_points_{p}"]

    # save value in status_df
    plr["points_WE_effect"][p] = value

    # update scoring
    update.scoring()


# -----------------------------------------------------------------------------
def select_MOL(p: int, m: int) -> None:
    # shorten df's
    plr = st.session_state.plr
    MOLs = st.session_state.MOLs
    MOLs_df = st.session_state.df["MOLs_df"]

    # get infos of played/selected MOLs
    cbox_idx = st.session_state[f"MOL_{p}_{m}"]
    if cbox_idx == 0:
        played_idx = None
    else:
        played_idx = cbox_idx - 1
        played_str = MOLs_df.loc[played_idx].MOL
    played_previously = MOLs["played"][p][m]

    # return, if no MOL selected now and previously
    if cbox_idx == 0 and played_previously is None:
        # log
        print(["MOLs", "error_no_MOL"], m + 1, plr["name"][p])
        return

    # return, if same MOL selected
    if cbox_idx != 0 and (played_idx == played_previously):
        # log
        print(["MOLs", "error_keep_MOL"], m + 1, plr["name"][p], played_str)
        return

    # if MOL is de-selected
    if cbox_idx == 0:
        # log
        print(
            ["MOLs", "deselected_MOL"],
            plr["name"][p],
            m + 1,
            MOLs_df.loc[played_previously].MOL,
        )
    else:
        # log
        print(["MOLs", "MOL"], m + 1, plr["name"][p], played_str, played_idx)

    # set played MOL
    MOLs["played"][p][m] = played_idx

    # check for MOL_specific select_effects
    rules_mol.select_MOL(p, played_idx, played_previously)

    # update
    update.all()


# -----------------------------------------------------------------------------
def select_catastrophe(c: int, pos_cat_str) -> None:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]
    catastrophes_df = st.session_state.df["catastrophes_df"]
    catastrophe = st.session_state.catastrophe
    plr = st.session_state.plr

    # get played catastrophe
    cbox_idx = st.session_state[f"catastrophe_{c}"]
    if cbox_idx > 0:
        played_idx = catastrophe["possible"][c][cbox_idx - 1]
    played_str = pos_cat_str[cbox_idx]
    played_previously = catastrophe["played"][c]

    # return, if no catastrophe was selected
    if cbox_idx == 0:
        # if no catastrophe was selected before
        if played_previously is None:
            print(["catastrophe", "error_no_catastrophe"], c + 1)
        # else -> forced to keep previous selection
        else:
            old_cbox_idx = catastrophe["possible"][c].index(played_previously) + 1
            st.session_state[f"catastrophe_{c}"] = old_cbox_idx
            print(["catastrophe", "error_keep_catastrophe"], c + 1)
        return

    # return, if same catastrophe selected
    if played_previously == played_idx:
        print(["catastrophe", "error_same_catastrophe"], c + 1, played_str)
        return

    # log
    print(["catastrophe", "catastrophe"], c + 1, played_str, played_idx)

    # set played catastrophe
    catastrophe["played"][c] = played_idx

    # update possible catastrophes for other catastrophes
    for i in [i for i in range(st.session_state.game["n_catastrophes"]) if i != c]:
        # begin with ALL possible catastrophes - necessary bc this catastrophe may have changed
        catastrophe["possible"][i] = catastrophes_df.index.tolist()

        # remove other catastrophes from possible ones
        for j in [j for j in range(st.session_state.game["n_catastrophes"]) if j != i]:
            # only, if j'th catastrophe was played already
            if catastrophe["played"][j] is not None:
                # remove from list of possibles
                catastrophe["possible"][i].remove(catastrophe["played"][j])

    # --- if DENIAL is out there, save first catastrophe he sees ---
    denial_idx = traits_df.index[traits_df.trait == "Denial"].tolist()
    if (
        denial_idx != []
        and any(denial_idx[0] in tp for tp in plr["trait_pile"])
        and status_df.loc[denial_idx[0]].effects == "none"
    ):
        status_df.loc[denial_idx[0], "effects"] = played_str

    # update first player
    n_cat = sum(i is not None for i in catastrophe["played"])
    cur_fp = st.session_state["1st_player"]
    cur_fp = cur_fp + 1
    if cur_fp > st.session_state.game["n_player"] - 1:
        cur_fp = cur_fp - st.session_state.game["n_player"]
    st.session_state["1st_player"] = cur_fp

    print(
        ["catastrophe", "first_player"],
        plr["name"][st.session_state["1st_player"]],
        n_cat,
    )

    # update
    update.all()


# -----------------------------------------------------------------------------
def worlds_end_GO(played_catastrophes) -> None:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]
    worlds_end = st.session_state["worlds_end"]
    plr = st.session_state.plr

    # check if WE was played before, if so: remove effects from status_df
    if worlds_end["played"] != "none":
        # loop all traits in all trait piles
        for p in range(st.session_state.game["n_player"]):
            for trait_idx in plr["trait_pile"][p]:
                pre_WE_effects = status_df.loc[trait_idx].effects_WE

                for effect in pre_WE_effects.split():
                    match effect.lower():
                        case "face":
                            status_df.loc[trait_idx, "face"] = traits_df.loc[
                                trait_idx
                            ].face

                        case "inactive":
                            status_df.loc[trait_idx, "inactive"] = False

                status_df.loc[trait_idx, "effects_WE"] = "none"

        # log
        print(["worlds_end", "button_ready"], worlds_end["played"])

    # save played WE
    worlds_end["played"] = played_catastrophes[st.session_state["selected_worlds_end"]]

    # log
    print(["worlds_end", "play_WE"], worlds_end["played"])

    # update
    update.all()


# -----------------------------------------------------------------------------
def clear_trait_search():
    st.session_state.trait2play = None
