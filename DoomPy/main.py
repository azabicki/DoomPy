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
import rules_traits_worlds_end as rules_twe
import rules_worlds_end as rules_we

from globals_ import cfg, images_dict, sounds, music_onoff, icons_onoff, points_onoff, show_icons  # noqa: F401
from globals_ import traits_df, status_df, catastrophies_df
from globals_ import lbl_music_switch, lbl_icons_switch, lbl_points_switch, ent_trait_search, lbox_deck
from globals_ import frame_player, frame_trait_pile
from globals_ import game, plr, deck, deck_filtered_idx, catastrophe, worlds_end
from globals_ import neoteny_checkbutton, sleepy_spinbox


# functions ##############################################################
def pre_play():
    start_game()
    pre_play_set = 'attachments'

    if pre_play_set == 'attachments':
        lisa = [0, 1, 9, 11, 19, 21, 26, 29, 69, 89, 178, 256, 300]
        for t in lisa:
            tt = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(tt)
            btn_play_trait(0)

        julia = [52, 62, 68, 72, 81, 84, 30, 70, 301, 340]
        for t in julia:
            tt = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(tt)
            btn_play_trait(1)

        anton = [105, 107, 114, 115, 117, 177, 257, 341]
        for t in anton:
            tt = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(tt)
            btn_play_trait(2)

        adam = [362, 356, 347, 336, 320, 291, 283, 127, 128, 182, 183, 199, 200]
        for t in adam:
            tt = deck_filtered_idx.index(t)
            lbox_deck[0].selection_set(tt)
            btn_play_trait(3)

    if pre_play_set == 2:
        p0 = list(np.random.randint(low=0, high=len(traits_df), size=12))
        for t in p0:
            lbox_deck[0].selection_set(t)
            btn_play_trait(0)

        p1 = list(np.random.randint(low=0, high=len(traits_df), size=10))
        for t in p1:
            lbox_deck[0].selection_set(t)
            btn_play_trait(1)

        p2 = list(np.random.randint(low=0, high=len(traits_df), size=7))
        for t in p2:
            lbox_deck[0].selection_set(t)
            btn_play_trait(2)

        p3 = list(np.random.randint(low=0, high=len(traits_df), size=9))
        for t in p3:
            lbox_deck[0].selection_set(t)
            btn_play_trait(3)

    if pre_play_set == 3:
        lisa = [5, 27]
        for t in lisa:
            lbox_deck[0].selection_set(t)
            btn_play_trait(0)

        julia = [54, 175]
        for t in julia:
            lbox_deck[0].selection_set(t)
            btn_play_trait(1)

        anton = [202, 240]
        for t in anton:
            lbox_deck[0].selection_set(t)
            btn_play_trait(2)

        adam = [241, 293, 302]
        for t in adam:
            lbox_deck[0].selection_set(t)
            btn_play_trait(3)

    catastrophe['cbox'][0].current(3)
    catastrophe['cbox'][0].event_generate("<<ComboboxSelected>>")
    catastrophe['cbox'][1].current(15)
    catastrophe['cbox'][1].event_generate("<<ComboboxSelected>>")
    catastrophe['cbox'][2].current(18)
    catastrophe['cbox'][2].event_generate("<<ComboboxSelected>>")


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
            else:
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
                show_icons['drops'] = True        # default: True
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
                show_icons['drops'] = True          # default: True
                show_icons['gene_pool'] = True      # default: False
                show_icons['worlds_end'] = True     # default: False
                show_icons['effectless'] = True     # default: False
                show_icons['attachment'] = True     # default: False
            else:
                show_icons['color'] = False       # default: True
                show_icons['face'] = False        # default: True
                show_icons['collection'] = False  # default: False
                show_icons['dominant'] = False    # default: False
                show_icons['action'] = False      # default: False
                show_icons['drops'] = False       # default: True
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
                lbl_points_switch[0].configure(image=images['points_on'])
                write_log(['music', 'on'])
            else:
                points_onoff = 'off'
                lbl_points_switch[0].configure(image=images['points_off'])
                write_log(['music', 'off'])


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


def btn_play_worlds_end():
    # do nothing if no catastrophy selected
    if worlds_end['cbox'].current() == 0:
        write_log(['worlds_end', 'error_no_event'])
        return

    # print log
    write_log(['worlds_end', 'game_over'], worlds_end['name'].get())

    # update scoring
    update_scoring()

    # update all trait piles
    for p in range(game['n_player']):
        create_trait_pile(frame_trait_pile[p], p)


def btn_play_catastrophe(event, c):
    # get played catastrophe
    cbox_idx = event.widget.current()
    played_str = event.widget.get()
    played_before = catastrophe['played'][c]
    if cbox_idx > 0:
        played_idx = catastrophe['possible'][c][cbox_idx-1]

    # return, if no catastrophe was selected
    if cbox_idx == 0:
        if played_before is not None:
            old_cbox_idx = catastrophe['possible'][c].index(played_before) + 1
            catastrophe['cbox'][c].current(old_cbox_idx)
        write_log(['catastrophe', 'error_no_catastrophe'])
        return

    # return, if same catastrophe selected
    if played_before == played_idx:
        write_log(['catastrophe', 'error_same_catastrophe'])
        return

    # print log
    write_log(['catastrophe', 'catastrophe'], c+1, played_str, played_idx)

    # set played catastrophe
    catastrophe['played'][c] = played_idx

    # update possible catastrophies for later ones
    for i in range(1, game['n_catastrophies']):
        # reset possible's
        catastrophe['possible'][i] = catastrophies_df.index.tolist()

        # remove previous catastrophies from possible's
        for prev in range(0, i):
            if catastrophe['played'][prev] is not None:
                catastrophe['possible'][i].remove(catastrophe['played'][prev])

                pos_cat_values = [" catastrophe {}...".format(1+1)] \
                    + catastrophies_df.loc[catastrophe['possible'][i]].name.values.tolist()
                catastrophe['cbox'][i].configure(values=pos_cat_values)

                # check if current catastrophie was selected by a next one
                if catastrophe['played'][prev] == catastrophe['played'][i]:
                    # reset i'th catastrophe
                    catastrophe['played'][i] = None
                    catastrophe['cbox'][i].current(0)

                    # disable forthcoming catastrophies & worlds end
                    for z in range(i+1, game['n_catastrophies']):
                        catastrophe['cbox'][z].configure(state="disabled")
                        worlds_end['cbox'].configure(state="disabled")

    # enable next catastrophe
    if c < game['n_catastrophies']-1:
        catastrophe['cbox'][c+1].configure(state="readonly")
    else:
        worlds_end['cbox'].configure(state="readonly")

    # update worlds end combobox
    played_catastrophies = [catastrophies_df.loc[catastrophe['played'][i], "name"]
                            for i in range(game['n_catastrophies'])
                            if catastrophe['played'][i] is not None]
    worlds_end['cbox']['values'] = [" select world's end ..."] + played_catastrophies

    # update genes & scoring
    update_genes()
    update_scoring()

    # update all trait piles
    for p in range(game['n_player']):
        create_trait_pile(frame_trait_pile[p], p)

    # focus back to search field
    ent_trait_search[0].focus_set()


