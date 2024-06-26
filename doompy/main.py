import os
import time
import bisect
import tkinter as tk
from tkinter import ttk
from math import floor
from functools import partial
import numpy as np
from PIL import ImageTk
from pygame import mixer

from log import write_log
import rules_attachment as rules_at
import rules_drop as rules_dr
import rules_play as rules_pl
import rules_remove as rules_re
import rules_traits as rules_tr
import rules_trait_pile as rules_tp
import rules_worlds_end as rules_we
import rules_MOL as rules_mol

from globals_ import logfile, dir_log
from globals_ import (
    cfg,
    sim_running,
    images_dict,
    sounds,
    music_onoff,
    icons_onoff,
    points_onoff,
)
from globals_ import traits_df, status_df, catastrophes_df, MOLs_df
from globals_ import (
    lbl_music_switch,
    lbl_icons_switch,
    lbl_points_switch,
    ent_trait_search,
    lbox_deck,
)
from globals_ import frame_player, frame_trait_pile, frame_MOL
from globals_ import game, plr, deck, deck_filtered_idx, catastrophe, worlds_end, MOLs
from globals_ import neoteny_checkbutton, sleepy_spinbox


# functions ##############################################################
def simulate() -> None:
    start_time = time.time()
    sim_running[0] = True

    loops = 1
    for loop in range(loops):
        start_game()
        pre_play_set = "random"

        if (
            pre_play_set == "action"
        ):  # -----------------------------------------------------
            pre_play = {
                0: [100, 107, 119, 133, 142, 149, 152, 157, 179],
                1: [184, 186, 206, 207, 217, 220, 222, 225, 229],
                2: [235, 236, 237, 238, 249, 270, 271, 272, 281],
                3: [325, 326, 327, 330, 334, 337, 339, 342, 346],
            }

            for p, tp in pre_play.items():
                for t in tp:
                    lbox_deck[0].selection_set(deck_filtered_idx.index(t))
                    btn_play_trait(p)

        if (
            pre_play_set == "effectless"
        ):  # -------------------------------------------------
            pre_play = {
                0: [0, 1, 9, 11, 18, 19, 21],
                1: [26, 28, 43, 51, 61, 67, 71, 76, 78],
                2: [80, 83, 102, 104, 105, 106, 113, 114, 116],
                3: [117, 120, 123, 130, 134, 135, 147, 172, 178, 180],
            }

            for p, tp in pre_play.items():
                for t in tp:
                    lbox_deck[0].selection_set(deck_filtered_idx.index(t))
                    btn_play_trait(p)

        if (
            pre_play_set == "attachments"
        ):  # ------------------------------------------------
            pre_play = {
                0: [0, 1, 9, 11, 19, 21, 26, 29, 69, 88, 176, 256, 300],
                1: [51, 61, 67, 71, 81, 83, 30, 68, 301, 340],
                2: [105, 107, 114, 113, 117, 177, 257, 341],
                3: [362, 356, 347, 336, 320, 291, 283, 127, 126, 182, 181, 199, 198],
            }

            for p, tp in pre_play.items():
                for trait_idx in tp:
                    lbox_deck[0].selection_set(deck_filtered_idx.index(trait_idx))
                    btn_play_trait(p)

                    # attach to host if necessary
                    if traits_df.loc[trait_idx].attachment == 1:
                        host_idx = rules_at.filter_attachables(trait_idx, p)[0]

                        write_log(
                            ["attach_to", "attached"],
                            plr["name"][p].get(),
                            traits_df.loc[trait_idx].trait,
                            trait_idx,
                            traits_df.loc[host_idx].trait,
                            host_idx,
                        )

                        # set new attachment to status_row of host & update
                        # effects of attachment on host
                        status_df.loc[trait_idx, "host"] = host_idx
                        status_df.loc[host_idx, "attachment"] = trait_idx

                        # update scoring
                        update_all()

        if (
            pre_play_set == "drops"
        ):  # ------------------------------------------------------
            pre_play = {
                0: [4, 16, 24, 25, 37, 40, 41, 63, 65, 66, 81, 86],
                1: [
                    94,
                    97,
                    121,
                    122,
                    126,
                    127,
                    131,
                    139,
                    146,
                    159,
                    160,
                    161,
                    162,
                    163,
                    164,
                    165,
                ],
                2: [166, 167, 168, 169, 170, 189, 202, 207, 214],
                3: [
                    227,
                    231,
                    247,
                    260,
                    274,
                    275,
                    277,
                    278,
                    287,
                    290,
                    296,
                    317,
                    318,
                    324,
                    333,
                    352,
                ],
            }

            for p, tp in pre_play.items():
                for t in tp:
                    trait_idx = deck_filtered_idx.index(t)
                    lbox_deck[0].selection_set(trait_idx)
                    btn_play_trait(p)

        if (
            pre_play_set == "test"
        ):  # -------------------------------------------------------
            pre_play = {
                0: [1, 9, 21, 26, 69, 104, 125, 183, 245],
                1: [44, 52, 62, 68, 177, 200, 340],
                2: [11, 18, 19, 29, 66, 275, 300],
                3: [103, 105, 118, 128, 256],
            }

            for p, tp in pre_play.items():
                for trait_idx in tp:
                    lbox_deck[0].selection_set(deck_filtered_idx.index(trait_idx))
                    btn_play_trait(p)

                    # attach to host if necessary
                    if traits_df.loc[trait_idx].attachment == 1:
                        host_idx = rules_at.filter_attachables(trait_idx, p)[0]

                        write_log(
                            ["attach_to", "attached"],
                            plr["name"][p].get(),
                            traits_df.loc[trait_idx].trait,
                            trait_idx,
                            traits_df.loc[host_idx].trait,
                            host_idx,
                        )

                        # set new attachment to status_row of host & update
                        # effects of attachment on host
                        status_df.loc[trait_idx, "host"] = host_idx
                        status_df.loc[host_idx, "attachment"] = trait_idx

                        # update scoring
                        update_all()

            # catastrophes for all test_cases
            catastrophe["cbox"][0].current(1)
            catastrophe["cbox"][0].event_generate("<<ComboboxSelected>>")
            catastrophe["cbox"][1].current(2)
            catastrophe["cbox"][1].event_generate("<<ComboboxSelected>>")
            catastrophe["cbox"][2].current(6)
            catastrophe["cbox"][2].event_generate("<<ComboboxSelected>>")
            catastrophe["cbox"][3].current(6)
            catastrophe["cbox"][3].event_generate("<<ComboboxSelected>>")

        if (
            pre_play_set == "random"
        ):  # -----------------------------------------------------
            rounds = 12
            cats = 4
            cats_at = [int(rounds / cats * (i + 1)) - 1 for i in range(cats)]
            colors = ["blue", "green", "purple", "red"]

            # play rounds
            for r in range(rounds):
                for p in range(game["n_player"]):
                    print(r, "_", p)

                    t = np.random.randint(low=0, high=len(deck) - 1)

                    if p == 0 and r == 0:
                        t = deck_filtered_idx.index(
                            traits_df.trait.to_list().index("Amatoxins")
                        )
                    if p == 0 and r == 1:
                        t = deck_filtered_idx.index(
                            traits_df.trait.to_list().index("Faith")
                        )

                    if p == 1 and r == 0:
                        t = deck_filtered_idx.index(
                            traits_df.trait.to_list().index("Lily Pad")
                        )
                    if p == 1 and r == 1:
                        t = deck_filtered_idx.index(
                            traits_df.trait.to_list().index("Opposable Thumbs")
                        )

                    if p == 2 and r == 0:
                        t = deck_filtered_idx.index(
                            traits_df.trait.to_list().index("Rainbow Horn (WE)")
                        )
                    if p == 2 and r == 1:
                        t = deck_filtered_idx.index(
                            traits_df.trait.to_list().index("Sentience")
                        )

                    if p == 3 and r == 0:
                        t = deck_filtered_idx.index(
                            traits_df.trait.to_list().index("Free Will")
                        )
                    if p == 3 and r == 1:
                        t = deck_filtered_idx.index(
                            traits_df.trait.to_list().index("Viral")
                        )

                    lbox_deck[0].selection_set(t)
                    trait_idx = deck_filtered_idx[lbox_deck[0].curselection()[0]]

                    # log
                    write_log(
                        ["select", "deck"],
                        traits_df.loc[
                            deck_filtered_idx[lbox_deck[0].curselection()[0]]
                        ].trait,
                        trait_idx,
                    )

                    # repeat until trait played
                    while btn_play_trait(p) == 0:
                        btn_clear_trait_search()

                        t = np.random.randint(low=0, high=len(deck) - 1)
                        lbox_deck[0].selection_set(t)
                        trait_idx = deck_filtered_idx[lbox_deck[0].curselection()[0]]

                        write_log(
                            ["select", "deck"],
                            traits_df.loc[
                                deck_filtered_idx[lbox_deck[0].curselection()[0]]
                            ].trait,
                            trait_idx,
                        )

                    # attach to host if necessary
                    if traits_df.loc[trait_idx].attachment == 1:
                        host_idx = rules_at.filter_attachables(trait_idx, p)[0]

                        write_log(
                            ["attach_to", "attached"],
                            plr["name"][p].get(),
                            traits_df.loc[trait_idx].trait,
                            trait_idx,
                            traits_df.loc[host_idx].trait,
                            host_idx,
                        )

                        # set new attachment to status_row of host & update
                        # effects of attachment on host
                        status_df.loc[trait_idx, "host"] = host_idx
                        status_df.loc[host_idx, "attachment"] = trait_idx

                        # update scoring
                        update_all()

                    # reset trait to play
                    btn_clear_trait_search()
                    trait_idx = None

                # play catastrophe ?!
                if r in cats_at:
                    n_cat = cats_at.index(r)
                    if n_cat < game["n_catastrophes"]:
                        c = np.random.randint(
                            low=1, high=len(catastrophe["possible"][n_cat])
                        )
                        catastrophe["cbox"][n_cat].current(c)
                        catastrophe["cbox"][n_cat].event_generate(
                            "<<ComboboxSelected>>"
                        )

            # select traits_WE_effects
            for p in range(game["n_player"]):
                tp = plr["trait_pile"][p]
                for t in tp:
                    match traits_df.trait.loc[t]:
                        case "Amatoxins":
                            rnd = np.random.randint(low=1, high=3)
                            btn_traits_world_end(p, t, str(rnd))

                        case "Faith":
                            rnd1 = np.random.randint(low=0, high=3)
                            rnd2 = np.random.randint(low=0, high=3)
                            while rnd1 == rnd2:
                                rnd2 = np.random.randint(low=0, high=3)
                            rnd3 = colors[rnd1] + " -> " + colors[rnd2]
                            btn_traits_world_end(p, t, rnd3)

                        case "Free Will":
                            rnd = np.random.randint(low=0, high=3)
                            btn_traits_world_end(p, t, colors[rnd])

                        case "Lily Pad":
                            rnd = np.random.randint(low=1, high=3)
                            btn_traits_world_end(p, t, str(rnd))

                        case "Opposable Thumbs":
                            match traits_df.loc[t].worlds_end_task:
                                case "choose_color":
                                    btn_traits_world_end(p, t, "blue")
                                case "is_color_of_choice":
                                    btn_traits_world_end(p, t, "blue")
                                case "may_change_color":
                                    btn_traits_world_end(p, t, "green -> blue")
                                case "return_upto_3_traits_to_hand":
                                    btn_traits_world_end(p, t, "3")
                                case "discard_upto_3_traits":
                                    btn_traits_world_end(p, t, "3")
                                case "is_color_of_most_colors":
                                    btn_traits_world_end(p, t, "count them!")

                        case "Rainbow Horn (WE)":
                            btn_traits_world_end(p, t, "count them!")

                        case "Sentience":
                            rnd = np.random.randint(low=0, high=3)
                            btn_traits_world_end(p, t, colors[rnd])

                        case "Viral":
                            rnd = np.random.randint(low=0, high=3)
                            btn_traits_world_end(p, t, colors[rnd])

            # btn_WE_GO
            check_WE_status("check_button")
            btn_worlds_end_GO()

            # manual drops
            for p in range(game["n_player"]):
                tp = plr["trait_pile"][p]
                for t in tp:
                    cur_drop_eff = traits_df.loc[t].drop_effect
                    if (
                        isinstance(cur_drop_eff, str)
                        and not isinstance(traits_df.loc[t].worlds_end_task, str)
                        and (
                            "own_hand" in traits_df.loc[t].drop_effect
                            or "discarded" in traits_df.loc[t].drop_effect
                        )
                    ):
                        rnd = np.random.randint(low=1, high=10)
                        update_manual_drops(rnd, t, "+")

            # neoteny ?
            nt = np.random.randint(low=0, high=9)
            if nt in range(4):
                update_traits_current_status("neoteny", nt)

            # select MOLs
            for p in range(game["n_player"]):
                for m in range(MOLs["n"][p]):
                    im = np.random.randint(low=1, high=len(MOLs_df))
                    if MOLs_df.loc[im].MOL == "The Blind Dragon":
                        print("_")
                        im += 1
                    btn_select_MOLS(im, p, m)
                    # if blind dragon
                    if MOLs_df.loc[im].MOL == "The Blind Dragon":
                        for mm in [2, 3]:
                            im = np.random.randint(low=1, high=len(MOLs_df) - 1)
                            btn_select_MOLS(im, p, mm)
                # if manual MOL points
                for m in range(MOLs["n"][p]):
                    m_idx = MOLs["played"][p][m]
                    if MOLs["played"][p][m] is not None and (
                        "hand" in MOLs_df.loc[m_idx].MOL_type.lower()
                        or "draw" in MOLs_df.loc[m_idx].MOL_type.lower()
                    ):
                        rnd = np.random.randint(low=1, high=10)
                        update_manual_MOL(rnd, p, m, "+")
            #             create_MOL_frame(p)

        print("___done simulating___")
        print("--- %s seconds ---" % (time.time() - start_time))


