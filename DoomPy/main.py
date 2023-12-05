import os
import glob
import json
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
traits_df = pd.read_excel(os.path.join(curdir, "files", "cards.xlsx"), sheet_name="traits")
traits_list = sorted(traits_df.name.values.tolist())

ages_df = pd.read_excel(os.path.join(curdir, "files", "cards.xlsx"), sheet_name="ages")
ages_list = sorted(ages_df.name.values.tolist())
catastrophies_list = sorted(ages_df[ages_df["type"] == "Catastrophe"]["name"].values.tolist())

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
show['drop'] = True
show['gene_pool'] = False
show['worlds_end'] = True
show['effectless'] = False
show['attachment'] = False


# functions ##############################################################
def btn_clear_trait_search():
    search_trait.set("")
    lbox_cards.set(deck_cards.get())
    lbox_traits[0].selection_clear(0, tk.END)
    play_trait.set("")


def btn_attach_to(from_, attachment, event):
    # get host from event_data
    host = event.widget.get()

    print(">>> attachment <<< '{}' is attaching '{}' to '{}' "
          .format(player_name[from_].get(), attachment, host))

    # check if attachment moved from old_host
    old_idx = traits_df.index[traits_df.cur_attachment == attachment].tolist()
    if old_idx:
        old_host = traits_df.at[old_idx[0], 'name']
        print("___ OLD HOST: {}".format(old_host))
        update_hosts_current_status(old_host, [])
        # traits_df.loc[traits_df.cur_attachment == attachment, 'cur_attachment'] = 'none'
    else:
        print("no previous host....")

    # check if attachment is set back to "..." (idx=0)
    if event.widget.current() == 0:
        # set host to status_row of attachment
        traits_df.loc[traits_df.name == attachment, 'cur_host'] = 'none'
    else:
        # set host to status_row of attachment
        traits_df.loc[traits_df.name == attachment, 'cur_host'] = host

        # set attachment to status_row of host & update effects of attachment on host
        traits_df.loc[traits_df.name == host, 'cur_attachment'] = attachment
        update_hosts_current_status(host, attachment)

    # recreate trait pile & clear trait selection
    create_trait_pile(player_rb_frames[from_], from_)



def btn_discard_trait(from_):
    # get card
    card = player_trait_selected[from_].get()

    # return, if no trait selected
    if card == "none":
        print(">>> discard <<< ERROR - no trait selected")
        return

    # return, if attachment selected
    if traits_df[traits_df.name == card].attachment.values[0] == 1:
        print(">>> discard <<< ERROR - attachment not discardable -> discard host instead")
        return

    # check if card HAS attachment
    attachment = traits_df[traits_df.name == card]["cur_attachment"].values[0]

    # remove card from players traits, and attachment if neccessary
    cur_players_cards = list(player_traits[from_].get())
    cur_players_cards.remove(card)
    if attachment != 'none':
        cur_players_cards.remove(attachment)
    player_traits[from_].set(cur_players_cards)

    # update current status of card & host & attachment
    update_hosts_current_status(card, [])
    if attachment != 'none':
        update_hosts_current_status(attachment, [])

    # recreate trait pile & clear trait selection
    create_trait_pile(player_rb_frames[from_], from_)
    player_trait_selected[from_].set("none")

    # add to deck traits, if not there
    if card not in list(deck_cards.get()):
        cur_deck_cards = list(deck_cards.get())
        cur_deck_cards.append(card)
        deck_cards.set(sorted(cur_deck_cards))

    print(">>> discard <<< '{}' is discarding '{}'"
          .format(player_name[from_].get(), card))
    if attachment != 'none':
        print(">>> discard <<< ___ attachment '{}' is also discarded automatically"
              .format(attachment))

    # update scoring, stars & genes
    update_scoring(from_)
    update_stars()
    update_genes()

    # update trait search if discarded trait matches filter
    search_trait_in_list(search_trait)

    # reset current values of card
    reset_traits_current_status(card)


