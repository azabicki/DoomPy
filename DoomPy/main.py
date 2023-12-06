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
import rules as rules


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
traits_df["cur_effect"] = 'none'
traits_df["cur_host"] = 'none'
traits_df["cur_attachment"] = 'none'

# load images ------------------------------------------------------------
img_size_star = 30
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

# switches for icons
show = {}
show['color'] = True
show['face'] = True
show['collection'] = False
show['dominant'] = False
show['action'] = False
show['drops'] = True
show['gene_pool'] = False
show['worlds_end'] = False
show['effectless'] = False
show['attachment'] = False


# functions ##############################################################
def btn_clear_trait_search():
    global play_trait

    search_trait.set("")
    lbox_cards_idx.set(deck_cards)
    lbox_cards_str.set(traits_df.loc[deck_cards].trait.values.tolist())
    lbox_traits[0].selection_clear(0, tk.END)
    play_trait = None


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
        traits_df.loc[attachment, 'cur_host'] = 'none'
    else:
        # set new host_idx to status_row of attachment
        traits_df.loc[attachment, 'cur_host'] = host_idx

        # set new attachment to status_row of host & update effects of attachment on host
        update_traits_current_status('attachment', host_idx, attachment)

    # update trait pile & clear trait selection
    create_trait_pile(player_rb_frames[from_], from_)

    # update scoring
    update_scoring(from_)


def btn_discard_trait(from_):
    # get card & its attachment
    card = player_trait_selected[from_].get()
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

    # remove card(s) from player, update trait pile & clear trait selection
    player_traits[from_].remove(card)
    if attachment != 'none':
        player_traits[from_].remove(attachment)

    create_trait_pile(player_rb_frames[from_], from_)
    player_trait_selected[from_].set(np.nan)

    # add to deck traits & update deck_listbox
    bisect.insort_left(deck_cards, card)
    if attachment != 'none':
        bisect.insort_left(deck_cards, attachment)
    search_trait_in_list(search_trait)  # keep current str in search_entry

    # reset current status of card(s)
    update_traits_current_status('reset', card, [])
    if attachment != 'none':
        update_traits_current_status('reset', attachment, [])

    # update scoring, stars & genes
    update_scoring(from_)
    update_stars()
    update_genes()

    print(traits_df.loc[card].tolist())
    if attachment != 'none':
        print(traits_df.loc[attachment].tolist())


def btn_move_trait(from_, cbox_move_to):
    # get card & its attachment
    card = player_trait_selected[from_].get()
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

    create_trait_pile(player_rb_frames[to], to)

    # update scoring, stars & genes
    update_scoring(from_)
    update_scoring(to)
    update_stars()
    update_genes()

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
    create_trait_pile(player_rb_frames[to], to)

    # remove from deck & update deck_listbox
    deck_cards.remove(trait_idx)
    btn_clear_trait_search()

    # update scoring, stars & genes
    update_scoring(to)
    update_stars()
    update_genes()


def btn_play_worlds_end():
    # do nothing if no catastrophy selected
    if worlds_end.get() == " select world's end ...":
        return

    # print log
    print(">>> world's end <<< '{}' is happening now...".format(worlds_end.get()))

    for i in range(n_player.get()):
        update_scoring(i)


def btn_play_catastrophe(event, c):
    # get & set played catastrophe
    played_catastrophy = event.widget.get()
    catastrophies[c].set(played_catastrophy)

    # update worlds end combobox
    played_catastrophies = [catastrophies[i].get() for i in range(n_catastrophies.get()) if catastrophies[i].get()]
    worlds_end_cbox[0]['values'] = [" select world's end ..."] + played_catastrophies

    # print log
    print(">>> catastrophe <<< played catastrophe #{}: '{}'"
          .format(c+1, played_catastrophy))

    # update genes
    update_genes()


def update_traits_current_status(todo, *args):
    match todo:
        case 'reset':
            trait = args[0]
            log = args[-1]

            # reset trait
            true_color = traits_df.loc[trait].color
            true_face = traits_df.loc[trait].face

            traits_df.loc[trait, "cur_color"] = true_color
            traits_df.loc[trait, "cur_face"] = true_face
            traits_df.loc[trait, "cur_effect"] = 'none'
            traits_df.loc[trait, "cur_host"] = 'none'
            traits_df.loc[trait, "cur_attachment"] = 'none'
            traits_df.loc[trait, "cur_worlds_end"] = 'none'

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
            effects = rules.attachment_effects(traits_df, host, attachment)
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
            rules.traits_WE_effects(traits_df, trait_idx, trait_pile)


