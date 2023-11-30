import os
import tkinter as tk
from tkinter import ttk
from math import floor
from functools import partial
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
from rules_worlds_end import calculate_worlds_end


# system settings ########################################################
curdir = os.path.dirname(__file__)

# load card list #########################################################
traits_df = pd.read_excel(os.path.join(curdir, "cards.xlsx"), sheet_name="traits")
traits_list_all = sorted(traits_df.name.values.tolist())

ages_df = pd.read_excel(os.path.join(curdir, "cards.xlsx"), sheet_name="ages")
ages_list = sorted(ages_df.name.values.tolist())
catastrophies_list = sorted(ages_df[ages_df["type"] == "Catastrophe"]["name"].values.tolist())

# load images ------------------------------------------------------------
size_star = 30
img_star = Image.open(os.path.join(curdir, "files", "dominant_star.png"))
img_star = img_star.resize((size_star, size_star))
img_empty_star = Image.open(os.path.join(curdir, "files", "empty_star.png"))
img_empty_star = img_empty_star.resize((size_star, size_star))


# functions ##############################################################
def btn_clear_trait_search():
    search_trait_str.set("")
    lbox_cards.set(deck_cards.get())
    lbox_traits.selection_clear(0, tk.END)
    play_trait.set("")


def btn_restart_game(content, frame_menu_buttons, frame_menu_catastrophe):
    # reset deck & lbox lists
    deck_cards.set(traits_list_all)
    lbox_cards.set(traits_list_all)

    # clear traits listbox
    btn_clear_trait_search()

    # update player buttons
    create_player_buttons(frame_menu_buttons)

    # clear catastrophie comboboxes & clear variable
    create_catastrophies(frame_menu_catastrophe)
    catastrophies.clear()
    for i in range(n_catastrophies.get()):
        catastrophies.append(tk.StringVar(value=""))

    # clear grid configuration
    for i in range(n_player.get()):
        content.columnconfigure(i+1, weight=1)

    # forget current player_frames
    for w in frames_player:
        w.grid_forget()

    # create player_frames + tidy them up
    player_lbox.clear()
    frames_player.clear()
    for i in range(n_player.get()):
        # create gene_pool_var
        player_genes[i].set(genes_at_start.get())

        # reset players listbox'es
        player_lbox.append(None)

        # clear player_cards listbox
        player_cards[i].set("")

        # create frame
        frames_player.append(create_player_frame(content, defaults, i))

        # update scoring
        update_scoring(i)


def btn_discard_trait(from_):
    # return if no trait selected
    if handle_trait[from_].get() == "":
        print(">>> discard <<< no trait selected...")
        return

    # get card
    card = handle_trait[from_].get()
    card_face = int(traits_df[traits_df.name == card]['points'].values[0])

    # remove from players traits
    cur_players_cards = list(player_cards[from_].get())
    cur_players_cards.remove(card)
    player_cards[from_].set(cur_players_cards)

    # add to deck traits, if not there
    if card not in list(deck_cards.get()):
        cur_deck_cards = list(deck_cards.get())
        cur_deck_cards.append(card)
        deck_cards.set(sorted(cur_deck_cards))

    print(">>> discard <<< {} is discarding {} ({} pts)"
          .format(player_name[from_].get(), card, card_face))

    # update scoring
    update_scoring(from_)

    # clear player trait selection
    player_lbox[from_].selection_clear(0, tk.END)
    handle_trait[from_].set("")

    # clear trait search & update listbox & selection
    btn_clear_trait_search()

    # update stars & genes
    update_stars()
    update_genes()