def btn_traits_world_end(from_, trait_idx, event):
    # get trait & its WE effect
    # trait = traits_df.loc[trait_idx].trait
    effect = event.widget.get()
    effect_idx = event.widget.current()

    # print log
    if effect_idx == 0:
        write_log(['traits_WE', 'reset'], traits_df.loc[trait_idx].trait)
    else:
        write_log(['traits_WE', 'set'], traits_df.loc[trait_idx].trait, effect)

    # check if effect was selected previously & if its different than the current, reset old effect
    old_effect = traits_df.loc[trait_idx].cur_worlds_end_trait

    if old_effect != 'none' and old_effect != effect:
        for trait in plr['trait_pile'][from_]:
            # skip current worlds-end-trait
            if trait == trait_idx:
                continue

            # get current status before reseting
            attachment = traits_df.loc[trait].cur_attachment
            host = traits_df.loc[trait].cur_host
            we_effect = traits_df.loc[trait].cur_worlds_end_trait
            cur_drops = traits_df.loc[trait].cur_drops

            # reset trait
            update_traits_current_status('reset', trait, [])

            # redo attachment effects
            if attachment != 'none':
                update_traits_current_status('attachment', trait, attachment)

            # restore host in attachment
            traits_df.loc[trait, 'cur_host'] = host

            # restore cur_drop points
            traits_df.loc[trait, 'cur_drops'] = cur_drops

            # redo worlds_end effects
            if we_effect != 'none':
                traits_df.loc[trait, 'cur_worlds_end_trait'] = we_effect
                update_traits_current_status('worlds_end', trait, plr['trait_pile'][from_])

    # set WE-effect to status_row of trait
    if effect_idx == 0:
        traits_df.loc[trait_idx, 'cur_worlds_end_trait'] = 'none'
    else:
        traits_df.loc[trait_idx, 'cur_worlds_end_trait'] = effect

    # apply WE-effect and update current_values
    update_traits_current_status('worlds_end', trait_idx, plr['trait_pile'][from_])

    # *** !!! ***   VIRAL specific effect   *** !!! ************************
    # -> save list as string which will save drop points for each player
    if traits_df.loc[trait_idx].trait == 'Viral':
        if effect_idx == 0:
            traits_df.loc[trait_idx, "cur_effect"] = 'none'
        else:
            vp = [np.nan] * game['n_player']
            vp_s = ' '.join(str(x) for x in vp)
            traits_df.loc[trait_idx, "cur_effect"] = vp_s

    # *** !!! ***   AMATOXINS specific effect   *** !!! ************************
    # -> save number of discarded different colors into string
    if traits_df.loc[trait_idx].trait == 'Amatoxins':
        if effect_idx == 0:
            traits_df.loc[trait_idx, "cur_effect"] = 'none'
        else:
            traits_df.loc[trait_idx, "cur_effect"] = effect

    # update scoring
    update_genes()
    update_scoring()

    # update all trait piles
    for p in range(game['n_player']):
        create_trait_pile(frame_trait_pile[p], p)


def btn_remove_trait(from_):
    # get card & its attachment
    card = plr['trait_selected'][from_].get()
    if not np.isnan(card):
        attachment = traits_df.loc[card].cur_attachment

    # return, if no trait selected
    if np.isnan(card):
        write_log(['remove', 'error_no_trait'])
        return

    # return, if attachment selected
    if traits_df.loc[card].attachment == 1:
        write_log(['remove', 'error_attachment_selected'])
        return

    # print log
    write_log(['remove', 'error_discard'], plr['name'][from_].get(), traits_df.loc[card].trait, card)
    if attachment != 'none':
        write_log(['remove', 'error_discard_attachment'], traits_df.loc[attachment].trait, attachment)

    # remove card(s) from player & clear trait selection
    plr['trait_pile'][from_].remove(card)
    if attachment != 'none':
        plr['trait_pile'][from_].remove(attachment)
    plr['trait_selected'][from_].set(np.nan)

    # add to deck traits & update deck_listbox
    bisect.insort_left(deck, card)
    if attachment != 'none':
        bisect.insort_left(deck, attachment)
    search_trait_in_list(str_trait_search)  # keep current str in search_entry

    # check, if this trait has a special "remove-rule"
    remove_rule = rules_re.check_trait(traits_df, card, from_)

    # reset current status of card(s)
    update_traits_current_status('reset', card, remove_rule)
    if attachment != 'none':
        update_traits_current_status('reset', attachment, [])

    # update scoring, stars & genes
    update_stars()
    update_genes()
    update_scoring()

    # update all trait piles
    for p in range(game['n_player']):
        create_trait_pile(frame_trait_pile[p], p)

    # focus back to search field
    ent_trait_search[0].focus_set()


