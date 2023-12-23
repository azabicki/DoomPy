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

from globals_ import logfile, dir_log
from globals_ import cfg, images_dict, sounds, music_onoff, icons_onoff, points_onoff
from globals_ import traits_df, status_df, catastrophes_df
from globals_ import lbl_music_switch, lbl_icons_switch, lbl_points_switch, ent_trait_search, lbox_deck
from globals_ import frame_player, frame_trait_pile
from globals_ import game, plr, deck, deck_filtered_idx, catastrophe, worlds_end
from globals_ import neoteny_checkbutton, sleepy_spinbox


# functions ##############################################################
def get_sup(tp):
    lib = {'0': '\u2070', '1': '\u00B9', '2': '\u00B2', '3': '\u00B3', '4': '\u2074',
           '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079'}

    return ''.join(lib[i] for i in str(len(tp)))


def pre_play():
    start_game()
    pre_play_set = 'test'

    if pre_play_set == 'action':
        lisa = [210, 218, 221, 222, 223, 226, 227, 230, 233]
        for t in lisa:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(0)

        julia = [234, 236, 237, 238, 239, 249, 254, 259, 264, 266, 267, 269, 270, 271, 272]
        for t in julia:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(1)

        anton = [276, 281, 286, 294, 295, 298, 304, 316, 322, 323, 325, 326, 327, 328, 330]
        for t in anton:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(2)

        adam = [331, 334, 337, 338, 339, 342, 343, 345, 346, 348, 350, 353, 354, 360, 363]
        for t in adam:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(3)

    if pre_play_set == 'effectless':
        lisa = [0, 1, 9, 11, 18, 19, 21]
        for t in lisa:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(0)

        julia = [26, 28, 44, 52, 62, 68, 72, 76, 77]
        for t in julia:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(1)

        anton = [79, 81, 84, 103, 105, 106, 107, 114, 115]
        for t in anton:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(2)

        adam = [117, 118, 121, 124, 131, 135, 136, 148, 173, 179]
        for t in adam:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(3)

    if pre_play_set == 'attachments':
        lisa = [0, 1, 9, 11, 19, 21, 26, 29, 69, 89, 178, 256, 300]
        for t in lisa:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(0)

        julia = [52, 62, 68, 72, 81, 84, 30, 70, 301, 340]
        for t in julia:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(1)

        anton = [105, 107, 114, 115, 117, 177, 257, 341]
        for t in anton:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(2)

        adam = [362, 356, 347, 336, 320, 291, 283, 127, 128, 182, 183, 199, 200]
        for t in adam:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(3)

    if pre_play_set == 'drops_A':
        lisa = [4, 16, 24, 25, 37, 40, 41, 64, 66, 67, 82, 87]
        for t in lisa:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(0)

        julia = [95, 98, 122, 123, 127, 128, 132, 140, 147, 160, 161, 162, 163, 164, 165, 166]
        for t in julia:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(1)

        anton = [167, 168, 169, 170, 171, 190, 203, 208, 215]
        for t in anton:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(2)

        adam = [228, 232, 247, 260, 274, 275, 277, 278, 287, 290, 296, 317, 318, 324, 333, 352]
        for t in adam:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(3)

    if pre_play_set == 'drops_B':
        lisa = [37, 41, 66, 67]
        for t in lisa:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(0)

        julia = [122, 123]
        for t in julia:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(1)

        anton = [203, 260]
        for t in anton:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(2)

        adam = [274, 275, 296, 333]
        for t in adam:
            trait_idx = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(trait_idx)
            btn_play_trait(3)

    if pre_play_set == 'random':
        rounds = 6
        for r in range(rounds):
            for p in range(game['n_player']):
                print(p, ' _ ', r)

                t = np.random.randint(low=0, high=len(deck)-1)
                lbox_deck[0].selection_set(t)
                trait_idx = deck_filtered_idx[lbox_deck[0].curselection()[0]]

                # write log
                write_log(['select', 'deck'],
                          traits_df.loc[deck_filtered_idx[lbox_deck[0].curselection()[0]]].trait,
                          trait_idx)

                # repeat until trait played
                while btn_play_trait(p) == 0:
                    btn_clear_trait_search()

                    t = np.random.randint(low=0, high=len(deck)-1)
                    lbox_deck[0].selection_set(t)
                    trait_idx = deck_filtered_idx[lbox_deck[0].curselection()[0]]

                    write_log(['select', 'deck'],
                              traits_df.loc[deck_filtered_idx[lbox_deck[0].curselection()[0]]].trait,
                              trait_idx)

                # attach to host if neccessary
                if traits_df.loc[trait_idx].attachment == 1:
                    host_idx = rules_at.filter_attachables(trait_idx, p)[0]

                    write_log(['attach_to', 'attached'], plr['name'][p].get(),
                              traits_df.loc[trait_idx].trait, trait_idx,
                              traits_df.loc[host_idx].trait, host_idx)

                    # set new attachment to status_row of host & update effects of attachment on host
                    status_df.loc[trait_idx, 'host'] = host_idx
                    status_df.loc[host_idx, 'attachment'] = trait_idx

                    # update scoring
                    update_all()

                # reset trait to play
                btn_clear_trait_search()
                trait_idx = None

            # play catastrophe ?!
            if r % 3 == 2:
                n_cat = sum(i is not None for i in catastrophe['played'])
                if n_cat < game['n_catastrophes']:
                    c = np.random.randint(low=0, high=len(catastrophe['possible'][n_cat]))
                    catastrophe['cbox'][n_cat].current(c)
                    catastrophe['cbox'][n_cat].event_generate("<<ComboboxSelected>>")

    if pre_play_set == 'test':
        to_play = [[1, 9, 21, 26, 69, 104, 125],
                   [44, 52, 62, 68, 177, 340],
                   [11, 18, 19, 29, 300],
                   [103, 105, 118, 128, 256]]
        for p in range(4):
            for trait_idx in to_play[p]:
                lbox_deck[0].selection_set(deck_filtered_idx.index(trait_idx))
                btn_play_trait(p)

                # attach to host if neccessary
                if traits_df.loc[trait_idx].attachment == 1:
                    host_idx = rules_at.filter_attachables(trait_idx, p)[0]

                    write_log(['attach_to', 'attached'], plr['name'][p].get(),
                              traits_df.loc[trait_idx].trait, trait_idx,
                              traits_df.loc[host_idx].trait, host_idx)

                    # set new attachment to status_row of host & update effects of attachment on host
                    status_df.loc[trait_idx, 'host'] = host_idx
                    status_df.loc[host_idx, 'attachment'] = trait_idx

                    # update scoring
                    update_all()

        for r in range(game['n_catastrophes']):
            c = np.random.randint(low=0, high=len(catastrophe['possible'][r]))
            catastrophe['cbox'][r].current(c)
            catastrophe['cbox'][r].event_generate("<<ComboboxSelected>>")

    print('___done___')


def switch(inp):
    global icons_onoff, music_onoff, points_onoff

    match inp:
        case 'icons':
            if icons_onoff == 'off':
                icons_onoff = 'on'
                lbl_icons_switch[0].configure(image=images['icons_on'])
                write_log(['icons', 'on'])
            elif icons_onoff == 'on':
                icons_onoff = 'full'
                lbl_icons_switch[0].configure(image=images['icons_full'])
                write_log(['icons', 'full'])
            elif icons_onoff == 'full':
                icons_onoff = 'off'
                lbl_icons_switch[0].configure(image=images['icons_off'])
                write_log(['icons', 'off'])

            switch('show_icons')
            # update all trait piles
            for p in range(game['n_player']):
                if frame_trait_pile[p] is not None:
                    create_trait_pile(frame_trait_pile[p], p)

        case 'show_icons':
            if icons_onoff == 'on':
                show_icons['color'] = True        # default: True
                show_icons['face'] = True         # default: True
                show_icons['collection'] = False  # default: False
                show_icons['dominant'] = False    # default: False
                show_icons['action'] = False      # default: False
                show_icons['drops'] = False       # default: False
                show_icons['gene_pool'] = False   # default: False
                show_icons['worlds_end'] = False  # default: False
                show_icons['effectless'] = False  # default: False
                show_icons['attachment'] = False  # default: False
            elif icons_onoff == 'full':
                show_icons['color'] = True          # default: True
                show_icons['face'] = True           # default: True
                show_icons['collection'] = True     # default: False
                show_icons['dominant'] = True       # default: False
                show_icons['action'] = True         # default: False
                show_icons['drops'] = True          # default: False
                show_icons['gene_pool'] = True      # default: False
                show_icons['worlds_end'] = True     # default: False
                show_icons['effectless'] = True     # default: False
                show_icons['attachment'] = True     # default: False
            elif icons_onoff == 'off':
                show_icons['color'] = False       # default: True
                show_icons['face'] = False        # default: True
                show_icons['collection'] = False  # default: False
                show_icons['dominant'] = False    # default: False
                show_icons['action'] = False      # default: False
                show_icons['drops'] = False       # default: False
                show_icons['gene_pool'] = False   # default: False
                show_icons['worlds_end'] = False  # default: False
                show_icons['effectless'] = False  # default: False
                show_icons['attachment'] = False  # default: False

        case 'music':
            if music_onoff == 'off':
                music_onoff = 'on'
                lbl_music_switch[0].configure(image=images['note_on'])
                write_log(['music', 'on'])
            else:
                music_onoff = 'off'
                lbl_music_switch[0].configure(image=images['note_off'])
                write_log(['music', 'off'])

        case 'points':
            if points_onoff == 'off':
                points_onoff = 'on'
                lbl_points_switch[0].configure(image=images['points_123'])
                write_log(['music', 'on'])
                update_scoring()
            else:
                points_onoff = 'off'
                lbl_points_switch[0].configure(image=images['question_mark'])
                write_log(['music', 'off'])
                update_scoring()


def play_sound(trait):
    if music_onoff == 'on':
        if trait.replace(' ', '_').lower() in sounds:
            sounds[trait.replace(' ', '_').lower()].play()
            write_log(['music', 'play'], trait)


