import os
import glob
import json
import bisect
import tkinter as tk
from tkinter import ttk
from math import floor
from functools import partial
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
from pygame import mixer
import attachment_rules as at_rules
import discard_rules as di_rules
import drop_rules as dr_rules
import traits_worlds_end_rules as twe_rules
import worlds_end_rules as we_rules


# system settings ########################################################
curdir = os.path.dirname(__file__)

# load defaults ----------------------------------------------------------
with open("DoomPy/config.json") as json_file:
    defaults = json.load(json_file)

# load cards.xlsx --------------------------------------------------------
traits_df_unsorted = pd.read_excel(os.path.join(curdir, "files", "cards.xlsx"), sheet_name="traits")
traits_df = traits_df_unsorted.sort_values(by='trait').reset_index(drop=True)
traits_dfi = traits_df.index.tolist()

ages_df_unsorted = pd.read_excel(os.path.join(curdir, "files", "cards.xlsx"), sheet_name="ages")
ages_df = ages_df_unsorted.sort_values(by='name').reset_index(drop=True)
ages_dfi = ages_df[ages_df["type"] == "Age"].index.tolist()
catastrophies_dfi = ages_df[ages_df["type"] == "Catastrophe"].index.tolist()

# add columns to traits_df
traits_df["cur_color"] = traits_df.color
traits_df["cur_face"] = traits_df.face
traits_df["cur_drops"] = np.nan
traits_df["cur_effect"] = 'none'
traits_df["cur_host"] = 'none'
traits_df["cur_attachment"] = 'none'
traits_df["cur_worlds_end_trait"] = 'none'
traits_df["cur_worlds_end_effect"] = np.nan

# load images ------------------------------------------------------------
img_size_star = 30
img_size_scoreboard = 24
img_size_icons = 20
img_size_icons_w = int(img_size_icons*1.5)
img_colors_set = "circle"
img_trait_properties_set = "official_setA"