def btn_move_trait(from_, cbox_move_to):
    # get card & its attachment
    card = plr['trait_selected'][from_].get()
    if not np.isnan(card):
        attachment = traits_df.loc[card].cur_attachment

    # return, if no target selected
    if cbox_move_to.current() == 0:
        cbox_move_to.current(0)
        write_log(['move', 'error_move_to'])
        return

    # return, if no trait selected
    to = cfg["names"].index(cbox_move_to.get())
    if np.isnan(card):
        cbox_move_to.current(0)
        write_log(['move', 'error_no_trait'])
        return

    # return, if from == to
    if from_ == to:
        cbox_move_to.current(0)
        write_log(['move', 'error_source_target'])
        return

    # return, if attachment selected
    if traits_df.loc[card].attachment == 1:
        cbox_move_to.current(0)
        write_log(['move', 'error_attachment'])
        return

    # print log
    add_txt = "(and its attachment '{}' (id:{}))".format(traits_df.loc[attachment].trait, attachment) \
        if attachment != 'none' else ''
    write_log(['move', 'move_to'],
              traits_df.loc[card].trait, card, add_txt, plr['name'][from_].get(), plr['name'][to].get())

    # remove traits(s) from 'giving' player, update trait_pile & clear trait selection
    plr['trait_pile'][from_].remove(card)
    if attachment != 'none':
        plr['trait_pile'][from_].remove(attachment)

    create_trait_pile(frame_trait_pile[from_], from_)
    plr['trait_selected'][from_].set(np.nan)

    # add to 'receiving' players traits
    bisect.insort_left(plr['trait_pile'][to], card)
    if attachment != 'none':
        bisect.insort_left(plr['trait_pile'][to], attachment)

    # update scoring, stars & genes
    update_stars()
    update_genes()
    update_scoring()

    # update all trait piles
    for p in range(game['n_player']):
        create_trait_pile(frame_trait_pile[p], p)

    # clear combobox
    cbox_move_to.current(0)

    # focus back to search field
    ent_trait_search[0].focus_set()


def btn_attach_to(from_, attachment, event, possible_hosts):
    # get host_data from event_data
    host = event.widget.get()
    host_idx = possible_hosts[event.widget.current()]

    # return, if clicked on current host
    old_host_idx = status_df[status_df['attachment'] == attachment].index.values.tolist()
    if host_idx in old_host_idx:
        write_log(['attach_to', 'error_own_host'])
        return

    # print log
    if host == ' ... ':
        write_log(['attach_to', 'detached'], traits_df.loc[attachment].trait, attachment)
    else:
        write_log(['attach_to', 'attached'],
                  plr['name'][from_].get(), traits_df.loc[attachment].trait,
                  attachment, host, host_idx)

    # check if attachment moved from old_host
    if old_host_idx:
        write_log(['attach_to', 'change_host'], traits_df.loc[old_host_idx[0]].trait, old_host_idx[0])
        update_traits_current_status('reset', old_host_idx[0], [])

    # check if attachment is set back to "..." (idx=0)
    if event.widget.current() == 0:
        # reset host='none' to status_row of attachment
        status_df.loc[attachment, 'host'] = 'none'
    else:
        # set new host_idx to status_row of attachment
        status_df.loc[attachment, 'host'] = host_idx

        # set new attachment to status_row of host & update effects of attachment on host
        update_traits_current_status('attachment', host_idx, attachment)

    # update scoring
    update_genes()
    update_scoring()

    # update all trait piles
    for p in range(game['n_player']):
        create_trait_pile(frame_trait_pile[p], p)


def btn_play_trait(to):
    # return, if no trait selected
    if not lbox_deck[0].curselection():
        write_log(['play', 'error_no_trait'])
        return

    # get card
    trait_idx = deck_filtered_idx[lbox_deck[0].curselection()[0]]
    trait = traits_df.loc[trait_idx].trait

    # return, if player already has two dominants
    if traits_df.loc[trait_idx].dominant == 1:
        if sum([1 for t in plr['trait_pile'][to] if traits_df.loc[t].dominant == 1]) == 2:
            write_log(['play', 'error_2dominants'])
            return

    # return, if any trait specific requirements are not met
    if rules_pl.check_requirement(trait_idx, to):
        return

    # return, if attachment does not have any trait to attach to
    if traits_df.loc[trait_idx].attachment == 1:
        attachables = rules_at.filter_attachables(trait_idx, to)
        if len(attachables) == 0:
            write_log(['play', 'error_no_attachables'])
            return

    # print log
    write_log(['play', 'play'], plr['name'][to].get(), trait, trait_idx)

    # add to players traits & update trait_pile
    bisect.insort_left(plr['trait_pile'][to], trait_idx)

    # remove from deck & update deck_listbox
    deck.remove(trait_idx)
    btn_clear_trait_search()

    # update scoring, stars & genes
    update_stars()
    update_genes()
    update_scoring()

    # update all trait piles
    for p in range(game['n_player']):
        create_trait_pile(frame_trait_pile[p], p)

    # play sound bites
    play_sound(trait)


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


def update_manual_drops(event, trait, p):
    value = event.widget.get()

    # check if input is numeric
    if value.isnumeric():
        # check limit of (hord-coded) 20
        if int(value) > 20:
            value = '20'
            manual_drops[trait].set('20')

        # save manually calculkated drop value to main traits_df
        traits_df.loc[trait, 'cur_drops'] = int(value)
    else:
        manual_drops[trait].set('')
        traits_df.loc[trait, 'cur_drops'] = np.nan

    # update scoring
    update_scoring()

    # update this players trait pile
    create_trait_pile(frame_trait_pile[p], p)