def btn_quit() -> None:
    write_log("*", "bye")
    root.quit()


def switch(inp: str) -> None:
    global icons_onoff, music_onoff, points_onoff

    match inp:
        case "icons":
            if icons_onoff == "off":
                icons_onoff = "on"
                lbl_icons_switch[0].configure(image=images["icons_on"])
                write_log(["icons", "on"])

            elif icons_onoff == "on":
                icons_onoff = "full"
                lbl_icons_switch[0].configure(image=images["icons_full"])
                write_log(["icons", "full"])

            elif icons_onoff == "full":
                icons_onoff = "off"
                lbl_icons_switch[0].configure(image=images["icons_off"])
                write_log(["icons", "off"])

            switch("show_icons")
            # update all trait piles
            for p in range(game["n_player"]):
                if frame_trait_pile[p] is not None:
                    create_trait_pile(frame_trait_pile[p], p)

        case "show_icons":
            if icons_onoff == "on":
                show_icons["color"] = True  # default: True
                show_icons["face"] = True  # default: True
                show_icons["collection"] = False  # default: False
                show_icons["dominant"] = False  # default: False
                show_icons["action"] = False  # default: False
                show_icons["drops"] = False  # default: False
                show_icons["gene_pool"] = False  # default: False
                show_icons["worlds_end"] = False  # default: False
                show_icons["effectless"] = False  # default: False
                show_icons["persistent"] = False  # default: False
                show_icons["attachment"] = False  # default: False

            elif icons_onoff == "full":
                show_icons["color"] = True  # default: True
                show_icons["face"] = True  # default: True
                show_icons["collection"] = True  # default: False
                show_icons["dominant"] = True  # default: False
                show_icons["action"] = True  # default: False
                show_icons["drops"] = True  # default: False
                show_icons["gene_pool"] = True  # default: False
                show_icons["worlds_end"] = True  # default: False
                show_icons["effectless"] = True  # default: False
                show_icons["persistent"] = True  # default: False
                show_icons["attachment"] = True  # default: False

            elif icons_onoff == "off":
                show_icons["color"] = False  # default: True
                show_icons["face"] = False  # default: True
                show_icons["collection"] = False  # default: False
                show_icons["dominant"] = False  # default: False
                show_icons["action"] = False  # default: False
                show_icons["drops"] = False  # default: False
                show_icons["gene_pool"] = False  # default: False
                show_icons["worlds_end"] = False  # default: False
                show_icons["effectless"] = False  # default: False
                show_icons["persistent"] = False  # default: False
                show_icons["attachment"] = False  # default: False

        case "music":
            if music_onoff == "off":
                music_onoff = "on"
                lbl_music_switch[0].configure(image=images["note_on"])
                write_log(["music", "on"])

            else:
                music_onoff = "off"
                lbl_music_switch[0].configure(image=images["note_off"])
                write_log(["music", "off"])

        case "points":
            if points_onoff == "off":
                # show actual points
                points_onoff = "on"
                lbl_points_switch[0].configure(image=images["points_123"])

                gui_style.configure(
                    "total.TLabel",
                    font=("", 50, "bold"),
                    foreground=cfg["font_color_total_score"],
                )
                gui_style.configure("points.TLabel", font=("", 14))

                write_log(["points", "on"])
                update_scoring()

            elif points_onoff == "on":
                # show rank
                points_onoff = "rank"
                lbl_points_switch[0].configure(image=images["rank"])

                gui_style.configure("total.TLabel", font=("Arial", 40, "bold"))
                gui_style.configure("points.TLabel", font=("Arial", 14))

                write_log(["points", "rank"])
                update_scoring()

            else:
                # show ***
                points_onoff = "off"
                lbl_points_switch[0].configure(image=images["question_mark"])

                gui_style.configure(
                    "total.TLabel",
                    font=("", 50, "bold"),
                    foreground=cfg["font_color_total_score"],
                )
                gui_style.configure("points.TLabel", font=("", 18))

                write_log(["points", "off"])
                update_scoring()


def play_sound(trait: str) -> None:
    if music_onoff == "on":
        if trait.replace(" ", "_").lower() in sounds:
            sounds[trait.replace(" ", "_").lower()].play()
            write_log(["music", "play"], trait)


def calc_MOLs(p: int) -> None:
    p_MOL = 0
    for m in range(MOLs["n"][p]):
        # calculate, if MOL is selected
        if MOLs["played"][p][m] is not None:
            # calculate points
            p_MOL_m = rules_mol.calc_MOL_points(p, m)

            # update sum of MOL points
            p_MOL += p_MOL_m

            # log
            write_log(
                ["MOLs", "MOL_points"],
                plr["name"][p].get(),
                MOLs_df.loc[MOLs["played"][p][m]].MOL,
                MOLs["played"][p][m],
                p_MOL_m,
            )

        # update points_icon of MOL
        if MOLs["played"][p][m] is not None and points_onoff == "on":
            MOLs["icon"][p][m].configure(image=images[str(p_MOL_m)])
        else:
            MOLs["icon"][p][m].configure(image=images["question_mark"])

    return p_MOL


def btn_select_MOLS(cbox_idx: int, p: int, m: int) -> None:
    # get infos of played/selected MOLs
    played_idx = None
    played_previously = MOLs["played"][p][m]
    if cbox_idx > 0:
        played_idx = cbox_idx - 1
        played_str = MOLs_df.loc[played_idx].MOL

    # return, if no MOL selected now and previously
    if cbox_idx == 0 and played_previously is None:
        # log
        write_log(["MOLs", "error_no_MOL"], m + 1, plr["name"][p].get())
        return

    # return, if same MOL selected
    if cbox_idx != 0 and (played_idx == played_previously):
        # log
        write_log(["MOLs", "error_keep_MOL"], m + 1, plr["name"][p].get(), played_str)
        return

    # if MOL is de-selected
    if cbox_idx == 0:
        # log
        write_log(
            ["MOLs", "deselected_MOL"],
            plr["name"][p].get(),
            m + 1,
            MOLs_df.loc[played_previously].MOL,
        )
    else:
        # log
        write_log(["MOLs", "MOL"], m + 1, plr["name"][p].get(), played_str, played_idx)

    # set played MOL
    MOLs["played"][p][m] = played_idx

    # check for MOL_specific select_effects
    rules_mol.select_MOL(p, played_idx, played_previously)
    create_MOL_frame(p)

    # update
    update_all()


def btn_clear_trait_search() -> None:
    str_trait_search.set("")
    deck_filtered_idx.clear()
    deck_filtered_idx.extend(deck)
    deck_filtered_str.set(traits_df.loc[deck_filtered_idx].trait.values.tolist())
    ent_trait_search[0].focus_set()
    lbox_deck[0].selection_clear(0, tk.END)
    lbox_deck[0].see(0)


def btn_worlds_end_GO() -> None:
    # check if WE was played before, if so: remove effects from status_df
    if worlds_end["played"] != "none":
        # loop all traits in all trait piles
        for p in range(game["n_player"]):
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
        write_log(["worlds_end", "button_ready"], worlds_end["played"])

    # save played WE
    worlds_end["played"] = worlds_end["selected"].get()

    # log
    write_log(["worlds_end", "play_WE"], worlds_end["played"])

    # update
    update_all()


def check_WE_status(todo: str) -> None:
    match todo:
        case "select_WE":
            # log
            write_log(["worlds_end", "select"], worlds_end["selected"].get())

            # and check button
            check_WE_status("check_button")

        case "check_button":
            if any(
                [
                    status_df.loc[trait_idx].traits_WE == "none"
                    for tp in plr["trait_pile"]
                    for trait_idx in tp
                    if isinstance(traits_df.loc[trait_idx].worlds_end_task, str)
                ]
            ):

                # disable WE_button
                worlds_end["btn"].configure(state="disabled", style="disabled.TButton")

                # log
                write_log(["worlds_end", "button_not_ready"])

            else:
                # enable WE_button
                worlds_end["btn"].configure(state="normal", style="TButton")

                # log
                write_log(["worlds_end", "button_ready"])


def btn_play_catastrophe(event: tk.Event, c: int) -> None:
    # get played catastrophe
    cbox_idx = event.widget.current()  # selected item_idx in combobox
    played_str = event.widget.get()
    played_previously = catastrophe["played"][c]
    if cbox_idx > 0:
        played_idx = catastrophe["possible"][c][cbox_idx - 1]

    # return, if no catastrophe was selected
    if cbox_idx == 0:
        # if no catastrophe was selected before
        if played_previously is None:
            write_log(["catastrophe", "error_no_catastrophe"], c + 1)
        # else -> forced to keep previous selection
        else:
            old_cbox_idx = catastrophe["possible"][c].index(played_previously) + 1
            catastrophe["cbox"][c].current(old_cbox_idx)
            write_log(["catastrophe", "error_keep_catastrophe"], c + 1)
        return

    # return, if same catastrophe selected
    if played_previously == played_idx:
        write_log(["catastrophe", "error_same_catastrophe"], c + 1, played_str)
        return

    # log
    write_log(["catastrophe", "catastrophe"], c + 1, played_str, played_idx)

    # set played catastrophe
    catastrophe["played"][c] = played_idx

    # update possible catastrophes for other catastrophes
    for i in [i for i in range(game["n_catastrophes"]) if i != c]:
        # begin with ALL possible catastrophes - necessary bc this catastrophe may have changed
        catastrophe["possible"][i] = catastrophes_df.index.tolist()

        # remove other catastrophes from possible ones
        for j in [j for j in range(game["n_catastrophes"]) if j != i]:
            # only, if j'th catastrophe was played already
            if catastrophe["played"][j] is not None:
                # remove from list of possibles
                catastrophe["possible"][i].remove(catastrophe["played"][j])

        # create list of catastrophe names & update combobox
        pos_cat_values = [" catastrophe {}...".format(i + 1)] + catastrophes_df.loc[
            catastrophe["possible"][i]
        ].name.values.tolist()
        catastrophe["cbox"][i].configure(values=pos_cat_values)

    # enable next catastrophe
    if c < game["n_catastrophes"] - 1:
        catastrophe["cbox"][c + 1].configure(state="readonly")

    # update worlds_end-combobox
    played_catastrophes = [
        catastrophes_df.loc[catastrophe["played"][i], "name"]
        for i in range(game["n_catastrophes"])
        if catastrophe["played"][i] is not None
    ]
    # worlds_end['cbox']['values'] = [" select world's end ..."] + played_catastrophes
    worlds_end["cbox"]["values"] = played_catastrophes

    # enable worlds_end-combobox and select last entry
    if c == game["n_catastrophes"] - 1:
        worlds_end["cbox"].configure(state="readonly")
        worlds_end["cbox"].current(game["n_catastrophes"] - 1)
        check_WE_status("select_WE")

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
    options["first_player"].set(options["first_player"].get() + 1)
    if options["first_player"].get() > game["n_player"] - 1:
        options["first_player"].set(options["first_player"].get() - game["n_player"])
    write_log(
        ["catastrophe", "first_player"],
        plr["name"][options["first_player"].get()].get(),
        n_cat,
    )

    # update all player's label_style
    update_first_player()

    # update
    update_all()