def btn_clear_trait_search():
    str_trait_search.set("")
    deck_filtered_idx.clear()
    deck_filtered_idx.extend(deck)
    deck_filtered_str.set(traits_df.loc[deck_filtered_idx].trait.values.tolist())
    ent_trait_search[0].focus_set()
    lbox_deck[0].selection_clear(0, tk.END)
    lbox_deck[0].see(0)


def btn_worlds_end_apply():
    print('_____ WE _____')


def btn_worlds_end_select():
    # do nothing if no catastrophy selected
    if worlds_end['cbox'].current() == 0:
        worlds_end['btn'].configure(state="disabled", style="disabled.TButton")
        write_log(['worlds_end', 'error_no_event'])
        return

    # print log
    write_log(['worlds_end', 'select'], worlds_end['played'].get())

    # enable WE_button
    worlds_end['btn'].configure(state="normal", style="TButton")


def btn_play_catastrophe(event, c):
    # get played catastrophe
    cbox_idx = event.widget.current()   # selected item_idx in combobox
    played_str = event.widget.get()
    played_previously = catastrophe['played'][c]
    if cbox_idx > 0:
        played_idx = catastrophe['possible'][c][cbox_idx-1]

    # return, if no catastrophe was selected
    if cbox_idx == 0:
        # OR -> force to keep previous selection -> NO WAY BACK
        if played_previously is None:
            write_log(['catastrophe', 'error_no_catastrophe'], c+1)
        else:
            old_cbox_idx = catastrophe['possible'][c].index(played_previously) + 1
            catastrophe['cbox'][c].current(old_cbox_idx)
            write_log(['catastrophe', 'error_keep_catastrophe'], c+1)
        return

    # return, if same catastrophe selected
    if played_previously == played_idx:
        write_log(['catastrophe', 'error_same_catastrophe'], c+1, played_str)
        return

    # print log
    write_log(['catastrophe', 'catastrophe'], c+1, played_str, played_idx)

    # set played catastrophe
    catastrophe['played'][c] = played_idx

    # update possible catastrophes for other catastrophes
    # for i in range(1, game['n_catastrophes']):
    for i in [i for i in range(game['n_catastrophes']) if i != c]:
        # begin with ALL possible catastrophes
        catastrophe['possible'][i] = catastrophes_df.index.tolist()

        # remove other catastrophes from possible ones
        for j in [j for j in range(game['n_catastrophes']) if j != i]:
            # only, if j'th catastrophe was played already
            if catastrophe['played'][j] is not None:
                # remove from list of possibles
                catastrophe['possible'][i].remove(catastrophe['played'][j])

        # create list of catastrophe names & update combobox
        pos_cat_values = [" catastrophe {}...".format(i+1)] \
            + catastrophes_df.loc[catastrophe['possible'][i]].name.values.tolist()
        catastrophe['cbox'][i].configure(values=pos_cat_values)

    # enable next catastrophe
    if c < game['n_catastrophes']-1:
        catastrophe['cbox'][c+1].configure(state="readonly")
    else:
        worlds_end['cbox'].configure(state="readonly")

    # update worlds end combobox
    played_catastrophes = [catastrophes_df.loc[catastrophe['played'][i], "name"]
                           for i in range(game['n_catastrophes'])
                           if catastrophe['played'][i] is not None]
    worlds_end['cbox']['values'] = [" select world's end ..."] + played_catastrophes

    # --- if DENIAL is out there, save first catastrophe he sees ---
    denial_idx = status_df.index[status_df.trait == 'Denial'].tolist()[0]
    if (any(denial_idx in tp for tp in plr['trait_pile'])
            and status_df.loc[denial_idx].effects == 'none'):
        status_df.loc[denial_idx, "effects"] = played_str

    # update first player
    n_cat = sum(i is not None for i in catastrophe['played'])
    game['first_player'] = game['first_player_start'] + n_cat
    if game['first_player'] > game['n_player']-1:
        game['first_player'] = game['first_player'] - game['n_player']
    write_log(['catastrophe', 'first_player'], plr['name'][game['first_player']].get(), n_cat)

    # update label_style
    for p in range(game['n_player']):
        tmp_frame = frame_player[p].winfo_children()
        lbl1 = frame_player[p].nametowidget(str(tmp_frame[0]) + '.!label')
        lbl2 = frame_player[p].nametowidget(str(tmp_frame[0]) + '.!label2')
        lbl1.configure(style="n_traitsFirstPlayer.TLabel"
                       if game['first_player'] == p else "n_traits.TLabel")
        lbl2.configure(style="n_traitsFirstPlayer.TLabel"
                       if game['first_player'] == p else "n_traits.TLabel")

    # update
    update_all()


def btn_traits_world_end(from_, trait_idx, event):
    # get trait & its WE effect
    # trait = traits_df.loc[trait_idx].trait
    effect = event.widget.get()
    effect_idx = event.widget.current()

    # print log
    if effect_idx == 0:
        write_log(['traits_WE', 'reset'], traits_df.loc[trait_idx].trait, trait_idx)
    else:
        write_log(['traits_WE', 'set'], traits_df.loc[trait_idx].trait, trait_idx, effect)

    # reverse traits_WE-effects, if it is changed, therefore check if WE-effect was selected
    # previously & if its different than the current, reset old effect
    old_effect = status_df.loc[trait_idx].traits_WE
    if old_effect != 'none' and old_effect != effect:
        # loop every trait in this trait pile
        for trait in plr['trait_pile'][from_]:
            # skip if its current worlds-end-trait
            if trait == trait_idx:
                continue

            # get current status before reseting
            prev_drops = status_df.loc[trait].drops
            prev_host = status_df.loc[trait].host
            prev_attachment = status_df.loc[trait].attachment
            prev_traits_WE = status_df.loc[trait].traits_WE

            # reset trait
            update_traits_current_status('reset', trait, [])

            # redo attachment effects
            if prev_attachment != 'none':
                update_traits_current_status('attachment', trait, prev_attachment)

            # restore host in attachment
            status_df.loc[trait, 'cur_host'] = prev_host

            # restore cur_drop points
            status_df.loc[trait, 'cur_drops'] = prev_drops

            # redo worlds_end effects
            if prev_traits_WE != 'none':
                status_df.loc[trait, 'cur_worlds_end_trait'] = prev_traits_WE
                update_traits_current_status('worlds_end', trait, plr['trait_pile'][from_])

    # set traits_WE-effect to status_df of trait
    if effect_idx == 0:
        status_df.loc[trait_idx, 'traits_WE'] = 'none'
    else:
        status_df.loc[trait_idx, 'traits_WE'] = effect

    # apply traits_WE-effects and update status of traits in this trait pile
    rules_tr.assign_traits_WE_effects(trait_idx, plr['trait_pile'][from_])

    # update
    update_all()


def btn_remove_trait(from_, where_to):
    # get card & its attachment
    trait_idx = plr['trait_selected'][from_].get()
    if not np.isnan(trait_idx):
        attachment = status_df.loc[trait_idx].attachment

    # return, if no trait selected
    if np.isnan(trait_idx):
        write_log(['remove', 'error_no_trait'])
        return

    # print log
    if where_to == 'hand':
        write_log(['remove', 'hand'], plr['name'][from_].get(), traits_df.loc[trait_idx].trait, trait_idx)
    else:
        write_log(['remove', 'discard'], plr['name'][from_].get(), traits_df.loc[trait_idx].trait, trait_idx)
    if attachment != 'none':
        write_log(['remove', 'error_discard_attachment'], traits_df.loc[attachment].trait, attachment)

    # remove card(s) from player & clear player trait selection
    plr['trait_pile'][from_].remove(trait_idx)
    if attachment != 'none':
        plr['trait_pile'][from_].remove(attachment)
    plr['trait_selected'][from_].set(np.nan)

    # add to deck traits & update deck_listbox
    bisect.insort_left(deck, trait_idx)
    if attachment != 'none':
        bisect.insort_left(deck, attachment)
    search_trait_in_list(str_trait_search)  # keep current str in search_entry

    # check, if this trait has a special "remove-rule", which may be needed for "status_updating"
    remove_rule = rules_re.check_trait(trait_idx, from_, where_to)

    # reset current status of card(s)
    update_traits_current_status('reset', trait_idx, remove_rule)
    if attachment != 'none':
        update_traits_current_status('reset', attachment, [])

    # update
    update_all()


def btn_move_trait(from_, cbox_move_to):
    # get card, its attachment & target
    trait_idx = plr['trait_selected'][from_].get()
    if not np.isnan(trait_idx):
        attachment = status_df.loc[trait_idx].attachment
    cbox_str = cbox_move_to.get().split()
    if cbox_str[0] != 'move':
        to = cfg["names"].index(cbox_str[-1])

    # return, if no target selected
    if cbox_move_to.current() == 0:
        cbox_move_to.current(0)
        write_log(['move', 'error_move_to'])
        return

    # return, if no trait selected
    if np.isnan(trait_idx):
        cbox_move_to.current(0)
        write_log(['move', 'error_no_trait'])
        return

    # return, if from == to
    if from_ == to:
        cbox_move_to.current(0)
        write_log(['move', 'error_source_target'])
        return

    # print log
    add_txt = "(and its attachment '{}' (id:{}))".format(traits_df.loc[attachment].trait, attachment) \
        if attachment != 'none' else ''
    write_log(['move', 'move_to'],
              traits_df.loc[trait_idx].trait, trait_idx, add_txt, plr['name'][from_].get(), plr['name'][to].get())

    # remove traits(s) from 'giving' player - update trait_pile - check remove_rules - clear trait selection
    plr['trait_pile'][from_].remove(trait_idx)
    if attachment != 'none':
        plr['trait_pile'][from_].remove(attachment)
    create_trait_pile(frame_trait_pile[from_], from_)
    rules_re.check_trait(trait_idx, from_, 'different_trait_pile')
    plr['trait_selected'][from_].set(np.nan)

    # add to 'receiving' players traits
    bisect.insort_left(plr['trait_pile'][to], trait_idx)
    if attachment != 'none':
        bisect.insort_left(plr['trait_pile'][to], attachment)

    # clear combobox
    cbox_move_to.current(0)

    # update
    update_all()


