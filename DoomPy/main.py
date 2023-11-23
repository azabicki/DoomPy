import os
import tkinter as tk
from tkinter import ttk
from math import floor
from functools import partial
import pandas as pd

# system settings ######################################################
curdir = os.path.dirname(__file__)

# load card list #######################################################
traits_df = pd.read_excel(os.path.join(curdir, "cards.xlsx"))
traits_list_all = sorted(traits_df["name"].values.tolist())


# functions ############################################################
def btn_clear_trait_search():
    search_trait_str.set("")
    lbox_cards.set(deck_cards.get())
    lbox_traits.selection_clear(0, tk.END)
    play_trait.set("")


def btn_restart_game(content, frame_menu_buttons):
    # reset game variables
    search_trait_str.set("")
    deck_cards.set(traits_list_all)
    lbox_cards.set(traits_list_all)
    play_trait.set("")

    player_points = []
    player_cards = []
    for i in range(max_player.get()):
        player_points.append({'face': tk.IntVar(value=0), 'drop': tk.IntVar(value=0),
                              'worlds_end': tk.IntVar(value=0), 'MOL': tk.IntVar(value=0),
                              'total': tk.IntVar(value=0)})
        player_cards.append(tk.Variable(value=[]))

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


def btn_play_trait(p):
    # get card
    card = play_trait.get()

    # return if no trait selected
    if card == "":
        print("no trait is selected...")
        return

    # add to players traits
    cur_players_lst = list(player_cards[p].get())
    cur_players_lst.append(card)
    player_cards[p].set(cur_players_lst)

    # remove from deck if all cards played
    card_played = 0
    for i in range(n_player.get()):
        card_played = card_played + sum([1 for x in list(player_cards[i].get()) if x == card])
    card_n = traits_df[traits_df['name'] == card]['n_of_cards'].values[0]

    if card_played == card_n:
        cur_deck_cards = list(deck_cards.get())
        cur_deck_cards.remove(card)
        deck_cards.set(cur_deck_cards)

    # clear trait search & selection
    btn_clear_trait_search()

    print("{} is playing {}, which is {} times in the deck and was played {} times".format(
        player_name[p].get(), card, card_n, card_played))


def search_trait_in_list(event):
    value = event.widget.get()

    if value == "":
        lbox_cards.set(deck_cards.get())
    else:
        lbox_cards.set([item for item in deck_cards.get() if value.lower() in item.lower()])


def update_selected_trait(x):
    selected_card = lbox_cards.get()[int(x[0])]
    play_trait.set(selected_card)


def create_player_frame(content, defaults, i):
    frame = tk.Frame(content, bg=defaults["bg_frame_1"])
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)  # name
    frame.rowconfigure(1, weight=1)  # points
    frame.rowconfigure(2, weight=5)  # traits
    frame.grid(column=i + 1, row=0, padx=5, pady=5, sticky="n")  # or use nesw for x-streched frames!

    # ----- name + overview current points --------------
    frame_points = tk.Frame(frame)
    frame_points.grid(row=0, column=0, padx=5, pady=5, ipady=5, sticky="nesw")
    frame_points.columnconfigure(0, weight=1)
    frame_points.columnconfigure(1, weight=1)
    frame_points.columnconfigure(2, weight=1)

    # name
    ttk.Label(
        frame_points,
        textvariable=player_name[i],
        font='"Comic Sans MS" 36 italic',
    ).grid(row=0, column=0, padx=5, pady=(0, 10), columnspan=3)

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
    ).grid(row=1, column=2, rowspan=4, padx=0, pady=0)

    # ----- list of traits played --------------
    frame_traits = tk.Frame(frame)
    frame_traits.grid(row=1, column=0, padx=5, sticky="nesw")
    frame_traits.columnconfigure(0, weight=1)
    frame_traits.columnconfigure(1, weight=1)
    frame_traits.columnconfigure(2, weight=1)

    tk.Listbox(
        frame_traits,
        height=20,
        listvariable=player_cards[i],
        selectmode=tk.SINGLE,
    ).grid(row=0, column=0, padx=10, pady=10)

    # ----- xxx --------------

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
        frame_menu_traits, height=8, listvariable=lbox_cards, selectmode=tk.SINGLE
    )
    lbox_traits.grid(row=2, column=0, columnspan=2, padx=10)
    lbox_traits.bind(
        "<<ListboxSelect>>", lambda e: update_selected_trait(lbox_traits.curselection())
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


###########################################################################
# default variables
defaults = {
    "names": ["Lisa", "Julia", "Anton", "Adam", "Ben", "Franzi"],
    "n_player": 4,
    "max_player": 6,
    "bg_content": "grey",
    "bg_frame_1": "lightgrey",
}

# create a window
root = tk.Tk()
root.title("LIVE Doomlings Calculator")
root.geometry("1600x800")
root.configure(background="grey")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# init variables
n_player = tk.IntVar(value=defaults["n_player"])
max_player = tk.IntVar(value=defaults["max_player"])
search_trait_str = tk.StringVar(value="")
deck_cards = tk.Variable(value=traits_list_all)
lbox_cards = tk.Variable(value=traits_list_all)
play_trait = tk.StringVar(value="")

player_name = []
player_points = []
player_cards = []
for i in range(max_player.get()):
    player_name.append(tk.StringVar(value=defaults["names"][i]))
    player_points.append({'face': tk.IntVar(value=0), 'drop': tk.IntVar(value=0),
                          'worlds_end': tk.IntVar(value=0), 'MOL': tk.IntVar(value=0),
                          'total': tk.IntVar(value=0)})
    player_cards.append(tk.Variable(value=[]))

# styling
gui_style = ttk.Style()
gui_style.configure("total.TLabel", font=("", 56, "bold"), foreground="red")

# content frame
content = tk.Frame(root, width=1200, height=800, bg=defaults["bg_content"])
content.grid(column=0, row=0, sticky="nesw")
content.columnconfigure(0, weight=0)
for i in range(n_player.get()):
    content.columnconfigure(i + 1, weight=1)

# create menu frame
frame_menu, lbox_traits = create_menu_frame(content, defaults)
frame_menu.grid(column=0, row=0, padx=5, pady=5, stick="nesw")

# create player-frames
frames_player = []
for i in range(n_player.get()):
    frames_player.append(create_player_frame(content, defaults, i))

# ----- run ---------------
root.mainloop()