def btn_move_trait(from_, cbox_move_to):
    # get card
    card = player_trait_selected[from_].get()

    # clear combobox
    cbox_move_to.current(0)

    # return, if no trait selected
    if card == "none":
        print(">>> move <<< ERROR - no trait selected")
        return

    # return, if no target selected
    if cbox_move_to.get() == " move trait to ...":
        print(">>> move <<< ERROR - clicked on 'move trait to...'")
        return

    # return, if from == to
    to = defaults["names"].index(cbox_move_to.get())
    if from_ == to:
        print(">>> move <<< ERROR - 'source' and 'target' player are the same")
        return

    # return, if attachment selected
    if traits_df[traits_df.name == card].attachment.values[0] == 1:
        print(">>> move <<< ERROR - attachment not moveable -> move host instead")
        return

    # check if card HAS attachment
    attachment = traits_df[traits_df.name == card]["cur_attachment"].values[0]

    add_txt = "(and its attachment '{}')".format(attachment) if attachment != 'none' else ''
    print(">>> move <<< '{}' {} is moved from '{}' to '{}'"
          .format(card, add_txt, player_name[from_].get(), player_name[to].get()))

    # remove from 'giving' players traits & clear trait selection
    from_players_cards = list(player_traits[from_].get())
    from_players_cards.remove(card)
    if attachment != 'none':
        from_players_cards.remove(attachment)
    player_traits[from_].set(from_players_cards)

    create_trait_pile(player_rb_frames[from_], from_)
    player_trait_selected[from_].set("none")

    # add to 'receiving' players traits
    to_players_cards = list(player_traits[to].get())
    to_players_cards.append(card)
    if attachment != 'none':
        to_players_cards.append(attachment)
    player_traits[to].set(sorted(to_players_cards))

    create_trait_pile(player_rb_frames[to], to)

    # update scoring, stars & genes
    update_scoring(from_)
    update_scoring(to)
    update_stars()
    update_genes()


def btn_play_trait(to):
    # get card
    card = play_trait.get()

    # return, if no trait selected
    if card == "":
        print(">>> play <<< ERROR - no trait selected")
        return

    # return, if player already has two dominants
    if traits_df[traits_df.name == card]['dominant'].values[0] == 1:
        if sum([1 for t in player_traits[to].get()
                if traits_df[traits_df.name == t]['dominant'].values[0] == 1]) == 2:
            print(">>> play <<< ERROR - already 2 dominant traits in trait pile")
            return

    card_n = traits_df[traits_df.name == card]['n_of_cards'].values[0]

    # add to players traits
    cur_players_cards = list(player_traits[to].get())
    cur_players_cards.append(card)
    player_traits[to].set(sorted(cur_players_cards))

    create_trait_pile(player_rb_frames[to], to)

    # remove from deck if all cards played
    card_played = 0
    for i in range(n_player.get()):
        card_played = card_played + sum([1 for x in list(player_traits[i].get()) if x == card])

    if card_played == card_n:
        cur_deck_cards = list(deck_cards.get())
        cur_deck_cards.remove(card)
        deck_cards.set(cur_deck_cards)

    print(">>> play <<< '{}' is playing '{}', which is {} times in the deck and was played {} times"
          .format(player_name[to].get(), card, card_n, card_played))

    # update scoring
    update_scoring(to)

    # update stars & genes
    update_stars()
    update_genes()

    # clear trait search & update listbox & selection
    btn_clear_trait_search()


def btn_play_worlds_end():
    # do nothing if no catastrophy selected
    if worlds_end.get() == " select world's end ...":
        return

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

    # debug outout
    print(">>> catastrophe <<< played catastrophe #{}: '{}'"
          .format(c+1, played_catastrophy))

    # update genes
    update_genes()


def update_hosts_current_status(host, attachment):
    # if 'attachment' is empty, host will be reseted
    if attachment:
        # get effects of attachments from rules.py
        effects = rules.attachment_effects(traits_df, host, attachment)

        # update cur_values of host
        traits_df.loc[traits_df.name == host, "cur_color"] = effects['color']
        traits_df.loc[traits_df.name == host, "cur_face"] = effects['face']
        traits_df.loc[traits_df.name == host, "cur_effect"] = effects['effect']

        print(">>> cur_values <<< '{}' is updated due to effects of {}".format(host, attachment))

    else:
        # reset host
        true_color = traits_df[traits_df.name == host]["color"].values[0]
        true_face = traits_df[traits_df.name == host]["face"].values[0]

        traits_df.loc[traits_df.name == host, "cur_color"] = true_color
        traits_df.loc[traits_df.name == host, "cur_face"] = true_face
        traits_df.loc[traits_df.name == host, "cur_effect"] = 'none'
        traits_df.loc[traits_df.name == host, "cur_host"] = 'none'
        traits_df.loc[traits_df.name == host, "cur_attachment"] = 'none'

        print(">>> cur_values <<< '{}' is reseted to defaults".format(host))


def update_scoring(p):
    # get cards
    cards = player_traits[p].get()

    # calculate face value
    p_face = int(np.nansum([traits_df[traits_df.name == card]['face'].values[0] for card in cards]))
    player_points[p]['face'].set(p_face)

    # calculate drop points
    p_drop = 0
    player_points[p]['drop'].set(p_drop)

    # calculate world's end points
    p_worlds_end = rules.worlds_end(worlds_end.get(), p, player_traits, traits_df)
    player_points[p]['worlds_end'].set(p_worlds_end)

    # calculate total score
    total = p_face + p_drop + p_worlds_end
    player_points[p]['total'].set(total)

    print(">>> scoring <<< current points for '{}': face = {}  |  drops = {}  |  WE = {}  |  total = {}"
          .format(player_name[p].get(), p_face, p_drop, p_worlds_end, total))