def btn_move_trait(from_, cbox_move_to):
    # return if no trait selected
    if handle_trait[from_].get() == "":
        cbox_move_to.current(0)
        print(">>> move <<< no trait selected...")
        return

    # return if no target selected
    if cbox_move_to.get() == " move trait to ...":
        cbox_move_to.current(0)
        print(">>> move <<< clicked on 'move trait to...'")
        return

    # return if from == to
    to = defaults["names"].index(cbox_move_to.get())
    if from_ == to:
        cbox_move_to.current(0)
        print(">>> move <<< 'source' and 'target' player are the same...")
        return

    # get card
    card = handle_trait[from_].get()

    print(">>> move <<< '{}' is moved from '{}' to '{}'"
          .format(card, player_name[from_].get(), player_name[to].get()))

    # remove from 'giving' players traits
    from_players_cards = list(player_cards[from_].get())
    from_players_cards.remove(card)
    player_cards[from_].set(from_players_cards)

    # add to 'receiving' players traits
    to_players_cards = list(player_cards[to].get())
    to_players_cards.append(card)
    player_cards[to].set(sorted(to_players_cards))

    # keep correct trait selected in list of receiving player
    if not handle_trait[to].get() == "":
        print(">>> move <<< trait selection corrected in '{}'s trait pile"
              .format(player_name[to].get()))
        list_idx_old_selection = player_cards[to].get().index(handle_trait[to].get())
        player_lbox[to].selection_clear(0, tk.END)
        player_lbox[to].selection_set(list_idx_old_selection)

    # deselect traits in list of giving player
    update_selected_trait(from_, ())
    player_lbox[from_].selection_clear(0, tk.END)

    # clear combobox
    cbox_move_to.current(0)

    # update scoring
    update_scoring(from_)
    update_scoring(to)

    # update stars & genes
    update_stars()
    update_genes()


def btn_play_trait(p):
    # return if no trait selected
    if play_trait.get() == "":
        print(">>> play <<< no trait selected...")
        return

    # get card
    card = play_trait.get()
    card_n = traits_df[traits_df.name == card]['n_of_cards'].values[0]
    card_face = int(traits_df[traits_df.name == card]['points'].values[0])

    # add to players traits
    cur_players_cards = list(player_cards[p].get())
    cur_players_cards.append(card)
    player_cards[p].set(sorted(cur_players_cards))

    # remove from deck if all cards played
    card_played = 0
    for i in range(n_player.get()):
        card_played = card_played + sum([1 for x in list(player_cards[i].get()) if x == card])

    if card_played == card_n:
        cur_deck_cards = list(deck_cards.get())
        cur_deck_cards.remove(card)
        deck_cards.set(cur_deck_cards)

    print(">>> play <<< {} is playing {} ({} pts), which is {} times in the deck and was played {} times"
          .format(player_name[p].get(), card, card_face, card_n, card_played))

    # update scoring
    update_scoring(p)

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
    print(">>> catastrophe <<< played catastrophe #{}: {}"
          .format(c+1, played_catastrophy))

    # update genes
    update_genes()


def update_scoring(p):
    # get cards
    cards = player_cards[p].get()

    # calculate face value
    p_face = int(sum([traits_df[traits_df.name == card]['points'].values[0] for card in cards]))
    player_points[p]['face'].set(p_face)

    # calculate drop points
    p_drop = 0
    player_points[p]['drop'].set(p_drop)

    # calculate world's end points
    p_worlds_end = calculate_worlds_end(worlds_end.get(), p, player_cards, traits_df)
    player_points[p]['worlds_end'].set(p_worlds_end)

    # calculate total score
    total = p_face + p_drop + p_worlds_end
    player_points[p]['total'].set(total)

    print(">>> scoring <<< calculations updated for {}: face = {}  -  drops = {}  -  WE = {}  -  total = {}"
          .format(player_name[p].get(), p_face, p_drop, p_worlds_end, total))