def update_traits_current_status(todo, *args):
    match todo:
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
            status_df.loc[trait, 'traits_WE'] = 'none'
            status_df.loc[trait, 'we_effect'] = 'none'

            # apply rule after resetting
            match reset_rule:
                case 'keep_cur_effect':
                    status_df.loc[trait, 'effects'] = bkp.effects

            # print log
            write_log(['update_trait_status', 'reset'], traits_df.loc[trait].trait)

        case 'attachment':
            host = args[0]
            attachment = args[1]

            # save attachment to host
            status_df.loc[host, 'attachment'] = attachment

            # update current status of host
            rules_at.attachment_effects(host, attachment)

            # print log
            write_log(['update_trait_status', 'attachment'],
                      traits_df.loc[host].trait, traits_df.loc[attachment].trait)

        case 'worlds_end':
            trait_idx = args[0]
            trait_pile = args[1]

            # call rules_function to update other current_values due to current effect
            rules_twe.traits_WE_effects(traits_df, trait_idx, trait_pile)

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
                write_log(['update_trait_status', 'neoteny_that_one'], p)

            # update scoreboard
            update_scoring()

            # update all trait piles
            for p in range(game['n_player']):
                create_trait_pile(frame_trait_pile[p], p)

        case 'update_all':
            update_stars()
            update_genes()
            update_scoring()

            # update all trait piles
            for p in range(game['n_player']):
                create_trait_pile(frame_trait_pile[p], p)


def update_scoring():
    for p in range(game['n_player']):
        # get cards
        trait_pile = plr['trait_pile'][p]

        # calculate world's end points
        p_worlds_end = rules_we.worlds_end(traits_df, worlds_end['name'].get(), plr['trait_pile'],
                                           p, plr['genes'], plr['WE_effect'])

        # calculate face value
        p_face = int(sum([status_df.loc[trait_idx].face for trait_idx in trait_pile
                          if not isinstance(status_df.loc[trait_idx].face, str)]))

        # calculate drops points
        p_drop = rules_dr.drop_points(traits_df, plr['trait_pile'], p, plr['genes'])

        # calculate drops points
        p_MOL = 0
        for x in [x.get() for x in plr['MOL'][p]]:
            if x.isnumeric():
                p_MOL += int(x)

        # calculate total score
        total = p_face + p_drop + p_worlds_end + p_MOL

        # update points
        plr['points'][p]['face'].set(p_face)
        plr['points'][p]['drops'].set(p_drop)
        plr['points'][p]['worlds_end'].set(p_worlds_end)
        plr['points'][p]['MOL'].set(p_MOL)
        plr['points'][p]['total'].set(total)

        # print log, only if points changed
        write_log(['scoring', 'update'], plr['name'][p].get(), p_face, p_drop, p_worlds_end, p_MOL, total)


def update_genes():
    # init vars
    diff_genes = [0] * game['n_player']

    # loop players and calculate +- genes of all played traits --------------------------
    for p in range(game['n_player']):
        # loop traits in trait_pile
        for trait_idx in plr['trait_pile'][p]:
            # get gene effect of this card
            effect = traits_df.loc[trait_idx].effect_gene_pool

            # if there is a rule saved as strings
            if isinstance(effect, str):
                tmp = effect.split()
                value = int(tmp[0])
                who = tmp[1]
                if len(tmp) > 2:
                    restriction = tmp[2]
                else:
                    restriction = False

                # apply rule, only if no restrictions
                if not restriction:
                    match who:
                        case 'all':
                            diff_genes = [i + value for i in diff_genes]
                        case 'self':
                            diff_genes[p] += value
                        case 'opponents':
                            diff_genes = [i+value if i != p else i for i in diff_genes]

                # print log
                write_log(['genes', 'trait'],
                          plr['name'][p].get(), traits_df.loc[trait_idx].trait, value, who, diff_genes)

    # check what catastrophies were played alread ---------------------------------------
    for c in range(game['n_catastrophies']):
        # get card & effect
        c_idx = catastrophe['played'][c]

        # check if catastrophy was played
        if c_idx is not None:
            c_str = catastrophies_df.loc[c_idx, "name"]
            # get effect and apply it
            effect = int(catastrophies_df.loc[c_idx].gene_pool)
            diff_genes = [i + effect for i in diff_genes]

            # print log
            write_log(['genes', 'catastrophe'], c_str, effect, diff_genes)

    # check for special effects by specific traits --------------------------------------
    # Spores
    sprs_idx = traits_df.index[traits_df.trait == 'Spores'].tolist()[0]
    sprs_eff = traits_df.loc[sprs_idx].cur_effect
    if sprs_eff != 'none':
        if '_' in sprs_eff:
            sprs_eff = sprs_eff.split('_')

        for eff in sprs_eff:
            if eff.isnumeric() and int(eff) < game['n_player']:
                p = int(eff)
                diff_genes[p] += 1

                # print log
                write_log(['genes', 'spores'], sprs_idx, plr['name'][p].get(), diff_genes)

    # Sleepy
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

        # check special cases
        Epic_idx = traits_df.index[traits_df.trait == 'Epic'].tolist()[0]
        if Epic_idx in plr['trait_pile'][p]:
            n_dominant = 2

        # find label widgets
        tmp_frame = frame_player[p].winfo_children()
        lbl1 = frame_player[p].nametowidget(str(tmp_frame[0]) + '.!label2')
        lbl2 = frame_player[p].nametowidget(str(tmp_frame[0]) + '.!label3')

        # edit images
        lbl1.configure(image=images['no_star'])
        lbl2.configure(image=images['no_star'])
        if n_dominant > 0:
            lbl1.configure(image=images['star'])
            if n_dominant > 1:
                lbl2.configure(image=images['star'])


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


