import os
import tkinter as tk
from tkinter import ttk
from math import floor
from functools import partial
import pandas as pd
from PIL import Image, ImageTk


# system settings ########################################################
curdir = os.path.dirname(__file__)

# load card list #########################################################
traits_df = pd.read_excel(os.path.join(curdir, "cards.xlsx"))
traits_list_all = sorted(traits_df["name"].values.tolist())

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


def btn_restart_game(content, frame_menu_buttons):
    # reset card/trait variables
    search_trait_str.set("")
    deck_cards.set(traits_list_all)
    lbox_cards.set(traits_list_all)
    play_trait.set("")

    # clear traits listbox
    btn_clear_trait_search()

    # update player buttons
    create_player_buttons(frame_menu_buttons)

    # clear grid configuration
    for i in range(n_player.get()):
        content.columnconfigure(i+1, weight=1)

    # forget current player_frames
    for w in frames_player:
        w.grid_forget()

    # create player_frames + tidy them up
    frames_player.clear()
    for i in range(n_player.get()):
        # create frame
        frames_player.append(create_player_frame(content, defaults, i))

        # clear player_cards listbox
        player_cards[i].set("")


def btn_discard_trait(from_, lbox_player):
    # return if no trait selected
    if handle_trait[from_].get() == "":
        print(">>> discard <<< no trait selected...")
        return

    # get card
    card = handle_trait[from_].get()
    card_face = int(traits_df[traits_df['name'] == card]['points'].values[0])

    # remove from players traits
    cur_players_cards = list(player_cards[from_].get())
    cur_players_cards.remove(card)
    player_cards[from_].set(cur_players_cards)

    # add to deck traits, if not there
    if card not in list(deck_cards.get()):
        cur_deck_cards = list(deck_cards.get())
        cur_deck_cards.append(card)
        deck_cards.set(sorted(cur_deck_cards))

    print(">>> discard <<< {} is discarding {} ({} pts)".format(player_name[from_].get(), card, card_face))

    # update scoring
    update_scoring(from_)

    # clear player trait selection
    lbox_player.selection_clear(0, tk.END)
    handle_trait[from_].set("")

    # clear trait search & update listbox & selection
    btn_clear_trait_search()


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

    # remove from 'giving' players traits
    from_players_cards = list(player_cards[from_].get())
    from_players_cards.remove(card)
    player_cards[from_].set(from_players_cards)

    # add to 'receiving' players traits
    to_players_cards = list(player_cards[to].get())
    to_players_cards.append(card)
    player_cards[to].set(sorted(to_players_cards))

    print(">>> move <<< '{}' is moved from '{}' to '{}'".format(
        card, player_name[from_].get(), player_name[to].get()))

    # clear combobox
    cbox_move_to.current(0)

    # update scoring
    update_scoring(from_)
    update_scoring(to)

    # update dominant stars
    update_stars()


def btn_play_trait(p):
    # return if no trait selected
    if play_trait.get() == "":
        print(">>> play <<< no trait selected...")
        return

    # get card
    card = play_trait.get()
    card_n = traits_df[traits_df['name'] == card]['n_of_cards'].values[0]
    card_face = int(traits_df[traits_df['name'] == card]['points'].values[0])

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

    print(">>> play <<< {} is playing {} ({} pts), which is {} times in the deck and was played {} times".format(
        player_name[p].get(), card, card_face, card_n, card_played))

    # update scoring
    update_scoring(p)

    # update dominant stars
    update_stars()

    # clear trait search & update listbox & selection
    btn_clear_trait_search()


def update_scoring(p):
    # get cards
    cards = player_cards[p].get()

    # calculate face value
    cards_face = int(sum([traits_df[traits_df['name'] == card]['points'].values[0] for card in cards]))
    player_points[p]['face'].set(cards_face)

    # calculate drop points
    cards_drop = 0
    player_points[p]['drop'].set(cards_drop)

    # calculate world's end points
    cards_worlds_end = 0
    player_points[p]['worlds_end'].set(cards_worlds_end)

    # calculate total score
    total = cards_face + cards_drop + cards_worlds_end
    player_points[p]['total'].set(total)

    print(">>> scoring <<< calculations are updated for {} ".format(player_name[p].get()))
    print("  -> face score is: {} ".format(cards_face))
    print("  -> drop score is: {} ".format(cards_drop))
    print("  -> total score is: {} ".format(total))