def btn_attach_to(from_, attachment_idx, event, possible_hosts):
    # get host_data from event_data
    host = event.widget.get()
    host_idx = possible_hosts[event.widget.current()]
    attachment = traits_df.loc[attachment_idx].trait

    # return, if clicked on current host
    old_host_idx = status_df[status_df['attachment'] == attachment_idx].index.values.tolist()
    if host_idx in old_host_idx:
        write_log(['attach_to', 'error_own_host'])
        return

    # print log
    if host == ' ... ':
        write_log(['attach_to', 'detached'], attachment, attachment_idx)
    else:
        write_log(['attach_to', 'attached'],
                  plr['name'][from_].get(), attachment, attachment_idx, host, host_idx)

    # update old_host, where attachment was removed from
    if old_host_idx:
        write_log(['attach_to', 'change_host'], traits_df.loc[old_host_idx[0]].trait, old_host_idx[0])
        update_traits_current_status('reset', old_host_idx[0], [])

    # check if attachment is set back to "..." (idx=0)
    if event.widget.current() == 0:
        # reset host='none' to status_row of attachment
        status_df.loc[attachment_idx, 'host'] = 'none'
    else:
        # update status of attachment/host - saving idx's of each other
        status_df.loc[attachment_idx, 'host'] = host_idx
        status_df.loc[host_idx, 'attachment'] = attachment_idx

    # update
    update_all()


def btn_play_trait(to):
    # return, if no trait selected
    if not lbox_deck[0].curselection():
        write_log(['play', 'error_no_trait'])
        return 0

    # get card
    trait_idx = deck_filtered_idx[lbox_deck[0].curselection()[0]]
    trait = traits_df.loc[trait_idx].trait

    # return, if any trait specific requirements are not met
    if rules_pl.check_requirement(trait_idx, to):
        return 0

    # return, if player already has two dominants
    if traits_df.loc[trait_idx].dominant == 1:
        if sum([1 for t in plr['trait_pile'][to] if traits_df.loc[t].dominant == 1]) >= 2:
            # check if HEROIC is born during 'Birth of a Hero'
            heroic_idx = traits_df.index[traits_df.trait == 'Heroic'].tolist()[0]
            is_born = status_df.loc[heroic_idx, 'effects']

            # no hero, then return
            if trait_idx == heroic_idx and is_born:
                write_log(['play', 'heroic'])
            else:
                write_log(['play', 'error_2dominants'])
                return 0

    # return, if attachment does not have any trait to attach to
    if traits_df.loc[trait_idx].attachment == 1:
        attachables = rules_at.filter_attachables(trait_idx, to)
        if len(attachables) == 0:
            write_log(['play', 'error_no_attachables'])
            return 0

    # print log
    write_log(['play', 'play'], plr['name'][to].get(), trait, trait_idx)

    # check for rules/effects to apply when playing this trait
    rules_pl.play_effect(trait_idx, to)

    # add to players traits & update trait_pile
    bisect.insort_left(plr['trait_pile'][to], trait_idx)

    # remove from deck & update deck_listbox
    deck.remove(trait_idx)
    btn_clear_trait_search()

    # play sound bites
    play_sound(trait)

    # update
    update_all()

    return 1


def update_manual_we(event, p):
    value = event.widget.get()

    # check if input is numeric
    if (value.isnumeric() or (len(value) > 1 and value.lstrip('-').isnumeric())):
        # check limit of (hard-coded) 20
        if int(value) > 20:
            value = '20'
            plr['WE_effect'][p].set(value)
        if int(value) < -20:
            value = '-20'
            plr['WE_effect'][p].set(value)

        # update scoring
        update_scoring()

        # update this players trait pile
        create_trait_pile(frame_trait_pile[p], p)


def update_manual_drops(event, trait, p, change):
    cur_value = event.widget.get()

    # check, if spinbox is in initial state
    if cur_value == '-':
        cur_value = '0'

    # change value according to button
    if change == '+':
        value = int(cur_value) + 1
    else:
        value = int(cur_value) - 1

    # save value in status_df
    status_df.loc[trait, 'drops'] = value

    # print log
    write_log(['scoring', 'manual_drops'], traits_df.iloc[trait].trait, trait, value)

    # update scoring
    update_scoring()

    # update this players trait pile
    create_trait_pile(frame_trait_pile[p], p)

    # focus back to search field
    ent_trait_search[0].focus_set()


def update_traits_current_status(todo, *args):
    # space for various effects which may affect traits in certain situations (like Neoteny...)
    match todo:
        # 'reset' routine to reset traits status_df_row to initial state
        case 'reset':
            trait = args[0]
            reset_rule = args[-1]

            # backup current state
            bkp = status_df.loc[trait].copy()

            # reset trait
            true_color = traits_df.loc[trait].color
            true_face = traits_df.loc[trait].face

            status_df.loc[trait, 'color'] = true_color
            status_df.loc[trait, 'face'] = true_face
            status_df.loc[trait, 'drops'] = np.nan
            status_df.loc[trait, 'host'] = 'none'
            status_df.loc[trait, 'attachment'] = 'none'
            status_df.loc[trait, 'inactive'] = False
            status_df.loc[trait, 'no_remove'] = False
            status_df.loc[trait, 'no_discard'] = False
            status_df.loc[trait, 'no_steal'] = False
            status_df.loc[trait, 'no_swap'] = False
            status_df.loc[trait, 'effects'] = 'none'
            status_df.loc[trait, 'effects_attachment'] = 'none'
            status_df.loc[trait, 'effects_traits_WE'] = 'none'
            status_df.loc[trait, 'effects_WE'] = 'none'
            status_df.loc[trait, 'traits_WE'] = 'none'
            status_df.loc[trait, 'we_effect'] = 'none'

            # apply rule after resetting
            match reset_rule:
                case 'keep_trait_effect':
                    status_df.loc[trait, 'effects'] = bkp.effects

            # print log
            write_log(['update_trait_status', 'reset'], traits_df.loc[trait].trait)

        # Neoteny-Checkbox is clicked somewhere
        case 'neoteny':
            neoteny_idx = traits_df.index[traits_df.trait == 'Neoteny'].tolist()[0]
            p = args[0]

            # set other player to 0
            for i in range(game['n_player']):
                if i != p:
                    neoteny_checkbutton[i].set(0)

            # update 'cur_effect'
            if not any([i.get() for i in neoteny_checkbutton]):
                status_df.loc[neoteny_idx, 'effects'] = 'none'
                write_log(['update_trait_status', 'neoteny_no_one'])
            else:
                status_df.loc[neoteny_idx, 'effects'] = str(p)
                write_log(['update_trait_status', 'neoteny_that_one'], plr['name'][p].get())

            # update
            update_all()


def update_scoring():
    for p in range(game['n_player']):
        # get cards
        trait_pile = plr['trait_pile'][p]

        # calculate world's end points
        p_worlds_end = rules_we.worlds_end(traits_df, worlds_end['played'].get(), plr['trait_pile'],
                                           p, plr['genes'], plr['WE_effect'])

        # calculate face value
        p_face = int(sum([status_df.loc[trait_idx].face for trait_idx in trait_pile
                          if not isinstance(status_df.loc[trait_idx].face, str)]))

        # calculate drops points
        p_drop = rules_dr.drop_points(p)

        # calculate drops points
        p_MOL = 0
        for x in [x.get() for x in plr['MOL'][p]]:
            if x.isnumeric():
                p_MOL += int(x)

        # calculate total score
        total = p_face + p_drop + p_worlds_end + p_MOL

        # update points
        if points_onoff == 'on':
            plr['points'][p]['face'].set(p_face)
            plr['points'][p]['drops'].set(p_drop)
            plr['points'][p]['worlds_end'].set(p_worlds_end)
            plr['points'][p]['MOL'].set(p_MOL)
            plr['points'][p]['total'].set(total)
        else:
            plr['points'][p]['face'].set('**')
            plr['points'][p]['drops'].set('**')
            plr['points'][p]['worlds_end'].set('**')
            plr['points'][p]['MOL'].set('**')
            plr['points'][p]['total'].set('**')

        # print log
        write_log(['scoring', 'update'], plr['name'][p].get(), p_face, p_drop, p_worlds_end, p_MOL, total)


