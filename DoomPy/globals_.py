# global variable for all modules
import os
import glob
import json
import time
import numpy as np
import pandas as pd
from PIL import Image
from pygame import mixer


# loading stuff ####################################################################################
curdir = os.path.dirname(__file__)
dir_log = os.path.join(curdir, "logs")
dir_files = os.path.join(curdir, "files")
dir_images = os.path.join(curdir, "images")

# load config file ---------------------------------------------------------------------------------
global cfg
with open(os.path.join(curdir, "config.json")) as json_file:
    cfg = json.load(json_file)

# logfile to store debug lines ---------------------------------------------------------------------
global logfile
logfile = os.path.join(dir_log, "DoomPyLog_" + time.strftime("%Y%m%d-%H%M%S") + ".txt")

# load cards.xlsx ----------------------------------------------------------------------------------
global traits_df, status_df, catastrophies_df

# traits
xlsx_traits = pd.read_excel(os.path.join(dir_files, "cards.xlsx"), sheet_name="traits")
traits_df = (xlsx_traits
             .sort_values(by='trait')
             .reset_index(drop=True)
             .drop(columns='id'))

# create new status dataframe containing current status of each trait
status_df = traits_df[['trait', 'color', 'face']].copy()
status_df['drops'] = np.nan
status_df['host'] = None
status_df['attachment'] = None
status_df['effects'] = True
status_df['remove'] = True
status_df['discard'] = True
status_df['steal'] = True
status_df['swap'] = True
status_df['traits_WE'] = None
status_df['we_effect'] = None

# catastrophies
xlsx_ages = pd.read_excel(os.path.join(dir_files, "cards.xlsx"), sheet_name="ages")
xlsx_catastrophies = xlsx_ages.loc[xlsx_ages['type'] == 'Catastrophe']
catastrophies_df = (xlsx_catastrophies
                    .sort_values(by='name')
                    .reset_index(drop=True)
                    .drop(columns=['game', 'type']))

# load images --------------------------------------------------------------------------------------
global images_dict
images_dict = {}
img_size_star = 30
img_size_scoreboard = 24
img_size_icons = 20

# basic
for files in glob.glob(os.path.join(dir_images, "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files).resize((img_size_icons, img_size_icons))

# dominant-star
for files in glob.glob(os.path.join(dir_images, "dominant_star", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files).resize((img_size_star, img_size_star))

# color icons
for files in glob.glob(os.path.join(dir_images, "colors", cfg["img_colors_set"], "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files).resize((img_size_icons, img_size_icons))

# trait porperties
for files in glob.glob(os.path.join(dir_images, "trait_properties", cfg["img_trait_properties_set"], "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files).resize((img_size_icons, img_size_icons))

# scoreboard icons
for files in glob.glob(os.path.join(dir_images, "trait_properties", cfg["img_trait_properties_set"], "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0] + '_sb'
    images_dict[var_name] = Image.open(files).resize((img_size_scoreboard, img_size_scoreboard))

# effects on traits
for files in glob.glob(os.path.join(dir_images, "effects", "*.png")):
    var_name = os.path.splitext(os.path.basename(files))[0]
    images_dict[var_name] = Image.open(files)

    # pay attention to w/h-ratio
    w, h = images_dict[var_name].size
    actual_img_w = int(w / h * img_size_icons)
    images_dict[var_name] = images_dict[var_name].resize((actual_img_w, img_size_icons))

# points
for files in glob.glob(os.path.join(dir_images, "points", "*.png")):
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


# switches #########################################################################################
global music_onoff, icons_onoff, points_onoff, show_icons
music_onoff = 'off'     # 'off' / 'on'
icons_onoff = 'on'      # 'off' / 'on' / 'full'
points_onoff = 'on'     # 'off' / 'on'

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


# tk_inter variables ###############################################################################
global lbl_music_switch, lbl_icons_switch, lbl_points_switch, ent_trait_search, lbox_menu_deck
lbl_music_switch = [None]   # label containing music-switch-icon
lbl_icons_switch = [None]   # label containing icon-switch-icon
lbl_points_switch = [None]   # label containing icon-switch-icon
ent_trait_search = [None]   # entry for trait_search
lbox_deck = [None]     # listbox widget of deck cards -> needed to be able to edit selected traits

global frame_player, frame_trait_pile
frame_player = []          # list of all players frames
frame_trait_pile = []       # frame containing players traits -> needed to be able to edit selected traits


# define game variables ############################################################################
# settings -----------------------------------------------------------------------------------------
global game, plr, deck, deck_filtered_idx, catastrophe, worlds_end
game = {}
game['n_player'] = []           # number of current players
game['n_genes'] = []            # gene pool at start
game['n_catastrophies'] = []    # number of catastrophies
game['n_MOLs'] = []             # number of MOLs

plr = {}
plr['name'] = []
plr['genes'] = []
plr['points'] = []
plr['trait_pile'] = []
plr['trait_selected'] = []
plr['WE_effect'] = []
plr['MOL'] = []

deck = []                       # all traits in deck (or discard pile) left to be drawn / list of idx
deck_filtered_idx = []          # _filtered_ deck of trait_idx in listbox after searching -> idx

catastrophe = {}
catastrophe['possible'] = []                  # occured catastrophies / StringVar
catastrophe['played'] = []                  # occured catastrophies / StringVar
catastrophe['cbox'] = []             # comboxes containing possible catastrophies

worlds_end = {}
worlds_end['cbox'] = [None]
worlds_end['name'] = None


# trait specific variables #########################################################################
global neoteny_checkbutton, sleepy_spinbox
neoteny_checkbutton = []
sleepy_spinbox = []