def update_stars():

    for p in range(n_player.get()):
        n_stars = sum([traits_df[traits_df['name'] == card]['dominant'].values[0] for card in player_cards[p].get()])
        print("---------------------> {} dominant traits".format(n_stars))

        tmp_frame = frames_player[p].winfo_children()
        lbl1 = frames_player[p].nametowidget(str(tmp_frame[0]) + '.!frame.!label')
        lbl2 = frames_player[p].nametowidget(str(tmp_frame[0]) + '.!frame.!label2')

        lbl1.configure(image=pic_empty_star)
        lbl2.configure(image=pic_empty_star)
        if n_stars >= 1:
            lbl1.configure(image=pic_star)

        if n_stars == 2:
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

            print(">>> select <<< handle DECK_listbox -> selected trait = {}".format(play_trait.get()))

    else:
        # trait in one of PLAYERS traits is selected, note: 'where' represents the player here
        if idx == ():
            handle_trait[where].set("")
            print(">>> select <<<  no trait in players list available...")

        else:
            selected_card = player_cards[where].get()[int(idx[0])]
            handle_trait[where].set(selected_card)

            print(">>> select <<< handle PLAYER_listbox -> selected trait = {} - by {}".format(
                handle_trait[where].get(), player_name[where].get()))


def create_player_frame(content, defaults, i):
    frame = tk.Frame(content, bg=defaults["bg_frame_1"])
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)  # name + points
    frame.rowconfigure(1, weight=5)  # traits
#    frame.rowconfigure(2, weight=1)  # further actions
    frame.grid(column=i + 1, row=0, padx=5, pady=5, sticky="nesw")  # or use nesw for x-streched frames!

    # ----- name + overview current points -------------------------------
    frame_points = tk.Frame(frame, borderwidth=2, relief="solid")
    frame_points.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")
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
        frame_points,
        textvariable=player_points[i]['face'],
    ).grid(row=1, column=1, sticky="w")
    ttk.Label(
        frame_points,
        textvariable=player_points[i]['drop'],
    ).grid(row=2, column=1, sticky="w")
    ttk.Label(
        frame_points,
        textvariable=player_points[i]['worlds_end'],
    ).grid(row=3, column=1, sticky="w")
    ttk.Label(
        frame_points,
        textvariable=player_points[i]['MOL'],
    ).grid(row=4, column=1, sticky="w")

    # total points
    ttk.Label(
        frame_points,
        textvariable=player_points[i]['total'],
        style="total.TLabel",
    ).grid(row=1, column=2, rowspan=4, padx=0, pady=0, sticky='nesw')

    # ----- list of traits played ----------------------------------------
    frame_traits = tk.Frame(frame, borderwidth=2, relief="solid")
    frame_traits.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nesw")
    frame_traits.columnconfigure(0, weight=1)
    frame_traits.columnconfigure(1, weight=1)
    frame_traits.columnconfigure(2, weight=1)

    lbox_player = tk.Listbox(
        frame_traits,
        height=20,
        listvariable=player_cards[i],
        selectmode=tk.SINGLE,
        exportselection=False,
    )
    lbox_player.grid(row=0, column=0, padx=5, pady=5, sticky='nesw')
    lbox_player.bind(
        "<<ListboxSelect>>", lambda e: update_selected_trait(i, lbox_player.curselection())
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
        command=partial(btn_discard_trait, i, lbox_player),
    ).grid(row=2, column=0, padx=5, sticky='nsw')

    # ----- action buttons -------------------------------------
