import streamlit as st
import numpy as np


def init_vars():
    from functions.globals_ import cfg, images_dict
    from functions.globals_ import traits_df, status_df, catastrophes_df, MOLs_df
    from functions.globals_ import game, plr, deck, catastrophe, worlds_end, MOLs

    # cfg / general settings --------------------------------------------------
    if "cfg" not in st.session_state:
        st.session_state.cfg = cfg
    if "images_dict" not in st.session_state:
        st.session_state.images_dict = images_dict

    # load excel --------------------------------------------------------------
    if "df" not in st.session_state:
        st.session_state.df = {
            "traits": traits_df,
            "status": status_df,
            "catastrophes": catastrophes_df,
            "MOLs": MOLs_df,
        }

    # game/player vars --------------------------------------------------------
    if "game" not in st.session_state:
        st.session_state.game = game
    if "plr" not in st.session_state:
        st.session_state.plr = plr
    if "deck" not in st.session_state:
        st.session_state.deck = deck
    if "catastrophe" not in st.session_state:
        st.session_state.catastrophe = catastrophe
    if "worlds_end" not in st.session_state:
        st.session_state.worlds_end = worlds_end
    if "MOLs" not in st.session_state:
        st.session_state.MOLs = MOLs

    # options -----------------------------------------------------------------
    if "options" not in st.session_state:
        options = {}
        options["n_player"] = cfg["n_player"]  # OPTIONS: number of players
        options["n_genes"] = cfg["n_genes"]  # OPTIONS: gene pool at beginning
        options["n_catastrophes"] = cfg[
            "n_catastrophes"
        ]  # OPTIONS: number of catastrophes
        options["n_MOLs"] = cfg["n_MOLs"]  # OPTIONS: number of MOLs
        options["names"] = []
        for i in range(len(cfg["names"])):
            options["names"].append(cfg["names"][i])  # OPTIONS: name of players

        st.session_state.options = options

    if "deck_str" not in st.session_state:
        st.session_state.deck_str = ""


def reset_variables():
    # update current settings
    st.session_state.game["n_player"] = st.session_state.options["n_player"]
    st.session_state.game["n_genes"] = st.session_state.options["n_genes"]
    st.session_state.game["n_catastrophes"] = st.session_state.options["n_catastrophes"]
    st.session_state.game["n_MOLs"] = st.session_state.options["n_MOLs"]

    # update first player if not playing anymore
    if st.session_state.game["first_player"] + 1 > st.session_state.game["n_player"]:
        st.session_state.game["first_player"] = st.session_state.game["n_player"] - 1

    # reset _player_ variables
    st.session_state.plr["name"].clear()
    st.session_state.plr["genes"].clear()
    st.session_state.plr["points"].clear()
    st.session_state.plr["trait_pile"].clear()
    st.session_state.plr["n_tp"].clear()
    st.session_state.plr["trait_selected"].clear()
    st.session_state.plr["points_WE_effect"].clear()
    st.session_state.plr["points_MOL"].clear()

    # reset MOLs
    st.session_state.MOLs["played"].clear()
    st.session_state.MOLs["cbox"].clear()
    st.session_state.MOLs["icon"].clear()
    st.session_state.MOLs["n"].clear()

    # reset trait_specific variables
    st.session_state.game["neoteny_checkbutton"].clear()
    st.session_state.game["sleepy_spinbox"].clear()

    # fill variables
    for p in range(st.session_state.game["n_player"]):
        st.session_state.plr["name"].append(st.session_state.options["names"][p])

        st.session_state.plr["genes"].append(st.session_state.game["n_genes"])
        st.session_state.plr["points"].append(
            {
                "face": 0,
                "drops": 0,
                "worlds_end": 0,
                "MOL": 0,
                "total": 0,
            }
        )
        st.session_state.plr["trait_pile"].append([])
        st.session_state.plr["n_tp"].append(
            {
                "b": "0",
                "g": "0",
                "p": "0",
                "r": "0",
                "c": "0",
                "t": "0",
                "xtra": 0,
                "sb": "\u2211 0",
            }
        )
        st.session_state.plr["trait_selected"].append(np.nan)
        st.session_state.plr["points_WE_effect"].append(0)
        st.session_state.plr["points_MOL"].append([])
        st.session_state.MOLs["played"].append([])
        st.session_state.MOLs["cbox"].append([])
        st.session_state.MOLs["icon"].append([])
        st.session_state.MOLs["n"].append(st.session_state.options["n_MOLs"])

        st.session_state.game["neoteny_checkbutton"].append(0)
        st.session_state.game["sleepy_spinbox"].append(0)

        for m in range(st.session_state.game["n_MOLs"]):
            st.session_state.plr["points_MOL"][p].append(
                0
            )  # for now, manually editing MOL points in entries
            st.session_state.MOLs["played"][p].append(None)
            st.session_state.MOLs["cbox"][p].append([])
            st.session_state.MOLs["icon"][p].append([])

    # reset deck/lbox card-lists
    st.session_state.deck.clear()
    st.session_state.deck.extend(st.session_state.df["traits"].index.tolist())
    st.session_state.deck_str = st.session_state.df["traits"] \
        .loc[st.session_state.deck].trait.values.tolist()

    # reset occurred catastrophes
    st.session_state.catastrophe["possible"].clear()
    st.session_state.catastrophe["played"].clear()
    st.session_state.catastrophe["cbox"].clear()
    for i in range(st.session_state.game["n_catastrophes"]):
        st.session_state.catastrophe["possible"].append(
            st.session_state.df["catastrophes"].index.tolist()
        )
        st.session_state.catastrophe["played"].append(None)
        st.session_state.catastrophe["cbox"].append([])

    # reset worlds end
    st.session_state.worlds_end["selected"] = ""
    st.session_state.worlds_end["played"] = "none"
    st.session_state.worlds_end["cbox"] = [None]
    st.session_state.worlds_end["btn"] = [None]

    # reset current status
    st.session_state.df["status"]["color"] = st.session_state.df["traits"].color
    st.session_state.df["status"]["face"] = st.session_state.df["traits"].face
    st.session_state.df["status"]["drops"] = np.nan
    st.session_state.df["status"]["host"] = "none"
    st.session_state.df["status"]["attachment"] = "none"
    st.session_state.df["status"]["inactive"] = False
    st.session_state.df["status"]["no_remove"] = False
    st.session_state.df["status"]["no_discard"] = False
    st.session_state.df["status"]["no_steal"] = False
    st.session_state.df["status"]["no_swap"] = False
    st.session_state.df["status"]["effects"] = "none"
    st.session_state.df["status"]["effects_attachment"] = "none"
    st.session_state.df["status"]["effects_traits_WE"] = "none"
    st.session_state.df["status"]["effects_WE"] = "none"
    st.session_state.df["status"]["traits_WE"] = "none"


def start_game():
    reset_variables()


def switch_first_player():
    pass
