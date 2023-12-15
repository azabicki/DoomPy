# global variable for all modules
import os
import glob
import json
import time
import numpy as np
import pandas as pd
from PIL import Image
from pygame import mixer
import tkinter as tk


# loading stuff ####################################################################################
curdir = os.path.dirname(__file__)

# load config file ---------------------------------------------------------------------------------
global cfg
with open("DoomPy/config.json") as json_file:
    cfg = json.load(json_file)

# logfile to store debug lines ---------------------------------------------------------------------
global logfile
logfile = os.path.join(curdir, "logs", "DoomPyLog_" + time.strftime("%Y%m%d-%H%M%S") + ".txt")

# load cards.xlsx ----------------------------------------------------------------------------------
global traits_df, traits_dfi, ages_df, catastrophies_dfi

traits_df_unsorted = pd.read_excel(os.path.join(curdir, "files", "cards.xlsx"), sheet_name="traits")
traits_df = traits_df_unsorted.sort_values(by='trait').reset_index(drop=True)
traits_dfi = traits_df.index.tolist()

ages_df_unsorted = pd.read_excel(os.path.join(curdir, "files", "cards.xlsx"), sheet_name="ages")
ages_df = ages_df_unsorted.sort_values(by='name').reset_index(drop=True)
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

# load images --------------------------------------------------------------------------------------
global images_dict
images_dict = {}
img_size_star = 30
img_size_scoreboard = 24
img_size_icons = 20

# basic
for files in glob.glob(os.path.join(curdir, "images", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files).resize((img_size_icons, img_size_icons))

# dominant-star
for files in glob.glob(os.path.join(curdir, "images", "dominant_star", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files).resize((img_size_star, img_size_star))

# color icons
for files in glob.glob(os.path.join(curdir, "images", "colors", cfg["img_colors_set"], "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files).resize((img_size_icons, img_size_icons))

# trait porperties
for files in glob.glob(os.path.join(curdir, "images", "trait_properties", cfg["img_trait_properties_set"], "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files).resize((img_size_icons, img_size_icons))

# scoreboard icons
for files in glob.glob(os.path.join(curdir, "images", "trait_properties", cfg["img_trait_properties_set"], "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0] + '_sb'
    images_dict[var_name] = Image.open(files).resize((img_size_scoreboard, img_size_scoreboard))

# effects on traits
for files in glob.glob(os.path.join(curdir, "images", "effects", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files)

    # pay attention to w/h-ratio
    w, h = images_dict[var_name].size
    actual_img_w = int(w / h * img_size_icons)
    images_dict[var_name] = images_dict[var_name].resize((actual_img_w, img_size_icons))

# points
for files in glob.glob(os.path.join(curdir, "images", "points", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files)

    # pay attention to w/h-ratio
    w, h = images_dict[var_name].size
    actual_img_w = int(w / h * img_size_icons)
    images_dict[var_name] = images_dict[var_name].resize((actual_img_w, img_size_icons))

# load sounds --------------------------------------------------------------------------------------
global sounds
sounds = {}
mixer.init()

for files in glob.glob(os.path.join(curdir, "sounds", "*.mp3")):
    var_name = os.path.splitext(os.path.basename(files))[0].lower()
    sounds[var_name] = mixer.Sound(files)


# design variables #################################################################################
global music_onoff, icons_onoff, show_icons
music_onoff = tk.StringVar(value='on')
icons_onoff = tk.StringVar(value='on')

show_icons = {}
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


# define game variables ############################################################################