def update_genes():
    # init vars
    diff_genes = [0] * n_player.get()

    # loop players and calculate +- genes of all played traits
    for p in range(n_player.get()):
        # get cards
        cards = player_traits[p].get()

        # loop cards
        for card in cards:
            # get gene effect of this card
            effect = traits_df[traits_df.name == card]['effect_gene_pool'].values[0]

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

                print(">>> genes <<< '{}'s '{}' has gene effect off '{}' on '{}' -> current effect: {}"
                      .format(player_name[p].get(), card, value, who, diff_genes))

    # check what catastrophies were played alread
    for c in range(n_catastrophies.get()):
        # get card & effect
        card = catastrophies[c].get()
        # check if catastrophy was played
        if card in ages_df.name.values.tolist():
            # get effect and apply it
            effect = int(ages_df[ages_df.name == card]['gene_pool'].values[0])
            diff_genes = [i + effect for i in diff_genes]

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

    if any(i > 0 for i in diff_genes):
        print("   >>> total gene effect: {} -> new gene pools are {}"
              .format(diff_genes, [player_genes[i].get() for i in range(n_player.get())]))


def update_stars():
    # loop players
    for p in range(n_player.get()):
        # number of dominant traits
        n_stars = np.nansum([traits_df[traits_df.name == card]['dominant'].values[0]
                             for card in player_traits[p].get()])

        # find label widgets
        tmp_frame = frames_player[p].winfo_children()
        lbl1 = frames_player[p].nametowidget(str(tmp_frame[0]) + '.!label2')
        lbl2 = frames_player[p].nametowidget(str(tmp_frame[0]) + '.!label3')

        # edit images
        lbl1.configure(image=images['no_star'])
        lbl2.configure(image=images['no_star'])
        if n_stars > 0:
            lbl1.configure(image=images['star'])
            if n_stars > 1:
                lbl2.configure(image=images['star'])


def search_trait_in_list(inp):
    value = inp.get()
    lbox_traits[0].selection_clear(0, tk.END)

    if value == "":
        lbox_cards.set(deck_cards.get())
    else:
        lbox_cards.set([item for item in deck_cards.get() if value.lower() in item.lower()])


def update_selected_trait(where, idx):
    if where == "lbox":
        # trait in DECK is selected
        if idx == ():
            play_trait.set("")
        else:
            selected_card = lbox_cards.get()[int(idx[0])]
            play_trait.set(selected_card)

            print(">>> select <<< handle DECK_listbox -> selected trait = '{}'"
                  .format(play_trait.get()))

    else:
        # trait in one of PLAYERS traits is selected, note: 'where' represents the player here
        player_trait_selected[where].set(idx.get())
        print(">>> select <<< handle PLAYER_listbox -> selected trait = '{}' - by '{}'"
              .format(player_trait_selected[where].get(), player_name[where].get()))