def update_genes():
    # init vars
    diff_genes = [0] * game['n_player']

    # loop players and calculate +- genes of all played traits --------------------------
    for p in range(game['n_player']):
        # loop traits in trait_pile
        for trait_idx in plr['trait_pile'][p]:
            # get gene effect of this card
            who = traits_df.loc[trait_idx].gene_pool_target
            effect = traits_df.loc[trait_idx].gene_pool_effect
            rule = traits_df.loc[trait_idx].gene_pool_rule

            # if there is an effect and no restrictions
            if isinstance(who, str) and not isinstance(rule, str):
                match who:
                    case 'all':
                        diff_genes = [i + int(effect) for i in diff_genes]
                    case 'self':
                        diff_genes[p] += int(effect)
                    case 'opponents':
                        diff_genes = [g+int(effect)
                                      if i != p else g
                                      for i, g in enumerate(diff_genes)]

                # print log
                write_log(['genes', 'trait'],
                          plr['name'][p].get(), traits_df.loc[trait_idx].trait, int(effect), who, diff_genes)

    # check for special effects by specific traits --------------------------------------
    # ----- Denial --------------
    dnl_idx = status_df.index[status_df.trait == 'Denial'].tolist()[0]
    dnl_effect = status_df.loc[dnl_idx].effects
    if (dnl_effect != 'none'):
        # find player
        dnl_in = [dnl_idx in tp for tp in plr['trait_pile']]
        dnl_p = dnl_in.index(True)

        if dnl_effect == 'The Four Horsemen':
            # write log
            write_log(['genes', 'denial_t4h'], dnl_idx, plr['name'][dnl_p].get(), dnl_effect, diff_genes)
        else:
            # reverse effect
            reverse_effect = catastrophes_df[catastrophes_df.name == dnl_effect].gene_pool.values[0] * -1
            diff_genes[dnl_p] += int(reverse_effect)

            # write log
            write_log(['genes', 'denial'], dnl_idx, plr['name'][dnl_p].get(), dnl_effect, diff_genes)

    # ----- Sleepy --------------
    slp_idx = traits_df.index[traits_df.trait == 'Sleepy'].tolist()[0]
    if any(slp_idx in tp for tp in plr['trait_pile']):
        slp_eff = [i.get() for i in sleepy_spinbox]
        diff_genes = [diff_genes[x]+slp_eff[x] for x in range(len(diff_genes))]
        if any(slp_eff):
            p = [i for i, e in enumerate(slp_eff) if e != 0]
            write_log(['genes', 'sleepy'], plr['name'][p[0]].get(), slp_eff[p[0]], diff_genes)
    else:  # sleepy in no trait pile -> reset values
        for i in range(game['n_player']):
            sleepy_spinbox[i].set(0)

    # ----- Spores ---------------
    sprs_idx = traits_df.index[traits_df.trait == 'Spores'].tolist()[0]
    sprs_eff = status_df.loc[sprs_idx].effects
    if sprs_eff != 'none':
        # check if more players are affected
        if '_' in sprs_eff:
            sprs_eff = sprs_eff.split('_')

        # apply effects
        for eff in sprs_eff:
            p = int(eff)
            diff_genes[p] += 1

            # print log
            write_log(['genes', 'spores'], sprs_idx, plr['name'][p].get(), diff_genes)

    # check what catastrophes were played alread ---------------------------------------
    for c in range(game['n_catastrophes']):
        # get card & effect
        c_idx = catastrophe['played'][c]

        # check if catastrophy was played
        if c_idx is not None:
            c_str = catastrophes_df.loc[c_idx, "name"]
            # get effect and apply it
            effect = int(catastrophes_df.loc[c_idx].gene_pool)
            diff_genes = [i + effect for i in diff_genes]

            # print log
            write_log(['genes', 'catastrophe'], c_str, effect, diff_genes)

    # update gene values ----------------------------------------------------------------
    for p in range(game['n_player']):
        new_gp = game['n_genes'] + diff_genes[p]
        if new_gp > 8:
            plr['genes'][p].set(8)
        elif new_gp < 1:
            plr['genes'][p].set(1)
        else:
            plr['genes'][p].set(new_gp)

    # print log - if genes are effected
    if any(i > 0 for i in diff_genes):
        write_log(['genes', 'total_effect'],
                  diff_genes, [plr['genes'][i].get() for i in range(game['n_player'])])


def update_stars():
    # loop players
    for p in range(game['n_player']):
        # number of dominant traits
        n_dominant = np.nansum([traits_df.loc[trait_idx].dominant for trait_idx in plr['trait_pile'][p]])

        # write log
        write_log(['stars', 'n'], plr['name'][p].get(), int(n_dominant))

        # check special cases
        Epic_idx = traits_df.index[traits_df.trait == 'Epic'].tolist()[0]
        if Epic_idx in plr['trait_pile'][p]:
            n_dominant = 2
            write_log(['stars', 'epic'])

        # find label widgets
        tmp_frame = frame_player[p].winfo_children()
        lbl1 = frame_player[p].nametowidget(str(tmp_frame[0]) + '.!label3')
        lbl2 = frame_player[p].nametowidget(str(tmp_frame[0]) + '.!label4')

        # edit images
        lbl1.configure(image=images['no_star'])
        lbl2.configure(image=images['no_star'])
        if n_dominant > 0:
            lbl1.configure(image=images['star'])
            if n_dominant == 2:
                lbl2.configure(image=images['star'])
            elif n_dominant == 3:
                lbl2.configure(image=images['heroic_star'])


def resolve_effects():
    # loop players
    for p in range(game['n_player']):
        # loop trait pile
        for trait_idx in plr['trait_pile'][p]:
            # 1: attachment effect
            rules_at.apply_effects(trait_idx)

            # 2: traits WE effect(s)

            # 3: worlds end effect


def update_all():
    # first, resolve all effects on traits
    resolve_effects()

    # update stuff
    update_stars()
    update_genes()
    update_scoring()

    # update all trait piles
    for p in range(game['n_player']):
        create_trait_pile(frame_trait_pile[p], p)

    # focus back to search field
    ent_trait_search[0].focus_set()


def search_trait_in_list(inp):
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

        # if only 1 pssibility left, select it automatically
        if (len(filtered_trait_idx) == 1 or
                (len(filtered_trait_idx) == 2 and filtered_trait_str[0] == filtered_trait_str[1])):
            lbox_deck[0].selection_clear(0, tk.END)
            lbox_deck[0].selection_set(0)
            lbox_deck[0].focus()
            lbox_deck[0].see(0)
            write_log(['select', 'deck'],
                      traits_df.loc[deck_filtered_idx[0]].trait,
                      deck_filtered_idx[0])