images_dict = {}
for files in glob.glob(os.path.join(curdir, "images", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files).resize((img_size_icons, img_size_icons))

for files in glob.glob(os.path.join(curdir, "images", "dominant_star", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files).resize((img_size_star, img_size_star))

for files in glob.glob(os.path.join(curdir, "images", "colors", img_colors_set, "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files).resize((img_size_icons, img_size_icons))

for files in glob.glob(os.path.join(curdir, "images", "trait_properties", img_trait_properties_set, "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files).resize((img_size_icons, img_size_icons))

for files in glob.glob(os.path.join(curdir, "images", "trait_properties", img_trait_properties_set, "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0] + '_sb'
    images_dict[var_name] = Image.open(files).resize((img_size_scoreboard, img_size_scoreboard))

for files in glob.glob(os.path.join(curdir, "images", "effects", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files)

    # pay attention to w/h-ratio
    w, h = images_dict[var_name].size
    actual_img_w = int(w / h * img_size_icons)
    images_dict[var_name] = images_dict[var_name].resize((actual_img_w, img_size_icons))

for files in glob.glob(os.path.join(curdir, "images", "face", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files)

    # pay attention to w/h-ratio
    w, h = images_dict[var_name].size
    actual_img_w = int(w / h * img_size_icons)
    images_dict[var_name] = images_dict[var_name].resize((actual_img_w, img_size_icons))

# init mixer 4 playing sounds & preload files ----------------------------
mixer.init()
sounds = {}
for files in glob.glob(os.path.join(curdir, "sounds", "*.mp3")):
    var_name = os.path.splitext(os.path.basename(files))[0].lower()
    sounds[var_name] = mixer.Sound(files)


# functions ##############################################################
def pre_play():
    global play_trait

    start_game()
    pre_play_set = 1

    if pre_play_set == 1:
        lisa = [5, 16, 22, 25, 64, 98, 160, 161]
        for play_trait in lisa:
            btn_play_trait(0)

        julia = [137, 162, 163, 164, 175, 208]
        for play_trait in julia:
            btn_play_trait(1)

        anton = [196, 209, 232, 277, 278, 287, 290, 311, 312, 313, 314]
        for play_trait in anton:
            btn_play_trait(2)

        adam = [235, 246, 315, 317, 318, 324, 352]
        for play_trait in adam:
            btn_play_trait(3)

    if pre_play_set == 2:
        play_trait = 0
        btn_play_trait(0)

        play_trait = 1
        btn_play_trait(0)
        play_trait = 6
        btn_play_trait(0)
        play_trait = 16
        btn_play_trait(0)
        play_trait = 17
        btn_play_trait(0)
        play_trait = 18
        btn_play_trait(0)
        play_trait = 29
        btn_play_trait(0)
        play_trait = 37
        btn_play_trait(0)
        play_trait = 41
        btn_play_trait(0)
        play_trait = 42
        btn_play_trait(0)
        play_trait = 78
        btn_play_trait(0)
        play_trait = 85
        btn_play_trait(0)
        play_trait = 109
        btn_play_trait(0)
        play_trait = 118
        btn_play_trait(0)
        play_trait = 177
        btn_play_trait(0)
        play_trait = 207
        btn_play_trait(0)

        play_trait = 19
        btn_play_trait(1)
        play_trait = 35
        btn_play_trait(1)
        play_trait = 46
        btn_play_trait(1)
        play_trait = 68
        btn_play_trait(1)
        play_trait = 91
        btn_play_trait(1)
        play_trait = 111
        btn_play_trait(1)
        play_trait = 121
        btn_play_trait(1)
        play_trait = 129
        btn_play_trait(1)
        play_trait = 155
        btn_play_trait(1)
        play_trait = 174
        btn_play_trait(1)
        play_trait = 184
        btn_play_trait(1)
        play_trait = 199
        btn_play_trait(1)

        play_trait = 166
        btn_play_trait(2)
        play_trait = 204
        btn_play_trait(2)

        play_trait = 3
        btn_play_trait(3)
        play_trait = 5
        btn_play_trait(3)
        play_trait = 7
        btn_play_trait(3)
        play_trait = 9
        btn_play_trait(3)
        play_trait = 33
        btn_play_trait(3)
        play_trait = 34
        btn_play_trait(3)
        play_trait = 36
        btn_play_trait(3)
        play_trait = 64
        btn_play_trait(3)
        play_trait = 76
        btn_play_trait(3)
        play_trait = 89
        btn_play_trait(3)
        play_trait = 203
        btn_play_trait(3)
        play_trait = 205
        btn_play_trait(3)
        play_trait = 209
        btn_play_trait(3)
        play_trait = 211
        btn_play_trait(3)

    catastrophies_cbox[0].current(3)
    catastrophies_cbox[0].event_generate("<<ComboboxSelected>>")
    catastrophies_cbox[1].current(15)
    catastrophies_cbox[1].event_generate("<<ComboboxSelected>>")
    catastrophies_cbox[2].current(18)
    catastrophies_cbox[2].event_generate("<<ComboboxSelected>>")
    catastrophies_cbox[3].current(24)
    catastrophies_cbox[3].event_generate("<<ComboboxSelected>>")


def switch_music():
    if music_onoff.get():
        music_onoff.set(0)
        music_lbl[0].configure(image=images['note_off'])
    else:
        music_onoff.set(1)
        music_lbl[0].configure(image=images['note_on'])


def switch_icons():
    if icons_onoff.get():
        print(' icons switched on')
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
        print(' icons switched off')
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

    # update all trait piles
    for p in range(n_player.get()):
        if player_rb_frames[p] is not None:
            create_trait_pile(player_rb_frames[p], p)


def play(trait):
    if music_onoff.get():
        if trait.lower() in sounds:
            sounds[trait.lower()].play()


def btn_clear_trait_search():
    global play_trait

    search_trait.set("")
    lbox_cards_idx.set(deck_cards)
    lbox_cards_str.set(traits_df.loc[deck_cards].trait.values.tolist())
    lbox_traits[0].selection_clear(0, tk.END)
    play_trait = None


def btn_traits_world_end(from_, trait_idx, event):
    # get trait & its WE effect
    # trait = traits_df.loc[trait_idx].trait
    effect = event.widget.get()
    effect_idx = event.widget.current()

    # print log
    if effect_idx == 0:
        print(">>> traits world end <<< resetting '{}'s worlds-end-effect..."
              .format(traits_df.loc[trait_idx].trait))
    else:
        print(">>> traits world end <<< setting '{}'s worlds-end-effect to '{}'"
              .format(traits_df.loc[trait_idx].trait, effect))

    # check if effect was selected previously & if its different than the current, reset old effect
    old_effect = traits_df.loc[trait_idx].cur_worlds_end_trait

    if old_effect != 'none' and old_effect != effect:
        for trait in player_traits[from_]:
            # skip current worlds-end-trait
            if trait == trait_idx:
                continue

            # get current status before reseting
            attachment = traits_df.loc[trait].cur_attachment
            host = traits_df.loc[trait].cur_host
            we_effect = traits_df.loc[trait].cur_worlds_end_trait
            cur_drops = traits_df.loc[trait].cur_drops

            # reset trait
            update_traits_current_status('reset', trait, False)

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
                update_traits_current_status('worlds_end', trait, player_traits[from_])

    # set WE-effect to status_row of trait
    if effect_idx == 0:
        traits_df.loc[trait_idx, 'cur_worlds_end_trait'] = 'none'
    else:
        traits_df.loc[trait_idx, 'cur_worlds_end_trait'] = effect

    # apply WE-effect and update current_values
    update_traits_current_status('worlds_end', trait_idx, player_traits[from_])

    # *** !!! ***   VIRAL specific effect   *** !!! ************************
    # -> save list as string which will save drop points for each player
    if traits_df.loc[trait_idx].trait == 'Viral':
        if effect_idx == 0:
            traits_df.loc[trait_idx, "cur_effect"] = 'none'
        else:
            vp = [np.nan] * n_player.get()
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
    for p in range(n_player.get()):
        create_trait_pile(player_rb_frames[p], p)


def btn_attach_to(from_, attachment, event, possible_hosts):
    # get host_data from event_data
    host = event.widget.get()
    host_idx = possible_hosts[event.widget.current()]

    # return, if clicked on current host
    old_host_idx = traits_df[traits_df['cur_attachment'] == attachment].index.values.tolist()
    if host_idx in old_host_idx:
        print(">>> attachment <<< ERROR - clicked on own host")
        return

    # print log
    if host == ' ... ':
        print(">>> attachment <<< '{}' is dettached from all host..."
              .format(traits_df.loc[attachment].trait))
    else:
        print(">>> attachment <<< '{}' is attaching '{}' to '{}'"
              .format(player_name[from_].get(), traits_df.loc[attachment].trait, host))

    # check if attachment moved from old_host
    if old_host_idx:
        print("    >>> was until now on old host: {}".format(traits_df.loc[old_host_idx[0]].trait))
        update_traits_current_status('reset', old_host_idx[0], [])

    # check if attachment is set back to "..." (idx=0)
    if event.widget.current() == 0:
        # reset host='none' to status_row of attachment
        update_traits_current_status('reset', attachment, [])
    else:
        # set new host_idx to status_row of attachment
        traits_df.loc[attachment, 'cur_host'] = host_idx

        # set new attachment to status_row of host & update effects of attachment on host
        update_traits_current_status('attachment', host_idx, attachment)

    # update scoring
    update_genes()
    update_scoring()

    # update all trait piles
    for p in range(n_player.get()):
        create_trait_pile(player_rb_frames[p], p)


def btn_discard_trait(from_):
    # get card & its attachment
    card = player_trait_selected[from_].get()
    if not np.isnan(card):
        attachment = traits_df.loc[card].cur_attachment

    # return, if no trait selected
    if np.isnan(card):
        print(">>> discard <<< ERROR - no trait selected")
        return

    # return, if attachment selected
    if traits_df.loc[card].attachment == 1:
        print(">>> discard <<< ERROR - attachment not discardable -> discard host instead")
        return

    # print log
    print(">>> discard <<< '{}' is discarding '{}' (id:{})"
          .format(player_name[from_].get(), traits_df.loc[card].trait, card))
    if attachment != 'none':
        print(">>> discard <<< ___ attachment '{}' (id:{}) is also discarded automatically"
              .format(traits_df.loc[attachment].trait, attachment))

    # remove card(s) from player & clear trait selection
    player_traits[from_].remove(card)
    if attachment != 'none':
        player_traits[from_].remove(attachment)
    player_trait_selected[from_].set(np.nan)

    # add to deck traits & update deck_listbox
    bisect.insort_left(deck_cards, card)
    if attachment != 'none':
        bisect.insort_left(deck_cards, attachment)
    search_trait_in_list(search_trait)  # keep current str in search_entry

    # in case that trait have a special "discard-rule"
    special_rule = di_rules.check_trait(traits_df, card, from_)

    # reset current status of card(s)
    update_traits_current_status('reset', card, special_rule, [])
    if attachment != 'none':
        update_traits_current_status('reset', attachment, [])

    # update scoring, stars & genes
    update_stars()
    update_genes()
    update_scoring()

    # update all trait piles
    for p in range(n_player.get()):
        create_trait_pile(player_rb_frames[p], p)

    print(traits_df.loc[card].tolist())
    if attachment != 'none':
        print(traits_df.loc[attachment].tolist())


def btn_move_trait(from_, cbox_move_to):
    # get card & its attachment
    card = player_trait_selected[from_].get()
    if not np.isnan(card):
        attachment = traits_df.loc[card].cur_attachment

    # return, if no target selected
    if cbox_move_to.current() == 0:
        cbox_move_to.current(0)
        print(">>> move <<< ERROR - clicked on 'move trait to...'")
        return

    # return, if no trait selected
    to = defaults["names"].index(cbox_move_to.get())
    if np.isnan(card):
        cbox_move_to.current(0)
        print(">>> move <<< ERROR - no trait selected")
        return

    # return, if from == to
    if from_ == to:
        cbox_move_to.current(0)
        print(">>> move <<< ERROR - 'source' and 'target' player are the same")
        return

    # return, if attachment selected
    if traits_df.loc[card].attachment == 1:
        cbox_move_to.current(0)
        print(">>> move <<< ERROR - attachment not moveable -> move host instead")
        return

    # print log
    add_txt = "(and its attachment '{}' (id:{}))".format(traits_df.loc[attachment].trait, attachment) \
        if attachment != 'none' else ''
    print(">>> move <<< '{}' (id:{}) {} is moved from '{}' to '{}'"
          .format(traits_df.loc[card].trait, card, add_txt, player_name[from_].get(), player_name[to].get()))

    # remove traits(s) from 'giving' player, update trait_pile & clear trait selection
    player_traits[from_].remove(card)
    if attachment != 'none':
        player_traits[from_].remove(attachment)

    create_trait_pile(player_rb_frames[from_], from_)
    player_trait_selected[from_].set(np.nan)

    # add to 'receiving' players traits
    bisect.insort_left(player_traits[to], card)
    if attachment != 'none':
        bisect.insort_left(player_traits[to], attachment)

    # update scoring, stars & genes
    update_stars()
    update_genes()
    update_scoring()

    # update all trait piles
    for p in range(n_player.get()):
        create_trait_pile(player_rb_frames[p], p)

    # clear combobox
    cbox_move_to.current(0)


def btn_play_trait(to):
    # return, if no trait selected
    if play_trait is None:
        print(">>> play <<< ERROR - no trait selected")
        return

    # get card
    trait_idx = play_trait
    trait = traits_df.loc[trait_idx].trait

    # return, if player already has two dominants
    if traits_df.loc[trait_idx]['dominant'] == 1:
        if sum([1 for t in player_traits[to] if traits_df.loc[t].dominant == 1]) == 2:
            print(">>> play <<< ERROR - already 2 dominant traits in trait pile")
            return

    # print log
    print(">>> play <<< '{}' is playing '{}'"
          .format(player_name[to].get(), trait))

    # add to players traits & update trait_pile
    bisect.insort_left(player_traits[to], trait_idx)

    # remove from deck & update deck_listbox
    deck_cards.remove(trait_idx)
    btn_clear_trait_search()

    # update scoring, stars & genes
    update_stars()
    update_genes()
    update_scoring()

    # update all trait piles
    for p in range(n_player.get()):
        create_trait_pile(player_rb_frames[p], p)

    # play sound bites
    play(trait)


def btn_play_worlds_end():
    # do nothing if no catastrophy selected
    if worlds_end_cbox[0].current() == 0:
        print(">>> world's end <<< ERROR - no event selected")
        return

    # print log
    print(">>> world's end <<< '{}' is happening now...".format(worlds_end.get()))

    # update scoring
    update_scoring()

    # update all trait piles
    for p in range(n_player.get()):
        create_trait_pile(player_rb_frames[p], p)


def btn_play_catastrophe(event, c):
    # get played catastrophe
    cbox_idx = event.widget.current()
    played_str = event.widget.get()
    played_before = catastrophies_played[c]
    if cbox_idx > 0:
        played_idx = catastrophies_possible[c][cbox_idx-1]

    # return, if no catastrophe was selected
    if cbox_idx == 0:
        if played_before is not None:
            old_cbox_idx = catastrophies_possible[c].index(played_before) + 1
            catastrophies_cbox[c].current(old_cbox_idx)
        print(">>> catastrophe <<< ERROR - no catastrophe selected")
        return

    # return, if same catastrophe selected
    if played_before == played_idx:
        print(">>> catastrophe <<< ERROR - same catastrophe selected as before")
        return

    # print log
    print(">>> catastrophe <<< played catastrophe #{}: '{}' (id:{})"
          .format(c+1, played_str, played_idx))

    # set played catastrophe
    catastrophies_played[c] = played_idx

    # update possible catastrophies for later ones
    for i in range(1, n_catastrophies.get()):
        # reset possible's
        catastrophies_possible[i] = catastrophies_dfi.copy()

        # remove previous catastrophies from possible's
        for prev in range(0, i):
            if catastrophies_played[prev] is not None:
                catastrophies_possible[i].remove(catastrophies_played[prev])

                pos_cat_values = [" catastrophe {}...".format(1+1)] + \
                    ages_df.loc[catastrophies_possible[i]].name.values.tolist()
                catastrophies_cbox[i].configure(values=pos_cat_values)

                # check if current catastrophie was selected by a next one
                if catastrophies_played[prev] == catastrophies_played[i]:
                    # reset i'th catastrophe
                    catastrophies_played[i] = None
                    catastrophies_cbox[i].current(0)

                    # disable forthcoming catastrophies & worlds end
                    for z in range(i+1, n_catastrophies.get()):
                        catastrophies_cbox[z].configure(state="disabled")
                        worlds_end_cbox[0].configure(state="disabled")

    # enable next catastrophe
    if c < n_catastrophies.get()-1:
        catastrophies_cbox[c+1].configure(state="readonly")
    else:
        worlds_end_cbox[0].configure(state="readonly")

    # update worlds end combobox
    played_catastrophies = [ages_df.loc[catastrophies_played[i], "name"]
                            for i in range(n_catastrophies.get())
                            if catastrophies_played[i] is not None]
    worlds_end_cbox[0]['values'] = [" select world's end ..."] + played_catastrophies

    # update genes & scoring
    update_genes()
    update_scoring()

    # update all trait piles
    for p in range(n_player.get()):
        create_trait_pile(player_rb_frames[p], p)


def update_manual_we(event, p):
    value = event.widget.get()

    # check if input is numeric
    if (value.isnumeric() or (len(value) > 1 and value.lstrip('-').isnumeric())):
        # check limit of (hard-coded) 20
        if int(value) > 20:
            value = '20'
            player_we_effects[p].set(value)
        if int(value) < -20:
            value = '-20'
            player_we_effects[p].set(value)

        # update scoring
        update_scoring()

        # update this players trait pile
        create_trait_pile(player_rb_frames[p], p)


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
    create_trait_pile(player_rb_frames[p], p)


def update_traits_current_status(todo, *args):
    match todo:
        case 'reset':
            trait = args[0]
            rule = args[1]
            log = args[-1]

            # backup current state
            bkp = traits_df.loc[trait].copy()

            # reset trait
            true_color = traits_df.loc[trait].color
            true_face = traits_df.loc[trait].face

            traits_df.loc[trait, "cur_color"] = true_color
            traits_df.loc[trait, "cur_face"] = true_face
            traits_df.loc[trait, "cur_drops"] = np.nan
            traits_df.loc[trait, "cur_effect"] = 'none'
            traits_df.loc[trait, "cur_host"] = 'none'
            traits_df.loc[trait, "cur_attachment"] = 'none'
            traits_df.loc[trait, "cur_worlds_end_trait"] = 'none'

            # apply rule after resetting
            match rule:
                case "keep_cur_effect":
                    traits_df.loc[trait, "cur_effect"] = bkp.cur_effect

            # print log
            if log:
                print(">>> current effects <<< '{}' is reseted to defaults"
                      .format(traits_df.loc[trait].trait))

        case 'attachment':
            host = args[0]
            attachment = args[1]

            # save attachment to host
            traits_df.loc[host, 'cur_attachment'] = attachment

            # get effects of attachments from rules.py & update current status of host
            effects = at_rules.attachment_effects(traits_df, host, attachment)
            traits_df.loc[host, "cur_color"] = effects['color']
            traits_df.loc[host, "cur_face"] = effects['face']
            traits_df.loc[host, "cur_effect"] = effects['effect']

            # print log
            print(">>> current effects <<< '{}' is updated due to effects of '{}'"
                  .format(traits_df.loc[host].trait, traits_df.loc[attachment].trait))

        case 'worlds_end':
            trait_idx = args[0]
            trait_pile = args[1]

            # call rules_function to update other current_values due to current effect
            twe_rules.traits_WE_effects(traits_df, trait_idx, trait_pile)

        case 'neoteny':
            neoteny_idx = traits_df.index[traits_df.trait == 'Neoteny'].tolist()[0]
            p = args[0]

            # set other player to 0
            for i in range(n_player.get()):
                if i != p:
                    neoteny_checkbutton[i].set(0)

            # update 'cur_effect'
            if not any([i.get() for i in neoteny_checkbutton]):
                print('_no one_')
                traits_df.loc[neoteny_idx, "cur_effect"] = 'none'
            else:
                print('_that one: {} _'.format(p))
                traits_df.loc[neoteny_idx, "cur_effect"] = str(p)

            # update scoreboard
            update_scoring()

            # update all trait piles
            for p in range(n_player.get()):
                create_trait_pile(player_rb_frames[p], p)

        case 'update_all':
            update_stars()
            update_genes()
            update_scoring()

            # update all trait piles
            for p in range(n_player.get()):
                create_trait_pile(player_rb_frames[p], p)


def update_scoring():
    for p in range(n_player.get()):
        # get cards
        trait_pile = player_traits[p]

        # calculate world's end points
        p_worlds_end = we_rules.worlds_end(traits_df, worlds_end.get(), player_traits,
                                           p, player_genes, player_we_effects)

        # calculate face value
        p_face = int(sum([traits_df.loc[trait_idx].cur_face for trait_idx in trait_pile
                          if not isinstance(traits_df.loc[trait_idx].cur_face, str)]))

        # calculate drops points
        p_drop = dr_rules.drop_points(traits_df, player_traits, p, player_genes)

        # calculate drops points
        p_MOL = 0
        for x in [x.get() for x in player_MOLs[p]]:
            if x.isnumeric():
                p_MOL += int(x)

        # calculate total score
        total = p_face + p_drop + p_worlds_end + p_MOL

        # update points
        player_points[p]['face'].set(p_face)
        player_points[p]['drops'].set(p_drop)
        player_points[p]['worlds_end'].set(p_worlds_end)
        player_points[p]['MOL'].set(p_MOL)
        player_points[p]['total'].set(total)

        # print log, only if points changed
        print(">>> scoring <<< current points 4 '{}': face = {}  |  drops = {}  |  WE = {}  |  MOL = {}  |  total = {}"
              .format(player_name[p].get(), p_face, p_drop, p_worlds_end, p_MOL, total))


def update_genes():
    # init vars
    diff_genes = [0] * n_player.get()

    # loop players and calculate +- genes of all played traits --------------------------
    for p in range(n_player.get()):
        # loop traits in trait_pile
        for trait_idx in player_traits[p]:
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
                        case 'other':
                            diff_genes = [i+value if i != p else i for i in diff_genes]

                # print log
                print(">>> genes <<< '{}'s '{}' has gene effect off '{}' on '{}' -> current effect: {}"
                      .format(player_name[p].get(), traits_df.loc[trait_idx].trait, value, who, diff_genes))

    # check what catastrophies were played alread ---------------------------------------
    for c in range(n_catastrophies.get()):
        # get card & effect
        c_idx = catastrophies_played[c]

        # check if catastrophy was played
        if c_idx is not None:
            c_str = ages_df.loc[c_idx, "name"]
            # get effect and apply it
            effect = int(ages_df.loc[c_idx].gene_pool)
            diff_genes = [i + effect for i in diff_genes]

            # print log
            print(">>> genes <<< catastrophe '{}' has gene effect off '{}' -> current effect: {}"
                  .format(c_str, effect, diff_genes))

    # check for special effects by specific traits --------------------------------------
    # Spores
    sprs_idx = traits_df.index[traits_df.trait == 'Spores'].tolist()[0]
    sprs_eff = traits_df.loc[sprs_idx].cur_effect
    if sprs_eff != 'none':
        if '_' in sprs_eff:
            sprs_eff = sprs_eff.split('_')

        for eff in sprs_eff:
            if eff.isnumeric() and int(eff) < n_player.get():
                p = int(eff)
                diff_genes[p] += 1

                # print log
                print(">>> genes <<< 'Spores' (id:{}) has an gene effect (+1) on '{}' -> current effect: {}"
                      .format(sprs_idx, player_name[p].get(), diff_genes))

    # Sleepy
    slp_idx = traits_df.index[traits_df.trait == 'Sleepy'].tolist()[0]
    if any(slp_idx in tp for tp in player_traits):
        slp_eff = [i.get() for i in sleepy_spinbox]
        diff_genes = [diff_genes[x]+slp_eff[x] for x in range(len(diff_genes))]
        if any(slp_eff):
            p = [i for i, e in enumerate(slp_eff) if e != 0]
            print(">>> genes <<< 'Sleepy' (id:?) has an gene effect on '{}' by {} -> current effect: {}"
                  .format(player_name[p[0]].get(), slp_eff[p[0]], diff_genes))
    else:  # sleepy in no trait pile -> reset values
        for i in range(n_player.get()):
            sleepy_spinbox[i].set(0)

    # update gene values ----------------------------------------------------------------
    for p in range(n_player.get()):
        new_gp = n_genes.get() + diff_genes[p]
        if new_gp > 8:
            player_genes[p].set(8)
        elif new_gp < 1:
            player_genes[p].set(1)
        else:
            player_genes[p].set(new_gp)

    # print log - if genes are effected
    if any(i > 0 for i in diff_genes):
        print("   >>> total gene effect: {} -> new gene pools are {}"
              .format(diff_genes, [player_genes[i].get() for i in range(n_player.get())]))


def update_stars():
    # loop players
    for p in range(n_player.get()):
        # number of dominant traits
        n_dominant = np.nansum([traits_df.loc[trait_idx].dominant for trait_idx in player_traits[p]])

        # find label widgets
        tmp_frame = frames_player[p].winfo_children()
        lbl1 = frames_player[p].nametowidget(str(tmp_frame[0]) + '.!label2')
        lbl2 = frames_player[p].nametowidget(str(tmp_frame[0]) + '.!label3')

        # edit images
        lbl1.configure(image=images['no_star'])
        lbl2.configure(image=images['no_star'])
        if n_dominant > 0:
            lbl1.configure(image=images['star'])
            if n_dominant > 1:
                lbl2.configure(image=images['star'])


def search_trait_in_list(inp):
    value = inp.get()
    lbox_traits[0].selection_clear(0, tk.END)

    if value == "":
        lbox_cards_idx.set(deck_cards)
        lbox_cards_str.set(traits_df.loc[deck_cards].trait.values.tolist())
    else:
        filtered_trait_str = []
        filtered_trait_idx = []
        for idx in deck_cards:
            if value.lower() in traits_df.loc[idx].trait.lower():
                filtered_trait_idx.append(idx)
                filtered_trait_str.append(traits_df.loc[idx].trait)

        lbox_cards_idx.set(filtered_trait_idx)
        lbox_cards_str.set(filtered_trait_str)


def update_selected_trait(where, idx):
    # select trait in deck/listbox
    if where == "lbox":
        # trait in DECK is selected as 'play_trait'
        global play_trait
        play_trait = lbox_cards_idx.get()[idx[0]]

        # print log
        print(">>> select <<< handle DECK_listbox -> selected trait = '{}' (id:{})"
              .format(traits_df.loc[play_trait].trait, play_trait))

    # select trait in one of players trait pile
    else:
        # note: 'where'  == 'who'
        player_trait_selected[where].set(idx.get())

        # print log
        print(">>> select <<< handle PLAYER_listbox -> selected trait = '{}' is selecting '{}' (id:{})"
              .format(player_name[where].get(), traits_df.loc[idx.get()].trait, idx.get()))


def create_trait_pile(frame_trait_overview, p):
    # first, clean up frame
    for w in frame_trait_overview.grid_slaves():
        w.grid_forget()

    # loop traits in pile
    irow = -1
    for trait_idx in player_traits[p]:
        # get trait name
        trait = traits_df.loc[trait_idx].trait

        # init some vars
        ypad = (3, 0) if irow == 0 else 0
        irow += 1

        # ----- radiobutton -----------------------------------------------------------------------
        rb_trait = tk.Radiobutton(
            frame_trait_overview,
            text=" " + trait,
            variable=player_trait_selected[p],
            value=trait_idx,
            command=lambda: update_selected_trait(p, player_trait_selected[p]))
        rb_trait.grid(row=irow, column=0, padx=3, pady=ypad, sticky='nsw')

        # change font color if dominant
        if traits_df.loc[trait_idx].dominant == 1:
            rb_trait.config(fg=defaults["font_color_trait_pile_dominant"])

        # ----- icons -----------------------------------------------------------------------------
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
        if show_icons['face'] and 'face' not in traits_df.loc[trait_idx].cur_worlds_end_effect.lower():
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

        # ----- current effects due to attachments ------------------------------------------------
        # _current_ color ----------
        cur_color = traits_df.loc[trait_idx].cur_color.lower()
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
        cur_drops = traits_df.loc[trait_idx].cur_drops
        if not np.isnan(cur_drops):
            icol += 1
            drop_string = str(int(cur_drops))

            tk.Label(
                frame_pics,
                image=images[drop_string]
                ).grid(row=0, column=icol)

        # has attachment ----------
        if traits_df.loc[trait_idx].cur_attachment != 'none':
            icol += 1
            tk.Label(
                frame_pics,
                image=images['attachment']
                ).grid(row=0, column=icol)

        # noFX ----------
        if 'Inactive' in traits_df.loc[trait_idx].cur_effect:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noFX']
                ).grid(row=0, column=icol)

        # noRemove ----------
        if 'NoRemove' in traits_df.loc[trait_idx].cur_effect:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noRemove']
                ).grid(row=0, column=icol)

        # noDiscard ----------
        if 'NoDiscard' in traits_df.loc[trait_idx].cur_effect:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noDiscard']
                ).grid(row=0, column=icol)

        # noSteal ----------
        if 'NoSteal' in traits_df.loc[trait_idx].cur_effect:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noSteal']
                ).grid(row=0, column=icol)

        # noSwap ----------
        if 'NoSwap' in traits_df.loc[trait_idx].cur_effect:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noSwap']
                ).grid(row=0, column=icol)

        # ----- current effects due to WORLDS END -------------------------------------------------
        if traits_df.loc[trait_idx].cur_worlds_end_effect != 'none':
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

        # ----- manual DROP points entry ----------------------------------------------------------
        cur_drop_eff = traits_df.loc[trait_idx].effect_drop
        if (isinstance(cur_drop_eff, str) and not isinstance(traits_df.loc[trait_idx].effect_worlds_end, str)
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

        # ----- ATTACHMENT combobox if trait is attachment ----------------------------------------
        if traits_df.loc[trait_idx].attachment == 1:
            irow += 1
            tk.Label(
                frame_trait_overview,
                text="Attach to:"
                ).grid(row=irow, column=0, padx=(40, 0), sticky='e')

            # filter only non-attachment-traits and check if this is already attached to a trait
            traits_filtered_idx = [None] + at_rules.filter_attachables(traits_df, player_traits[p], trait_idx)
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
            if traits_df.loc[trait_idx].cur_host == 'none':
                cbox_attach_to.current(0)
            else:
                cur_host = traits_df.loc[trait_idx].cur_host
                cbox_attach_to.current(traits_filtered_idx.index(cur_host))

        # ----- WORLDS_END combobox if trait has worlds end effect --------------------------------
        if isinstance(traits_df.loc[trait_idx].effect_worlds_end, str):
            irow += 1
            tk.Label(
                frame_trait_overview,
                text="Worlds End:"
                ).grid(row=irow, column=0, padx=(40, 0), sticky='e')

            # get task what to do at worlds end
            we_effect = twe_rules.traits_WE_tasks(traits_df, trait_idx)

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

        # ----- SLEEPY may affect gene pool ?!?!  -------------------------------------------------
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
    if any([viral_idx in tp for tp in player_traits]) and viral_idx not in player_traits[p]:
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

            print("Viral acts on '{}' traits in '{}'s trait pile -> drop points = {}"
                  .format(we_viral, player_name[p].get(), vp_s[p]))

    # --- AMATOXINS --- add passively Amatoxins to this trait pile ---------------
    amatoxins_idx = traits_df.index[traits_df.trait == 'Amatoxins'].tolist()[0]
    if any([amatoxins_idx in tp for tp in player_traits]) and amatoxins_idx not in player_traits[p]:
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

            print("Amatoxins' effect is based on amount of discraded colors -> drop points = {}"
                  .format(we_drops))

    # --- PROWLER --- add passively Prowler to this trait pile ---------------
    prowler_idx = traits_df.index[traits_df.trait == 'Prowler'].tolist()[0]
    if any([prowler_idx in tp for tp in player_traits]) and prowler_idx not in player_traits[p]:
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

        print("Viral acts on 'color_count' in '{}'s trait pile -> drop points = {}"
              .format(player_name[p].get(), vp_s[p]))

    # --- SHINY --- add passively Shiny to this trait pile ---------------
    shiny_idx = traits_df.index[traits_df.trait == 'Shiny'].tolist()[0]
    if any([shiny_idx in tp for tp in player_traits]) and shiny_idx not in player_traits[p]:
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

        print("Shiny acts on 'colorless' traits in '{}'s trait pile -> drop points = {}"
              .format(player_name[p].get(), vp_s[p]))

    # --- NEOTENY --- check button if Neoteny is in your hand ------------
    # is NEOTENY in your hand? asked via checkbox? But only if its not pöayed
    neoteny_idx = traits_df.index[traits_df.trait == 'Neoteny'].tolist()[0]
    if "select world's end" not in worlds_end.get() and all(neoteny_idx not in tp for tp in player_traits):
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

    # ******* !!! *** special, individual case *** !!! *******************

    # **********************************************************************************************
    # ------ worlds end -> manual entries ---------------------------------------------------------
    if "select world's end" not in worlds_end.get():
        irow += 1
        ttk.Separator(frame_trait_overview, orient='horizontal'
                      ).grid(row=irow, column=0, columnspan=2, padx=5, pady=10, sticky='we')

        # get world's end name & index
        we = worlds_end.get()
        we_idx = ages_df[ages_df['name'] == we].index.values[0]
        we_eff = ages_df.loc[we_idx].worlds_end

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
                                 textvariable=player_we_effects[p],
                                 justify=tk.CENTER,
                                 width=3)
            we_entry.grid(row=0, column=1)
            we_entry.bind("<KeyRelease>", lambda e: update_manual_we(e, p))

        else:
            we_points = str(player_points[p]['worlds_end'].get())
            tk.Label(frame_weB, image=images[we_points],
                     ).grid(row=0, column=1, sticky='w')


def create_player_frame(p):
    border = defaults["color_frame_width"]

    frame = tk.Frame(frame_playground, bg=defaults["player_frame_color"])
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
    ttk.Label(frame_points, textvariable=player_name[p], style="name.TLabel"
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

    ttk.Label(frame_points, textvariable=player_points[p]['face'], style="points.TLabel"
              ).grid(row=1, column=1, sticky="sw")
    ttk.Label(frame_points, textvariable=player_points[p]['drops'], style="points.TLabel"
              ).grid(row=1, column=3, sticky="sw")
    ttk.Label(frame_points, textvariable=player_points[p]['worlds_end'], style="points.TLabel"
              ).grid(row=2, column=1, sticky="w")
    ttk.Label(frame_points, textvariable=player_points[p]['MOL'], style="points.TLabel"
              ).grid(row=2, column=3, sticky="w")

    # total points
    ttk.Label(frame_points, textvariable=player_points[p]['total'], style="total.TLabel"
              ).grid(row=1, column=4, rowspan=2, padx=0, pady=0, sticky='ns')

    # gene pool
    ttk.Label(frame_points, text="gene pool"
              ).grid(row=1, column=5, columnspan=2, padx=0, pady=0, sticky='s')

    ttk.Label(frame_points, textvariable=player_genes[p], style="genes.TLabel"
              ).grid(row=2, column=5, columnspan=2, padx=0, pady=0, sticky='n')

    # ----- list of traits played ----------------------------------------
    frame_traits = tk.Frame(frame)
    frame_traits.grid(row=1, column=0, padx=border, pady=(0, border), sticky="nesw")
    frame_traits.rowconfigure(2, weight=1)
    frame_traits.columnconfigure(0, weight=1)  # for left button under trait-pile
    frame_traits.columnconfigure(1, weight=1)  # for right button under trait-pile

    player_rb_frames[p] = tk.Frame(frame_traits)
    player_rb_frames[p].grid(row=0, column=0, columnspan=2, sticky='nesw', padx=border, pady=border)
    player_rb_frames[p].columnconfigure(1, weight=1)  # for left button under trait-pile
    create_trait_pile(player_rb_frames[p], p)

    # action buttons -----
    ttk.Separator(
        frame_traits, orient='horizontal'
        ).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='we')

    cbox_move_to = ttk.Combobox(
        frame_traits,
        height=n_player,
        values=[" move trait to ..."] + defaults["names"][:n_player.get()],
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
        text="discard trait",
        command=partial(btn_discard_trait, p),
    ).grid(row=2, column=1, pady=(0, border), sticky='n')

    # ----- Meaning of Life -------------------------------------
    frame_MOL = tk.Frame(frame)
    frame_MOL.grid(row=2, column=0, padx=border, pady=(0, border), sticky="nesw")

    ttk.Label(frame_MOL, text="Meaning of Life", font="'' 18"
              ).grid(row=0, column=0, padx=5, columnspan=2*n_MOLs.get(), sticky='ns')

    for m in range(n_MOLs.get()):
        frame_MOL.columnconfigure(2*m, weight=1)
        frame_MOL.columnconfigure(2*m+1, weight=1)

        ttk.Label(frame_MOL,
                  text="MOL #{}:".format(m+1)
                  ).grid(row=1, column=2*m, sticky='e')
        MOL_ent = ttk.Entry(frame_MOL,
                            width=4,
                            textvariable=player_MOLs[p][m])
        MOL_ent.grid(row=1, column=2*m+1, sticky='w')
        MOL_ent.bind("<KeyRelease>", lambda e: update_scoring())
    return frame


def create_menu_frame():
    border = defaults["color_frame_width"]

    frame_menu.columnconfigure(0, weight=1)
    frame_menu.rowconfigure(0, weight=1)
    frame_menu.rowconfigure(1, weight=1)
    frame_menu.rowconfigure(2, weight=4)
    frame_menu.rowconfigure(3, weight=1)

    # ----- frame 4 options -------------------------------------------------------------
    frame_menu_options = tk.Frame(frame_menu)
    frame_menu_options.grid(row=0, column=0, padx=border, pady=border, sticky="nesw")
    frame_menu_options.columnconfigure(0, weight=1)
    frame_menu_options.columnconfigure(1, weight=1)

    # title -----
    frame_title = tk.Frame(frame_menu_options)
    frame_title.grid(row=0, column=0, columnspan=2, sticky="nesw")
    frame_title.columnconfigure(0, weight=3)

    ttk.Label(
        frame_title,
        text="OPTIONS",
        font="'' 24"
        ).grid(row=0, column=0, pady=(5, 5))
    music_lbl[0] = ttk.Label(
        frame_title,
        image=images['note_off'],
        cursor="heart")
    music_lbl[0].grid(row=0, column=1, padx=(0, 10))
    music_lbl[0].bind("<Button-1>", lambda e: switch_music())

    # nr players -----
    ttk.Label(
        frame_menu_options,
        text="# players: ",
    ).grid(row=1, column=0, sticky='e')
    ttk.Spinbox(
        frame_menu_options,
        from_=2,
        to=defaults["max_player"],
        width=3,
        textvariable=opt_n_player,
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
        textvariable=opt_n_genes,
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
        textvariable=opt_n_catastrophies,
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
        textvariable=opt_n_MOLs,
        wrap=False
    ).grid(row=4, column=1, sticky='w')

    # restart button -----
    ttk.Button(
        frame_menu_options,
        text="restart game",
        command=start_game,
    ).grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    # info current game -----
    ttk.Label(
        frame_menu_options,
        text="running game",
        font="'' 12 underline",
    ).grid(row=6, column=0, columnspan=2)
    ttk.Label(
        frame_menu_options,
        text="{} catastrophies + {} genes + {} MOLs"
        .format(n_catastrophies.get(), n_genes.get(), n_MOLs.get()),
        style="game_info.TLabel",
    ).grid(row=7, column=0, columnspan=2, pady=(0, 5))

    # ----- frame 4 player names --------------------------------------------------------
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
    for i in range(n_player.get()):
        ttk.Label(
            frame_menu_names,
            text="player {}: ".format(i+1),
        ).grid(row=i+1, column=0, sticky='e')
        ttk.Entry(
            frame_menu_names,
            textvariable=player_name[i],
            width=8,
        ).grid(row=i+1, column=1, sticky='w')

    # ----- frame 4 trait selection -----------------------------------------------------
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
    trait_ent = ttk.Entry(
        frame_menu_traits,
        width=10,
        textvariable=search_trait)
    trait_ent.grid(row=1, column=0, padx=(10, 0), sticky="w")
    trait_ent.bind("<KeyRelease>", lambda e: search_trait_in_list(search_trait))
    trait_ent.bind('<Down>', lambda e: lbox_traits[0].focus(), add='+')         # down arrow key is pressed
    trait_ent.bind('<Down>', lambda e: lbox_traits[0].selection_set(0), add='+')
    trait_ent.bind('<Down>', lambda e: update_selected_trait("lbox", lbox_traits[0].curselection()), add='+')

    ttk.Button(
        frame_menu_traits,
        text="clear",
        width=4,
        command=btn_clear_trait_search,
    ).grid(row=1, column=1, padx=(0, 10), sticky="w")

    # listbox with (filtered) deck-cards -----
    lbox_traits[0] = tk.Listbox(
        frame_menu_traits,
        height=4,
        listvariable=lbox_cards_str,
        exportselection=False)
    lbox_traits[0].grid(row=2, column=0, columnspan=2, padx=10)
    lbox_traits[0].bind("<<ListboxSelect>>",
                        lambda e: update_selected_trait("lbox", lbox_traits[0].curselection()))
    # create key bindings to play trait into player's trait pile by hitting number on keyboard
    for p in range(n_player.get()):
        lbox_traits[0].bind('{}'.format(p+1), lambda e, pp=p: btn_play_trait(pp))

    # 'who gets it?' -----
    ttk.Label(
        frame_menu_traits,
        text="who gets the trait?",
        font="'' 18",
    ).grid(row=3, column=0, columnspan=2, pady=(10, 0))

    # player buttons -----
    frame_menu_buttons = tk.Frame(frame_menu_traits)
    frame_menu_buttons.grid(row=4, column=0, columnspan=2, pady=(0, 5))
    for i in range(n_player.get()):
        clspn = int(i + 1 == n_player.get() and (i + 1) % 2 == 1) + 1
        ttk.Button(
            frame_menu_buttons,
            textvariable=player_name[i],
            command=partial(btn_play_trait, i),
        ).grid(row=floor(i / 2), column=i % 2, columnspan=clspn)

    # ----- frame 4 catastrophy selection -----------------------------------------------
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
    for c in range(n_catastrophies.get()):
        pos_cat_values = [" catastrophe {}...".format(c+1)] + \
            ages_df.loc[catastrophies_possible[c]].name.values.tolist()

        catastrophies_cbox[c] = ttk.Combobox(
            frame_menu_catastrophe,
            values=pos_cat_values,
            exportselection=0,
            state="readonly" if c == 0 else "disabled",
            width=18,
            style="move.TCombobox")
        catastrophies_cbox[c].current(0)
        catastrophies_cbox[c].grid(row=c+1, column=0, columnspan=2, padx=4, sticky='ns')
        catastrophies_cbox[c].bind("<<ComboboxSelected>>", lambda ev, c=c: btn_play_catastrophe(ev, c))

    # world's end -----
    ttk.Label(
        frame_menu_catastrophe,
        text="World's End",
        font="'' 18",
    ).grid(row=n_catastrophies.get()+1, column=0, columnspan=2, pady=(5, 0))

    worlds_end_cbox[0] = ttk.Combobox(
        frame_menu_catastrophe,
        values=[" select world's end ..."],
        exportselection=0,
        state="disabled",
        width=18,
        style="move.TCombobox",
        textvariable=worlds_end)
    worlds_end_cbox[0].current(0)
    worlds_end_cbox[0].grid(row=n_catastrophies.get()+2, column=0, columnspan=2, padx=4, pady=(0, 5), sticky='ns')
    worlds_end_cbox[0].bind("<<ComboboxSelected>>", lambda e: btn_play_worlds_end())

    # ----- frame for control buttons ---------------------------------------------------
    frame_menu_controls = tk.Frame(frame_menu)
    frame_menu_controls.grid(row=4, column=0, padx=border, pady=(0, border), sticky="nesw")
    frame_menu_controls.columnconfigure(0, weight=0)
    frame_menu_controls.columnconfigure(1, weight=0)
    frame_menu_controls.columnconfigure(1, weight=1)

    ttk.Checkbutton(frame_menu_controls,
                    variable=icons_onoff,
                    command=switch_icons
                    ).grid(row=0, column=0, padx=(10, 0))
    ttk.Button(frame_menu_controls,
               image=images['no_star'],
               command=pre_play,
               width=2
               ).grid(row=0, column=1, padx=5)
    ttk.Button(frame_menu_controls,
               text="quit",
               command=root.quit
               ).grid(row=0, column=2, padx=(0, 10), pady=5, sticky="we")


def reset_variables():
    # update current settings
    n_player.set(opt_n_player.get())
    n_genes.set(opt_n_genes.get())
    n_catastrophies.set(opt_n_catastrophies.get())
    n_MOLs.set(opt_n_MOLs.get())

    # save previous names
    last_names = player_name.copy()

    # reset _player_ variables
    frames_player.clear()
    player_name.clear()
    player_genes.clear()
    player_points.clear()
    player_traits.clear()
    player_trait_selected.clear()
    player_rb_frames.clear()
    player_we_effects.clear()
    player_MOLs.clear()

    neoteny_checkbutton.clear()
    sleepy_spinbox.clear()

    # fill variables
    for i in range(n_player.get()):
        if len(last_names) >= i+1:
            player_name.append(tk.StringVar(value=last_names[i].get()))
            print("   >>> use *previous* name for player #{} = {}".format(i+1, player_name[i].get()))
        else:
            player_name.append(tk.StringVar(value=defaults["names"][i]))
            print("   >>> use *default* name for player #{} = {}".format(i+1, player_name[i].get()))

        player_genes.append(tk.IntVar(value=n_genes.get()))
        player_points.append({'face': tk.IntVar(value=0), 'drops': tk.IntVar(value=0),
                              'worlds_end': tk.IntVar(value=0), 'MOL': tk.IntVar(value=0),
                              'total': tk.IntVar(value=0)})
        player_traits.append([])
        player_trait_selected.append(tk.Variable(value=np.nan))
        player_rb_frames.append(None)
        player_we_effects.append(tk.StringVar(value='0'))
        player_MOLs.append([])
        neoteny_checkbutton.append(tk.IntVar(value=0))
        sleepy_spinbox.append(tk.IntVar(value=0))

        for m in range(n_MOLs.get()):
            player_MOLs[i].append(tk.StringVar(value="0"))  # for now, manually editing MOL points in entries

    # reset deck/lbox card-lists
    deck_cards.clear()
    deck_cards.extend(traits_dfi)   # complete list of indicies of all traits
    lbox_cards_idx.set(traits_dfi)  # complete list of indices of traits for menu_listbox
    lbox_cards_str.set(traits_df.loc[traits_dfi].trait.values.tolist())  # complete list of names of traits

    # reset manually calculated drop values
    manual_drops.clear()
    for i in range(len(traits_dfi)):
        manual_drops.append(tk.StringVar(value='-'))

    # reset occured catastrophies
    catastrophies_possible.clear()
    catastrophies_played.clear()
    catastrophies_cbox.clear()
    for i in range(n_catastrophies.get()):
        catastrophies_possible.append(catastrophies_dfi.copy())
        catastrophies_played.append(None)
        catastrophies_cbox.append([])
    worlds_end_cbox[0] = None

    # reset current status
    traits_df["cur_color"] = traits_df.color
    traits_df["cur_face"] = traits_df.face
    traits_df["cur_drops"] = np.nan
    traits_df["cur_effect"] = 'none'
    traits_df["cur_host"] = 'none'
    traits_df["cur_attachment"] = 'none'
    traits_df["cur_worlds_end_trait"] = 'none'
    traits_df["cur_worlds_end_effect"] = 'none'


def start_game():
    # reset variables ----------------------------------------------------
    print(">>> initialize <<< reset variables")
    reset_variables()
    switch_icons()

    # update frame_configurations settings -------------------------------
    for w in frame_menu.grid_slaves():
        w.grid_forget()

    for w in frame_playground.grid_slaves():
        w.grid_forget()

    for i in range(defaults["max_player"]):
        w = 0 if i >= n_player.get() else 1  # w=1 -> player_frames are stretchable
        frame_playground.columnconfigure(i, weight=w)

    # fill _menu_ frame --------------------------------------------------
    print(">>> initialize <<< create menu")
    create_menu_frame()

    # fill _playground_ frame with _player_ frames -----------------------
    print(">>> initialize <<< create playground")
    for i in range(n_player.get()):
        # frame_playground.columnconfigure(i, weight=1)
        frames_player.append(create_player_frame(i))

    # clear traits listbox -----------------------------------------------
    btn_clear_trait_search()


##########################################################################
# create a window --------------------------------------------------------
root = tk.Tk()
root.title("LIVE Doomlings Calculator")
root.geometry("1600x900")
root.configure(background="grey")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# styling ----------------------------------------------------------------
gui_style = ttk.Style()
gui_style.configure("game_info.TLabel", font=("", 10, "italic"))
gui_style.configure("name.TLabel", font=("Comic Sans MS", 36, "bold"))
gui_style.configure("points.TLabel", font=("", 20))
gui_style.configure("total.TLabel", font=("", 80, "bold"), foreground="orangered1")
gui_style.configure("genes.TLabel", font=("", 38, "bold"), foreground="hotpink1")
gui_style.configure("move.TCombobox", selectbackground="none")

# load images ------------------------------------------------------------
images = {}
for k, v in images_dict.items():
    images[k] = ImageTk.PhotoImage(v)

# init variables ---------------------------------------------------------
music_onoff = tk.IntVar(value=0)
music_lbl = [None]
icons_onoff = tk.IntVar(value=0)
show_icons = {}

opt_n_player = tk.IntVar(value=defaults["n_player"])                # OPTIONS: number of players
opt_n_genes = tk.IntVar(value=defaults["n_genes"])                  # OPTIONS: gene pool at beginning
opt_n_catastrophies = tk.IntVar(value=defaults["n_catastrophies"])  # OPTIONS: number of catastrophies
opt_n_MOLs = tk.IntVar(value=defaults["n_MOLs"])                    # OPTIONS: number of MOLs

n_player = tk.IntVar()          # number of current players
n_genes = tk.IntVar()           # gene pool at start
n_catastrophies = tk.IntVar()   # number of catastrophies
n_MOLs = tk.IntVar()            # number of MOLs

search_trait = tk.StringVar(value="")   # searching for traits in playable deck
deck_cards = []                         # all traits in deck (or discard pile) left to be drawn / list of idx
lbox_cards_idx = tk.Variable(value="")  # traits >>shown<< in listbox on the left, i.e. after filtering / list of idx
lbox_cards_str = tk.Variable(value="")  # traits >>shown<< in listbox on the left, i.e. after filtering / as string
play_trait = None                       # selected trait (by index in traits_df) in listbox
lbox_traits = [None]                    # listbox widget of deck cards -> needed to be able to edit selected traits
manual_drops = []                       # list to save manual drop entries to

catastrophies_possible = []                  # occured catastrophies / StringVar
catastrophies_played = []                  # occured catastrophies / StringVar
catastrophies_cbox = []             # comboxes containing possible catastrophies
worlds_end_cbox = [None]
worlds_end = tk.StringVar(value="")

frames_player = []          # list of all players frames
player_name = []            # current players names / tk.StringVar
player_genes = []           # current players gene pool / tk.IntVar
player_points = []          # current players points / dictionary
player_traits = []          # current players traits played / lists
player_trait_selected = []  # selected traits in players trait piles / StringVar
player_rb_frames = []       # frame containing players traits -> needed to be able to edit selected traits
player_we_effects = []      # frame containing players traits -> needed to be able to edit selected traits
player_MOLs = []            # list of lists containing MOLs for each player

neoteny_checkbutton = []
sleepy_spinbox = []

# create _content_ frame -------------------------------------------------
content = tk.Frame(root, width=1200, height=800, bg=defaults["bg_content"])
content.grid(column=0, row=0, sticky="nesw")
content.columnconfigure(0, weight=0)  # menu on the left
content.columnconfigure(1, weight=1)  # complete playground, set =1 to stretch it to the right side

# create _menu_ frame ----------------------------------------------------
frame_menu = tk.Frame(content, bg=defaults["menu_frame_color"])
frame_menu.grid(row=0, column=0, padx=5, pady=5, stick="nesw")

# create _playground_ frame ----------------------------------------------
frame_playground = tk.Frame(content, bg=defaults["bg_content"])
frame_playground.grid(row=0, column=1, padx=0, pady=0, stick="nesw")
frame_playground.rowconfigure(0, weight=1)  # stretch playground to bottom

# (re)start game -------------------------------------------------------------
start_game()

# ----- run --------------------------------------------------------------
root.mainloop()