def update_genes():
    # init vars
    diff_genes = [0] * n_player.get()

    # loop players and calculate +- genes of all played traits
    for p in range(n_player.get()):
        # get cards
        cards = player_cards[p].get()

        # loop cards
        for card in cards:
            # get gene effect of this card
            effect = traits_df[traits_df.name == card]['gene_pool'].values[0]

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

                print(">>> genes <<< {}'s '{}' has gene effect off '{}' on '{}' -> current effect: {}"
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
        new_gp = genes_at_start.get() + diff_genes[p]
        if new_gp > 8:
            player_genes[p].set(8)
        elif new_gp < 1:
            player_genes[p].set(1)
        else:
            player_genes[p].set(new_gp)

    print(">>> genes <<< total gene effect: {} -> new gene pools are {}"
          .format(diff_genes, [player_genes[i].get() for i in range(n_player.get())]))


def update_stars():
    # loop players
    for p in range(n_player.get()):
        # number of dominant traits
        n_stars = np.nansum([traits_df[traits_df.name == card]['dominant'].values[0]
                             for card in player_cards[p].get()])

        # find label widgets
        tmp_frame = frames_player[p].winfo_children()
        lbl1 = frames_player[p].nametowidget(str(tmp_frame[0]) + '.!label2')
        lbl2 = frames_player[p].nametowidget(str(tmp_frame[0]) + '.!label3')

        # edit images
        lbl1.configure(image=pic_empty_star)
        lbl2.configure(image=pic_empty_star)
        if n_stars > 0:
            lbl1.configure(image=pic_star)
            if n_stars > 1:
                lbl2.configure(image=pic_star)


def search_trait_in_list(event):
    value = event.widget.get()
    lbox_traits.selection_clear(0, tk.END)

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

            print(">>> select <<< handle DECK_listbox -> selected trait = {}"
                  .format(play_trait.get()))

    else:
        # trait in one of PLAYERS traits is selected, note: 'where' represents the player here
        if idx == ():
            handle_trait[where].set("")

            print(">>> select <<<  no trait selected in '{}'s list..."
                  .format(player_name[where].get()))

        else:
            selected_card = player_cards[where].get()[int(idx[0])]
            handle_trait[where].set(selected_card)

            print(">>> select <<< handle PLAYER_listbox -> selected trait = {} - by {}"
                  .format(handle_trait[where].get(), player_name[where].get()))


def create_player_frame(content, defaults, i):
    frame = tk.Frame(content, bg=defaults["bg_frame_player"])
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)  # traits
    # frame.rowconfigure(2, weight=1)  # further actions
    frame.grid(column=i+1, row=0, padx=5, pady=5, sticky="nesw")  # or use nsw for non-x-streched frames!

    # ----- name + overview current points -------------------------------
    frame_points = tk.Frame(frame)
    frame_points.grid(row=0, column=0, padx=5, pady=5, ipady=3, sticky="nesw")
    frame_points.columnconfigure(0, weight=1)
    frame_points.columnconfigure(1, weight=1)
    frame_points.columnconfigure(2, weight=2)
    frame_points.columnconfigure(3, weight=1)
    frame_points.columnconfigure(4, weight=1)

    # name
    ttk.Label(
        frame_points,
        textvariable=player_name[i],
        font='"Comic Sans MS" 36 italic',
    ).grid(row=0, column=0, padx=5, pady=(0, 10), columnspan=3, sticky='ns')

    ttk.Label(frame_points, image=pic_empty_star).grid(row=0, column=3, padx=0, pady=0, sticky="nes")
    ttk.Label(frame_points, image=pic_empty_star).grid(row=0, column=4, padx=0, pady=0, sticky="nsw")

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
        frame_points, textvariable=player_points[i]['face'],
    ).grid(row=1, column=1, sticky="w")
    ttk.Label(
        frame_points, textvariable=player_points[i]['drop'],
    ).grid(row=2, column=1, sticky="w")
    ttk.Label(
        frame_points, textvariable=player_points[i]['worlds_end'],
    ).grid(row=3, column=1, sticky="w")
    ttk.Label(
        frame_points, textvariable=player_points[i]['MOL'],
    ).grid(row=4, column=1, sticky="w")

    # total points
    ttk.Label(
        frame_points,
        textvariable=player_points[i]['total'],
        style="total.TLabel",
    ).grid(row=1, column=2, rowspan=4, padx=0, pady=0, sticky='ns')

    # gene pool
    ttk.Label(
        frame_points,
        text="gene pool",
    ).grid(row=1, column=3, columnspan=2, padx=0, pady=0, sticky='ns')

    ttk.Label(
        frame_points,
        textvariable=player_genes[i],
        style="genes.TLabel",
    ).grid(row=2, column=3, rowspan=3, columnspan=2, padx=0, pady=0, sticky='n')

    # ----- list of traits played ----------------------------------------
    frame_traits = tk.Frame(frame)
    frame_traits.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nesw")
    frame_traits.columnconfigure(0, weight=1)
    frame_traits.columnconfigure(1, weight=1)
    frame_traits.columnconfigure(2, weight=1)

    player_lbox[i] = tk.Listbox(
        frame_traits,
        height=22,
        listvariable=player_cards[i],
        selectmode=tk.SINGLE,
        exportselection=False,
    )
    player_lbox[i].grid(row=0, column=0, padx=8, pady=8, sticky='nesw')
    player_lbox[i].bind(
        "<<ListboxSelect>>", lambda e: update_selected_trait(i, player_lbox[i].curselection())
    )

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
    cbox_move_to.grid(row=1, column=0, padx=4, sticky='nsw')
    cbox_move_to.bind(
        "<<ComboboxSelected>>", lambda e: btn_move_trait(i, cbox_move_to)
    )

    ttk.Button(
        frame_traits,
        text="discard trait",
        command=partial(btn_discard_trait, i),
    ).grid(row=2, column=0, padx=8, sticky='nsw')

    # ----- action buttons -------------------------------------