def create_trait_pile(frame_trait_overview, p):
    # first, clean up frame
    for w in frame_trait_overview.grid_slaves():
        w.grid_forget()

    # then, scan trait pile for any effects by any traits, like protecting other traits...
    rules_tr.permanent_effects(plr['trait_pile'][p])

    # then, update n_tp
    plr['n_tp'][p].set(get_sup(plr['trait_pile'][p]))

    # --- loop traits in trait pile ------------------------------------------------
    irow = -1
    for trait_idx in plr['trait_pile'][p]:
        # get trait name
        trait = traits_df.loc[trait_idx].trait

        # init some vars
        irow += 1
        ypad = (3, 0) if irow == 0 else 0

        # ----- radiobutton / label if attachment --------------------------------------------------
        if traits_df.loc[trait_idx].attachment == 1:
            lbl = tk.Label(frame_trait_overview,
                           text=" " + trait,
                           image=images["attachment"],
                           compound=tk.LEFT)
            lbl.grid(row=irow, column=0, padx=2, pady=ypad, sticky='nsw')

            # it also could be a DOMINANT
            if traits_df.loc[trait_idx].dominant == 1:
                lbl.config(fg=cfg["font_color_trait_pile_dominant"])

        elif traits_df.loc[trait_idx].dominant == 1:
            tk.Label(frame_trait_overview,
                     text=" " + trait,
                     image=images["dominant"],
                     compound=tk.LEFT,
                     fg=cfg["font_color_trait_pile_dominant"],
                     font="'' 14 bold"
                     ).grid(row=irow, column=0, padx=2, pady=ypad, sticky='nsw')
        else:
            tk.Radiobutton(frame_trait_overview,
                           text=" " + trait,
                           variable=plr['trait_selected'][p],
                           value=trait_idx,
                           command=lambda t_idx=trait_idx: write_log(['select', 'trait_pile'],
                                                                     plr['name'][p].get(),
                                                                     traits_df.loc[t_idx].trait,
                                                                     t_idx)
                           ).grid(row=irow, column=0, padx=3, pady=ypad, sticky='nsw')

        # ----- icons ------------------------------------------------------------------------------
        frame_pics = tk.Frame(frame_trait_overview)
        frame_pics.grid(row=irow, column=1, sticky='sw')
        icol = -1  # initialize column index which changes depending on card

        # _true_ color
        if show_icons['color']:
            icol += 1
            color = traits_df.loc[trait_idx].color
            cc = 'c' if 'colorless' in color.lower() else ''
            cb = 'b' if 'blue' in color.lower() else ''
            cg = 'g' if 'green' in color.lower() else ''
            cp = 'p' if 'purple' in color.lower() else ''
            cr = 'r' if 'red' in color.lower() else ''

            tk.Label(
                frame_pics,
                image=images[cc+cb+cg+cp+cr]
                ).grid(row=0, column=icol)

        # face
        if (show_icons['face'] and 'face' not in status_df.loc[trait_idx].we_effect.lower()):
            icol += 1
            face_value = traits_df.loc[trait_idx].face
            face_string = face_value if isinstance(face_value, str) else str(int(face_value))

            tk.Label(
                frame_pics,
                image=images[face_string]
                ).grid(row=0, column=icol)

        # collection
        if show_icons['collection']:
            icol += 1
            lbl_collection = tk.Label(
                frame_pics,
                image=images['no_star'],
                )
            lbl_collection.grid(row=0, column=icol)

            match traits_df.loc[trait_idx].game.lower():
                case 'classic':
                    lbl_collection['image'] = images['classic']
                case 'kickstarter':
                    lbl_collection['image'] = images['kickstarter']
                case 'techlings':
                    lbl_collection['image'] = images['techlings']
                case 'mythlings':
                    lbl_collection['image'] = images['mythlings']
                case 'dinolings':
                    lbl_collection['image'] = images['dinolings']
                case 'multi-color':
                    lbl_collection['image'] = images['multicolor']
                case 'overlush':
                    lbl_collection['image'] = images['overlush']

        # dominant
        if show_icons['dominant'] and traits_df.loc[trait_idx].dominant == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['dominant']
                ).grid(row=0, column=icol)

        # action
        if show_icons['action'] and traits_df.loc[trait_idx].action == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['action']
                ).grid(row=0, column=icol)

        # drops
        if show_icons['drops'] and traits_df.loc[trait_idx].drops == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['drops']
                ).grid(row=0, column=icol)

        # gene pool
        if show_icons['gene_pool'] and traits_df.loc[trait_idx].gene_pool == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['gene_pool']
                ).grid(row=0, column=icol)

        # worlds_end
        if show_icons['worlds_end'] and traits_df.loc[trait_idx].worlds_end == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['worlds_end']
                ).grid(row=0, column=icol)

        # effectless
        if show_icons['effectless'] and traits_df.loc[trait_idx].effectless == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['effectless']
                ).grid(row=0, column=icol)

        # attachment
        if show_icons['attachment'] and traits_df.loc[trait_idx].attachment == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['attachment']
                ).grid(row=0, column=icol)

        # add SEPERATOR after _true_ icons
        icol += 1
        ttk.Separator(frame_pics, orient='vertical'
                      ).grid(row=0, column=icol, padx=3, pady=3, sticky='ns')

        # ----- current drop/attachment effects  ---------------------------------------------------
        # *new* color ---------------------------
        cur_color = status_df.loc[trait_idx].color.lower()
        if cur_color != traits_df.loc[trait_idx].color.lower():
            icol += 1
            cc = 'c' if 'colorless' in cur_color.lower() else ''
            cb = 'b' if 'blue' in cur_color.lower() else ''
            cg = 'g' if 'green' in cur_color.lower() else ''
            cp = 'p' if 'purple' in cur_color.lower() else ''
            cr = 'r' if 'red' in cur_color.lower() else ''

            tk.Label(
                frame_pics,
                image=images[cc+cb+cg+cp+cr]
                ).grid(row=0, column=icol)

        # drop value ----------------------------
        cur_drops = status_df.loc[trait_idx].drops
        if traits_df.loc[trait_idx].drops == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['drops']
                ).grid(row=0, column=icol)

            if np.isnan(cur_drops):
                # add question mark as long as no drop value is calculated
                icol += 1
                tk.Label(
                    frame_pics,
                    image=images['question_mark']
                    ).grid(row=0, column=icol)
            else:
                # check if values are higher/lower than drop icons exist
                if int(cur_drops) > 20:
                    drop_string = '20+'
                elif int(cur_drops) < -20:
                    drop_string = '-20-'
                else:
                    drop_string = str(int(cur_drops))
                # add value icon
                icol += 1
                tk.Label(
                    frame_pics,
                    image=images[drop_string]
                    ).grid(row=0, column=icol)

        # has attachment ------------------------
        if status_df.loc[trait_idx].attachment != 'none':
            icol += 1
            tk.Label(
                frame_pics,
                image=images['attachment']
                ).grid(row=0, column=icol)

        # noFX ----------------------------------
        if status_df.loc[trait_idx].inactive:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noFX']
                ).grid(row=0, column=icol)

        # noRemove ------------------------------
        if status_df.loc[trait_idx].no_remove:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noRemove']
                ).grid(row=0, column=icol)

        # noDiscard -----------------------------
        if status_df.loc[trait_idx].no_discard:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noDiscard']
                ).grid(row=0, column=icol)

        # noSteal -------------------------------
        if status_df.loc[trait_idx].no_steal:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noSteal']
                ).grid(row=0, column=icol)

        # noSwap --------------------------------
        if status_df.loc[trait_idx].no_swap:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noSwap']
                ).grid(row=0, column=icol)

        # if WORLDS END effects this trait ------
        if status_df.loc[trait_idx].we_effect != 'none':
            icol += 1
            tk.Label(
                frame_pics,
                image=images['worlds_end']
                ).grid(row=0, column=icol)

            if 'face' in traits_df.loc[trait_idx].cur_worlds_end_effect.lower():
                icol += 1
                we_face_string = str(int(traits_df.loc[trait_idx].cur_face))
                tk.Label(
                    frame_pics,
                    image=images[we_face_string]
                    ).grid(row=0, column=icol)

            if 'inactive' in traits_df.loc[trait_idx].cur_worlds_end_effect.lower():
                icol += 1
                tk.Label(
                    frame_pics,
                    image=images['noFX']
                    ).grid(row=0, column=icol)

        # ----- SLEEPY may affect gene pool ?!?!  --------------------------------------------------
        if traits_df.loc[trait_idx].trait == 'Sleepy':
            irow += 1
            tk.Label(frame_trait_overview, text="gene effect:", fg='grey'
                     ).grid(row=irow, column=0, padx=(40, 0), sticky='e')

            # create combobox
            ttk.Spinbox(frame_trait_overview,
                        from_=-1, to=1, width=3, wrap=False,
                        textvariable=sleepy_spinbox[p],
                        command=lambda: update_all()
                        ).grid(row=irow, column=1, sticky='w')

        # ----- ATTACHMENT combobox if trait is attachment -----------------------------------------
        if traits_df.loc[trait_idx].attachment == 1:
            irow += 1
            tk.Label(frame_trait_overview, text="Attach to:", fg='grey'
                     ).grid(row=irow, column=0, padx=(40, 0), sticky='e')

            # filter only non-attachment-traits and check if this is already attached to a trait
            traits_filtered_idx = [None] + rules_at.filter_attachables(trait_idx, p)
            traits_filtered_str = [" ... "] + [traits_df.loc[idx].trait
                                               for idx in traits_filtered_idx if idx is not None]

            # create combobox
            cbox_attach_to = ttk.Combobox(
                frame_trait_overview,
                height=len(traits_filtered_str),
                values=traits_filtered_str,
                exportselection=0,
                state="readonly",
                width=10)
            cbox_attach_to.grid(row=irow, column=1, sticky='w')
            cbox_attach_to.bind("<<ComboboxSelected>>",
                                lambda e, t=trait_idx, idx=traits_filtered_idx:
                                    btn_attach_to(p, t, e, idx))

            # check if already attached to host
            if status_df.loc[trait_idx].host == 'none':
                cbox_attach_to.current(0)
            else:
                cur_host = status_df.loc[trait_idx].host
                cbox_attach_to.current(traits_filtered_idx.index(cur_host))

        # ----- WORLDS_END combobox if trait has worlds end effect ---------------------------------
        if isinstance(traits_df.loc[trait_idx].worlds_end_task, str):
            irow += 1
            tk.Label(frame_trait_overview, text="Worlds End:", fg='grey'
                     ).grid(row=irow, column=0, padx=(40, 0), sticky='e')

            # get task what to do at worlds end
            we_effect = rules_tr.traits_WE_tasks(trait_idx)

            # set state depending on 'played' catastrophes
            state = 'readonly' if sum(i is None for i in catastrophe['played']) == 0 else 'disabled'

            # create combobox
            cbox_attach_to = ttk.Combobox(
                frame_trait_overview,
                height=len(we_effect),
                values=we_effect,
                exportselection=0,
                state=state,
                width=11)
            cbox_attach_to.grid(row=irow, column=1, sticky='w')
            cbox_attach_to.bind(
               "<<ComboboxSelected>>", lambda e, t=trait_idx: btn_traits_world_end(p, t, e))

            # check if effect already selected
            if status_df.loc[trait_idx].traits_WE == 'none':
                cbox_attach_to.current(0)
            else:
                cur_effect = status_df.loc[trait_idx].traits_WE
                cbox_attach_to.current(we_effect.index(cur_effect))

        # ----- manual DROP points spinbox -----------------------------------------------------------
        cur_drop_eff = traits_df.loc[trait_idx].drop_effect
        if (isinstance(cur_drop_eff, str)
            and not isinstance(traits_df.loc[trait_idx].worlds_end_task, str)
            and ('own_hand' in traits_df.loc[trait_idx].drop_effect
                 or 'discarded' in traits_df.loc[trait_idx].drop_effect)):
            irow += 1
            tk.Label(frame_trait_overview, text="Drop of Life:", fg='grey'
                     ).grid(row=irow, column=0, padx=(40, 0), sticky='e')

            # set state depending on 'played' worlds end
            state = 'readonly' if worlds_end['played'].get() != " select world's end ..." else 'disabled'

            # create spinbox
            drop_sbox = ttk.Spinbox(
                frame_trait_overview,
                state=state,
                from_=-100,
                to=100,
                width=3,
                wrap=False)
            drop_sbox.grid(row=irow, column=1, sticky='w')
            drop_sbox.bind("<<Increment>>", lambda e, t=trait_idx: update_manual_drops(e, t, p, '+'))
            drop_sbox.bind("<<Decrement>>", lambda e, t=trait_idx: update_manual_drops(e, t, p, '-'))

            # fill entry, depending on drops_status
            if np.isnan(status_df.loc[trait_idx].drops):
                drop_sbox.set('-')
            else:
                dp = str(int(status_df.loc[trait_idx].drops))
                drop_sbox.set(dp)

    # *********** special, individual case *** !!! *************************************************
    # Some Drop-of-Life-Effects are affecting other players! hence, effects of these traits need to
    # be shown on each other players trait pile, allowing to enter individual drop values
    irow += 1
    ttk.Separator(frame_trait_overview, orient='horizontal'
                  ).grid(row=irow, column=0, columnspan=2, padx=5, pady=10, sticky='nesw')
    # call function to insert special-effects from various traits
    irow = rules_tp.special_trait_effects(frame_trait_overview, p, irow, images)

    # --- NEOTENY needs to stay here ---------------------------------------------------------------
    # --- because 'create_trait_pile' needs to be run once the checkbox is clicked -----------------
    neoteny_idx = traits_df.index[traits_df.trait == 'Neoteny'].tolist()[0]
    neoteny_effect = status_df.loc[neoteny_idx].effects
    if ("select world's end" not in worlds_end['played'].get()
            and all(neoteny_idx not in tp for tp in plr['trait_pile'])):
        # only if no one has it or this player has it
        if neoteny_effect == 'none' or neoteny_effect == str(p):
            # create separate frame for NEOTENY
            irow += 1
            frame_ntny = tk.Frame(frame_trait_overview)
            frame_ntny.grid(row=irow, column=0, columnspan=2, sticky='we')

            # add trait
            tk.Label(frame_ntny, text="NEOTENY", fg="#1C86EE", font='"" 14 bold'
                     ).grid(row=0, column=0, padx=(10, 0), sticky='en')
            # if is this hand
            if neoteny_checkbutton[p].get() == 1:
                ttk.Checkbutton(frame_ntny, variable=neoteny_checkbutton[p], text=' got it -> ',
                                # command=lambda: update_traits_current_status('neoteny', int(p))
                                command=lambda: update_traits_current_status('neoteny', p)
                                ).grid(row=0, column=1, padx=(0, 0), sticky='wns')
                ttk.Label(frame_ntny, image=images['drops']
                          ).grid(row=0, column=2, sticky='ns')
                tk.Label(frame_ntny, image=images['4']
                         ).grid(row=0, column=3, sticky='ns')
            # not in this hand
            else:
                ttk.Checkbutton(frame_ntny, variable=neoteny_checkbutton[p], text=' in my hand???',
                                command=lambda: update_traits_current_status('neoteny', p)
                                ).grid(row=0, column=1, padx=(0, 0), sticky='wns')

    # **********************************************************************************************
    # ------ worlds end -> manual entries ---------------------------------------------------------
    if "select world's end" not in worlds_end['played'].get():
        irow += 1
        ttk.Separator(frame_trait_overview, orient='horizontal'
                      ).grid(row=irow, column=0, columnspan=2, padx=5, pady=10, sticky='we')

        # get world's end name & index
        we = worlds_end['played'].get()
        we_idx = catastrophes_df[catastrophes_df['name'] == we].index.values[0]
        we_eff = catastrophes_df.loc[we_idx].worlds_end

        # create separate frame for WE_TITLE
        irow += 1
        frame_weA = tk.Frame(frame_trait_overview)
        frame_weA.grid(row=irow, column=0, columnspan=2, sticky='we')

        # add label & drop icon
        tk.Label(frame_weA,
                 image=images["catastrophe"],
                 ).grid(row=0, column=0, padx=(20, 0), sticky='e')
        tk.Label(frame_weA,
                 text=" " + we + " ",
                 fg="#FF3030",
                 font="'', 14"
                 ).grid(row=0, column=1, sticky='ns')
        tk.Label(frame_weA,
                 image=images["catastrophe"],
                 ).grid(row=0, column=2, padx=(0, 20), sticky='w')

        # create separate frame for WE_EFFECTS
        irow += 1
        frame_weB = tk.Frame(frame_trait_overview)
        frame_weB.grid(row=irow, column=0, columnspan=2, sticky='we')
        frame_weB.columnconfigure(0, weight=1)
        frame_weB.columnconfigure(1, weight=0)
        frame_weB.columnconfigure(2, weight=1)

        tk.Label(frame_weB, text=">>>").grid(row=0, column=0, sticky='e')
        tk.Label(frame_weB, text="<<<").grid(row=0, column=2, sticky='w')

        if isinstance(we_eff, str) and ('hand' in we_eff or 'draw' in we_eff):
            we_entry = ttk.Entry(frame_weB,
                                 textvariable=plr['WE_effect'][p],
                                 justify=tk.CENTER,
                                 width=3)
            we_entry.grid(row=0, column=1)
            we_entry.bind("<KeyRelease>", lambda e: update_manual_we(e, p))
        else:
            we_points = str(plr['points'][p]['worlds_end'].get())
            tk.Label(frame_weB, image=images[we_points],
                     ).grid(row=0, column=1, sticky='w')


