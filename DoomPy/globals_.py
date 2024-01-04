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
global cfg, sim_running
with open(os.path.join(curdir, "config.json")) as json_file:
    cfg = json.load(json_file)

# flag for simulation
sim_running = [False]

# load cards.xlsx ----------------------------------------------------------------------------------
global traits_df, status_df, catastrophes_df, MOLs_df

# traits
xlsx_traits = pd.read_excel(os.path.join(dir_files, "cards.xlsx"), sheet_name="traits")
xlsx_traits = xlsx_traits[xlsx_traits['in_game'] == 'yes']
traits_df = (xlsx_traits
             .sort_values(by='trait')
             .reset_index(drop=True)
             .drop(columns='id'))

# create new status dataframe containing current status of each trait
status_df = traits_df[['trait', 'color', 'face']].copy()
status_df['drops'] = np.nan
status_df['host'] = 'none'
status_df['attachment'] = 'none'
status_df['inactive'] = False
status_df['no_remove'] = False
status_df['no_discard'] = False
status_df['no_steal'] = False
status_df['no_swap'] = False
status_df['effects'] = 'none'
status_df['effects_attachment'] = 'none'
status_df['effects_traits_WE'] = 'none'
status_df['effects_WE'] = 'none'
status_df['traits_WE'] = 'none'

# catastrophes
xlsx_ages = pd.read_excel(os.path.join(dir_files, "cards.xlsx"), sheet_name="ages")
xlsx_catastrophes = xlsx_ages.loc[xlsx_ages['type'] == 'Catastrophe']
xlsx_catastrophes = xlsx_catastrophes.loc[xlsx_catastrophes['in_game'] == 'yes']
catastrophes_df = (xlsx_catastrophes
                   .sort_values(by='name')
                   .reset_index(drop=True)
                   .drop(columns=['game', 'type']))

# MOLs
xlsx_MOLs = pd.read_excel(os.path.join(dir_files, "cards.xlsx"), sheet_name="MOL")
xlsx_MOLs = xlsx_MOLs[xlsx_MOLs['in_game'] == 'yes']
MOLs_df = (xlsx_MOLs
           .sort_values(by='MOL')
           .reset_index(drop=True)
           .drop(columns='game'))

# load images --------------------------------------------------------------------------------------
global images_dict
images_dict = {}
img_size_scoreboard = 24
img_size_star = 30
img_size_icons = 20
img_size_WE = 40

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

    if var_name == 'catastrophe':
        var_WE = var_name + '_WE'
        images_dict[var_WE] = Image.open(files).resize((img_size_WE, img_size_WE))

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
    images_dict[var_name] = Image.open(files).resize((img_size_icons, img_size_icons))

    # create red-crossed-point-icons
    images_dict[var_name + 'X'] = images_dict[var_name].copy()
    images_dict[var_name + 'X'].paste(images_dict['red_cross'], (0, 0), images_dict['red_cross'])

# load sounds --------------------------------------------------------------------------------------
global sounds
sounds = {}
mixer.init()

for files in glob.glob(os.path.join(curdir, "sounds", "*.mp3")):
    var_name = os.path.splitext(os.path.basename(files))[0].lower()
    sounds[var_name] = mixer.Sound(files)


# switches #########################################################################################
global music_onoff, icons_onoff, points_onoff
music_onoff = 'off'     # 'off' / 'on'
icons_onoff = 'on'      # 'off' / 'on' / 'full'
points_onoff = 'on'     # 'off' / 'on' / 'rank'


# tk_inter variables ###############################################################################
global lbl_music_switch, lbl_icons_switch, lbl_points_switch, ent_trait_search, lbox_menu_deck
lbl_music_switch = [None]   # label containing music-switch-icon
lbl_icons_switch = [None]   # label containing icon-switch-icon
lbl_points_switch = [None]  # label containing icon-switch-icon
ent_trait_search = [None]   # entry for trait_search
lbox_deck = [None]          # listbox widget of deck cards -> needed to be able to edit selected traits

global frame_player, frame_trait_pile, frame_MOL
frame_player = []           # list of all players frames
frame_trait_pile = []       # frame containing players traits -> needed to be able to edit selected traits
frame_MOL = []              # frame containing MOLs

# define game variables ############################################################################
# settings -----------------------------------------------------------------------------------------
global game, plr, deck, deck_filtered_idx, catastrophe, worlds_end, MOLs
game = {}
game['n_player'] = []            # number of current players
game['n_genes'] = []             # gene pool at start
game['n_catastrophes'] = []      # number of catastrophes
game['n_MOLs'] = []              # number of MOLs

plr = {}
plr['name'] = []
plr['genes'] = []
plr['points'] = []
plr['trait_pile'] = []
plr['n_tp'] = []                # count of traits -> separated by colors / xtra_effects / scoreboard
plr['trait_selected'] = []
plr['points_WE_effect'] = []
plr['points_MOL'] = []

deck = []                       # all traits in deck (or discard pile) left to be drawn / list of idx
deck_filtered_idx = []          # _filtered_ deck of trait_idx in listbox after searching -> idx

catastrophe = {}
catastrophe['possible'] = []    # list of possibles catastrophes
catastrophe['played'] = []      # occured catastrophes / needed for worlds end
catastrophe['cbox'] = []        # comboxes containing possible catastrophes

worlds_end = {}
worlds_end['selected'] = None   # selected world-ends
worlds_end['played'] = 'none'   # play this world-end-event
worlds_end['cbox'] = [None]     # combobox 4 worlds end
worlds_end['btn'] = [None]      # button running worlds end

MOLs = {}
MOLs['played'] = []     # played MOLs
MOLs['cbox'] = []       # comboxes containing MOLs
MOLs['icon'] = []       # labels for icon showing MOL points
MOLs['n'] = []          # number of MOLs for each player -> may be different

# logfile to store debug lines ---------------------------------------------------------------------
global logfile
logfile = {'file': os.path.join(dir_log, "DoomPyLog_" + time.strftime("%Y%m%d-%H%M%S") + ".txt")}


# trait specific variables #########################################################################
global neoteny_checkbutton, sleepy_spinbox
neoteny_checkbutton = []
sleepy_spinbox = []
