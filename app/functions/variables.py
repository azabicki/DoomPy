import streamlit as st
import numpy as np


def init_vars():
    from functions.globals_ import cfg, images
    from functions.globals_ import traits_df, status_df, catastrophes_df, MOLs_df
    from functions.globals_ import game, plr, deck, catastrophe, worlds_end, MOLs

    # booting --------------------------------------------------
    if "booting" not in st.session_state:
        st.session_state.booting = True

    # cfg / general settings --------------------------------------------------
    if "cfg" not in st.session_state:
        st.session_state.cfg = cfg
    if "images_dict" not in st.session_state:
        st.session_state.images = images

    # load excel --------------------------------------------------------------
    if "df" not in st.session_state:
        st.session_state.df = {
            "traits_df": traits_df,
            "status_df": status_df,
            "catastrophes_df": catastrophes_df,
            "MOLs_df": MOLs_df,
        }

    # game/player vars --------------------------------------------------------
    if "game" not in st.session_state:
        st.session_state.game = game
    if "plr" not in st.session_state:
        st.session_state.plr = plr
    if "deck" not in st.session_state:
        st.session_state.deck = deck
    if "deck_str" not in st.session_state:
        st.session_state.deck_str = ""
    if "catastrophe" not in st.session_state:
        st.session_state.catastrophe = catastrophe
    if "worlds_end" not in st.session_state:
        st.session_state.worlds_end = worlds_end
    if "MOLs" not in st.session_state:
        st.session_state.MOLs = MOLs
    if "1st_player" not in st.session_state:
        st.session_state["1st_player"] = 0
    if "points_onoff" not in st.session_state:
        st.session_state["points_onoff"] = (
            0  # 0: "visible" / 1: "rank only" / 2: "hidden"
        )


def reset_variables():
    # player -----------------------------------------
    st.session_state.plr["name"].clear()
    st.session_state.plr["genes"].clear()
    st.session_state.plr["points"].clear()
    st.session_state.plr["trait_pile"].clear()
    st.session_state.plr["n_tp"].clear()
    st.session_state.plr["trait_selected"].clear()
    st.session_state.plr["points_WE_effect"].clear()
    st.session_state.plr["points_MOL"].clear()

    # players - fill -----
    for p in range(st.session_state.game["n_player"]):
        st.session_state.plr["name"].append(st.session_state.cfg["names"][p])
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
                "sb": "\u22110",
            }
        )
        st.session_state.plr["trait_selected"].append(np.nan)
        st.session_state.plr["points_WE_effect"].append(0)
        st.session_state.plr["points_MOL"].append([])

        for m in range(st.session_state.game["n_MOLs"]):
            st.session_state.plr["points_MOL"][p].append(
                0
            )  # for now, manually editing MOL points in entries

    # MOLs -----------------------------------------
    st.session_state.MOLs["played"].clear()
    st.session_state.MOLs["n"].clear()

    # MOLs - fill -----
    for p in range(st.session_state.game["n_player"]):
        st.session_state.MOLs["n"].append(st.session_state.game["n_MOLs"])
        st.session_state.MOLs["played"].append([])

        for m in range(st.session_state.game["n_MOLs"]):
            st.session_state.MOLs["played"][p].append(None)

    # game -----------------------------------------
    st.session_state.game["neoteny_checkbutton"].clear()
    st.session_state.game["sleepy_spinbox"].clear()

    # game - fill -----
    for p in range(st.session_state.game["n_player"]):
        st.session_state.game["neoteny_checkbutton"].append(0)
        st.session_state.game["sleepy_spinbox"].append(0)

    # deck -----------------------------------------
    st.session_state.deck.clear()

    # deck - fill -----
    st.session_state.deck.extend(st.session_state.df["traits_df"].index.tolist())
    st.session_state.deck_str = (
        st.session_state.df["traits_df"]
        .loc[st.session_state.deck]
        .trait.values.tolist()
    )

    # catastrophes -----------------------------------------
    st.session_state.catastrophe["possible"].clear()
    st.session_state.catastrophe["played"].clear()

    # catastrophes - fill -----
    for c in range(st.session_state.game["n_catastrophes"]):
        st.session_state.catastrophe["possible"].append(
            st.session_state.df["catastrophes_df"].index.tolist()
        )
        st.session_state.catastrophe["played"].append(None)

    # worlds end -----------------------------------------
    st.session_state.worlds_end["played"] = "none"
    st.session_state.worlds_end["btn"] = [None]

    # status_df -----------------------------------------
    st.session_state.df["status_df"]["color"] = st.session_state.df["traits_df"].color
    st.session_state.df["status_df"]["face"] = st.session_state.df["traits_df"].face
    st.session_state.df["status_df"]["drops"] = np.nan
    st.session_state.df["status_df"]["host"] = "none"
    st.session_state.df["status_df"]["attachment"] = "none"
    st.session_state.df["status_df"]["inactive"] = False
    st.session_state.df["status_df"]["no_remove"] = False
    st.session_state.df["status_df"]["no_discard"] = False
    st.session_state.df["status_df"]["no_steal"] = False
    st.session_state.df["status_df"]["no_swap"] = False
    st.session_state.df["status_df"]["effects"] = "none"
    st.session_state.df["status_df"]["effects_attachment"] = "none"
    st.session_state.df["status_df"]["effects_traits_WE"] = "none"
    st.session_state.df["status_df"]["effects_WE"] = "none"
    st.session_state.df["status_df"]["traits_WE"] = "none"

    # first player -----------------------------------------
    if st.session_state["1st_player"] + 1 > st.session_state.game["n_player"]:
        st.session_state["1st_player"] = st.session_state.game["n_player"] - 1

    # widget-status-variables -----------------------------------------
    for p in range(st.session_state.game["n_player"]):
        st.session_state[f"move_to_{p}"] = "move to"
        st.session_state[f"neoteny_{p}"] = False

        for m in range(st.session_state.game["n_MOLs"] + 2):
            st.session_state[f"MOL_{p}_{m}"] = 0
            st.session_state[f"mol_points_{p}_{m}"] = 0

    for c in range(st.session_state.game["n_catastrophes"]):
        st.session_state[f"catastrophe_{c}"] = 0

    st.session_state["selected_worlds_end"] = None