def create_player_frame(p):
    border = cfg["color_frame_width"]

    frame = tk.Frame(frame_playground, bg=cfg["player_frame_color"])
    frame.columnconfigure(0, weight=1)  # stretch sub_frames to playground (=1!)
    frame.rowconfigure(1, weight=1)  # stretch trait-pile to bottom of playground
    # frame.rowconfigure(2, weight=1)  # MOL
    frame.grid(column=p, row=0, padx=5, pady=5, sticky="nesw")  # or use nsw for non-x-streched frames!

    # ----- name + overview current points ---------------------------------------------------------
    frame_points = tk.Frame(frame)
    frame_points.grid(row=0, column=0, padx=border, pady=border, ipady=3, sticky="nesw")
    frame_points.columnconfigure(0, weight=1)
    frame_points.columnconfigure(1, weight=1)
    frame_points.columnconfigure(2, weight=1)
    frame_points.columnconfigure(3, weight=1)
    frame_points.columnconfigure(4, weight=3)
    frame_points.columnconfigure(5, weight=1)
    frame_points.columnconfigure(6, weight=1)

    # name
    ttk.Label(frame_points, textvariable=plr['n_tp'][p],
              style="n_traitsFirstPlayer.TLabel" if game['first_player'] == p else "n_traits.TLabel"
              ).grid(row=0, column=0, padx=5, pady=(5, 0), columnspan=1, sticky='ns')
    ttk.Label(frame_points, textvariable=plr['name'][p],
              style="nameFirstPlayer.TLabel" if game['first_player'] == p else "name.TLabel"
              ).grid(row=0, column=1, padx=5, pady=(5, 0), columnspan=4, sticky='ns')

    # stars
    ttk.Label(frame_points, image=images['no_star']
              ).grid(row=0, column=5, padx=0, pady=0, sticky="nes")
    ttk.Label(frame_points, image=images['no_star']
              ).grid(row=0, column=6, padx=0, pady=0, sticky="nsw")

    # single points
    ttk.Label(frame_points, image=images['blank_sb']
              ).grid(row=1, column=0, sticky="se")
    ttk.Label(frame_points, image=images['drops_sb']
              ).grid(row=1, column=2, sticky="se")
    ttk.Label(frame_points, image=images['worlds_end_sb']
              ).grid(row=2, column=0, sticky="e")
    ttk.Label(frame_points, image=images['MOL_sb']
              ).grid(row=2, column=2, sticky="e")

    ttk.Label(frame_points, textvariable=plr['points'][p]['face'], style="points.TLabel"
              ).grid(row=1, column=1, sticky="sw")
    ttk.Label(frame_points, textvariable=plr['points'][p]['drops'], style="points.TLabel"
              ).grid(row=1, column=3, sticky="sw")
    ttk.Label(frame_points, textvariable=plr['points'][p]['worlds_end'], style="points.TLabel"
              ).grid(row=2, column=1, sticky="w")
    ttk.Label(frame_points, textvariable=plr['points'][p]['MOL'], style="points.TLabel"
              ).grid(row=2, column=3, sticky="w")

    # total points
    ttk.Label(frame_points, textvariable=plr['points'][p]['total'], style="total.TLabel"
              ).grid(row=1, column=4, rowspan=2, padx=0, pady=0, sticky='ns')

    # gene pool
    ttk.Label(frame_points, text="gene pool"
              ).grid(row=1, column=5, columnspan=2, padx=0, pady=0, sticky='s')

    ttk.Label(frame_points, textvariable=plr['genes'][p], style="genes.TLabel"
              ).grid(row=2, column=5, columnspan=2, padx=0, pady=0, sticky='n')

    # ----- gaming ares ------------------------------------------------------------------
    frame_traits = tk.Frame(frame)
    frame_traits.grid(row=1, column=0, padx=border, pady=(0, border), sticky="nesw")
    frame_traits.rowconfigure(2, weight=1)
    frame_traits.columnconfigure(0, weight=1)  # for left button under trait-pile
    frame_traits.columnconfigure(1, weight=1)  # for middle button under trait-pile
    frame_traits.columnconfigure(2, weight=1)  # for right button under trait-pile

    # action buttons -----------------
    cbox_move_to = ttk.Combobox(
        frame_traits,
        height=game['n_player']+1,
        values=[" move to ..."] + ['p' + str(i+1) + ': ' + j.get()
                                   for i, j in enumerate(plr['name'])
                                   if i != p],
        exportselection=0,
        state="readonly",
        width=6,
        style="move.TCombobox")
    cbox_move_to.grid(row=0, column=0, pady=(border, 0), sticky='ne')
    cbox_move_to.current(0)
    cbox_move_to.bind(
        "<<ComboboxSelected>>", lambda e: btn_move_trait(p, cbox_move_to))

    ttk.Button(frame_traits, text="to hand", width=5,
               command=partial(btn_remove_trait, p, 'hand')
               ).grid(row=0, column=1, pady=(border, 0), sticky='n')

    ttk.Button(frame_traits, text="discard", width=5,
               command=partial(btn_remove_trait, p, 'discard')
               ).grid(row=0, column=2, pady=(border, 0), sticky='nw')

    ttk.Separator(
        frame_traits, orient='horizontal'
        ).grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='we')

    # ----- trait pile ---------------
    frame_trait_pile[p] = tk.Frame(frame_traits)
    frame_trait_pile[p].grid(row=2, column=0, columnspan=3, sticky='nesw', padx=border, pady=border)
    frame_trait_pile[p].columnconfigure(1, weight=1)
    create_trait_pile(frame_trait_pile[p], p)

    # ----- Meaning of Life ------------------------------------------------------------------------
    frame_MOL = tk.Frame(frame)
    frame_MOL.grid(row=2, column=0, padx=border, pady=(0, border), sticky="nesw")

    ttk.Label(frame_MOL, text="Meaning of Life", font="'' 18"
              ).grid(row=0, column=0, padx=5, columnspan=2*game['n_MOLs'], sticky='ns')

    for m in range(game['n_MOLs']):
        frame_MOL.columnconfigure(2*m, weight=1)
        frame_MOL.columnconfigure(2*m+1, weight=1)

        ttk.Label(frame_MOL,
                  text="MOL #{}:".format(m+1)
                  ).grid(row=1, column=2*m, sticky='e')
        MOL_ent = ttk.Entry(frame_MOL,
                            width=4,
                            textvariable=plr['MOL'][p][m])
        MOL_ent.grid(row=1, column=2*m+1, sticky='w')
        MOL_ent.bind("<KeyRelease>", lambda e: update_scoring())
    return frame


def create_name_entries(frame_menu_names):
    # forget all previous widgets
    for w in frame_menu_names.grid_slaves():
        w.grid_forget()

    # note to keep order
    ttk.Label(frame_menu_names, text="important:", font="'' 12 underline"
              ).grid(row=0, column=0, columnspan=1, pady=(0, 5), sticky='e')
    ttk.Label(frame_menu_names, text="keep order", font="'' 12"
              ).grid(row=0, column=1, columnspan=2, pady=(0, 5), sticky='w')

    # fix 1st player radiobutton if outside
    if options['first_player'].get() > (options['n_player'].get()-1):
        options['first_player'].set(options['n_player'].get()-1)

    # name entries ---
    for i in range(options['n_player'].get()):
        ttk.Label(frame_menu_names, text="player {}: ".format(i+1)
                  ).grid(row=i+1, column=0, sticky='e')
        ttk.Entry(frame_menu_names, textvariable=options['names'][i], width=6
                  ).grid(row=i+1, column=1, sticky='we')
        tk.Radiobutton(frame_menu_names,
                       variable=options['first_player'],
                       value=i
                       ).grid(row=i+1, column=2, sticky='e')