def create_trait_pile(frame_trait_overview, p):
    # first, clean up frame
    for w in frame_trait_overview.grid_slaves():
        w.grid_forget()

    # loop traits in pile
    irow = -1
    for trait in player_traits[p].get():
        ypad = (3, 0) if irow == 0 else 0
        irow += 1

        # ----- radiobutton ----------------------------------------------
        tk.Radiobutton(
            frame_trait_overview,
            text=" " + trait,
            variable=player_trait_selected[p],
            value=trait,
            bg=defaults["bg_trait_pile"],
            fg='black',
            command=lambda: update_selected_trait(p, player_trait_selected[p]),
            ).grid(row=irow, column=0, padx=3, pady=ypad, sticky='nsw')

        # ----- icons ----------------------------------------------------
        frame_pics = tk.Frame(frame_trait_overview, bg=defaults["bg_trait_pile"])
        frame_pics.grid(row=irow, column=1, sticky='sw')
        icol = -1  # initialize column index which changes depending on card

        # _true_ color
        if show['color']:
            icol += 1
            color = traits_df[traits_df.name == trait]['color'].values[0]
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
            face_value = traits_df[traits_df.name == trait]['face'].values[0]
            face_string = str(face_value) if np.isnan(face_value) else str(int(face_value))

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

            match traits_df[traits_df.name == trait]['game'].values[0].lower():
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
        if show['dominant'] and traits_df[traits_df.name == trait]['dominant'].values[0] == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['dominant'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # action
        if show['action'] and traits_df[traits_df.name == trait]['action'].values[0] == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['action'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # drop
        if show['drop'] and traits_df[traits_df.name == trait]['drop'].values[0] == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['drop'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # gene pool
        if show['gene_pool'] and traits_df[traits_df.name == trait]['gene_pool'].values[0] == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['gene_pool'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # worlds_end
        if show['worlds_end'] and traits_df[traits_df.name == trait]['worlds_end'].values[0] == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['worlds_end'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # effectless
        if show['effectless'] and traits_df[traits_df.name == trait]['effectless'].values[0] == 1:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['effectless'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # attachment
        if show['attachment'] and traits_df[traits_df.name == trait]['attachment'].values[0] == 1:
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
        cur_color = traits_df[traits_df.name == trait].cur_color.values[0]
        cc = 'c' if 'colorless' in cur_color.lower() else ''
        cb = 'b' if 'blue' in cur_color.lower() else ''
        cg = 'g' if 'green' in cur_color.lower() else ''
        cp = 'p' if 'purple' in cur_color.lower() else ''
        cr = 'r' if 'red' in cur_color.lower() else ''

        if cur_color != traits_df[traits_df.name == trait]['color'].values[0]:
            icol += 1
            tk.Label(
                frame_pics,
                image=images[cc+cb+cg+cp+cr],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # noFX
        if 'Inactive' in traits_df[traits_df.name == trait]['cur_effect'].values[0]:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noFX'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # noRemove
        if 'NoRemove' in traits_df[traits_df.name == trait]['cur_effect'].values[0]:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noRemove'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # noDiscard
        if 'NoDiscard' in traits_df[traits_df.name == trait]['cur_effect'].values[0]:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noDiscard'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # noSteal
        if 'NoSteal' in traits_df[traits_df.name == trait]['cur_effect'].values[0]:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noSteal'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # noSwap
        if 'NoSwap' in traits_df[traits_df.name == trait]['cur_effect'].values[0]:
            icol += 1
            tk.Label(
                frame_pics,
                image=images['noSwap'],
                bg=defaults["bg_trait_pile"]
                ).grid(row=0, column=icol)

        # ----- ATTACHMENT combobox if trait is attachment ---------------
        if traits_df[traits_df.name == trait]['attachment'].values[0] == 1:
            irow += 1
            # filter only non-attachment-traits and check if this is already attached to a trait
            traits_filtered = rules.filter_attachables(traits_df, player_traits[p].get(), trait)

            # create combobox
            cbox_attach_to = ttk.Combobox(
                frame_trait_overview,
                height=len(traits_filtered)+1,
                values=["attach to"] + traits_filtered,
                exportselection=0,
                state="readonly",
                width=7,
            )
            cbox_attach_to.grid(row=irow, column=0, sticky='e')
            cbox_attach_to.bind(
                "<<ComboboxSelected>>", lambda e, t=trait: btn_attach_to(p, t, e)
            )

            # check if already attached to host
            if traits_df[traits_df.name == trait]['cur_host'].values[0] == 'none':
                cbox_attach_to.current(0)
            else:
                cur_host = traits_df[traits_df.name == trait]['cur_host'].values[0]
                cbox_attach_to.current(traits_filtered.index(cur_host)+1)


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
        frame_points, textvariable=player_points[p]['drop'],
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
        style="move.TCombobox"
    )
    cbox_move_to.current(0)
    cbox_move_to.grid(row=1, column=0, pady=(0, border), sticky='ns')
    cbox_move_to.bind(
        "<<ComboboxSelected>>", lambda e: btn_move_trait(p, cbox_move_to)
    )

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

    # 'play trai' -----
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
        listvariable=lbox_cards,
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
            values=[" catastrophe {}...".format(c+1)] + catastrophies_list,
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
        player_points.append({'face': tk.IntVar(value=0), 'drop': tk.IntVar(value=0),
                              'worlds_end': tk.IntVar(value=0), 'MOL': tk.IntVar(value=0),
                              'total': tk.IntVar(value=0)})
        player_traits.append(tk.Variable(value=[]))
        player_trait_selected.append(tk.StringVar(value="none"))
        player_rb_frames.append(None)

    # reset deck/lbox card-lists
    deck_cards.set(traits_list)
    lbox_cards.set(traits_list)

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
        w = 0 if i >= n_player.get() else 1  # 1 => player_frames are stretchable
        print("player {} - w={}".format(i+1, w))
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
deck_cards = tk.Variable(value="")      # all traits in deck (or discard pile) left to be drawn
lbox_cards = tk.Variable(value="")      # traits >>shown<< in listbox on the left, i.e. after filtering
play_trait = tk.StringVar(value="")     # selected trait in listbox
lbox_traits = [None]                    # listbox widget of deck cards -> needed to be able to edit selected traits

catastrophies = []                  # occured catastrophies / StringVar
worlds_end = tk.StringVar(value="")
worlds_end_cbox = [None]

frames_player = []          # list of all players frames
player_name = []            # current players names / StringVar
player_genes = []           # current players gene pool / IntVar
player_points = []          # current players points / dictionary
player_traits = []          # current players traits played / Var 4 listbox
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