#    frame_actions = tk.Frame(frame)
#    frame_actions.grid(row=2, column=0, padx=5, pady=5, sticky="nesw")
#    frame_actions.columnconfigure(0, weight=1)
#    frame_actions.columnconfigure(1, weight=1)

    return frame


def create_catastrophies(container):
    for w in container.grid_slaves():
        if not w.winfo_class() == 'TLabel':
            w.grid_forget()

    for c in range(n_catastrophies.get()):
        cbox_catastrophy = ttk.Combobox(
            container,
            values=[" catastrophe {}...".format(c+1)] + catastrophies_list,
            exportselection=0,
            state="readonly",
            width=18,
            style="move.TCombobox"
        )
        cbox_catastrophy.current(0)
        cbox_catastrophy.grid(row=c+1, column=0, columnspan=2, padx=4, sticky='ns')
        cbox_catastrophy.bind("<<ComboboxSelected>>", lambda ev, c=c: btn_play_catastrophe(ev, c))


def create_player_buttons(container):
    for w in container.grid_slaves():
        w.grid_forget()

    for i in range(n_player.get()):
        clspn = int(i + 1 == n_player.get() and (i + 1) % 2 == 1) + 1
        ttk.Button(
            container,
            textvariable=player_name[i],
            command=partial(btn_play_trait, i),
        ).grid(row=floor(i / 2), column=i % 2, columnspan=clspn)

    container.grid(row=4, column=0, columnspan=2, pady=(0, 10))


def create_player_entries(container):
    for w in container.grid_slaves():
        w.grid_forget()

    for i in range(n_player.get()):
        ttk.Label(
            container,
            text="player {}: ".format(i+1),
        ).grid(row=i, column=0)
        ttk.Entry(
            container,
            textvariable=player_name[i],
            width=8,
        ).grid(row=i, column=1)

    container.grid(row=5, column=0, columnspan=2)


