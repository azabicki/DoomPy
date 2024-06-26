# global variable for all modules
import os
import glob
import numpy as np
import pandas as pd


# loading stuff ###############################################################
curdir = os.path.dirname(__file__)
dir_files = os.path.join(curdir, "..")
dir_images = os.path.join(curdir, "..", "..", "doompy", "images")

# region load config file -----------------------------------------------------
cfg = dict()
cfg["names"] = ["Lisa", "Julia", "Anton", "Adam", "Ben", "Franzi"]
cfg["n_player"] = 4
cfg["n_genes"] = 5
cfg["n_catastrophes"] = 3
cfg["n_MOLs"] = 1
cfg["max_player"] = 6

# set trait colors
cfg["color_blue"] = "#1C86ee"
cfg["color_green"] = "#0da953"
cfg["color_purple"] = "#e066ff"
cfg["color_red"] = "#e1484a"
cfg["color_colorless"] = "#8e8e8e"

# set specific colors
cfg["font_color_dominant"] = "#EE7621"
cfg["font_color_1st_player"] = "#0da953"
cfg["font_color_total_score"] = "#e1484a"
cfg["font_color_genes"] = "#bf3eff"

# region load cards.xlsx ------------------------------------------------------
# traits
xlsx_traits = pd.read_excel(os.path.join(dir_files, "assets", "cards.xlsx"), sheet_name="traits")
xlsx_traits = xlsx_traits[xlsx_traits["in_game"] == "yes"]
traits_df = (
    xlsx_traits.loc[xlsx_traits.index.repeat(xlsx_traits.n_cards)]
    .sort_values(by="trait")
    .reset_index(drop=True)
)

# create new status dataframe containing current status of each trait
status_df = traits_df[["trait", "color", "face"]].copy()
status_df["drops"] = np.nan
status_df["host"] = "none"
status_df["attachment"] = "none"
status_df["inactive"] = False
status_df["no_remove"] = False
status_df["no_discard"] = False
status_df["no_steal"] = False
status_df["no_swap"] = False
status_df["effects"] = "none"
status_df["effects_attachment"] = "none"
status_df["effects_traits_WE"] = "none"
status_df["effects_WE"] = "none"
status_df["traits_WE"] = "none"

# catastrophes
xlsx_ages = pd.read_excel(os.path.join(dir_files, "assets", "cards.xlsx"), sheet_name="ages")
xlsx_catastrophes = xlsx_ages.loc[xlsx_ages["type"] == "Catastrophe"]
xlsx_catastrophes = xlsx_catastrophes.loc[xlsx_catastrophes["in_game"] == "yes"]
catastrophes_df = (
    xlsx_catastrophes.sort_values(by="name")
    .reset_index(drop=True)
    .drop(columns=["game", "type"])
)

# MOLs
xlsx_MOLs = pd.read_excel(os.path.join(dir_files, "assets", "cards.xlsx"), sheet_name="MOL")
xlsx_MOLs = xlsx_MOLs[xlsx_MOLs["in_game"] == "yes"]
MOLs_df = xlsx_MOLs.sort_values(by="MOL").reset_index(drop=True).drop(columns="game")

# region load images ----------------------------------------------------------
images = {}

# basic
for files in glob.glob(os.path.join(dir_images, "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images[var_name] = files

# dominant-star
for files in glob.glob(os.path.join(dir_images, "dominant_star", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images[var_name] = files

# color icons
for files in glob.glob(os.path.join(dir_images, "colors", "circle", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images[var_name] = files

# trait properties
for files in glob.glob(
    os.path.join(dir_images, "trait_properties", "official_setA", "*.png")
):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images[var_name] = files

    if var_name == "catastrophe":
        var_WE = var_name + "_WE"
        images[var_WE] = files

# scoreboard icons
for files in glob.glob(
    os.path.join(dir_images, "trait_properties", "official_setA", "*_sb.png")
):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images[var_name] = files

# effects on traits
for files in glob.glob(os.path.join(dir_images, "effects", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images[var_name] = files

# points
for files in glob.glob(os.path.join(dir_images, "points", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images[var_name] = files


# region tk_inter variables ---------------------------------------------------
lbl_points_switch = [None]  # label containing icon-switch-icon

# region game variables -------------------------------------------------------
game = {}
game["n_player"] = cfg["n_player"]  # number of current players
game["n_genes"] = cfg["n_genes"]  # gene pool at start
game["n_catastrophes"] = cfg["n_catastrophes"]  # number of catastrophes
game["n_MOLs"] = cfg["n_MOLs"]  # number of MOLs
game["neoteny_checkbutton"] = []
game["sleepy_spinbox"] = []

deck = []  # all traits in deck (or discard pile) left to be drawn / list of idx

plr = {}
plr["name"] = []
plr["genes"] = []
plr["points"] = []
plr["trait_pile"] = []
plr["n_tp"] = []  # count of traits -> separated by colors / xtra_effects / scoreboard
plr["trait_selected"] = []
plr["points_WE_effect"] = []
plr["points_MOL"] = []

MOLs = {}
MOLs["played"] = []  # played MOLs
MOLs["n"] = []  # number of MOLs for each player -> may be different


catastrophe = {}
catastrophe["possible"] = []  # list of possibles catastrophes
catastrophe["played"] = []  # occurred catastrophes / needed for worlds end

worlds_end = {}
worlds_end["played"] = "none"  # play this world-end-event
worlds_end["btn"] = [None]  # button running worlds end
