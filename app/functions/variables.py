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


def reset_variables():
    # update first player if someone is not playing anymore
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
                "sb": "\u2211 0",
            }
        )
        st.session_state.plr["trait_selected"].append(np.nan)
        st.session_state.plr["points_WE_effect"].append(0)
        st.session_state.plr["points_MOL"].append([])
        st.session_state.MOLs["played"].append([])
        st.session_state.MOLs["cbox"].append([])
        st.session_state.MOLs["icon"].append([])
        st.session_state.MOLs["n"].append(st.session_state.game["n_MOLs"])

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
    st.session_state.deck.extend(st.session_state.df["traits_df"].index.tolist())
    st.session_state.deck_str = (
        st.session_state.df["traits_df"]
        .loc[st.session_state.deck]
        .trait.values.tolist()
    )

    # reset occurred catastrophes
    st.session_state.catastrophe["possible"].clear()
    st.session_state.catastrophe["played"].clear()
    st.session_state.catastrophe["cbox"].clear()
    for i in range(st.session_state.game["n_catastrophes"]):
        st.session_state.catastrophe["possible"].append(
            st.session_state.df["catastrophes_df"].index.tolist()
        )
        st.session_state.catastrophe["played"].append(None)
        st.session_state.catastrophe["cbox"].append([])

    # reset worlds end
    st.session_state.worlds_end["selected"] = ""
    st.session_state.worlds_end["played"] = "none"
    st.session_state.worlds_end["cbox"] = [None]
    st.session_state.worlds_end["btn"] = [None]

    # reset current status
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