def create_menu_frame(content, defaults):
    frame = tk.Frame(content, bg=defaults["bg_frame_menu"])
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=4)
    frame.rowconfigure(2, weight=1)

    # ----- frame 4 settings --------------------------------------------------------
    frame_menu_options = tk.Frame(frame)
    frame_menu_options.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")
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
        to=max_player.get(),
        width=3,
        textvariable=n_player,
        wrap=False,
        command=lambda: create_player_entries(frame_player_entries),
    ).grid(row=1, column=1, sticky='w')

    # genes at beginning -----
    ttk.Label(
        frame_menu_options,
        text="gene pool: ",
    ).grid(row=2, column=0, sticky='e')
    ttk.Spinbox(
        frame_menu_options,
        from_=4,
        to=8,
        width=3,
        textvariable=genes_at_start,
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
        textvariable=n_catastrophies,
        wrap=False
    ).grid(row=3, column=1, sticky='w')

    # name of players -----
    ttk.Label(
        frame_menu_options,
        text="who's playing?",
        font="'' 18",
    ).grid(row=4, column=0, columnspan=2, pady=(20, 0))

    frame_player_entries = tk.Frame(frame_menu_options)
    create_player_entries(frame_player_entries)

    # restart button -----
    ttk.Button(
        frame_menu_options,
        text="restart game",
        command=lambda: btn_restart_game(content, frame_menu_buttons, frame_menu_catastrophe),
    ).grid(row=n_player.get() + 6, column=0, columnspan=2, pady=10)

    # ----- frame 4 trait selection --------------------------------------------------------
    frame_menu_traits = tk.Frame(frame)
    frame_menu_traits.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nesw")
    frame_menu_traits.columnconfigure(0, weight=1)
    frame_menu_traits.columnconfigure(1, weight=1)

    ttk.Label(
        frame_menu_traits,
        text="play trait",
        font="'' 18",
    ).grid(row=0, column=0, columnspan=2, pady=(5, 0))

    trait_ent = ttk.Entry(
        frame_menu_traits,
        width=10,
        textvariable=search_trait_str,
    )
    trait_ent.grid(row=1, column=0, padx=(10, 0), sticky="w")
    trait_ent.bind("<KeyRelease>", search_trait_in_list)

    ttk.Button(
        frame_menu_traits,
        text="clear",
        width=4,
        command=btn_clear_trait_search,
    ).grid(row=1, column=1, padx=(0, 10), sticky="w")

    lbox_traits = tk.Listbox(
        frame_menu_traits, height=4, listvariable=lbox_cards, selectmode=tk.SINGLE, exportselection=False
    )
    lbox_traits.grid(row=2, column=0, columnspan=2, padx=10)
    lbox_traits.bind(
        "<<ListboxSelect>>", lambda e: update_selected_trait("lbox", lbox_traits.curselection())
    )

    ttk.Label(
        frame_menu_traits,
        text="who gets the trait?",
        font="'' 18",
    ).grid(row=3, column=0, columnspan=2, pady=(10, 0))

    frame_menu_buttons = tk.Frame(frame_menu_traits)
    create_player_buttons(frame_menu_buttons)

    # ----- frame 4 catastrophy selection --------------------------------------------------------
    frame_menu_catastrophe = tk.Frame(frame)
    frame_menu_catastrophe.grid(row=2, column=0, padx=5, pady=0, ipady=5, sticky="nesw")
    frame_menu_catastrophe.columnconfigure(0, weight=1)
    frame_menu_catastrophe.columnconfigure(1, weight=1)

    # catastrophies -----
    ttk.Label(
        frame_menu_catastrophe,
        text="Catastrophies",
        font="'' 18",
    ).grid(row=0, column=0, columnspan=2, pady=(5, 0))

    create_catastrophies(frame_menu_catastrophe)

    # world's end -----
    ttk.Label(
        frame_menu_catastrophe,
        text="World's End",
        font="'' 18",
    ).grid(row=n_catastrophies.get()+1, column=0, columnspan=2, pady=(8, 5))

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
    worlds_end_cbox[0].grid(row=n_catastrophies.get()+2, column=0, columnspan=2, padx=4, sticky='ns')
    worlds_end_cbox[0].bind("<<ComboboxSelected>>", lambda e: btn_play_worlds_end())

    # ----- frame for control buttons --------------------------------------------------------
    frame_menu_controls = tk.Frame(frame)
    frame_menu_controls.grid(row=3, column=0, padx=5, pady=5, sticky="nesw")
    frame_menu_controls.columnconfigure(0, weight=1)

    ttk.Button(
        frame_menu_controls,
        text="quit",
        command=root.quit,
    ).grid(padx=10, pady=5, sticky="we")

    return frame, lbox_traits