def create_menu_frame():
    border = cfg["color_frame_width"]

    frame_menu.columnconfigure(0, weight=1)
    frame_menu.rowconfigure(0, weight=1)
    frame_menu.rowconfigure(1, weight=1)
    frame_menu.rowconfigure(2, weight=4)
    frame_menu.rowconfigure(3, weight=1)

    # ----- frame 4 options ------------------------------------------------------------------------
    frame_menu_options = tk.Frame(frame_menu)
    frame_menu_options.grid(row=0, column=0, padx=border, pady=border, sticky="nesw")
    frame_menu_options.columnconfigure(0, weight=1)
    frame_menu_options.columnconfigure(1, weight=1)

    # title -----
    frame_options = tk.Frame(frame_menu_options)
    frame_options.grid(row=0, column=0, columnspan=2, sticky="nesw")
    frame_options.columnconfigure(0, weight=3)

    ttk.Label(
        frame_options,
        text="OPTIONS",
        font="'' 24"
        ).grid(row=0, column=0, pady=(5, 5))
    lbl_music_switch[0] = ttk.Label(
        frame_options,
        image=init_switch['music'],
        cursor="heart")
    lbl_music_switch[0].grid(row=0, column=1, padx=(0, 10))
    lbl_music_switch[0].bind("<Button-1>", lambda e: switch('music'))

    # nr players -----
    ttk.Label(
        frame_menu_options,
        text="# players: ",
    ).grid(row=1, column=0, sticky='e')
    ttk.Spinbox(
        frame_menu_options,
        from_=2,
        to=cfg["max_player"],
        width=3,
        textvariable=options['n_player'],
        wrap=False,
        command=lambda: create_name_entries(frame_menu_names),
    ).grid(row=1, column=1, sticky='w')

    # genes at beginning -----
    ttk.Label(
        frame_menu_options,
        text="gene pool: ",
    ).grid(row=2, column=0, sticky='e')
    ttk.Spinbox(
        frame_menu_options,
        from_=3,
        to=8,
        width=3,
        textvariable=options['n_genes'],
        wrap=False
    ).grid(row=2, column=1, sticky='w')

    # nr catastrophes -----
    ttk.Label(
        frame_menu_options,
        text="# catastrophes: ",
    ).grid(row=3, column=0, sticky='e')
    ttk.Spinbox(
        frame_menu_options,
        from_=2,
        to=6,
        width=3,
        textvariable=options['n_catastrophes'],
        wrap=False
    ).grid(row=3, column=1, sticky='w')

    # nr MOLs -----
    ttk.Label(
        frame_menu_options,
        text="# MOLs: ",
    ).grid(row=4, column=0, sticky='e')
    ttk.Spinbox(
        frame_menu_options,
        from_=0,
        to=4,
        width=3,
        textvariable=options['n_MOLs'],
        wrap=False
    ).grid(row=4, column=1, sticky='w')

    ttk.Separator(
            frame_menu_options, orient='horizontal'
            ).grid(row=5, column=0, columnspan=3, padx=10, pady=8, sticky='we')

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
    ).grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    # info current game -----
    ttk.Label(
        frame_menu_options,
        text="running game",
        font="'' 12 underline",
    ).grid(row=8, column=0, columnspan=2)
    ttk.Label(
        frame_menu_options,
        text="{} catastrophes + {} genes + {} MOLs"
        .format(game['n_catastrophes'], game['n_genes'], game['n_MOLs']),
        style="game_info.TLabel",
    ).grid(row=9, column=0, columnspan=2, pady=(0, 8))

    # ----- frame 4 trait selection ----------------------------------------------------------------
    frame_menu_traits = tk.Frame(frame_menu)
    frame_menu_traits.grid(row=2, column=0, padx=border, pady=(0, border), sticky="nesw")
    frame_menu_traits.columnconfigure(0, weight=1)
    frame_menu_traits.columnconfigure(1, weight=1)

    # 'play trait' -----
    ttk.Label(
        frame_menu_traits,
        text="play trait",
        font="'' 18",
    ).grid(row=0, column=0, columnspan=2, pady=(5, 0))

    # search field -----
    ent_trait_search[0] = ttk.Entry(
        frame_menu_traits,
        width=10,
        textvariable=str_trait_search)
    ent_trait_search[0].grid(row=1, column=0, padx=(10, 0), sticky="w")
    ent_trait_search[0].bind("<KeyRelease>",
                             lambda e: search_trait_in_list(str_trait_search))
    ent_trait_search[0].bind('<Down>',
                             lambda e: lbox_deck[0].selection_clear(0, tk.END), add='+')
    ent_trait_search[0].bind('<Down>',
                             lambda e: lbox_deck[0].selection_set(0), add='+')
    ent_trait_search[0].bind('<Down>',
                             lambda e: lbox_deck[0].focus(), add='+')
    ent_trait_search[0].bind('<Down>',
                             lambda e: lbox_deck[0].see(0), add='+')
    ent_trait_search[0].bind('<Down>',
                             lambda e: write_log(['select', 'deck'],
                                                 traits_df.loc[deck_filtered_idx[0]].trait,
                                                 deck_filtered_idx[0]), add='+')

    ttk.Button(
        frame_menu_traits,
        text="clear",
        width=4,
        command=btn_clear_trait_search,
    ).grid(row=1, column=1, padx=(0, 10), sticky="w")

    # listbox with (filtered) deck-cards -----
    lbox_deck[0] = tk.Listbox(
        frame_menu_traits,
        height=4,
        listvariable=deck_filtered_str,
        exportselection=False)
    lbox_deck[0].grid(row=2, column=0, columnspan=2, padx=10)
    lbox_deck[0].bind("<<ListboxSelect>>",
                      lambda e: write_log(['select', 'deck'],
                                          traits_df.loc[deck_filtered_idx[lbox_deck[0].curselection()[0]]].trait,
                                          deck_filtered_idx[lbox_deck[0].curselection()[0]]))
    lbox_deck[0].bind("<Up>",
                      lambda e: ent_trait_search[0].focus() if lbox_deck[0].curselection()[0] == 0 else None)
    # create key bindings to play trait into player's trait pile by hitting number on keyboard
    for p in range(game['n_player']):
        lbox_deck[0].bind('{}'.format(p+1), lambda e, pp=p: btn_play_trait(pp))

    # 'who gets it?' -----
    ttk.Label(
        frame_menu_traits,
        text="who gets the trait?",
        font="'' 18",
    ).grid(row=3, column=0, columnspan=2, pady=(10, 0))

    # player buttons -----
    frame_menu_buttons = tk.Frame(frame_menu_traits)
    frame_menu_buttons.grid(row=4, column=0, columnspan=2, pady=(0, 5))
    for i in range(game['n_player']):
        clspn = int(i + 1 == game['n_player'] and (i + 1) % 2 == 1) + 1
        ttk.Button(
            frame_menu_buttons,
            textvariable=plr['name'][i],
            command=partial(btn_play_trait, i),
        ).grid(row=floor(i / 2), column=i % 2, columnspan=clspn)

    # ----- frame 4 catastrophy selection ----------------------------------------------------------
    frame_menu_catastrophe = tk.Frame(frame_menu)
    frame_menu_catastrophe.grid(row=3, column=0, padx=border, pady=(0, border), sticky="nesw")
    frame_menu_catastrophe.columnconfigure(0, weight=1)
    frame_menu_catastrophe.columnconfigure(1, weight=1)

    # catastrophes -----
    ttk.Label(
        frame_menu_catastrophe,
        text="catastrophes",
        font="'' 18",
    ).grid(row=0, column=0, columnspan=2, pady=(5, 0))
    for c in range(game['n_catastrophes']):
        pos_cat_values = [" catastrophe {}...".format(c+1)] + \
            catastrophes_df.loc[catastrophe['possible'][c]].name.values.tolist()

        catastrophe['cbox'][c] = ttk.Combobox(
            frame_menu_catastrophe,
            values=pos_cat_values,
            exportselection=0,
            state="readonly" if c == 0 else "disabled",
            width=18,
            style="move.TCombobox")
        catastrophe['cbox'][c].current(0)
        catastrophe['cbox'][c].grid(row=c+1, column=0, columnspan=2, padx=4, sticky='ns')
        catastrophe['cbox'][c].bind("<<ComboboxSelected>>", lambda ev, c=c: btn_play_catastrophe(ev, c))

    # world's end -----
    ttk.Label(
        frame_menu_catastrophe,
        text="World's End",
        font="'' 18",
    ).grid(row=game['n_catastrophes']+1, column=0, columnspan=2, pady=(5, 0))

    worlds_end['cbox'] = ttk.Combobox(
        frame_menu_catastrophe,
        values=[" select world's end ..."],
        exportselection=0,
        state="disabled",
        width=10,
        style="move.TCombobox",
        textvariable=worlds_end['played'])
    worlds_end['cbox'].current(0)
    worlds_end['cbox'].grid(row=game['n_catastrophes']+2, column=0,
                            padx=(4, 0), pady=(0, 5), sticky='ns')
    worlds_end['cbox'].bind("<<ComboboxSelected>>", lambda e: btn_worlds_end_select())

    worlds_end['btn'] = ttk.Button(
        frame_menu_catastrophe,
        text="GO!",
        width=3,
        state="disabled",
        style="disabled.TButton",
        command=lambda: btn_worlds_end_apply())
    worlds_end['btn'].grid(row=game['n_catastrophes']+2, column=1, padx=(0, 4), pady=(0, 5), sticky="nse")

    # ----- frame for control buttons --------------------------------------------------------------
    frame_menu_controls = tk.Frame(frame_menu)
    frame_menu_controls.grid(row=4, column=0, padx=border, pady=(0, border), sticky="nesw")
    frame_menu_controls.columnconfigure(0, weight=0)
    frame_menu_controls.columnconfigure(1, weight=0)
    frame_menu_controls.columnconfigure(1, weight=1)

    lbl_icons_switch[0] = ttk.Label(
        frame_menu_controls,
        image=init_switch['icons'],
        cursor="target")
    lbl_icons_switch[0].grid(row=0, column=0, padx=(10, 0))
    lbl_icons_switch[0].bind("<Button-1>", lambda e: switch('icons'))
    lbl_points_switch[0] = ttk.Label(
        frame_menu_controls,
        image=init_switch['points'],
        cursor="target")
    lbl_points_switch[0].grid(row=0, column=1, padx=5)
    lbl_points_switch[0].bind("<Button-1>", lambda e: switch('points'))
    ttk.Button(frame_menu_controls,
               text="quit",
               command=root.quit
               ).grid(row=0, column=2, padx=(0, 10), pady=5, sticky="we")