def create_trait_pile(frame_trait_overview, p):
    # first, clean up frame
    for w in frame_trait_overview.grid_slaves():
        w.grid_forget()

    # loop traits in pile
    irow = -1
    for trait_idx in plr['trait_pile'][p]:
        # get trait name
        trait = traits_df.loc[trait_idx].trait

        # init some vars
        ypad = (3, 0) if irow == 0 else 0
        irow += 1

        # ----- radiobutton / label if attachment --------------------------------------------------
        if traits_df.loc[trait_idx].attachment != 1:
            row_trait = tk.Radiobutton(
                frame_trait_overview,
                text=" " + trait,
                variable=plr['trait_selected'][p],
                value=trait_idx,
                command=lambda t_idx=trait_idx: write_log(['select', 'trait_pile'],
                                                          plr['name'][p].get(),
                                                          traits_df.loc[t_idx].trait,
                                                          t_idx))
            row_trait.grid(row=irow, column=0, padx=3, pady=ypad, sticky='nsw')
        else:
            row_trait = tk.Label(
                frame_trait_overview,
                text=" " + trait)
            row_trait.grid(row=irow, column=0, padx=(24, 3), pady=ypad, sticky='nsw')

        # change font color if dominant
        if traits_df.loc[trait_idx].dominant == 1:
            row_trait.config(fg=cfg["font_color_trait_pile_dominant"])

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

        # ----- current effects due to attachments -------------------------------------------------
        # _current_ color ----------
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

        # drop value ----------
        cur_drops = status_df.loc[trait_idx].drops
        if not np.isnan(cur_drops):
            icol += 1
            drop_string = str(int(cur_drops))

            tk.Label(
                frame_pics,
                image=images[drop_string]
                ).grid(row=0, column=icol)

        # has attachment ----------
        if status_df.loc[trait_idx].attachment != 'none':
            icol += 1
            tk.Label(
                frame_pics,
                image=images['attachment']
                ).grid(row=0, column=icol)

        # noFX ----------
        if status_df.loc[trait_idx].inactive:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noFX']
                ).grid(row=0, column=icol)

        # noRemove ----------
        if status_df.loc[trait_idx].no_remove:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noRemove']
                ).grid(row=0, column=icol)

        # noDiscard ----------
        if status_df.loc[trait_idx].no_discard:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noDiscard']
                ).grid(row=0, column=icol)

        # noSteal ----------
        if status_df.loc[trait_idx].no_steal:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noSteal']
                ).grid(row=0, column=icol)

        # noSwap ----------
        if status_df.loc[trait_idx].no_swap:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noSwap']
                ).grid(row=0, column=icol)

        # ----- current effects due to WORLDS END --------------------------------------------------
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

        # ----- manual DROP points entry -----------------------------------------------------------
        cur_drop_eff = traits_df.loc[trait_idx].effect_drop
        if (isinstance(cur_drop_eff, str)
            and not isinstance(traits_df.loc[trait_idx].effect_worlds_end, str)
            and ('own_hand' in traits_df.loc[trait_idx].effect_drop
                 or 'discarded' in traits_df.loc[trait_idx].effect_drop)):
            irow += 1
            tk.Label(
                frame_trait_overview,
                text="Drop of Life:"
                ).grid(row=irow, column=0, padx=(40, 0), sticky='e')

            drop_entry = ttk.Entry(
                frame_trait_overview,
                width=3,
                textvariable=manual_drops[trait_idx])
            drop_entry.grid(row=irow, column=1, sticky='w')
            drop_entry.bind("<KeyRelease>", lambda e, t=trait_idx: update_manual_drops(e, t, p))

        # ----- ATTACHMENT combobox if trait is attachment -----------------------------------------
        if traits_df.loc[trait_idx].attachment == 1:
            irow += 1
            tk.Label(
                frame_trait_overview,
                text="Attach to:"
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
        if isinstance(traits_df.loc[trait_idx].effect_worlds_end, str):
            irow += 1
            tk.Label(
                frame_trait_overview,
                text="Worlds End:"
                ).grid(row=irow, column=0, padx=(40, 0), sticky='e')

            # get task what to do at worlds end
            we_effect = rules_twe.traits_WE_tasks(traits_df, trait_idx)

            # create combobox
            cbox_attach_to = ttk.Combobox(
                frame_trait_overview,
                height=len(we_effect),
                values=we_effect,
                exportselection=0,
                state="readonly",
                width=10)
            cbox_attach_to.grid(row=irow, column=1, sticky='w')
            cbox_attach_to.bind(
               "<<ComboboxSelected>>", lambda e, t=trait_idx: btn_traits_world_end(p, t, e))

            # check if effect already selected
            if traits_df.loc[trait_idx].cur_worlds_end_trait == 'none':
                cbox_attach_to.current(0)
            else:
                cur_effect = traits_df.loc[trait_idx].cur_worlds_end_trait
                cbox_attach_to.current(we_effect.index(cur_effect))

        # ----- SLEEPY may affect gene pool ?!?!  --------------------------------------------------
        if traits_df.loc[trait_idx].trait == 'Sleepy':
            irow += 1
            tk.Label(
                frame_trait_overview,
                text="gene effect:"
                ).grid(row=irow, column=0, padx=(40, 0), sticky='e')

            # create combobox
            ttk.Spinbox(
                frame_trait_overview,
                from_=-1,
                to=1,
                width=3,
                textvariable=sleepy_spinbox[p],
                wrap=False,
                command=lambda: update_traits_current_status('update_all')
            ).grid(row=irow, column=1, sticky='w')

    # *** !!! *** special, individual case *** !!! *************************************************
    # since 'VIRAL's Drop-of-Life-Effect is affecting other players, hence it needs to be shown on
    # each other players trait pile, allowing there to enter individual drop values, while giving
    # the host only the oppurtunity to perform worlds end effect first, find viral index, and check
    # if it is in another trait pile
    irow += 1
    ttk.Separator(frame_trait_overview, orient='horizontal'
                  ).grid(row=irow, column=0, columnspan=2, padx=5, pady=10, sticky='nesw')

    # --- VIRAL --- add passively Viral to this trait pile ---------------
    viral_idx = traits_df.index[traits_df.trait == 'Viral'].tolist()[0]
    if any([viral_idx in tp for tp in plr['trait_pile']]) and viral_idx not in plr['trait_pile'][p]:
        # create separate frame
        irow += 1
        frame_viral = tk.Frame(frame_trait_overview)
        frame_viral.grid(row=irow, column=0, columnspan=2, sticky='we')

        # add label & drop icon
        tk.Label(
            frame_viral,
            text="VIRAL",
            fg="mediumorchid1"
            ).grid(row=0, column=0, padx=(20, 0), sticky='e')
        tk.Label(
            frame_viral,
            text=" punishes ",
            image=images["drops"],
            compound=tk.LEFT
            ).grid(row=0, column=1, sticky='w')

        # check if worlds end effect was chosen
        we_viral = traits_df.loc[viral_idx].cur_worlds_end_trait
        if we_viral != 'none':
            vp_s = traits_df.loc[viral_idx].cur_effect.split()

            # add color icon
            tk.Label(
                frame_viral,
                image=images[we_viral[0]]
                ).grid(row=0, column=2)
            # add points icono
            tk.Label(
                frame_viral,
                image=images[vp_s[p]]
                ).grid(row=0, column=3)

            write_log(['trait_effects', 'viral'], we_viral, plr['name'][p].get(), vp_s[p])

    # --- AMATOXINS --- add passively Amatoxins to this trait pile ----------------
    amatoxins_idx = traits_df.index[traits_df.trait == 'Amatoxins'].tolist()[0]
    if any([amatoxins_idx in tp for tp in plr['trait_pile']]) and amatoxins_idx not in plr['trait_pile'][p]:
        # create separate frame
        irow += 1
        frame_amatoxins = tk.Frame(frame_trait_overview)
        frame_amatoxins.grid(row=irow, column=0, columnspan=2, sticky='we')

        # add label & drop icon
        tk.Label(
            frame_amatoxins,
            text="AMATOXINS",
            fg="mediumorchid1"
            ).grid(row=0, column=0, padx=(20, 0), sticky='e')
        tk.Label(
            frame_amatoxins,
            text=" discarded",
            image=images["drops"],
            compound=tk.LEFT
            ).grid(row=0, column=1, sticky='w')
        # add color icon
        tk.Label(
            frame_amatoxins,
            image=images['bgpr']
            ).grid(row=0, column=2)

        # check if worlds end effect was chosen
        we_amatoxins = traits_df.loc[amatoxins_idx].cur_worlds_end_trait
        if we_amatoxins != 'none':
            we_drops = str(int(traits_df.loc[amatoxins_idx].cur_effect) * -2)

            # add points icono
            tk.Label(
                frame_amatoxins,
                image=images[we_drops]
                ).grid(row=0, column=3)

            write_log(['trait_effects', 'amatoxins'], we_drops)

    # --- PROWLER --- add passively Prowler to this trait pile ---------------
    prowler_idx = traits_df.index[traits_df.trait == 'Prowler'].tolist()[0]
    if any([prowler_idx in tp for tp in plr['trait_pile']]) and prowler_idx not in plr['trait_pile'][p]:
        # create separate frame
        irow += 1
        frame_prowler = tk.Frame(frame_trait_overview)
        frame_prowler.grid(row=irow, column=0, columnspan=2, sticky='we')

        # add label & drop icon
        tk.Label(
            frame_prowler,
            text="PROWLER",
            fg="mediumorchid1"
            ).grid(row=0, column=0, padx=(20, 0), sticky='e')
        tk.Label(
            frame_prowler,
            text=" less",
            image=images["drops"],
            compound=tk.LEFT
            ).grid(row=0, column=1, sticky='w')

        # add color icon
        tk.Label(
            frame_prowler,
            image=images['bgpr']
            ).grid(row=0, column=2)
        tk.Label(
            frame_prowler,
            text=" as host",
            ).grid(row=0, column=3, sticky='w')
        # add points icono
        vp_s = traits_df.loc[prowler_idx].cur_effect.split()
        tk.Label(
            frame_prowler,
            image=images[vp_s[p]]
            ).grid(row=0, column=4)

        write_log(['trait_effects', 'prowler'], plr['name'][p].get(), vp_s[p])

    # --- SHINY --- add passively Shiny to this trait pile ---------------
    shiny_idx = traits_df.index[traits_df.trait == 'Shiny'].tolist()[0]
    if any([shiny_idx in tp for tp in plr['trait_pile']]) and shiny_idx not in plr['trait_pile'][p]:
        # create separate frame
        irow += 1
        frame_shiny = tk.Frame(frame_trait_overview)
        frame_shiny.grid(row=irow, column=0, columnspan=2, sticky='we')

        # add label & drop icon
        tk.Label(
            frame_shiny,
            text="SHINY",
            fg="#228B22"
            ).grid(row=0, column=0, padx=(20, 0), sticky='e')
        tk.Label(
            frame_shiny,
            text=" punishes ",
            image=images["drops"],
            compound=tk.LEFT
            ).grid(row=0, column=1, sticky='w')

        # add color icon
        tk.Label(
            frame_shiny,
            image=images['c']
            ).grid(row=0, column=2)
        # add points icon
        vp_s = traits_df.loc[shiny_idx].cur_effect.split()
        tk.Label(
            frame_shiny,
            image=images[vp_s[p]]
            ).grid(row=0, column=3)

        write_log(['trait_effects', 'shiny'], plr['name'][p].get(), vp_s[p])

    # --- NEOTENY --- check button if Neoteny is in your hand ------------
    # is NEOTENY in your hand? asked via checkbox? But only if its not pöayed
    neoteny_idx = traits_df.index[traits_df.trait == 'Neoteny'].tolist()[0]
    if ("select world's end" not in worlds_end['name'].get() and
            all(neoteny_idx not in tp for tp in plr['trait_pile'])):
        # only if no one has it or this player has it
        neoteny_effect = traits_df.loc[neoteny_idx].cur_effect
        if neoteny_effect == 'none' or neoteny_effect == str(p):
            # create separate frame for WE_TITLE
            irow += 1
            frame_neoteny = tk.Frame(frame_trait_overview)
            frame_neoteny.grid(row=irow, column=0, columnspan=2, sticky='we')

            tk.Label(frame_neoteny,
                     text="NEOTENY",
                     fg="#1C86EE"
                     ).grid(row=0, column=0, padx=(20, 0), sticky='e')
            if neoteny_checkbutton[p].get() == 1:
                ttk.Checkbutton(frame_neoteny,
                                variable=neoteny_checkbutton[p],
                                text=' got it!',
                                command=lambda: update_traits_current_status('neoteny', int(p))
                                ).grid(row=0, column=1, padx=(0, 0))
                ttk.Label(frame_neoteny,
                          image=images['drops']
                          ).grid(row=0, column=2)
                tk.Label(frame_neoteny,
                         image=images['4']
                         ).grid(row=0, column=3)
            else:
                ttk.Checkbutton(frame_neoteny,
                                variable=neoteny_checkbutton[p],
                                text=' in my hand???',
                                command=lambda: update_traits_current_status('neoteny', int(p))
                                ).grid(row=0, column=1, padx=(0, 0))

    # **********************************************************************************************
    # ------ worlds end -> manual entries ---------------------------------------------------------
    if "select world's end" not in worlds_end['name'].get():
        irow += 1
        ttk.Separator(frame_trait_overview, orient='horizontal'
                      ).grid(row=irow, column=0, columnspan=2, padx=5, pady=10, sticky='we')

        # get world's end name & index
        we = worlds_end['name'].get()
        we_idx = catastrophies_df[catastrophies_df['name'] == we].index.values[0]
        we_eff = catastrophies_df.loc[we_idx].worlds_end

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

    # ----- name + overview current points -------------------------------
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
    ttk.Label(frame_points, textvariable=plr['name'][p], style="name.TLabel"
              ).grid(row=0, column=0, padx=5, pady=(5, 0), columnspan=5, sticky='ns')

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

    # ----- list of traits played ----------------------------------------
    frame_traits = tk.Frame(frame)
    frame_traits.grid(row=1, column=0, padx=border, pady=(0, border), sticky="nesw")
    frame_traits.rowconfigure(2, weight=1)
    frame_traits.columnconfigure(0, weight=1)  # for left button under trait-pile
    frame_traits.columnconfigure(1, weight=1)  # for right button under trait-pile

    frame_trait_pile[p] = tk.Frame(frame_traits)
    frame_trait_pile[p].grid(row=0, column=0, columnspan=2, sticky='nesw', padx=border, pady=border)
    frame_trait_pile[p].columnconfigure(1, weight=1)  # for left button under trait-pile
    create_trait_pile(frame_trait_pile[p], p)

    # action buttons -----
    ttk.Separator(
        frame_traits, orient='horizontal'
        ).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='we')

    cbox_move_to = ttk.Combobox(
        frame_traits,
        height=game['n_player']+1,
        values=[" move trait to ..."] + ['p' + str(i+1) + ': ' + j.get()
                                         for i, j in enumerate(plr['name'])],
        exportselection=0,
        state="readonly",
        width=12,
        style="move.TCombobox")
    cbox_move_to.grid(row=2, column=0, pady=(0, border), sticky='n')
    cbox_move_to.current(0)
    cbox_move_to.bind(
        "<<ComboboxSelected>>", lambda e: btn_move_trait(p, cbox_move_to))

    ttk.Button(
        frame_traits,
        text="remove trait",
        command=partial(btn_remove_trait, p),
    ).grid(row=2, column=1, pady=(0, border), sticky='n')

    # ----- Meaning of Life -------------------------------------
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

    # nr catastrophies -----
    ttk.Label(
        frame_menu_options,
        text="# catastrophies: ",
    ).grid(row=3, column=0, sticky='e')
    ttk.Spinbox(
        frame_menu_options,
        from_=2,
        to=8,
        width=3,
        textvariable=options['n_catastrophies'],
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

    # restart button -----
    ttk.Button(
        frame_menu_options,
        text="restart game",
        command=start_game,
    ).grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    # info current game -----
    xxx = ttk.Label(
        frame_menu_options,
        text="running game",
        font="'' 12 underline",
    )
    xxx.grid(row=6, column=0, columnspan=2)
    xxx.bind("<Button-1>", lambda e: pre_play())
    ttk.Label(
        frame_menu_options,
        text="{} catastrophies + {} genes + {} MOLs"
        .format(game['n_catastrophies'], game['n_genes'], game['n_MOLs']),
        style="game_info.TLabel",
    ).grid(row=7, column=0, columnspan=2, pady=(0, 5))

    # ----- frame 4 player names -------------------------------------------------------------------
    frame_menu_names = tk.Frame(frame_menu)
    frame_menu_names.grid(row=1, column=0, padx=border, pady=(0, border), ipady=4, sticky="nesw")
    frame_menu_names.columnconfigure(0, weight=1)
    frame_menu_names.columnconfigure(1, weight=1)

    # title -----
    ttk.Label(
        frame_menu_names,
        text="who's playing?",
        font="'' 18",
    ).grid(row=0, column=0, columnspan=2, pady=(5, 5))

    # name entries ---
    for i in range(game['n_player']):
        ttk.Label(
            frame_menu_names,
            text="player {}: ".format(i+1),
        ).grid(row=i+1, column=0, sticky='e')
        ttk.Entry(
            frame_menu_names,
            textvariable=plr['name'][i],
            width=8,
        ).grid(row=i+1, column=1, sticky='w')

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

    # catastrophies -----
    ttk.Label(
        frame_menu_catastrophe,
        text="Catastrophies",
        font="'' 18",
    ).grid(row=0, column=0, columnspan=2, pady=(5, 0))
    for c in range(game['n_catastrophies']):
        pos_cat_values = [" catastrophe {}...".format(c+1)] + \
            catastrophies_df.loc[catastrophe['possible'][c]].name.values.tolist()

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
    ).grid(row=game['n_catastrophies']+1, column=0, columnspan=2, pady=(5, 0))

    worlds_end['cbox'] = ttk.Combobox(
        frame_menu_catastrophe,
        values=[" select world's end ..."],
        exportselection=0,
        state="disabled",
        width=18,
        style="move.TCombobox",
        textvariable=worlds_end['name'])
    worlds_end['cbox'].current(0)
    worlds_end['cbox'].grid(row=game['n_catastrophies']+2, column=0, columnspan=2,
                            padx=4, pady=(0, 5), sticky='ns')
    worlds_end['cbox'].bind("<<ComboboxSelected>>", lambda e: btn_play_worlds_end())

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
    game['n_catastrophies'] = options['n_catastrophies'].get()
    game['n_MOLs'] = options['n_MOLs'].get()

    # save previous names
    last_names = plr['name'].copy()

    # reset _player_ variables
    plr['name'].clear()
    plr['genes'].clear()
    plr['points'].clear()
    plr['trait_pile'].clear()
    plr['trait_selected'].clear()
    plr['WE_effect'].clear()
    plr['MOL'].clear()
    frame_trait_pile.clear()

    neoteny_checkbutton.clear()
    sleepy_spinbox.clear()

    # fill variables
    for i in range(game['n_player']):
        if len(last_names) >= i+1:
            plr['name'].append(tk.StringVar(value=last_names[i].get()))
            write_log(['init', 'previous_names'], i+1, plr['name'][i].get())
        else:
            plr['name'].append(tk.StringVar(value=cfg["names"][i]))
            write_log(['init', 'default_names'], i+1, plr['name'][i].get())

        plr['genes'].append(tk.IntVar(value=game['n_genes']))
        plr['points'].append({'face': tk.IntVar(value=0), 'drops': tk.IntVar(value=0),
                              'worlds_end': tk.IntVar(value=0), 'MOL': tk.IntVar(value=0),
                              'total': tk.IntVar(value=0)})
        plr['trait_pile'].append([])
        plr['trait_selected'].append(tk.Variable(value=np.nan))
        plr['WE_effect'].append(tk.StringVar(value='0'))
        plr['MOL'].append([])

        frame_trait_pile.append(None)
        neoteny_checkbutton.append(tk.IntVar(value=0))
        sleepy_spinbox.append(tk.IntVar(value=0))

        for m in range(game['n_MOLs']):
            plr['MOL'][i].append(tk.StringVar(value="0"))  # for now, manually editing MOL points in entries

    # reset deck/lbox card-lists
    deck.clear()
    deck.extend(traits_df.index.tolist())   # complete list of indicies of all traits
    deck_filtered_idx.clear()
    deck_filtered_idx.extend(traits_df.index.tolist())  # complete list of indices of traits for menu_listbox
    deck_filtered_str.set(traits_df.loc[deck].trait.values.tolist())  # complete list of names of traits

    # reset manually calculated drop values
    manual_drops.clear()
    for i in range(len(traits_df)):
        manual_drops.append(tk.StringVar(value='-'))

    # reset occured catastrophies
    catastrophe['possible'].clear()
    catastrophe['played'].clear()
    catastrophe['cbox'].clear()
    for i in range(game['n_catastrophies']):
        catastrophe['possible'].append(catastrophies_df.index.tolist())
        catastrophe['played'].append(None)
        catastrophe['cbox'].append([])

    # reset worlds end
    worlds_end['cbox'] = [None]
    worlds_end['name'] = tk.StringVar(value="")

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
    status_df['traits_WE'] = 'none'
    status_df['we_effect'] = 'none'