##########################################################################
# default variables ------------------------------------------------------
defaults = {
    "names": ["Lisa", "Julia", "Anton", "Adam", "Ben", "Franzi"],
    "n_player": 4,
    "max_player": 6,
    "n_catastrophies": 4,
    "genes_at_start": 6,
    "bg_content": "grey",
    "bg_frame_menu": "#71C671",
    "bg_frame_player": "lightskyblue",
    "bg_frame_1": "lightgrey",
}

# create a window --------------------------------------------------------
root = tk.Tk()
root.title("LIVE Doomlings Calculator")
root.geometry("1600x900")
root.configure(background="grey")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# init variables ---------------------------------------------------------
n_player = tk.IntVar(value=defaults["n_player"])                # number of current players
max_player = tk.IntVar(value=defaults["max_player"])            # theoretical max. num of players
n_catastrophies = tk.IntVar(value=defaults["n_catastrophies"])  # number of catastrophies
worlds_end_cbox = [None]
worlds_end = tk.StringVar(value="")
genes_at_start = tk.IntVar(value=defaults["genes_at_start"])    # gene pool at start
search_trait_str = tk.StringVar(value="")                       # searching for traits in playable deck
deck_cards = tk.Variable(value=traits_list_all)     # all traits in deck (or discard pile) left to be drawn
lbox_cards = tk.Variable(value=traits_list_all)     # traits >>shown<< in listbox on the left, i.e. after filtering
play_trait = tk.StringVar(value="")

player_name = []
player_genes = []
player_points = []
player_cards = []
player_lbox = []    # needed to be able to edit selected traits in players listbox
handle_trait = []
for i in range(max_player.get()):
    player_name.append(tk.StringVar(value=defaults["names"][i]))
    player_genes.append(tk.IntVar(value=genes_at_start.get()))
    player_points.append({'face': tk.IntVar(value=0), 'drop': tk.IntVar(value=0),
                          'worlds_end': tk.IntVar(value=0), 'MOL': tk.IntVar(value=0),
                          'total': tk.IntVar(value=0)})
    player_cards.append(tk.Variable(value=[]))
    player_lbox.append(None)
    handle_trait.append(tk.StringVar(value=""))

catastrophies = []
for i in range(n_catastrophies.get()):
    catastrophies.append(tk.StringVar(value=""))

# styling ----------------------------------------------------------------
gui_style = ttk.Style()
gui_style.configure("total.TLabel", font=("", 72, "bold"), foreground="orangered1")
gui_style.configure("genes.TLabel", font=("", 38, "bold"), foreground="hotpink1")
gui_style.configure("move.TCombobox", selectbackground="none")

# load images ------------------------------------------------------------
pic_star = ImageTk.PhotoImage(img_star)
pic_empty_star = ImageTk.PhotoImage(img_empty_star)

# content frame ----------------------------------------------------------
content = tk.Frame(root, width=1200, height=800, bg=defaults["bg_content"])
content.grid(column=0, row=0, sticky="nesw")
content.columnconfigure(0, weight=0)
for i in range(n_player.get()):
    content.columnconfigure(i + 1, weight=1)

# create menu frame ------------------------------------------------------
frame_menu, lbox_traits = create_menu_frame(content, defaults)
frame_menu.grid(column=0, row=0, padx=5, pady=5, stick="nesw")

# create player-frames ---------------------------------------------------
frames_player = []
for i in range(n_player.get()):
    frames_player.append(create_player_frame(content, defaults, i))

# ----- run --------------------------------------------------------------
root.mainloop()