def update_scoring(p):
    # get cards
    trait_pile = player_traits[p]

    # calculate face value
    p_face = int(sum([traits_df.loc[trait_idx].face for trait_idx in trait_pile
                      if not isinstance(traits_df.loc[trait_idx].face, str)]))
    player_points[p]['face'].set(p_face)

    # calculate drops points
    p_drop = 0
    player_points[p]['drops'].set(p_drop)

    # calculate world's end points
    p_worlds_end = rules.worlds_end(worlds_end.get(), p, player_traits, traits_df)
    player_points[p]['worlds_end'].set(p_worlds_end)

    # calculate total score
    total = p_face + p_drop + p_worlds_end
    player_points[p]['total'].set(total)

    # print log
    print(">>> scoring <<< current points for '{}': face = {}  |  drops = {}  |  WE = {}  |  total = {}"
          .format(player_name[p].get(), p_face, p_drop, p_worlds_end, total))


def update_genes():
    # init vars
    diff_genes = [0] * n_player.get()

    # loop players and calculate +- genes of all played traits
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

                # apply rule
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

    # check what catastrophies were played alread
    for c in range(n_catastrophies.get()):
        # get card & effect
        card = catastrophies[c].get()
        # check if catastrophy was played
        if card in ages_df.name.values.tolist():
            # get effect and apply it
            effect = int(ages_df[ages_df.name == card]['gene_pool'].values[0])
            diff_genes = [i + effect for i in diff_genes]

            # print log
            print(">>> genes <<< catastrophe '{}' has gene effect off '{}' -> current effect: {}"
                  .format(card, effect, diff_genes))

    # update gene values
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
        # trait in DECK is selected
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

        # ----- radiobutton ----------------------------------------------
        rb_trait = tk.Radiobutton(
            frame_trait_overview,
            text=" " + trait,
            variable=player_trait_selected[p],
            value=trait_idx,
            bg=defaults["bg_trait_pile"],
            fg=defaults["font_color_trait_pile"],
            command=lambda: update_selected_trait(p, player_trait_selected[p]))
        rb_trait.grid(row=irow, column=0, padx=3, pady=ypad, sticky='nsw')

        # change font color if dominant
        if traits_df.loc[trait_idx].dominant == 1:
            rb_trait.config(fg=defaults["font_color_trait_pile_dominant"])

        # ----- icons ----------------------------------------------------
        frame_pics = tk.Frame(frame_trait_overview, bg=defaults["bg_trait_pile"])
        frame_pics.grid(row=irow, column=1, sticky='sw')
        icol = -1  # initialize column index which changes depending on card

        # _true_ color
        if show['color']:
            icol += 1
            color = traits_df.loc[trait_idx].color
            cc = 'c' if 'colorless' in color.lower() else ''
            cb = 'b' if 'blue' in color.lower() else ''
            cg = 'g' if 'green' in color.lower() else ''
            cp = 'p' if 'purple' in color.lower() else ''
            cr = 'r' if 'red' in color.lower() else ''

            tk.Label(
                frame_pics,
                image=images[cc+cb+cg+cp+cr],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # face
        if show['face']:
            icol += 1
            face_value = traits_df.loc[trait_idx].face
            face_string = face_value if isinstance(face_value, str) else str(int(face_value))

            tk.Label(
                frame_pics,
                image=images[face_string],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # collection
        if show['collection']:
            icol += 1
            lbl_collection = tk.Label(
                frame_pics,
                image=images['no_star'],
                bg=defaults["bg_trait_pile"])
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
        if show['dominant'] and traits_df.loc[trait_idx].dominant == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['dominant'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # action
        if show['action'] and traits_df.loc[trait_idx].action == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['action'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # drops
        if show['drops'] and traits_df.loc[trait_idx].drops == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['drops'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # gene pool
        if show['gene_pool'] and traits_df.loc[trait_idx].gene_pool == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['gene_pool'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # worlds_end
        if show['worlds_end'] and traits_df.loc[trait_idx].worlds_end == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['worlds_end'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # effectless
        if show['effectless'] and traits_df.loc[trait_idx].effectless == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['effectless'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # attachment
        if show['attachment'] and traits_df.loc[trait_idx].attachment == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['attachment'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # add SEPERATOR after _true_ icons
        icol += 1
        ttk.Separator(frame_pics, orient='vertical'
                      ).grid(row=0, column=icol, padx=3, pady=3, sticky='ns')

        # ----- current effects due to attachments -----------------------
        # _current_ color
        cur_color = traits_df.loc[trait_idx].cur_color
        if cur_color != traits_df.loc[trait_idx].color:
            icol += 1
            cc = 'c' if 'colorless' in cur_color.lower() else ''
            cb = 'b' if 'blue' in cur_color.lower() else ''
            cg = 'g' if 'green' in cur_color.lower() else ''
            cp = 'p' if 'purple' in cur_color.lower() else ''
            cr = 'r' if 'red' in cur_color.lower() else ''

            tk.Label(
                frame_pics,
                image=images[cc+cb+cg+cp+cr],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # _current_ face
        cur_face = traits_df.loc[trait_idx].cur_face
        if cur_face != traits_df.loc[trait_idx].face:
            print("_______________ add current face falue icon")

        # noFX
        if 'Inactive' in traits_df.loc[trait_idx].cur_effect:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noFX'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # noRemove
        if 'NoRemove' in traits_df.loc[trait_idx].cur_effect:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noRemove'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # noDiscard
        if 'NoDiscard' in traits_df.loc[trait_idx].cur_effect:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noDiscard'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # noSteal
        if 'NoSteal' in traits_df.loc[trait_idx].cur_effect:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noSteal'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # noSwap
        if 'NoSwap' in traits_df.loc[trait_idx].cur_effect:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noSwap'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # ----- ATTACHMENT combobox if trait is attachment ---------------
        if traits_df.loc[trait_idx].attachment == 1:
            irow += 1
            tk.Label(
                frame_trait_overview,
                text="attach to:",
                bg=defaults["bg_trait_pile"],
                fg=defaults["font_color_trait_pile"]
                ).grid(row=irow, column=0, padx=(40, 0), sticky='e')

            # filter only non-attachment-traits and check if this is already attached to a trait
            traits_filtered_idx = [None] + rules.filter_attachables(traits_df, player_traits[p], trait_idx)
            traits_filtered_str = [" ... "] + [traits_df.loc[idx].trait
                                               for idx in traits_filtered_idx if idx is not None]

            # create combobox
            cbox_attach_to = ttk.Combobox(
                frame_trait_overview,
                height=len(traits_filtered_str),
                values=traits_filtered_str,
                exportselection=0,
                state="readonly",
                width=7)
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

        # ----- WORLDS_END combobox if trait has worlds end effect -------
        if isinstance(traits_df.loc[trait_idx].effect_worlds_end, str):
            irow += 1
            tk.Label(
                frame_trait_overview,
                text="@ worlds end:",
                bg=defaults["bg_trait_pile"],
                fg=defaults["font_color_trait_pile"]
                ).grid(row=irow, column=0, padx=(40, 0), sticky='e')

            # get task what to do at worlds end
            we_task = rules.traits_WE_effects(traits_df, trait_idx)

            # create combobox
            cbox_attach_to = ttk.Combobox(
                frame_trait_overview,
                height=len(we_task),
                values=we_task,
                exportselection=0,
                state="readonly",
                width=10)
            cbox_attach_to.grid(row=irow, column=1, sticky='w')
            # cbox_attach_to.bind(
            #    "<<ComboboxSelected>>", lambda e, t=trait_idx: btn_attach_to(p, t, e)
            # )

            # check if already attached to host
            if traits_df.loc[trait_idx].cur_host == 'none':
                cbox_attach_to.current(0)
            else:
                cur_host = traits_df.loc[trait_idx].cur_host
                cbox_attach_to.current(traits_filtered_idx.index(cur_host)+1)


def create_player_frame(p):
    border = defaults["color_frame_width"]

    frame = tk.Frame(frame_playground, bg=defaults["player_frame_color"])
    frame.columnconfigure(0, weight=1)  # stretch sub_frames to playground (=1!)
    frame.rowconfigure(1, weight=1)  # stretch trait-pile to bottom of playground
    # frame.rowconfigure(2, weight=1)  # further actions
    frame.grid(column=p, row=0, padx=5, pady=5, sticky="nesw")  # or use nsw for non-x-streched frames!

    # ----- name + overview current points -------------------------------
    frame_points = tk.Frame(frame)
    frame_points.grid(row=0, column=0, padx=border, pady=border, ipady=3, sticky="nesw")
    frame_points.columnconfigure(0, weight=1)
    frame_points.columnconfigure(1, weight=1)
    frame_points.columnconfigure(2, weight=3)
    frame_points.columnconfigure(3, weight=1)
    frame_points.columnconfigure(4, weight=1)

    # name
    ttk.Label(
        frame_points,
        textvariable=player_name[p],
        font='"Comic Sans MS" 36 italic',
    ).grid(row=0, column=0, padx=5, pady=(0, 10), columnspan=3, sticky='ns')

    # stars
    ttk.Label(frame_points, image=images['no_star']).grid(row=0, column=3, padx=0, pady=0, sticky="nes")
    ttk.Label(frame_points, image=images['no_star']).grid(row=0, column=4, padx=0, pady=0, sticky="nsw")

    # single points
    ttk.Label(
        frame_points,
        text="Face:",
    ).grid(row=1, column=0, sticky="e")
    ttk.Label(
        frame_points,
        text="Drops:",
    ).grid(row=2, column=0, sticky="e")
    ttk.Label(
        frame_points,
        text="World's End:",
    ).grid(row=3, column=0, sticky="e")
    ttk.Label(
        frame_points,
        text="MOL:",
    ).grid(row=4, column=0, sticky="e")

    ttk.Label(
        frame_points, textvariable=player_points[p]['face'],
    ).grid(row=1, column=1, sticky="w")
    ttk.Label(
        frame_points, textvariable=player_points[p]['drops'],
    ).grid(row=2, column=1, sticky="w")
    ttk.Label(
        frame_points, textvariable=player_points[p]['worlds_end'],
    ).grid(row=3, column=1, sticky="w")
    ttk.Label(
        frame_points, textvariable=player_points[p]['MOL'],
    ).grid(row=4, column=1, sticky="w")

    # total points
    ttk.Label(
        frame_points,
        textvariable=player_points[p]['total'],
        style="total.TLabel",
    ).grid(row=1, column=2, rowspan=4, padx=0, pady=0, sticky='ns')

    # gene pool
    ttk.Label(
        frame_points,
        text="gene pool",
    ).grid(row=1, column=3, columnspan=2, padx=0, pady=0, sticky='ns')

    ttk.Label(
        frame_points,
        textvariable=player_genes[p],
        style="genes.TLabel",
    ).grid(row=2, column=3, rowspan=3, columnspan=2, padx=0, pady=0, sticky='n')

    # ----- list of traits played ----------------------------------------
    frame_traits = tk.Frame(frame)
    frame_traits.grid(row=1, column=0, padx=border, pady=(0, border), sticky="nesw")
    frame_traits.rowconfigure(0, weight=1)
    frame_traits.columnconfigure(0, weight=1)  # for left button under trait-pile
    frame_traits.columnconfigure(1, weight=1)  # for right button under trait-pile

    player_rb_frames[p] = tk.Frame(frame_traits, bg=defaults["bg_trait_pile"])
    player_rb_frames[p].grid(row=0, column=0, columnspan=2, sticky='nesw', padx=border, pady=border)
    create_trait_pile(player_rb_frames[p], p)

    # action buttons -----
    cbox_move_to = ttk.Combobox(
        frame_traits,
        height=n_player,
        values=[" move trait to ..."] + defaults["names"][:n_player.get()],
        exportselection=0,
        state="readonly",
        width=12,
        style="move.TCombobox")
    cbox_move_to.grid(row=1, column=0, pady=(0, border), sticky='ns')
    cbox_move_to.current(0)
    cbox_move_to.bind(
        "<<ComboboxSelected>>", lambda e: btn_move_trait(p, cbox_move_to))

    ttk.Button(
        frame_traits,
        text="discard trait",
        command=partial(btn_discard_trait, p),
    ).grid(row=1, column=1, pady=(0, border), sticky='ns')

    # ----- action buttons -------------------------------------
#    frame_actions = tk.Frame(frame)
#    frame_actions.grid(row=2, column=0, padx=border, pady=(0, border), sticky="nesw")
#    frame_actions.columnconfigure(0, weight=1)
#    frame_actions.columnconfigure(1, weight=1)

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
    ttk.Label(
        frame_menu_options,
        text="OPTIONS",
        font="'' 24",
    ).grid(row=0, column=0, columnspan=2, pady=(5, 5))

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

    # restart button -----
    ttk.Button(
        frame_menu_options,
        text="restart game",
        command=start_game,
    ).grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")

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
        textvariable=search_trait,
    )
    trait_ent.grid(row=1, column=0, padx=(10, 0), sticky="w")
    trait_ent.bind("<KeyRelease>", lambda e: search_trait_in_list(search_trait))
    ttk.Button(
        frame_menu_traits,
        text="clear",
        width=4,
        command=btn_clear_trait_search,
    ).grid(row=1, column=1, padx=(0, 10), sticky="w")

    # listbox with (filtered) deck-cards -----
    lbox_traits[0] = tk.Listbox(
        frame_menu_traits,
        height=5,
        listvariable=lbox_cards_str,
        selectmode=tk.SINGLE,
        exportselection=False
    )
    lbox_traits[0].grid(row=2, column=0, columnspan=2, padx=10)
    lbox_traits[0].bind(
        "<<ListboxSelect>>", lambda e: update_selected_trait("lbox", lbox_traits[0].curselection())
    )

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
        cbox_catastrophy = ttk.Combobox(
            frame_menu_catastrophe,
            values=[" catastrophe {}...".format(c+1)] + ages_df.loc[catastrophies_dfi].name.values.tolist(),
            exportselection=0,
            state="readonly",
            width=18,
            style="move.TCombobox"
        )
        cbox_catastrophy.current(0)
        cbox_catastrophy.grid(row=c+1, column=0, columnspan=2, padx=4, sticky='ns')
        cbox_catastrophy.bind("<<ComboboxSelected>>", lambda ev, c=c: btn_play_catastrophe(ev, c))

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
        state="readonly",
        width=18,
        style="move.TCombobox",
        textvariable=worlds_end
    )
    worlds_end_cbox[0].current(0)
    worlds_end_cbox[0].grid(row=n_catastrophies.get()+2, column=0, columnspan=2, padx=4, pady=(0, 5), sticky='ns')
    worlds_end_cbox[0].bind("<<ComboboxSelected>>", lambda e: btn_play_worlds_end())

    # ----- frame for control buttons ---------------------------------------------------
    frame_menu_controls = tk.Frame(frame_menu)
    frame_menu_controls.grid(row=4, column=0, padx=border, pady=(0, border), sticky="nesw")
    frame_menu_controls.columnconfigure(0, weight=1)

    ttk.Button(
        frame_menu_controls,
        text="quit",
        command=root.quit,
    ).grid(padx=10, pady=5, sticky="we")


def reset_variables():
    # update current settings
    n_player.set(opt_n_player.get())
    n_genes.set(opt_n_genes.get())
    n_catastrophies.set(opt_n_catastrophies.get())

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

    # reset deck/lbox card-lists
    deck_cards.clear()
    deck_cards.extend(traits_dfi)   # complete list of indicies of all traits
    lbox_cards_idx.set(traits_dfi)  # complete list of indices of traits for menu_listbox
    lbox_cards_str.set(traits_df.loc[traits_dfi].trait.values.tolist())  # complete list of names of traits

    # reset occured catastrophies
    catastrophies.clear()
    for i in range(n_catastrophies.get()):
        catastrophies.append(tk.StringVar(value=""))


def start_game():
    # reset variables ----------------------------------------------------
    print(">>> initialize <<< reset variables")
    reset_variables()

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
gui_style.configure("total.TLabel", font=("", 72, "bold"), foreground="orangered1")
gui_style.configure("genes.TLabel", font=("", 38, "bold"), foreground="hotpink1")
gui_style.configure("move.TCombobox", selectbackground="none")

# load images ------------------------------------------------------------
images = {}
for k, v in images_dict.items():
    images[k] = ImageTk.PhotoImage(v)

# init variables ---------------------------------------------------------
opt_n_player = tk.IntVar(value=defaults["n_player"])                # OPTIONS: number of players
opt_n_genes = tk.IntVar(value=defaults["n_genes"])                  # OPTIONS: gene pool at beginning
opt_n_catastrophies = tk.IntVar(value=defaults["n_catastrophies"])  # OPTIONS: number of catastrophies

n_player = tk.IntVar()          # number of current players
n_genes = tk.IntVar()           # gene pool at start
n_catastrophies = tk.IntVar()   # number of catastrophies

search_trait = tk.StringVar(value="")   # searching for traits in playable deck
deck_cards = []                         # all traits in deck (or discard pile) left to be drawn / list of idx
lbox_cards_idx = tk.Variable(value="")  # traits >>shown<< in listbox on the left, i.e. after filtering / list of idx
lbox_cards_str = tk.Variable(value="")  # traits >>shown<< in listbox on the left, i.e. after filtering / as string
play_trait = None                       # selected trait (by index in traits_df) in listbox
lbox_traits = [None]                    # listbox widget of deck cards -> needed to be able to edit selected traits

catastrophies = []                  # occured catastrophies / StringVar
worlds_end = tk.StringVar(value="")
worlds_end_cbox = [None]

frames_player = []          # list of all players frames
player_name = []            # current players names / tk.StringVar
player_genes = []           # current players gene pool / tk.IntVar
player_points = []          # current players points / dictionary
player_traits = []          # current players traits played / lists
player_trait_selected = []  # selected traits in players trait piles / StringVar
player_rb_frames = []       # frame containing players traits -> needed to be able to edit selected traits

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