#    frame_actions = tk.Frame(frame, borderwidth=2, relief="solid")
#    frame_actions.grid(row=2, column=0, padx=5, pady=5, sticky="nesw")
#    frame_actions.columnconfigure(0, weight=1)
#    frame_actions.columnconfigure(1, weight=1)

    return frame


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

    container.grid(row=3, column=0, columnspan=2)


def create_menu_frame(content, defaults):
    frame = tk.Frame(content, bg=defaults["bg_frame_1"])
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=4)
    frame.rowconfigure(2, weight=1)

    # ----- frame 4 player names --------------------------------------------------------
    frame_menu_player = tk.Frame(frame, borderwidth=2, relief="solid")
    frame_menu_player.grid(row=0, column=0, padx=5, pady=5, sticky="nesw")
    frame_menu_player.columnconfigure(0, weight=1)

    ttk.Label(
        frame_menu_player,
        text="# of players?",
        font="'' 18",
    ).grid(row=0, column=0, columnspan=2, pady=(5, 0))

    ttk.Spinbox(
        frame_menu_player,
        from_=2,
        to=max_player.get(),
        width=3,
        textvariable=n_player,
        wrap=False,
        command=lambda: create_player_entries(frame_player_entries),
    ).grid(row=1, column=0, columnspan=2)

    ttk.Label(
        frame_menu_player,
        text="who's playing?",
        font="'' 18",
    ).grid(row=2, column=0, columnspan=2, pady=(10, 0))

    frame_player_entries = tk.Frame(frame_menu_player)
    create_player_entries(frame_player_entries)

    ttk.Button(
        frame_menu_player,
        text="restart game",
        command=lambda: btn_restart_game(content, frame_menu_buttons),
    ).grid(row=n_player.get() + 3, column=0, columnspan=2, pady=10)

    # ----- frame 4 trait selection --------------------------------------------------------
    frame_menu_traits = tk.Frame(frame, borderwidth=2, relief="solid")
    frame_menu_traits.grid(row=1, column=0, padx=5, pady=0, sticky="nesw")
    frame_menu_traits.columnconfigure(0, weight=1)
    frame_menu_traits.columnconfigure(1, weight=1)

    ttk.Label(
        frame_menu_traits,
        text="select trait:",
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
        frame_menu_traits, height=8, listvariable=lbox_cards, selectmode=tk.SINGLE, exportselection=False
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

    # ----- frame for control buttons --------------------------------------------------------
    frame_menu_controls = tk.Frame(frame, borderwidth=2, relief="solid")
    frame_menu_controls.grid(row=2, column=0, padx=5, pady=5, sticky="nesw")
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
    "bg_content": "grey",
    "bg_frame_1": "lightgrey",
}

# create a window --------------------------------------------------------
root = tk.Tk()
root.title("LIVE Doomlings Calculator")
root.geometry("1600x800")
root.configure(background="grey")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# init variables ---------------------------------------------------------
n_player = tk.IntVar(value=defaults["n_player"])        # number of cuurent players
max_player = tk.IntVar(value=defaults["max_player"])    # theoretical max. num of players
search_trait_str = tk.StringVar(value="")               # searching for traits in playable deck
deck_cards = tk.Variable(value=traits_list_all)
lbox_cards = tk.Variable(value=traits_list_all)     # traits >>shown<< in listbox on the left, i.e. after filtering
play_trait = tk.StringVar(value="")

player_name = []
player_points = []
player_cards = []
handle_trait = []
for i in range(max_player.get()):
    player_name.append(tk.StringVar(value=defaults["names"][i]))
    player_points.append({'face': tk.IntVar(value=0), 'drop': tk.IntVar(value=0),
                          'worlds_end': tk.IntVar(value=0), 'MOL': tk.IntVar(value=0),
                          'total': tk.IntVar(value=0)})
    player_cards.append(tk.Variable(value=[]))
    handle_trait.append(tk.StringVar(value=""))

# styling ----------------------------------------------------------------
gui_style = ttk.Style()
gui_style.configure("total.TLabel", font=("", 56, "bold"), foreground="red")
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