def reset_variables():
    # update current settings
    game['n_player'] = options['n_player'].get()
    game['n_genes'] = options['n_genes'].get()
    game['n_catastrophes'] = options['n_catastrophes'].get()
    game['n_MOLs'] = options['n_MOLs'].get()

    # reset _player_ variables
    plr['name'].clear()
    plr['genes'].clear()
    plr['points'].clear()
    plr['trait_pile'].clear()
    plr['n_tp'].clear()
    plr['trait_selected'].clear()
    plr['WE_effect'].clear()
    plr['MOL'].clear()
    frame_trait_pile.clear()

    # reset trait_specific variables
    neoteny_checkbutton.clear()
    sleepy_spinbox.clear()

    # fill variables
    for i in range(game['n_player']):
        plr['name'].append(tk.StringVar(value=options["names"][i].get()))
        write_log(['init', 'names'], i+1, plr['name'][i].get())

        plr['genes'].append(tk.IntVar(value=game['n_genes']))
        plr['points'].append({'face': tk.IntVar(value=0), 'drops': tk.IntVar(value=0),
                              'worlds_end': tk.IntVar(value=0), 'MOL': tk.IntVar(value=0),
                              'total': tk.IntVar(value=0)})
        plr['trait_pile'].append([])
        plr['n_tp'].append(tk.StringVar(value='0'))
        plr['trait_selected'].append(tk.Variable(value=np.nan))
        plr['WE_effect'].append(tk.StringVar(value='0'))
        plr['MOL'].append([])

        frame_trait_pile.append(None)
        neoteny_checkbutton.append(tk.IntVar(value=0))
        sleepy_spinbox.append(tk.IntVar(value=0))

        for m in range(game['n_MOLs']):
            plr['MOL'][i].append(tk.StringVar(value="0"))  # for now, manually editing MOL points in entries

    # first player
    game['first_player'] = options['first_player'].get()
    game['first_player_start'] = options['first_player'].get()
    write_log(['init', 'first_player'], plr['name'][game['first_player']].get())

    # reset deck/lbox card-lists
    deck.clear()
    deck.extend(traits_df.index.tolist())   # complete list of indicies of all traits
    deck_filtered_idx.clear()
    deck_filtered_idx.extend(traits_df.index.tolist())  # complete list of indices of traits for menu_listbox
    deck_filtered_str.set(traits_df.loc[deck].trait.values.tolist())  # complete list of names of traits

    # reset occured catastrophes
    catastrophe['possible'].clear()
    catastrophe['played'].clear()
    catastrophe['cbox'].clear()
    for i in range(game['n_catastrophes']):
        catastrophe['possible'].append(catastrophes_df.index.tolist())
        catastrophe['played'].append(None)
        catastrophe['cbox'].append([])

    # reset worlds end
    worlds_end['played'] = tk.StringVar(value="")
    worlds_end['cbox'] = [None]
    worlds_end['btn'] = [None]

    # reset current status
    status_df['color'] = traits_df.color
    status_df['face'] = traits_df.face
    status_df['drops'] = np.nan
    status_df['host'] = 'none'
    status_df['attachment'] = 'none'
    status_df['inactive'] = False
    status_df['no_remove'] = False
    status_df['no_discard'] = False
    status_df['no_steal'] = False
    status_df['no_swap'] = False
    status_df['effects'] = 'none'
    status_df['effects_attachment'] = 'none'
    status_df['effects_traits_WE'] = 'none'
    status_df['effects_WE'] = 'none'
    status_df['traits_WE'] = 'none'
    status_df['we_effect'] = 'none'


def start_game():
    # new logfile ----------------------------------------------------------------------------------
    dt = time.strftime("%Y%m%d-%H%M%S")
    logfile['file'] = os.path.join(dir_log, "DoomPyLog_" + dt + ".txt")
    write_log(['init', 'datetime'], dt)

    # reset variables ------------------------------------------------------------------------------
    write_log(['init', 'variables'])
    reset_variables()

    # update frame_configurations settings ---------------------------------------------------------
    for w in frame_menu.grid_slaves():
        w.grid_forget()

    for w in frame_playground.grid_slaves():
        w.grid_forget()

    for i in range(cfg["max_player"]):
        w = 0 if i >= game['n_player'] else 1  # 'else 1' => player_frames are stretchable
        frame_playground.columnconfigure(i, weight=w)

    # fill _menu_ frame ----------------------------------------------------------------------------
    write_log(['init', 'menu'])
    create_menu_frame()

    # set catastrophe F-key-bindings
    for i in range(game['n_catastrophes']):
        root.bind('<F' + str(i+1) + '>', lambda e, j=i: catastrophe['cbox'][j].focus())

    # fill _playground_ frame with _player_ frames -------------------------------------------------
    write_log(['init', 'playground'])
    frame_player.clear()
    for i in range(game['n_player']):
        # frame_playground.columnconfigure(i, weight=1)
        frame_player.append(create_player_frame(i))

    # clear traits listbox -------------------------------------------------------------------------
    btn_clear_trait_search()


# _tkinter_ ########################################################################################
# create a window ----------------------------------------------------------------------------------
root = tk.Tk()
root.title("LIVE Doomlings Calculator")
root.geometry("1600x900")
root.configure(background=cfg["bg_content"])
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# create gui_wide F-key bindings
root.bind("<F7>", lambda e: btn_clear_trait_search())
root.bind("<F8>", lambda e: start_game())
root.bind("<F9>", lambda e: pre_play())

# create _content_ frame ---------------------------------------------------------------------------
content = tk.Frame(root, width=1200, height=800, bg=cfg["bg_content"])
content.grid(column=0, row=0, sticky="nesw")
content.columnconfigure(0, weight=0)  # menu on the left
content.columnconfigure(1, weight=1)  # complete playground, set =1 to stretch it to the right side

# create _menu_ frame ------------------------------------------------------------------------------
frame_menu = tk.Frame(content, bg=cfg["menu_frame_color"])
frame_menu.grid(row=0, column=0, padx=5, pady=5, stick="nesw")

# create _playground_ frame ------------------------------------------------------------------------
frame_playground = tk.Frame(content, bg=cfg["bg_content"])
frame_playground.grid(row=0, column=1, padx=0, pady=0, stick="nesw")
frame_playground.rowconfigure(0, weight=1)  # stretch playground to bottom

# styling ------------------------------------------------------------------------------------------
gui_style = ttk.Style()
gui_style.configure("game_info.TLabel", font=("", 10, "italic"))
gui_style.configure("name.TLabel", font=("Comic Sans MS", 38, "bold"))
gui_style.configure("nameFirstPlayer.TLabel", font=("Comic Sans MS", 38, "bold"), foreground='#00CD66')
gui_style.configure("n_traits.TLabel", font=("Arial", 38, "bold"))
gui_style.configure("n_traitsFirstPlayer.TLabel", font=("Arial", 38, "bold"), foreground='#00CD66')
gui_style.configure("points.TLabel", font=("", 20))
gui_style.configure("total.TLabel", font=("", 80, "bold"), foreground="orangered1")
gui_style.configure("genes.TLabel", font=("", 38, "bold"), foreground="hotpink1")
gui_style.configure("move.TCombobox", selectbackground="none")
gui_style.configure("disabled.TButton", foreground="grey")

# tk_inter_variables -------------------------------------------------------------------------------
options = {}
options['n_player'] = tk.IntVar(value=cfg["n_player"])                # OPTIONS: number of players
options['n_genes'] = tk.IntVar(value=cfg["n_genes"])                  # OPTIONS: gene pool at beginning
options['n_catastrophes'] = tk.IntVar(value=cfg["n_catastrophes"])  # OPTIONS: number of catastrophes
options['n_MOLs'] = tk.IntVar(value=cfg["n_MOLs"])                    # OPTIONS: number of MOLs
options['names'] = []
for i in range(len(cfg["names"])):
    options['names'].append(tk.StringVar(value=cfg["names"][i]))      # OPTIONS: name of players
options['first_player'] = tk.IntVar(value=0)                          # OPTIONS: first player at begining

str_trait_search = tk.StringVar(value="")   # string searching for traits in DECK
deck_filtered_str = tk.Variable(value="")   # _filtered_ deck of traits_strings in listbox after searching -> str

# load tk-images ------------------------------------------------------------------------------------
images = {}
for k, v in images_dict.items():
    images[k] = ImageTk.PhotoImage(v)

# set switch images --------------------------------------------------------------------------------
init_switch = {}
show_icons = {}
if icons_onoff == 'on':
    init_switch['icons'] = images['icons_on']
elif icons_onoff == 'full':
    init_switch['icons'] = images['icons_full']
else:
    init_switch['icons'] = images['icons_off']

if music_onoff == 'on':
    init_switch['music'] = images['note_on']
else:
    init_switch['music'] = images['note_off']

if points_onoff == 'on':
    init_switch['points'] = images['points_123']
else:
    init_switch['points'] = images['question_mark']

# (re)start game ###################################################################################
mixer.init()
switch('show_icons')
start_game()

# run mainloop #####################################################################################
root.mainloop()