def btn_traits_world_end(from_: int, trait_idx: int, effect: str) -> None:
    # get index of WE_effect
    effect_idx = rules_tr.traits_WE_tasks(trait_idx).index(effect)

    # log
    if effect_idx == 0:
        write_log(["traits_WE", "reset"], traits_df.loc[trait_idx].trait, trait_idx)
    else:
        write_log(
            ["traits_WE", "set"], traits_df.loc[trait_idx].trait, trait_idx, effect
        )

    # set traits_WE-effect to status_df of trait
    if effect_idx == 0:
        status_df.loc[trait_idx, "traits_WE"] = "none"
    else:
        status_df.loc[trait_idx, "traits_WE"] = effect

    # apply traits_WE-effects and update status of traits in this trait pile
    rules_tr.assign_traits_WE_effects(trait_idx, plr["trait_pile"][from_])

    # update
    update_all()

    # check if WE_button should be enabled
    check_WE_status("check_button")


def btn_remove_trait(from_: int, where_to: str, *args) -> None:
    # get card & its attachment
    trait_idx = plr["trait_selected"][from_].get()
    if not np.isnan(trait_idx):
        attachment = status_df.loc[trait_idx].attachment

    # check if "emergency-removal" of attachment/dominant is triggered
    if args != ():
        trait_idx = args[0]
        attachment = "none"

        # reset possible host
        host = [
            i
            for i, v in enumerate(status_df.attachment.values.tolist())
            if trait_idx == v
        ]
        if host != []:
            status_df.loc[host[0], "attachment"] = "none"

    # return, if no trait selected
    if np.isnan(trait_idx):
        write_log(["remove", "error_no_trait"])
        return

    # log
    if where_to == "hand":
        write_log(
            ["remove", "hand"],
            plr["name"][from_].get(),
            traits_df.loc[trait_idx].trait,
            trait_idx,
        )
    else:
        write_log(
            ["remove", "discard"],
            plr["name"][from_].get(),
            traits_df.loc[trait_idx].trait,
            trait_idx,
        )
    if attachment != "none":
        write_log(
            ["remove", "discard_attachment"],
            traits_df.loc[attachment].trait,
            attachment,
        )

    # remove card(s) from player & clear player trait selection
    plr["trait_pile"][from_].remove(trait_idx)
    if attachment != "none":
        plr["trait_pile"][from_].remove(attachment)
    plr["trait_selected"][from_].set(np.nan)

    # add to deck traits & update deck_listbox
    bisect.insort_left(deck, trait_idx)
    if attachment != "none":
        bisect.insort_left(deck, attachment)
    search_trait_in_list(str_trait_search)  # keep current str in search_entry

    # check, if this trait has a special "remove-rule",
    # which may be needed for "status_updating"
    remove_rule = rules_re.check_trait(trait_idx, from_, where_to)

    # reset current status of card(s)
    update_traits_current_status("reset", trait_idx, remove_rule)
    if attachment != "none":
        update_traits_current_status("reset", attachment, [])

    # update
    update_all()


def btn_move_trait(from_: int, cbox_move_to: ttk.Combobox) -> None:
    # get card, its attachment & target
    trait_idx = plr["trait_selected"][from_].get()
    if not np.isnan(trait_idx):
        attachment = status_df.loc[trait_idx].attachment
    cbox_str = cbox_move_to.get().split()
    if cbox_str[0] != "move":
        to = [i.get() for i in plr["name"]].index(cbox_str[-1])

    # return, if no target selected
    if cbox_move_to.current() == 0:
        cbox_move_to.current(0)
        write_log(["move", "error_move_to"])
        return

    # return, if no trait selected
    if np.isnan(trait_idx):
        cbox_move_to.current(0)
        write_log(["move", "error_no_trait"])
        return

    # log
    add_txt = (
        "(and its attachment '{}' (id:{}))".format(
            traits_df.loc[attachment].trait, attachment
        )
        if attachment != "none"
        else ""
    )
    write_log(
        ["move", "move_to"],
        traits_df.loc[trait_idx].trait,
        trait_idx,
        add_txt,
        plr["name"][from_].get(),
        plr["name"][to].get(),
    )

    # remove traits(s) from 'giving' player - update trait_pile - check
    # remove_rules - clear trait selection
    plr["trait_pile"][from_].remove(trait_idx)
    if attachment != "none":
        plr["trait_pile"][from_].remove(attachment)
    create_trait_pile(frame_trait_pile[from_], from_)
    rules_re.check_trait(trait_idx, from_, "different_trait_pile")
    plr["trait_selected"][from_].set(np.nan)

    # add to 'receiving' players traits
    bisect.insort_left(plr["trait_pile"][to], trait_idx)
    if attachment != "none":
        bisect.insort_left(plr["trait_pile"][to], attachment)

    # clear combobox
    cbox_move_to.current(0)

    # update
    update_all()


def btn_attach_to(
    from_: int, attachment_idx: int, event: tk.Event, possible_hosts: list
) -> None:
    # get host_data from event_data
    host = event.widget.get()
    host_idx = possible_hosts[event.widget.current()]
    attachment = traits_df.loc[attachment_idx].trait

    # return, if clicked on current host
    old_host_idx = status_df[
        status_df["attachment"] == attachment_idx
    ].index.values.tolist()
    if host_idx in old_host_idx:
        write_log(["attach_to", "error_current_host"])
        return

    # log
    if host == " ... ":
        if len(old_host_idx) == 0:
            write_log(["attach_to", "still_detached"], attachment, attachment_idx)
        else:
            write_log(["attach_to", "detached"], attachment, attachment_idx)
    else:
        write_log(
            ["attach_to", "attached"],
            plr["name"][from_].get(),
            attachment,
            attachment_idx,
            host,
            host_idx,
        )

    # update old_host, where attachment was removed from
    if old_host_idx:
        write_log(
            ["attach_to", "change_host"],
            traits_df.loc[old_host_idx[0]].trait,
            old_host_idx[0],
        )
        update_traits_current_status("reset", old_host_idx[0], [])

    # check if attachment is set back to "..." (idx=0)
    if event.widget.current() == 0:
        # reset host='none' to status_row of attachment
        status_df.loc[attachment_idx, "host"] = "none"
    else:
        # update status of attachment/host - saving idx's of each other
        status_df.loc[attachment_idx, "host"] = host_idx
        status_df.loc[host_idx, "attachment"] = attachment_idx

    # update
    update_all()


def btn_play_trait(to: int) -> int:
    # return, if no trait selected
    if not lbox_deck[0].curselection():
        write_log(["play", "error_no_trait"])
        return 0

    # get card
    trait_idx = deck_filtered_idx[lbox_deck[0].curselection()[0]]
    trait = traits_df.loc[trait_idx].trait

    # return, if any trait specific requirements are not met
    if rules_pl.check_requirement(trait_idx, to):
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
                is_born = status_df.loc[heroic_idx[0], "effects"]
            else:
                is_born = False

            # no hero, then return
            if is_born and trait_idx == heroic_idx[0]:
                write_log(["play", "heroic"])
            else:
                write_log(["play", "error_2dominants"], plr["name"][to].get())
                return 0

    # return, if attachment does not have any trait to attach to
    if traits_df.loc[trait_idx].attachment == 1:
        attachables = rules_at.filter_attachables(trait_idx, to)
        if len(attachables) == 0:
            write_log(["play", "error_no_attachables"], plr["name"][to].get())
            return 0

    # log
    write_log(["play", "play"], plr["name"][to].get(), trait, trait_idx)

    # check for rules/effects to apply when playing this trait
    rules_pl.play_effect(trait_idx, to)

    # add to players traits & update trait_pile
    bisect.insort_left(plr["trait_pile"][to], trait_idx)

    # remove from deck & update deck_listbox
    deck.remove(trait_idx)
    btn_clear_trait_search()

    # play sound bites
    play_sound(trait)

    # update
    update_all()

    return 1


def update_manual_MOL(cur_value: int, p: int, m: int, change: str) -> None:
    # change value according to button
    if change == "+":
        value = cur_value + 1
    else:
        value = cur_value - 1

    # save current value
    plr["points_MOL"][p][m].set(value)

    # update all
    update_all()


def update_manual_we(cur_value: int, p: int, change: str) -> None:
    # change value according to button
    if change == "+":
        value = cur_value + 1
    else:
        value = cur_value - 1

    plr["points_WE_effect"][p].set(value)

    # update scoring
    update_scoring()

    # update this players trait pile
    create_trait_pile(frame_trait_pile[p], p)


def update_manual_drops(cur_value: int, trait: int, change: str) -> None:
    # change value according to button
    if change == "+":
        value = cur_value + 1
    else:
        value = cur_value - 1

    # save value in status_df
    status_df.loc[trait, "drops"] = value

    # log
    write_log(["scoring", "manual_drops"], traits_df.iloc[trait].trait, trait, value)

    # update all
    update_all()


def update_traits_current_status(todo: str, *args) -> None:
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
            write_log(
                ["update_trait_status", "reset"], traits_df.loc[trait].trait, trait
            )

        # Neoteny-Checkbox is clicked somewhere
        case "neoteny":
            neoteny_idx = traits_df.index[traits_df.trait == "Neoteny"].tolist()[0]
            p = args[0]

            # set other player to 0
            for i in range(game["n_player"]):
                if i != p:
                    neoteny_checkbutton[i].set(0)

            # update 'cur_effect'
            if not any([i.get() for i in neoteny_checkbutton]):
                status_df.loc[neoteny_idx, "effects"] = "none"
                write_log(["update_trait_status", "neoteny_no_one"])
            else:
                status_df.loc[neoteny_idx, "effects"] = str(p)
                write_log(
                    ["update_trait_status", "neoteny_that_one"], plr["name"][p].get()
                )

            # update
            update_all()


def update_first_player() -> None:
    # update all player frames
    for p in range(game["n_player"]):
        lbl = root.nametowidget(".content.playground.p{}.scoreboard.up.name".format(p))
        lbl.configure(
            style=(
                "nameFP.TLabel" if options["first_player"].get() == p else "name.TLabel"
            )
        )