def start_game():
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
gui_style.configure("name.TLabel", font=("Comic Sans MS", 36, "bold"))
gui_style.configure("points.TLabel", font=("", 20))
gui_style.configure("total.TLabel", font=("", 80, "bold"), foreground="orangered1")
gui_style.configure("genes.TLabel", font=("", 38, "bold"), foreground="hotpink1")
gui_style.configure("move.TCombobox", selectbackground="none")

# tk_inter_variables -------------------------------------------------------------------------------
options = {}
options['n_player'] = tk.IntVar(value=cfg["n_player"])                # OPTIONS: number of players
options['n_genes'] = tk.IntVar(value=cfg["n_genes"])                  # OPTIONS: gene pool at beginning
options['n_catastrophies'] = tk.IntVar(value=cfg["n_catastrophies"])  # OPTIONS: number of catastrophies
options['n_MOLs'] = tk.IntVar(value=cfg["n_MOLs"])                    # OPTIONS: number of MOLs

str_trait_search = tk.StringVar(value="")   # string searching for traits in DECK
deck_filtered_str = tk.Variable(value="")   # _filtered_ deck of traits_strings in listbox after searching -> str

# load tk-images ------------------------------------------------------------------------------------
images = {}
for k, v in images_dict.items():
    images[k] = ImageTk.PhotoImage(v)

# init variables -----------------------------------------------------------------------------------
manual_drops = []                       # list to save manual drop entries to

# set switch images --------------------------------------------------------------------------------
init_switch = {}
if music_onoff == 'on':
    init_switch['music'] = images['note_on']
else:
    init_switch['music'] = images['note_off']

if icons_onoff == 'on':
    init_switch['icons'] = images['icons_on']
elif icons_onoff == 'full':
    init_switch['icons'] = images['icons_full']
else:
    init_switch['icons'] = images['icons_off']

if points_onoff == 'on':
    init_switch['points'] = images['points_on']
else:
    init_switch['points'] = images['points_off']

# (re)start game ###################################################################################
mixer.init()
switch('show_icons')
start_game()

# run mainloop #####################################################################################
root.mainloop()