def update_scoring() -> None:
    # first, calculate all scores
    p_worlds_end = []
    p_face = []
    p_drop = []
    p_MOL = []
    total = []
    for p in range(game["n_player"]):
        # get cards
        trait_pile = plr["trait_pile"][p]

        # calculate world's end points
        p_worlds_end.append(
            rules_we.calc_WE_points(p) if worlds_end["played"] != "none" else 0
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
    for p in range(game["n_player"]):
        # update points
        if points_onoff == "on":
            plr["points"][p]["face"].set(p_face[p])
            plr["points"][p]["drops"].set(p_drop[p])
            plr["points"][p]["worlds_end"].set(p_worlds_end[p])
            plr["points"][p]["MOL"].set(p_MOL[p])
            plr["points"][p]["total"].set(total[p])
        elif points_onoff == "rank":
            plr["points"][p]["face"].set(str(r_face[p]) + add[r_face[p]])
            plr["points"][p]["drops"].set(str(r_drop[p]) + add[r_drop[p]])
            plr["points"][p]["worlds_end"].set(str(r_WE[p]) + add[r_WE[p]])
            plr["points"][p]["MOL"].set(str(r_MOL[p]) + add[r_MOL[p]])
            plr["points"][p]["total"].set(str(r_total[p]) + add[r_total[p]])
        else:
            plr["points"][p]["face"].set("\u2736")
            plr["points"][p]["drops"].set("\u2736")
            plr["points"][p]["worlds_end"].set("\u2736")
            plr["points"][p]["MOL"].set("\u2736")
            plr["points"][p]["total"].set("\u2736")

        # log
        write_log(
            ["scoring", "update"],
            plr["name"][p].get(),
            p_face[p],
            p_drop[p],
            p_worlds_end[p],
            p_MOL[p],
            total[p],
        )


def update_genes() -> None:
    # init vars
    diff_genes = [0] * game["n_player"]

    # loop players and calculate +- genes of all played traits ----------------
    for p in range(game["n_player"]):
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
                write_log(
                    ["genes", "trait"],
                    plr["name"][p].get(),
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
                write_log(
                    ["genes", "denial_t4h"],
                    dnl_idx[0],
                    plr["name"][dnl_p].get(),
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
                write_log(
                    ["genes", "denial"],
                    dnl_idx[0],
                    plr["name"][dnl_p].get(),
                    dnl_effect,
                    diff_genes,
                )

    # ----- Sleepy --------------
    slp_idx = traits_df.index[traits_df.trait == "Sleepy"].tolist()
    if slp_idx != []:
        slp_eff = [i.get() for i in sleepy_spinbox]
        diff_genes = [diff_genes[x] + slp_eff[x] for x in range(len(diff_genes))]
        if any(slp_eff):
            p = [i for i, e in enumerate(slp_eff) if e != 0]
            write_log(
                ["genes", "sleepy"], plr["name"][p[0]].get(), slp_eff[p[0]], diff_genes
            )

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
                write_log(
                    ["genes", "spores"], sprs_idx[0], plr["name"][p].get(), diff_genes
                )

    # check what catastrophes were played already -----------------------------
    for c in range(game["n_catastrophes"]):
        # get card & effect
        c_idx = catastrophe["played"][c]

        # check if catastrophe was played
        if c_idx is not None:
            c_str = catastrophes_df.loc[c_idx, "name"]
            # get effect and apply it
            effect = int(catastrophes_df.loc[c_idx].gene_pool)
            diff_genes = [i + effect for i in diff_genes]

            # log
            write_log(["genes", "catastrophe"], c_str, effect, diff_genes)

    # update gene values ------------------------------------------------------
    for p in range(game["n_player"]):
        new_gp = game["n_genes"] + diff_genes[p]
        if new_gp > 8:
            plr["genes"][p].set(8)
        elif new_gp < 1:
            plr["genes"][p].set(1)
        else:
            plr["genes"][p].set(new_gp)

    # log - if genes are effected
    if any(i > 0 for i in diff_genes):
        write_log(
            ["genes", "total_effect"],
            diff_genes,
            [plr["genes"][i].get() for i in range(game["n_player"])],
        )


def update_stars() -> None:
    # loop players
    nd_dict = {}
    for p in range(game["n_player"]):
        # number of dominant traits
        n_dominant = np.nansum(
            [traits_df.loc[trait_idx].dominant for trait_idx in plr["trait_pile"][p]]
        )
        nd_dict[plr["name"][p].get()] = int(n_dominant)

        # check special cases
        Epic_idx = traits_df.index[traits_df.trait == "Epic"].tolist()
        if Epic_idx != [] and Epic_idx[0] in plr["trait_pile"][p]:
            n_dominant = 2
            write_log(["stars", "epic"], plr["name"][p].get())

        # find label widgets
        tmp_frame = frame_player[p].winfo_children()
        lbl1 = frame_player[p].nametowidget(str(tmp_frame[0]) + ".up.star1")
        lbl2 = frame_player[p].nametowidget(str(tmp_frame[0]) + ".up.star2")

        # edit images
        lbl1.configure(image=images["no_star"])
        lbl2.configure(image=images["no_star"])
        if n_dominant > 0:
            lbl1.configure(image=images["star"])
            if n_dominant == 2:
                lbl2.configure(image=images["star"])
            elif n_dominant == 3:
                lbl2.configure(image=images["heroic_star"])

    # log
    write_log(["stars", "n_dom"], nd_dict)


def update_all() -> None:
    # first, update n_TP (count) & resolve all effects on traits
    for p in range(game["n_player"]):
        # get player's trait pile
        tp = plr["trait_pile"][p]

        # resolve all effects on traits ---------------------------------------
        for trait_idx in tp:
            # 1: attachment effect
            rules_at.apply_effects(trait_idx)

            # 2: traits WE effect(s)
            rules_tr.apply_traits_WE_effects(trait_idx)

            # 3: worlds end effect
            rules_we.apply_WE_effects(trait_idx)

        # update n_tp ---------------------------------------------------------
        # colors ------------------------
        for col in ["blue", "green", "purple", "red", "colorless"]:
            plr["n_tp"][p][col[0]].set(
                sum(col in color.lower() for color in status_df.iloc[tp].color.tolist())
            )

        # total -------------------------
        plr["n_tp"][p]["t"].set(len(tp) + plr["n_tp"][p]["xtra"])

        # scoreboard --------------------
        if plr["n_tp"][p]["xtra"] == 0:
            txt = "\u2211" + str(len(tp))
        else:
            txt = str(len(tp)) + "+" + str(plr["n_tp"][p]["xtra"])
        plr["n_tp"][p]["sb"].set(txt)

    # update stuff ------------------------------------------------------------
    update_stars()
    update_genes()
    update_scoring()

    # update all trait piles --------------------------------------------------
    for p in range(game["n_player"]):
        create_trait_pile(frame_trait_pile[p], p)

    # focus back to search field ----------------------------------------------
    ent_trait_search[0].focus_set()


def search_trait_in_list(inp: tk.StringVar) -> None:
    value = inp.get()
    lbox_deck[0].selection_clear(0, tk.END)

    if value == "":
        deck_filtered_idx.clear()
        deck_filtered_idx.extend(deck)
        deck_filtered_str.set(traits_df.loc[deck].trait.values.tolist())
    else:
        filtered_trait_str = []
        filtered_trait_idx = []
        for idx in deck:
            if value.lower() in traits_df.loc[idx].trait.lower():
                filtered_trait_idx.append(idx)
                filtered_trait_str.append(traits_df.loc[idx].trait)

        deck_filtered_idx.clear()
        deck_filtered_idx.extend(filtered_trait_idx)
        deck_filtered_str.set(filtered_trait_str)

        # if only 1 possibility left, select it automatically
        if len(filtered_trait_idx) == 1 or (
            len(filtered_trait_idx) == 2
            and filtered_trait_str[0] == filtered_trait_str[1]
        ):
            lbox_deck[0].selection_clear(0, tk.END)
            lbox_deck[0].selection_set(0)
            lbox_deck[0].focus()
            lbox_deck[0].see(0)
            write_log(
                ["select", "deck"],
                traits_df.loc[deck_filtered_idx[0]].trait,
                deck_filtered_idx[0],
            )


def create_MOL_frame(p: int) -> None:
    # forget all previous widgets
    for w in frame_MOL[p].grid_slaves():
        w.grid_forget()

    # --- title ---------------------------------------------------------------
    ttk.Label(frame_MOL[p], text="Meaning(s) of Life", style="menu_h1.TLabel").grid(
        row=0, column=0, pady=(3, 0), columnspan=2 * MOLs["n"][p], sticky="ns"
    )

    # --- MOLS - 2 per row ----------------------------------------------------
    cur_row = 0
    for m in range(MOLs["n"][p]):
        frame_MOL[p].columnconfigure(m, weight=1)
        frame_MOL[p].columnconfigure(m + 1, weight=2)

        cur_row = cur_row + 1 if (m % 2 == 0) else cur_row
        cur_col = 2 if m % 2 == 1 else 0
        xpad_L = 0 if m % 2 == 1 else 4
        xpad_R = 4 if m % 2 == 1 else 0

        pos_MOLs = ["select MOL #{}".format(m + 1)] + MOLs_df.MOL.values.tolist()
        MOLs["cbox"][p][m] = ttk.Combobox(
            frame_MOL[p], values=pos_MOLs, exportselection=0, state="enabled", width=10
        )
        MOLs["cbox"][p][m].current(0)
        MOLs["cbox"][p][m].grid(
            row=cur_row, column=cur_col, padx=(xpad_L, 0), pady=(0, 5), stick="nesw"
        )
        MOLs["cbox"][p][m].bind(
            "<<ComboboxSelected>>",
            lambda e, m=m: btn_select_MOLS(e.widget.current(), p, m),
        )

        MOLs["icon"][p][m] = ttk.Label(frame_MOL[p], image=images["question_mark"])
        MOLs["icon"][p][m].grid(
            row=cur_row, column=cur_col + 1, padx=(0, xpad_R), pady=(0, 5), sticky="nsw"
        )

        # set current selection if played
        if MOLs["played"][p][m] is not None:
            MOLs["cbox"][p][m].current(MOLs["played"][p][m] + 1)

    # --- spinboxes for manual entry ------------------------------------------
    for m in range(MOLs["n"][p]):
        m_idx = MOLs["played"][p][m]
        if MOLs["played"][p][m] is not None and (
            "hand" in MOLs_df.loc[m_idx].MOL_type.lower()
            or "draw" in MOLs_df.loc[m_idx].MOL_type.lower()
        ):
            # new frame
            cur_row += 1
            sbox_frame = tk.Frame(frame_MOL[p])
            sbox_frame.grid(row=cur_row, column=0, columnspan=3, sticky="nesw")

            # label
            tk.Label(sbox_frame, text=MOLs_df.loc[m_idx].MOL + ":").grid(
                row=cur_row, column=0, padx=(5, 0), sticky="e"
            )

            # create spinbox
            MOL_sbox = ttk.Spinbox(
                sbox_frame, state="readonly", from_=-50, to=500, width=2, wrap=False
            )
            MOL_sbox.grid(row=cur_row, column=1, sticky="w")
            MOL_sbox.bind(
                "<<Increment>>",
                lambda e, m=m: update_manual_MOL(int(e.widget.get()), p, m, "+"),
            )
            MOL_sbox.bind(
                "<<Decrement>>",
                lambda e, m=m: update_manual_MOL(int(e.widget.get()), p, m, "-"),
            )

            # fill spinbox, depending on drops_status
            MOL_sbox.set(plr["points_MOL"][p][m].get())


def create_trait_pile(frame_trait_overview: tk.Frame, p: int) -> None:
    # first, clean up frame
    for w in frame_trait_overview.grid_slaves():
        w.grid_forget()

    # then, scan trait pile for any effects by any traits, like protecting
    # other traits...
    rules_tr.permanent_effects(plr["trait_pile"][p])

    # --- loop traits in trait pile -------------------------------------------
    irow = -1
    for trait_idx in plr["trait_pile"][p]:
        # get trait name
        trait = traits_df.loc[trait_idx].trait

        # init some vars
        irow += 1
        ypad = (3, 0) if irow == 0 else 0

        # ----- radiobutton / label if attachment or dominant -----------------
        if traits_df.loc[trait_idx].attachment == 1:
            lbl = tk.Label(
                frame_trait_overview,
                text=" " + trait,
                image=images["attachment"],
                compound=tk.LEFT,
            )
            lbl.grid(row=irow, column=0, padx=2, pady=ypad, sticky="nsw")

            # it attachment is also could be a DOMINANT
            if traits_df.loc[trait_idx].dominant == 1:
                lbl.config(fg=cfg["font_color_dominant"], font="'' 14 bold")
        elif traits_df.loc[trait_idx].dominant == 1:
            tk.Label(
                frame_trait_overview,
                text=" " + trait,
                image=images["dominant"],
                compound=tk.LEFT,
                fg=cfg["font_color_dominant"],
                font="'' 14 bold",
            ).grid(row=irow, column=0, padx=2, pady=ypad, sticky="nsw")
        else:
            # check if trait has 'noRemove' status
            rb_state = "disabled" if status_df.loc[trait_idx].no_remove else "normal"

            # create radiobutton
            tk.Radiobutton(
                frame_trait_overview,
                text=" " + trait,
                variable=plr["trait_selected"][p],
                value=trait_idx,
                state=rb_state,
                command=lambda t_idx=trait_idx: write_log(
                    ["select", "trait_pile"],
                    plr["name"][p].get(),
                    traits_df.loc[t_idx].trait,
                    t_idx,
                ),
            ).grid(row=irow, column=0, padx=3, pady=ypad, sticky="nsw")

        # ----- TRAIT_icons -> inherent trait properties ----------------------
        frame_pics = tk.Frame(frame_trait_overview)
        frame_pics.grid(row=irow, column=1, sticky="sw")
        icol = -1  # initialize column index which changes depending on card

        # _true_ color
        if show_icons["color"]:
            icol += 1
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

            # show color icon
            tk.Label(frame_pics, image=images[cc + cb + cg + cp + cr + X]).grid(
                row=0, column=icol
            )

        # _true_ face
        if show_icons["face"]:
            icol += 1
            trait_face = traits_df.loc[trait_idx].face
            status_face = status_df.loc[trait_idx].face

            X = "X" if trait_face != status_face else ""
            face_string = (
                trait_face if isinstance(trait_face, str) else str(int(trait_face))
            )
            tk.Label(frame_pics, image=images[face_string + X]).grid(row=0, column=icol)

        # collection
        if show_icons["collection"]:
            icol += 1
            lbl_collection = tk.Label(frame_pics, image=images["no_star"])
            lbl_collection.grid(row=0, column=icol)

            match traits_df.loc[trait_idx].game.lower():
                case "classic":
                    lbl_collection["image"] = images["classic"]
                case "kickstarter":
                    lbl_collection["image"] = images["kickstarter"]
                case "techlings":
                    lbl_collection["image"] = images["techlings"]
                case "mythlings":
                    lbl_collection["image"] = images["mythlings"]
                case "dinolings":
                    lbl_collection["image"] = images["dinolings"]
                case "multi-color":
                    lbl_collection["image"] = images["multicolor"]
                case "special-edition":
                    lbl_collection["image"] = images["special_edition"]
                case "overlush":
                    lbl_collection["image"] = images["overlush"]

        # dominant
        if show_icons["dominant"] and traits_df.loc[trait_idx].dominant == 1:
            icol += 1
            tk.Label(frame_pics, image=images["dominant"]).grid(row=0, column=icol)

        # action
        if show_icons["action"] and traits_df.loc[trait_idx].action == 1:
            icol += 1
            tk.Label(frame_pics, image=images["action"]).grid(row=0, column=icol)

        # drops
        if show_icons["drops"] and traits_df.loc[trait_idx].drops == 1:
            icol += 1
            tk.Label(frame_pics, image=images["drops"]).grid(row=0, column=icol)

        # gene pool
        if show_icons["gene_pool"] and traits_df.loc[trait_idx].gene_pool == 1:
            icol += 1
            tk.Label(frame_pics, image=images["gene_pool"]).grid(row=0, column=icol)

        # worlds_end
        if show_icons["worlds_end"] and traits_df.loc[trait_idx].worlds_end == 1:
            icol += 1
            tk.Label(frame_pics, image=images["worlds_end"]).grid(row=0, column=icol)

        # effectless
        if show_icons["effectless"] and traits_df.loc[trait_idx].effectless == 1:
            icol += 1
            tk.Label(frame_pics, image=images["effectless"]).grid(row=0, column=icol)

        # persistent
        if show_icons["persistent"] and traits_df.loc[trait_idx].persistent == 1:
            icol += 1
            tk.Label(frame_pics, image=images["persistent"]).grid(row=0, column=icol)

        # attachment
        if show_icons["attachment"] and traits_df.loc[trait_idx].attachment == 1:
            icol += 1
            tk.Label(frame_pics, image=images["attachment"]).grid(row=0, column=icol)

        # add SEPARATOR after _true_ icons
        icol += 1
        sep = ttk.Separator(frame_pics, orient="vertical")
        sep.grid(row=0, column=icol, padx=3, pady=3, sticky="ns")

        if (
            traits_df.loc[trait_idx].attachment == 1
            or traits_df.loc[trait_idx].dominant == 1
        ):
            sep.bind(
                "<Button-1>",
                lambda e, t_idx=trait_idx: btn_remove_trait(p, "discard", t_idx),
            )

        # ----- STATE_icons -> current drop/attachment effects  ---------------
        # *new* color ---------------------------
        cur_color = status_df.loc[trait_idx].color.lower()
        if cur_color != traits_df.loc[trait_idx].color.lower():
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
                icol += 1
                X = "AT"
            else:
                X = ""

            # add new color icon
            icol += 1
            tk.Label(frame_pics, image=images[cc + cb + cg + cp + cr + X]).grid(
                row=0, column=icol
            )

        # drop value ----------------------------
        cur_drops = status_df.loc[trait_idx].drops
        if traits_df.loc[trait_idx].drops == 1:
            icol += 1
            tk.Label(frame_pics, image=images["drops"]).grid(row=0, column=icol)

            if np.isnan(cur_drops):
                # add question mark as long as no drop value is calculated
                icol += 1
                tk.Label(frame_pics, image=images["question_mark"]).grid(
                    row=0, column=icol
                )
            else:
                # check if values are higher/lower than drop icons exist
                if int(cur_drops) > 20:
                    drop_string = "20+"
                elif int(cur_drops) < -20:
                    drop_string = "-20-"
                else:
                    drop_string = str(int(cur_drops))
                # add value icon
                icol += 1
                tk.Label(frame_pics, image=images[drop_string]).grid(row=0, column=icol)

        # has attachment ------------------------
        if status_df.loc[trait_idx].attachment != "none":
            icol += 1
            tk.Label(frame_pics, image=images["attachment"]).grid(row=0, column=icol)

        # noFX ----------------------------------
        if (
            status_df.loc[trait_idx].inactive
            and "inactive" not in status_df.loc[trait_idx].effects_WE.lower()
        ):
            icol += 1
            tk.Label(frame_pics, image=images["noFX"]).grid(row=0, column=icol)

        # noRemove ------------------------------
        if status_df.loc[trait_idx].no_remove:
            icol += 1
            tk.Label(frame_pics, image=images["noRemove"]).grid(row=0, column=icol)

        # noDiscard -----------------------------
        if status_df.loc[trait_idx].no_discard:
            icol += 1
            tk.Label(frame_pics, image=images["noDiscard"]).grid(row=0, column=icol)

        # noSteal -------------------------------
        if status_df.loc[trait_idx].no_steal:
            icol += 1
            tk.Label(frame_pics, image=images["noSteal"]).grid(row=0, column=icol)

        # noSwap --------------------------------
        if status_df.loc[trait_idx].no_swap:
            icol += 1
            tk.Label(frame_pics, image=images["noSwap"]).grid(row=0, column=icol)

        # if WORLDS END effects this trait ------
        if status_df.loc[trait_idx].effects_WE != "none":
            icol += 1
            tk.Label(frame_pics, image=images["worlds_end"]).grid(row=0, column=icol)

            if "face" in status_df.loc[trait_idx].effects_WE.lower():
                icol += 1
                we_face_string = str(int(status_df.loc[trait_idx].face))
                tk.Label(frame_pics, image=images[we_face_string]).grid(
                    row=0, column=icol
                )

            if "inactive" in status_df.loc[trait_idx].effects_WE.lower():
                icol += 1
                tk.Label(frame_pics, image=images["noFX"]).grid(row=0, column=icol)

        # ----- SLEEPY may affect gene pool ?!?!  -----------------------------
        if traits_df.loc[trait_idx].trait == "Sleepy":
            irow += 1
            tk.Label(frame_trait_overview, text="gene effect:", fg="grey").grid(
                row=irow, column=0, padx=(40, 0), sticky="e"
            )

            # create combobox
            ttk.Spinbox(
                frame_trait_overview,
                from_=-5,
                to=5,
                width=3,
                wrap=False,
                textvariable=sleepy_spinbox[p],
                command=lambda: update_all(),
            ).grid(row=irow, column=1, sticky="w")

        # ----- ATTACHMENT combobox if trait is attachment --------------------
        if traits_df.loc[trait_idx].attachment == 1:
            irow += 1
            tk.Label(frame_trait_overview, text="Attach to:", fg="grey").grid(
                row=irow, column=0, padx=(40, 0), sticky="e"
            )

            # filter only non-attachment-traits and check if this is already attached to a trait
            traits_filtered_idx = [None] + rules_at.filter_attachables(trait_idx, p)
            traits_filtered_str = [" ... "] + [
                traits_df.loc[idx].trait
                for idx in traits_filtered_idx
                if idx is not None
            ]

            # create combobox
            cbox_attach_to = ttk.Combobox(
                frame_trait_overview,
                height=len(traits_filtered_str),
                values=traits_filtered_str,
                exportselection=0,
                state="readonly",
                width=9,
            )
            cbox_attach_to.grid(row=irow, column=1, sticky="w")
            cbox_attach_to.bind(
                "<<ComboboxSelected>>",
                lambda e, t=trait_idx, idx=traits_filtered_idx: btn_attach_to(
                    p, t, e, idx
                ),
            )

            # check if already attached to host
            if status_df.loc[trait_idx].host == "none":
                cbox_attach_to.current(0)
            else:
                cur_host = status_df.loc[trait_idx].host
                cbox_attach_to.current(traits_filtered_idx.index(cur_host))

        # ----- WORLDS_END combobox if trait has worlds end effect ------------
        if isinstance(traits_df.loc[trait_idx].worlds_end_task, str):
            irow += 1
            tk.Label(frame_trait_overview, text="Worlds End:", fg="grey").grid(
                row=irow, column=0, padx=(40, 0), sticky="e"
            )

            # get task what to do at worlds end
            twe_effect = rules_tr.traits_WE_tasks(trait_idx)

            # set state depending on 'played' catastrophes
            state = (
                "readonly"
                if sum(i is None for i in catastrophe["played"]) == 0
                else "disabled"
            )

            # create combobox
            cbox_attach_to = ttk.Combobox(
                frame_trait_overview,
                height=len(twe_effect),
                values=twe_effect,
                exportselection=0,
                state=state,
                width=9,
            )
            cbox_attach_to.grid(row=irow, column=1, sticky="w")
            cbox_attach_to.bind(
                "<<ComboboxSelected>>",
                lambda e, t=trait_idx: btn_traits_world_end(p, t, e.widget.get()),
            )

            # check if effect already selected
            if status_df.loc[trait_idx].traits_WE == "none":
                cbox_attach_to.current(0)
            else:
                cur_effect = status_df.loc[trait_idx].traits_WE
                cbox_attach_to.current(twe_effect.index(cur_effect))

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
            irow += 1
            tk.Label(frame_trait_overview, text="Drop of Life:", fg="grey").grid(
                row=irow, column=0, padx=(40, 0), sticky="e"
            )

            # set state depending on 'played' worlds end
            state = "readonly" if worlds_end["played"] != "none" else "disabled"

            # create spinbox
            drop_sbox = ttk.Spinbox(
                frame_trait_overview, state=state, from_=-50, to=50, width=3, wrap=False
            )
            drop_sbox.grid(row=irow, column=1, sticky="w")
            drop_sbox.bind(
                "<<Increment>>",
                lambda e, t=trait_idx: update_manual_drops(int(e.widget.get()), t, "+"),
            )
            drop_sbox.bind(
                "<<Decrement>>",
                lambda e, t=trait_idx: update_manual_drops(int(e.widget.get()), t, "-"),
            )

            # fill spinbox, depending on drops_status
            if not np.isnan(status_df.loc[trait_idx].drops):
                dp = status_df.loc[trait_idx].drops
                drop_sbox.set(int(dp))
            else:
                drop_sbox.set(0)

    # *********** special, individual case *** !!! ****************************
    # Some Drop-of-Life-Effects are affecting other players! hence, effects of
    # these traits need to be shown on each other players trait pile, allowing
    # to enter individual drop values
    irow += 1
    ttk.Separator(frame_trait_overview, orient="horizontal").grid(
        row=irow, column=0, columnspan=2, padx=5, pady=10, sticky="nesw"
    )
    # call function to insert special-effects from various traits
    irow = rules_tp.special_trait_effects(frame_trait_overview, p, irow, images)

    # --- NEOTENY needs to stay here ------------------------------------------
    # --- because 'create_trait_pile' needs to be run once checkbox is clicked
    neoteny_idx = traits_df.index[traits_df.trait == "Neoteny"].tolist()
    if neoteny_idx != []:
        neoteny_effect = status_df.loc[neoteny_idx[0]].effects
        if (worlds_end["played"] != "none") and (
            all(neoteny_idx[0] not in tp for tp in plr["trait_pile"])
        ):
            # only if no one has it or this player has it
            if neoteny_effect == "none" or neoteny_effect == str(p):
                # create separate frame for NEOTENY
                irow += 1
                frame_ntny = tk.Frame(frame_trait_overview)
                frame_ntny.grid(row=irow, column=0, columnspan=2, sticky="we")

                # add trait
                tk.Label(
                    frame_ntny, text="NEOTENY", fg=cfg["color_blue"], font='"" 14 bold'
                ).grid(row=0, column=0, padx=(10, 0), sticky="en")
                # if is this hand
                if neoteny_checkbutton[p].get() == 1:
                    ttk.Checkbutton(
                        frame_ntny,
                        variable=neoteny_checkbutton[p],
                        text=" got it -> ",
                        # command=lambda: update_traits_current_status('neoteny', int(p))
                        command=lambda: update_traits_current_status("neoteny", p),
                    ).grid(row=0, column=1, padx=(0, 0), sticky="wns")
                    ttk.Label(frame_ntny, image=images["drops"]).grid(
                        row=0, column=2, sticky="ns"
                    )
                    tk.Label(frame_ntny, image=images["4"]).grid(
                        row=0, column=3, sticky="ns"
                    )
                # not in this hand
                else:
                    ttk.Checkbutton(
                        frame_ntny,
                        variable=neoteny_checkbutton[p],
                        text=" in my hand???",
                        command=lambda: update_traits_current_status("neoteny", p),
                    ).grid(row=0, column=1, padx=(0, 0), sticky="wns")

    # *************************************************************************
    # ------ worlds end -> manual entries -------------------------------------
    if worlds_end["played"] != "none":
        irow += 1
        ttk.Separator(frame_trait_overview, orient="horizontal").grid(
            row=irow, column=0, columnspan=2, padx=5, pady=10, sticky="we"
        )

        # get world's end name & index
        we = worlds_end["played"]
        we_idx = catastrophes_df[catastrophes_df["name"] == we].index.values[0]
        we_type = catastrophes_df.loc[we_idx].worlds_end_type

        # create separate frame for WE_TITLE
        irow += 1
        frame_WE = tk.Frame(frame_trait_overview)
        frame_WE.grid(row=irow, column=0, columnspan=2, sticky="nwe")
        frame_WE.columnconfigure(0, weight=1)
        frame_WE.columnconfigure(1, weight=0)
        frame_WE.columnconfigure(2, weight=1)

        # add label & drop icon
        tk.Label(frame_WE, image=images["catastrophe_WE"]).grid(
            row=0, column=0, rowspan=2, padx=(20, 0), sticky="e"
        )
        lbl_we = tk.Label(
            frame_WE, text=" " + we + " ", fg=cfg["color_red"], font="'' 14 bold"
        )
        lbl_we.grid(row=0, column=1, sticky="ns")
        tk.Label(frame_WE, image=images["catastrophe_WE"]).grid(
            row=0, column=2, rowspan=2, padx=(0, 20), sticky="w"
        )

        # WE_EFFECTS
        if we_type == "hand" or we_type == "draw":
            # create spinbox
            we_sbox = ttk.Spinbox(
                frame_WE, state="readonly", from_=-30, to=30, width=3, wrap=False
            )
            we_sbox.grid(row=1, column=1)
            we_sbox.bind(
                "<<Increment>>", lambda e: update_manual_we(int(e.widget.get()), p, "+")
            )
            we_sbox.bind(
                "<<Decrement>>", lambda e: update_manual_we(int(e.widget.get()), p, "-")
            )

            # fill spinbox with players manually calculated WE points
            we_sbox.set(plr["points_WE_effect"][p].get())
        elif we_type == "calculate":
            we_points = (
                rules_we.calc_WE_points(p) if worlds_end["played"] != "none" else 0
            )
            tk.Label(
                frame_WE,
                image=images[str(we_points)],
            ).grid(row=1, column=1)
        else:
            lbl_we.grid(row=0, column=1, rowspan=2, sticky="ns")


def create_scoreboard(frame: tk.Frame, p: int) -> None:
    frame.columnconfigure(0, weight=1)

    # upper part: stars / name / gene_pool ------------------------------------
    fr_up = tk.Frame(frame, name="up")
    fr_up.grid(row=0, column=0, padx=5, pady=0, sticky="nesw")
    fr_up.columnconfigure(0, weight=1)
    fr_up.columnconfigure(1, weight=1)
    fr_up.columnconfigure(2, weight=6)

    # stars
    ttk.Label(fr_up, image=images["no_star"], name="star1").grid(
        row=0, column=0, sticky="e"
    )
    ttk.Label(fr_up, image=images["no_star"], name="star2").grid(
        row=0, column=1, sticky="w"
    )

    # name
    ttk.Label(
        fr_up,
        textvariable=plr["name"][p],
        name="name",
        style="nameFP.TLabel" if options["first_player"].get() == p else "name.TLabel",
    ).grid(row=0, column=2, sticky="ns")

    # gene pool
    ttk.Label(fr_up, text="gene\npool", justify=tk.RIGHT, style="genesTXT.TLabel").grid(
        row=0, column=3, sticky="e"
    )

    ttk.Label(fr_up, textvariable=plr["genes"][p], style="genes.TLabel").grid(
        row=0, column=4, sticky="w"
    )

    # separator ---------------------------------------------------------------
    ttk.Separator(frame, orient="horizontal").grid(
        row=1, column=0, padx=10, pady=0, sticky="we"
    )

    # lower part: points / n_traits -------------------------------------------
    mgn = 1  # defines space between rows of colors/points
    fr_down = tk.Frame(frame, name="down")
    fr_down.grid(row=2, column=0, padx=5, pady=0, sticky="new")
    fr_down.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
    fr_down.columnconfigure(7, weight=5)
    fr_down.columnconfigure((9, 10, 11, 12), weight=1)

    # color counts --------------------
    set = 1
    if set == 1:
        # simple version with colored text_labels
        ttk.Label(fr_down, textvariable=plr["n_tp"][p]["b"], style="cc_b.TLabel").grid(
            row=0, column=0, columnspan=2, pady=(0, mgn), sticky="se"
        )

        ttk.Label(fr_down, textvariable=plr["n_tp"][p]["g"], style="cc_g.TLabel").grid(
            row=0, column=2, columnspan=2, pady=(0, mgn), sticky="s"
        )

        ttk.Label(fr_down, textvariable=plr["n_tp"][p]["c"], style="cc_c.TLabel").grid(
            row=0, column=4, columnspan=2, pady=(0, mgn), sticky="sw"
        )

        ttk.Label(fr_down, textvariable=plr["n_tp"][p]["p"], style="cc_p.TLabel").grid(
            row=1, column=0, columnspan=2, pady=(mgn, 0), sticky="ne"
        )

        ttk.Label(fr_down, textvariable=plr["n_tp"][p]["r"], style="cc_r.TLabel").grid(
            row=1, column=2, columnspan=2, pady=(mgn, 0), sticky="n"
        )

        ttk.Label(
            fr_down, textvariable=plr["n_tp"][p]["sb"], style="cc_total.TLabel"
        ).grid(row=1, column=4, columnspan=2, pady=(mgn, 0), sticky="nw")
    else:
        # keep more beautiful version with colored circles... but this takes
        # more space... maybe later...
        ttk.Label(
            fr_down, textvariable=plr["n_tp"][p]["b"], style="colorcount.TLabel"
        ).grid(row=0, column=0, sticky="e")
        ttk.Label(fr_down, image=images["b"]).grid(row=0, column=1, sticky="w")

        ttk.Label(
            fr_down, textvariable=plr["n_tp"][p]["g"], style="colorcount.TLabel"
        ).grid(row=1, column=0, sticky="e")
        ttk.Label(fr_down, image=images["g"]).grid(row=1, column=1, sticky="w")

        ttk.Label(
            fr_down, textvariable=plr["n_tp"][p]["p"], style="colorcount.TLabel"
        ).grid(row=0, column=2, sticky="e")
        ttk.Label(fr_down, image=images["p"]).grid(row=0, column=3, sticky="w")

        ttk.Label(
            fr_down, textvariable=plr["n_tp"][p]["r"], style="colorcount.TLabel"
        ).grid(row=1, column=2, sticky="e")
        ttk.Label(fr_down, image=images["r"]).grid(row=1, column=3, sticky="w")

        ttk.Label(
            fr_down, textvariable=plr["n_tp"][p]["c"], style="colorcount.TLabel"
        ).grid(row=0, column=4, sticky="e")
        ttk.Label(fr_down, image=images["c"]).grid(row=0, column=5, sticky="w")

        ttk.Label(
            fr_down,
            textvariable=plr["n_tp"][p]["sb"],
            style="colorcount.TLabel",
            justify=tk.RIGHT,
        ).grid(row=1, column=4, sticky="e")
        ttk.Label(fr_down, image=images["sum"]).grid(row=1, column=5, sticky="w")

    # separator --------------------
    ttk.Separator(fr_down, orient="vertical").grid(
        row=0, column=6, rowspan=2, padx=5, pady=10, sticky="ns"
    )

    # total points --------------------
    ttk.Label(
        fr_down, textvariable=plr["points"][p]["total"], style="total.TLabel"
    ).grid(row=0, column=7, rowspan=2, padx=0, pady=0, sticky="ns")

    # separator --------------------
    ttk.Separator(fr_down, orient="vertical").grid(
        row=0, column=8, rowspan=2, padx=5, pady=10, sticky="ns"
    )

    # single points --------------------
    mgn = 7
    ttk.Label(fr_down, image=images["blank_sb"]).grid(
        row=0, column=9, pady=(mgn, 0), sticky="e"
    )
    ttk.Label(
        fr_down, textvariable=plr["points"][p]["face"], style="points.TLabel"
    ).grid(row=0, column=10, pady=(mgn, 0), sticky="w")

    ttk.Label(fr_down, image=images["drops_sb"]).grid(
        row=0, column=11, pady=(mgn, 0), sticky="e"
    )
    ttk.Label(
        fr_down, textvariable=plr["points"][p]["drops"], style="points.TLabel"
    ).grid(row=0, column=12, pady=(mgn, 0), sticky="w")

    ttk.Label(fr_down, image=images["worlds_end_sb"]).grid(
        row=1, column=9, pady=(0, mgn), sticky="e"
    )
    ttk.Label(
        fr_down, textvariable=plr["points"][p]["worlds_end"], style="points.TLabel"
    ).grid(row=1, column=10, pady=(0, mgn), sticky="w")

    ttk.Label(fr_down, image=images["MOL_sb"]).grid(
        row=1, column=11, pady=(0, mgn), sticky="e"
    )
    ttk.Label(
        fr_down, textvariable=plr["points"][p]["MOL"], style="points.TLabel"
    ).grid(row=1, column=12, pady=(0, mgn), sticky="w")


def create_player_frame(p: int) -> tk.Frame:
    # this is a one-time call -> all created frames needs to be stored for later usage
    border = cfg["width_frames"]

    frame = tk.Frame(frame_playground, bg=cfg["color_frames"], name="p" + str(p))
    frame.columnconfigure(
        0, weight=1
    )  # stretch sub_frames to width of playground (=1!)
    frame.rowconfigure(1, weight=1)  # stretch trait-pile to bottom of playground
    frame.grid(
        column=p, row=0, padx=(0, 10), pady=10, sticky="nesw"
    )  # or use nsw for non-x-stretched frames!

    # ----- score_board -------------------------------------------------------
    frame_scoreboard = tk.Frame(frame, name="scoreboard")
    frame_scoreboard.grid(
        row=0, column=0, padx=border, pady=border, ipady=0, sticky="nesw"
    )
    create_scoreboard(frame_scoreboard, p)

    # ----- gaming area -------------------------------------------------------
    frame_traits = tk.Frame(frame)
    frame_traits.grid(row=1, column=0, padx=border, pady=(0, border), sticky="nesw")
    frame_traits.rowconfigure(2, weight=1)
    frame_traits.columnconfigure(0, weight=1)  # for left button under trait-pile
    frame_traits.columnconfigure(1, weight=1)  # for middle button under trait-pile
    frame_traits.columnconfigure(2, weight=1)  # for right button under trait-pile

    # action buttons -----------------
    cbox_move_to = ttk.Combobox(
        frame_traits,
        height=game["n_player"] + 1,
        values=[" move to ..."]
        + [
            "p" + str(i + 1) + ": " + j.get()
            for i, j in enumerate(plr["name"])
            if i != p
        ],
        exportselection=0,
        state="readonly",
        width=6,
    )
    cbox_move_to.grid(row=0, column=0, pady=(border, 0), sticky="ne")
    cbox_move_to.current(0)
    cbox_move_to.bind("<<ComboboxSelected>>", lambda e: btn_move_trait(p, cbox_move_to))

    ttk.Button(
        frame_traits,
        text="to hand",
        width=5,
        command=partial(btn_remove_trait, p, "hand"),
    ).grid(row=0, column=1, pady=(border, 0), sticky="n")
    ttk.Button(
        frame_traits,
        text="discard",
        width=5,
        command=partial(btn_remove_trait, p, "discard"),
    ).grid(row=0, column=2, pady=(border, 0), sticky="nw")

    ttk.Separator(frame_traits, orient="horizontal").grid(
        row=1, column=0, columnspan=3, padx=5, pady=5, sticky="we"
    )

    # ----- trait pile ---------------
    frame_trait_pile[p] = tk.Frame(frame_traits, name="trait_pile")
    frame_trait_pile[p].grid(
        row=2, column=0, columnspan=3, sticky="nesw", padx=border, pady=border
    )
    frame_trait_pile[p].columnconfigure(1, weight=1)
    create_trait_pile(frame_trait_pile[p], p)

    # ----- Meaning of Life ---------------------------------------------------
    frame_MOL[p] = tk.Frame(frame, name="f_MOLs")
    frame_MOL[p].grid(row=2, column=0, padx=border, pady=(0, border), sticky="nesw")

    # call function to create MOL comboboxes
    create_MOL_frame(p)

    return frame


def create_name_entries(frame_menu_names: tk.Frame) -> None:
    # forget all previous widgets
    for w in frame_menu_names.grid_slaves():
        w.grid_forget()

    # note to keep order
    ttk.Label(frame_menu_names, text="important:", style="menu_h2u.TLabel").grid(
        row=0, column=0, columnspan=1, pady=(0, 5), sticky="e"
    )
    ttk.Label(frame_menu_names, text="keep order", style="menu_h2.TLabel").grid(
        row=0, column=1, columnspan=2, pady=(0, 5), sticky="w"
    )

    # name entries --- at least as much as current players, or more for next game
    for i in range(max([game["n_player"], options["n_player"].get()])):
        ttk.Label(frame_menu_names, text="player {}: ".format(i + 1)).grid(
            row=i + 1, column=0, sticky="e"
        )
        ttk.Entry(frame_menu_names, textvariable=options["names"][i], width=5).grid(
            row=i + 1, column=1, sticky="we"
        )
        tk.Radiobutton(
            frame_menu_names,
            variable=options["first_player"],
            value=i,
            state="normal" if i + 1 <= game["n_player"] else "disabled",
            command=lambda: update_first_player(),
        ).grid(row=i + 1, column=2, sticky="e")


def create_menu_frame() -> None:
    border = cfg["width_frames"]

    # ----- frame 4 options ---------------------------------------------------
    frame_menu_options = tk.Frame(frame_menu)
    frame_menu_options.grid(row=0, column=0, padx=border, pady=border, sticky="nesw")
    frame_menu_options.columnconfigure(0, weight=1)
    frame_menu_options.columnconfigure(1, weight=1)

    # title -----
    ttk.Label(frame_menu_options, text="Next Game", style="menu_h1.TLabel").grid(
        row=0, column=0, columnspan=2, pady=(border, 0)
    )

    # nr players -----
    ttk.Label(
        frame_menu_options,
        text="# players: ",
    ).grid(row=1, column=0, sticky="e")
    ttk.Spinbox(
        frame_menu_options,
        from_=2,
        to=cfg["max_player"],
        width=2,
        textvariable=options["n_player"],
        wrap=False,
        command=lambda: create_name_entries(frame_menu_names),
    ).grid(row=1, column=1, sticky="w")

    # genes at beginning -----
    ttk.Label(
        frame_menu_options,
        text="gene pool: ",
    ).grid(row=2, column=0, sticky="e")
    ttk.Spinbox(
        frame_menu_options,
        from_=3,
        to=8,
        width=2,
        textvariable=options["n_genes"],
        wrap=False,
    ).grid(row=2, column=1, sticky="w")

    # nr catastrophes -----
    ttk.Label(
        frame_menu_options,
        text="# catastrophes: ",
    ).grid(row=3, column=0, sticky="e")
    ttk.Spinbox(
        frame_menu_options,
        from_=2,
        to=6,
        width=2,
        textvariable=options["n_catastrophes"],
        wrap=False,
    ).grid(row=3, column=1, sticky="w")

    # nr MOLs -----
    ttk.Label(
        frame_menu_options,
        text="# MOLs: ",
    ).grid(row=4, column=0, sticky="e")
    ttk.Spinbox(
        frame_menu_options,
        from_=0,
        to=4,
        width=2,
        textvariable=options["n_MOLs"],
        wrap=False,
    ).grid(row=4, column=1, sticky="w")

    ttk.Separator(frame_menu_options, orient="horizontal").grid(
        row=5, column=0, columnspan=3, padx=10, pady=8, sticky="we"
    )

    # players names -----
    frame_menu_names = tk.Frame(frame_menu_options)
    frame_menu_names.grid(row=6, column=0, columnspan=2, sticky="ns")
    frame_menu_names.columnconfigure(0, weight=1)
    frame_menu_names.columnconfigure(1, weight=1)
    create_name_entries(frame_menu_names)

    # restart button -----
    ttk.Button(
        frame_menu_options,
        text="restart game",
        command=start_game,
        style="menu.TButton",
        width=12,
    ).grid(row=7, column=0, columnspan=2, padx=border, pady=border)

    # info current game -----
    ttk.Label(frame_menu_options, text="running game", style="menu_h2u.TLabel").grid(
        row=8, column=0, columnspan=2
    )
    ttk.Label(
        frame_menu_options,
        text="{} catast. + {} genes + {} MOLs".format(
            game["n_catastrophes"], game["n_genes"], game["n_MOLs"]
        ),
        style="game_info.TLabel",
    ).grid(row=9, column=0, columnspan=2, pady=(0, 8))

    # ----- frame 4 trait selection -------------------------------------------
    frame_menu_traits = tk.Frame(frame_menu)
    frame_menu_traits.grid(
        row=1, column=0, padx=border, pady=(0, border), sticky="nesw"
    )
    frame_menu_traits.columnconfigure(0, weight=1)
    frame_menu_traits.columnconfigure(1, weight=1)

    # 'play trait' -----
    ttk.Label(frame_menu_traits, text="who plays a trait", style="menu_h1.TLabel").grid(
        row=0, column=0, columnspan=2, pady=(5, 0)
    )

    # search field -----
    ent_trait_search[0] = ttk.Entry(
        frame_menu_traits, width=7, textvariable=str_trait_search
    )
    ent_trait_search[0].grid(row=1, column=0, padx=(border, 0), sticky="e")
    ent_trait_search[0].bind(
        "<KeyRelease>", lambda e: search_trait_in_list(str_trait_search)
    )
    ent_trait_search[0].bind(
        "<Down>", lambda e: lbox_deck[0].selection_clear(0, tk.END), add="+"
    )
    ent_trait_search[0].bind("<Down>", lambda e: lbox_deck[0].selection_set(0), add="+")
    ent_trait_search[0].bind("<Down>", lambda e: lbox_deck[0].focus(), add="+")
    ent_trait_search[0].bind("<Down>", lambda e: lbox_deck[0].see(0), add="+")
    ent_trait_search[0].bind(
        "<Down>",
        lambda e: write_log(
            ["select", "deck"],
            traits_df.loc[deck_filtered_idx[0]].trait,
            deck_filtered_idx[0],
        ),
        add="+",
    )

    ttk.Button(
        frame_menu_traits,
        text="clr",
        width=3,
        style="menu.TButton",
        command=btn_clear_trait_search,
    ).grid(row=1, column=1, padx=(0, 10), sticky="w")

    # listbox with (filtered) deck-cards -----
    lbox_deck[0] = tk.Listbox(
        frame_menu_traits,
        height=3,
        width=16,
        listvariable=deck_filtered_str,
        exportselection=False,
        font="'', 11",
    )
    lbox_deck[0].grid(row=2, column=0, columnspan=2, padx=2 * border, sticky="ew")
    lbox_deck[0].bind(
        "<<ListboxSelect>>",
        lambda e: write_log(
            ["select", "deck"],
            traits_df.loc[deck_filtered_idx[lbox_deck[0].curselection()[0]]].trait,
            deck_filtered_idx[lbox_deck[0].curselection()[0]],
        ),
    )
    lbox_deck[0].bind(
        "<Up>",
        lambda e: (
            ent_trait_search[0].focus() if lbox_deck[0].curselection()[0] == 0 else None
        ),
    )
    # create key bindings to play trait into player's trait pile by hitting
    # number on keyboard
    for p in range(game["n_player"]):
        lbox_deck[0].bind("{}".format(p + 1), lambda e, pp=p: btn_play_trait(pp))

    # player buttons -----
    frame_menu_buttons = tk.Frame(frame_menu_traits)
    frame_menu_buttons.grid(row=3, column=0, columnspan=2, pady=(0, 5))
    for i in range(game["n_player"]):
        clspn = int(i + 1 == game["n_player"] and (i + 1) % 2 == 1) + 1
        ttk.Button(
            frame_menu_buttons,
            textvariable=plr["name"][i],
            width=5,
            style="menu.TButton",
            command=partial(btn_play_trait, i),
        ).grid(row=floor(i / 2), column=i % 2, columnspan=clspn)

    # ----- frame 4 catastrophe selection -------------------------------------
    frame_menu_catastrophe = tk.Frame(frame_menu)
    frame_menu_catastrophe.grid(
        row=2, column=0, padx=border, pady=(0, border), sticky="nesw"
    )
    frame_menu_catastrophe.columnconfigure(0, weight=1)
    frame_menu_catastrophe.columnconfigure(1, weight=1)

    # catastrophes -----
    ttk.Label(frame_menu_catastrophe, text="Catastrophes", style="menu_h1.TLabel").grid(
        row=0, column=0, columnspan=2, pady=(5, 0)
    )

    for c in range(game["n_catastrophes"]):
        pos_cat_values = [" catastrophe {}...".format(c + 1)] + catastrophes_df.loc[
            catastrophe["possible"][c]
        ].name.values.tolist()

        catastrophe["cbox"][c] = ttk.Combobox(
            frame_menu_catastrophe,
            values=pos_cat_values,
            exportselection=0,
            state="readonly" if c == 0 else "disabled",
            width=14,
        )
        catastrophe["cbox"][c].current(0)
        catastrophe["cbox"][c].grid(
            row=c + 1, column=0, columnspan=2, padx=4, sticky="ns"
        )
        catastrophe["cbox"][c].bind(
            "<<ComboboxSelected>>", lambda ev, c=c: btn_play_catastrophe(ev, c)
        )

    # world's end -----
    ttk.Label(frame_menu_catastrophe, text="World's End", style="menu_h1.TLabel").grid(
        row=game["n_catastrophes"] + 1, column=0, columnspan=2
    )

    worlds_end["cbox"] = ttk.Combobox(
        frame_menu_catastrophe,
        values=[" ... "],
        exportselection=0,
        state="disabled",
        width=7,
        textvariable=worlds_end["selected"],
    )
    worlds_end["cbox"].current(0)
    worlds_end["cbox"].grid(
        row=game["n_catastrophes"] + 2,
        column=0,
        columnspan=1,
        padx=(border, 0),
        pady=(0, 5),
        sticky="nes",
    )
    worlds_end["cbox"].bind(
        "<<ComboboxSelected>>", lambda e: check_WE_status("select_WE")
    )

    worlds_end["btn"] = ttk.Button(
        frame_menu_catastrophe,
        text="GO!",
        width=3,
        state="disabled",
        style="disabled.TButton",
        command=lambda: btn_worlds_end_GO(),
    )
    worlds_end["btn"].grid(
        row=game["n_catastrophes"] + 2,
        column=1,
        columnspan=1,
        padx=(0, border),
        pady=(0, 5),
        sticky="nsw",
    )

    # ----- frame for control buttons -----------------------------------------
    frame_menu_controls = tk.Frame(frame_menu)
    frame_menu_controls.grid(
        row=3, column=0, padx=border, pady=(0, border), sticky="nesw"
    )
    frame_menu_controls.columnconfigure(0, weight=2)
    frame_menu_controls.columnconfigure(1, weight=2)
    frame_menu_controls.columnconfigure(2, weight=2)
    frame_menu_controls.columnconfigure(3, weight=0)

    lbl_music_switch[0] = ttk.Label(
        frame_menu_controls, image=init_switch["music"], cursor="heart"
    )
    lbl_music_switch[0].grid(row=0, column=0, padx=(border, 0))
    lbl_music_switch[0].bind("<Button-1>", lambda e: switch("music"))
    lbl_icons_switch[0] = ttk.Label(frame_menu_controls, image=init_switch["icons"])
    lbl_icons_switch[0].grid(row=0, column=1, padx=0)
    lbl_icons_switch[0].bind("<Button-1>", lambda e: switch("icons"))
    lbl_points_switch[0] = ttk.Label(frame_menu_controls, image=init_switch["points"])
    lbl_points_switch[0].grid(row=0, column=2, padx=0)
    lbl_points_switch[0].bind("<Button-1>", lambda e: switch("points"))
    lbl_exit = ttk.Label(frame_menu_controls, image=images["exit"])
    lbl_exit.grid(row=0, column=3, padx=(0, border), pady=5)
    lbl_exit.bind("<Button-1>", lambda e: btn_quit())


def reset_variables() -> None:
    # update current settings
    game["n_player"] = options["n_player"].get()
    game["n_genes"] = options["n_genes"].get()
    game["n_catastrophes"] = options["n_catastrophes"].get()
    game["n_MOLs"] = options["n_MOLs"].get()

    # update first player if not playing anymore
    if options["first_player"].get() + 1 > game["n_player"]:
        options["first_player"].set(game["n_player"] - 1)

    # reset _player_ variables
    plr["name"].clear()
    plr["genes"].clear()
    plr["points"].clear()
    plr["trait_pile"].clear()
    plr["n_tp"].clear()
    plr["trait_selected"].clear()
    plr["points_WE_effect"].clear()
    plr["points_MOL"].clear()
    frame_trait_pile.clear()

    # reset MOLs
    MOLs["played"].clear()
    MOLs["cbox"].clear()
    MOLs["icon"].clear()
    MOLs["n"].clear()

    # reset trait_specific variables
    neoteny_checkbutton.clear()
    sleepy_spinbox.clear()

    # fill variables
    for p in range(game["n_player"]):
        plr["name"].append(tk.StringVar(value=options["names"][p].get()))
        write_log(["init", "names"], p + 1, plr["name"][p].get())

        plr["genes"].append(tk.IntVar(value=game["n_genes"]))
        plr["points"].append(
            {
                "face": tk.IntVar(value=0),
                "drops": tk.IntVar(value=0),
                "worlds_end": tk.IntVar(value=0),
                "MOL": tk.IntVar(value=0),
                "total": tk.IntVar(value=0),
            }
        )
        plr["trait_pile"].append([])
        plr["n_tp"].append(
            {
                "b": tk.StringVar(value="0"),
                "g": tk.StringVar(value="0"),
                "p": tk.StringVar(value="0"),
                "r": tk.StringVar(value="0"),
                "c": tk.StringVar(value="0"),
                "t": tk.StringVar(value="0"),
                "xtra": 0,
                "sb": tk.StringVar(value="\u2211 0"),
            }
        )
        plr["trait_selected"].append(tk.Variable(value=np.nan))
        plr["points_WE_effect"].append(tk.IntVar(value=0))
        plr["points_MOL"].append([])
        MOLs["played"].append([])
        MOLs["cbox"].append([])
        MOLs["icon"].append([])
        MOLs["n"].append(options["n_MOLs"].get())

        frame_trait_pile.append(None)
        neoteny_checkbutton.append(tk.IntVar(value=0))
        sleepy_spinbox.append(tk.IntVar(value=0))

        for m in range(game["n_MOLs"]):
            plr["points_MOL"][p].append(
                tk.IntVar(value=0)
            )  # for now, manually editing MOL points in entries
            MOLs["played"][p].append(None)
            MOLs["cbox"][p].append([])
            MOLs["icon"][p].append([])

    # first player
    write_log(
        ["init", "first_player"], plr["name"][options["first_player"].get()].get()
    )

    # reset deck/lbox card-lists
    deck.clear()
    deck.extend(traits_df.index.tolist())  # complete list of indices of all traits
    deck_filtered_idx.clear()
    deck_filtered_idx.extend(
        traits_df.index.tolist()
    )  # complete list of indices of traits for menu_listbox
    deck_filtered_str.set(
        traits_df.loc[deck].trait.values.tolist()
    )  # complete list of names of traits

    # reset occurred catastrophes
    catastrophe["possible"].clear()
    catastrophe["played"].clear()
    catastrophe["cbox"].clear()
    for i in range(game["n_catastrophes"]):
        catastrophe["possible"].append(catastrophes_df.index.tolist())
        catastrophe["played"].append(None)
        catastrophe["cbox"].append([])

    # reset worlds end
    worlds_end["selected"] = tk.StringVar(value="")
    worlds_end["played"] = "none"
    worlds_end["cbox"] = [None]
    worlds_end["btn"] = [None]

    # reset current status
    status_df["color"] = traits_df.color
    status_df["face"] = traits_df.face
    status_df["drops"] = np.nan
    status_df["host"] = "none"
    status_df["attachment"] = "none"
    status_df["inactive"] = False
    status_df["no_remove"] = False
    status_df["no_discard"] = False
    status_df["no_steal"] = False
    status_df["no_swap"] = False
    status_df["effects"] = "none"
    status_df["effects_attachment"] = "none"
    status_df["effects_traits_WE"] = "none"
    status_df["effects_WE"] = "none"
    status_df["traits_WE"] = "none"


def start_game() -> None:
    # new logfile -------------------------------------------------------------
    dt = time.strftime("%Y%m%d-%H%M%S")
    logfile["file"] = os.path.join(dir_log, "DoomPyLog_" + dt + ".txt")
    write_log(["init", "datetime"], dt)

    # reset variables ---------------------------------------------------------
    write_log(["init", "variables"])
    reset_variables()

    # update frame_configurations settings ------------------------------------
    for w in frame_menu.grid_slaves():
        w.grid_forget()

    for w in frame_playground.grid_slaves():
        w.grid_forget()

    for i in range(cfg["max_player"]):
        w = (
            0 if i >= game["n_player"] else 1
        )  # 'else 1' => player_frames are stretchable
        frame_playground.columnconfigure(i, weight=w)

    # fill _menu_ frame -------------------------------------------------------
    write_log(["init", "menu"])
    create_menu_frame()

    # set catastrophe F-key-bindings
    for i in range(game["n_catastrophes"]):
        root.bind(
            "<F" + str(i + 1) + ">", lambda e, j=i: catastrophe["cbox"][j].focus()
        )

    # fill _playground_ frame with _player_ frames ----------------------------
    write_log(["init", "playground"])
    frame_player.clear()
    frame_MOL.clear()
    for i in range(game["n_player"]):
        frame_MOL.append([])
        frame_player.append(create_player_frame(i))

    # clear traits listbox ----------------------------------------------------
    btn_clear_trait_search()


# _tkinter_ ###################################################################
# create a window -------------------------------------------------------------
root = tk.Tk()
root.title("LIVE Doomlings Calculator")
root.geometry("1600x900")
root.configure(background=cfg["color_bg"])
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# create gui_wide F-key bindings
root.bind("<F7>", lambda e: btn_clear_trait_search())
root.bind("<F8>", lambda e: start_game())
root.bind("<F9>", lambda e: simulate())

# create _content_ frame ------------------------------------------------------
content = tk.Frame(root, width=1200, height=800, bg=cfg["color_bg"], name="content")
content.grid(column=0, row=0, sticky="nesw")
content.columnconfigure(0, weight=0)  # menu on the left
content.columnconfigure(
    1, weight=1
)  # full playground -> set =1 to stretch it to the right side

# create _menu_ frame ---------------------------------------------------------
frame_menu = tk.Frame(content, bg=cfg["color_frames"], name="menu")
frame_menu.grid(row=0, column=0, padx=10, pady=10, sticky="n")

# create _playground_ frame ---------------------------------------------------
frame_playground = tk.Frame(content, bg=cfg["color_bg"], name="playground")
frame_playground.grid(row=0, column=1, padx=0, pady=0, stick="nesw")
frame_playground.rowconfigure(0, weight=1)  # =1 -> stretch playground to bottom

# styling ---------------------------------------------------------------------
gui_style = ttk.Style()
gui_style.configure("menu.TButton", font=("", 12))
gui_style.configure("menu_h1.TLabel", font=("", 14))
gui_style.configure("menu_h2.TLabel", font=("", 12))
gui_style.configure("menu_h2u.TLabel", font=("", 12, "underline"))
gui_style.configure("game_info.TLabel", font=("", 10, "italic"))

gui_style.configure("name.TLabel", font=("Comic Sans MS", 38, "bold"))
gui_style.configure(
    "nameFP.TLabel",
    font=("Comic Sans MS", 38, "bold"),
    foreground=cfg["font_color_1st_player"],
)

gui_style.configure("n_traits.TLabel", font=("Arial", 30, "bold"))

gui_style.configure("colorcount.TLabel", font=("", 14))
gui_style.configure("cc_b.TLabel", font=("", 18, "bold"), foreground=cfg["color_blue"])
gui_style.configure("cc_g.TLabel", font=("", 18, "bold"), foreground=cfg["color_green"])
gui_style.configure(
    "cc_p.TLabel", font=("", 18, "bold"), foreground=cfg["color_purple"]
)
gui_style.configure("cc_r.TLabel", font=("", 18, "bold"), foreground=cfg["color_red"])
gui_style.configure(
    "cc_c.TLabel", font=("", 18, "bold"), foreground=cfg["color_colorless"]
)
gui_style.configure("cc_total.TLabel", font=("", 18, "bold"))

gui_style.configure(
    "total.TLabel", font=("", 50, "bold"), foreground=cfg["font_color_total_score"]
)
gui_style.configure("points.TLabel", font=("", 14))

gui_style.configure(
    "genesTXT.TLabel", font=("", 12, "bold"), foreground=cfg["font_color_genes"]
)
gui_style.configure(
    "genes.TLabel", font=("", 38, "bold"), foreground=cfg["font_color_genes"]
)

root.option_add("*TCombobox*Listbox.font", "'' 10")

gui_style.configure("disabled.TButton", foreground="grey", font="'', 11")

# tk_inter_variables ----------------------------------------------------------

options = {}
options["n_player"] = tk.IntVar(value=cfg["n_player"])  # OPTIONS: number of players
options["n_genes"] = tk.IntVar(value=cfg["n_genes"])  # OPTIONS: gene pool at beginning
options["n_catastrophes"] = tk.IntVar(
    value=cfg["n_catastrophes"]
)  # OPTIONS: number of catastrophes
options["n_MOLs"] = tk.IntVar(value=cfg["n_MOLs"])  # OPTIONS: number of MOLs
options["names"] = []
for i in range(len(cfg["names"])):
    options["names"].append(
        tk.StringVar(value=cfg["names"][i])
    )  # OPTIONS: name of players
options["first_player"] = tk.IntVar(value=0)  # OPTIONS: RADIOBUTTON - first player

str_trait_search = tk.StringVar(value="")  # string searching for traits in DECK
deck_filtered_str = tk.Variable(
    value=""
)  # _filtered_ deck of traits_strings in listbox after searching -> str

# load tk-images --------------------------------------------------------------
images = {}
for k, v in images_dict.items():
    images[k] = ImageTk.PhotoImage(v)

# set switch images -----------------------------------------------------------
init_switch = {}
show_icons = {}
if icons_onoff == "on":
    init_switch["icons"] = images["icons_on"]
elif icons_onoff == "full":
    init_switch["icons"] = images["icons_full"]
else:
    init_switch["icons"] = images["icons_off"]

if music_onoff == "on":
    init_switch["music"] = images["note_on"]
else:
    init_switch["music"] = images["note_off"]

if points_onoff == "on":
    init_switch["points"] = images["points_123"]
elif points_onoff == "rank":
    init_switch["points"] = images["rank"]
else:
    init_switch["points"] = images["question_mark"]

# (re)start game ##############################################################
mixer.init()
switch("show_icons")
start_game()

# run mainloop ################################################################
root.mainloop()
