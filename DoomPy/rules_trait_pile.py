from globals_ import status_df, traits_df, plr, neoteny_checkbutton, worlds_end, game
from log import write_log
import tkinter as tk
from tkinter import ttk


# single_trait_functions ###########################################################################
# --- AMATOXINS ------------------------------------------------------------------------------------
def amatoxins(frame_trait_overview, irow, images, trait_idx, trait_name):
    # create separate frame
    irow += 1
    frame = tk.Frame(frame_trait_overview)
    frame.grid(row=irow, column=0, columnspan=2, sticky='we')

    # add trait
    tk.Label(frame, text=trait_name.upper(), fg="mediumorchid1", font='"" 14 bold'
             ).grid(row=0, column=0, padx=(10, 0), sticky='ens')
    # add effect
    tk.Label(frame, text=" discarded", image=images["bgpr"], compound=tk.LEFT
             ).grid(row=0, column=1, sticky='wns')
    # add ?/drop icon
    lbl = tk.Label(frame, image=images['points_off'])
    lbl.grid(row=0, column=2)

    # check if worlds end effect was chosen
    traits_WE = status_df.loc[trait_idx].traits_WE
    if traits_WE != 'none':
        WE_drops = str(int(traits_WE) * -2)

        # change ?/drop icon
        lbl.configure(image=images['drops'])
        # add points icon
        tk.Label(frame, image=images[WE_drops]
                 ).grid(row=0, column=3)
        write_log(['trait_effects', 'amatoxins'], trait_name, WE_drops)

    return irow


# --- NEOTENY --------------------------------------------------------------------------------------
def neoteny(frame_trait_overview, p, irow, images):
    # in case NEOTENY checkbox is clicked
    def update_neoteny(p):
        neoteny_idx = traits_df.index[traits_df.trait == 'Neoteny'].tolist()[0]

        # set other player to 0
        for i in range(game['n_player']):
            if i != p:
                neoteny_checkbutton[i].set(0)

        # update 'cur_effect'
        if not any([i.get() for i in neoteny_checkbutton]):
            status_df.loc[neoteny_idx, 'effects'] = 'none'
            write_log(['update_trait_status', 'neoteny_no_one'])
        else:
            status_df.loc[neoteny_idx, 'effects'] = str(p)
            write_log(['update_trait_status', 'neoteny_that_one'], plr['name'][p].get())

    # create separate frame for WE_TITLE
    irow += 1
    frame = tk.Frame(frame_trait_overview)
    frame.grid(row=irow, column=0, columnspan=2, sticky='we')

    # add trait
    tk.Label(frame, text="NEOTENY", fg="#1C86EE", font='"" 14 bold'
             ).grid(row=0, column=0, padx=(10, 0), sticky='en')
    # if is this hand
    if neoteny_checkbutton[p].get() == 1:
        ttk.Checkbutton(frame, variable=neoteny_checkbutton[p], text=' got it -> ',
                        # command=lambda: update_traits_current_status('neoteny', int(p))
                        command=lambda: update_neoteny(int(p))
                        ).grid(row=0, column=1, padx=(0, 0), sticky='wns')
        ttk.Label(frame, image=images['drops']
                  ).grid(row=0, column=2, sticky='ns')
        tk.Label(frame, image=images['4']
                 ).grid(row=0, column=3, sticky='ns')
    # not in this hand
    else:
        ttk.Checkbutton(frame, variable=neoteny_checkbutton[p], text=' in my hand???',
                        command=lambda: update_neoteny(int(p))
                        ).grid(row=0, column=1, padx=(0, 0), sticky='wns')

    return irow


# --- PROWLER --------------------------------------------------------------------------------------
def prowler(frame_trait_overview, p, irow, images, trait_idx, trait_name):
    # create separate frame
    irow += 1
    frame = tk.Frame(frame_trait_overview)
    frame.grid(row=irow, column=0, columnspan=2, sticky='we')

    # add trait
    tk.Label(frame, text=trait_name.upper(), fg="mediumorchid1", font='"" 14 bold'
             ).grid(row=0, column=0, padx=(10, 0), sticky='e')
    # add effect
    tk.Label(frame, text="less ", image=images["bgpr"], compound=tk.RIGHT
             ).grid(row=0, column=1, sticky='we')
    tk.Label(frame, text="as host",
             ).grid(row=0, column=2, sticky='w')

    # add drop
    tk.Label(frame, image=images['drops']
             ).grid(row=0, column=3)
    # add points icon
    WE_drops = status_df.loc[trait_idx].effects.split()
    tk.Label(frame, image=images[WE_drops[p]]
             ).grid(row=0, column=4)

    write_log(['trait_effects', 'prowler'], trait_name, plr['name'][p].get(), WE_drops[p])

    return irow


# --- SHINY ----------------------------------------------------------------------------------------
def shiny(frame_trait_overview, p, irow, images, trait_idx):
    # create separate frame
    irow += 1
    frame = tk.Frame(frame_trait_overview)
    frame.grid(row=irow, column=0, columnspan=2, sticky='we')

    # add trait
    tk.Label(frame, text="SHINY", fg="#228B22", font="'' 14 bold"
             ).grid(row=0, column=0, padx=(10, 0), sticky='ens')
    # add effect
    tk.Label(frame, text="punishes ", image=images["c"], compound=tk.RIGHT
             ).grid(row=0, column=1, sticky='wns')
    # add drop icon
    tk.Label(frame, image=images['drops']
             ).grid(row=0, column=2)
    # add points icon
    shiny_dp = status_df.loc[trait_idx].effects.split()
    tk.Label(frame, image=images[shiny_dp[p]]
             ).grid(row=0, column=3)

    write_log(['trait_effects', 'shiny'], plr['name'][p].get(), shiny_dp[p])

    return irow


# --- SPORES ---------------------------------------------------------------------------------------
def spores(frame_trait_overview, p, irow, images, spores_effect):
    # check if more players are affected
    if '_' in spores_effect:
        spores_effect = spores_effect.split('_')

    # print Spores effects if this player is affected
    n_genes = sum(str(p) == i for i in spores_effect)
    if n_genes > 0:
        # create separate frame
        irow += 1
        frame = tk.Frame(frame_trait_overview)
        frame.grid(row=irow, column=0, columnspan=2, sticky='we')

        # add trait
        tk.Label(frame, text="SPORES", fg="#228B22", font="'' 14 bold"
                 ).grid(row=0, column=0, padx=(10, 0), sticky='ens')
        # add effect
        tk.Label(frame, text="adds genes "
                 ).grid(row=0, column=1, sticky='wns')
        # add gene_pool icon(s)
        for i in range(n_genes):
            tk.Label(frame, image=images['gene_pool']
                     ).grid(row=0, column=2+i)

    return irow


# --- VIRAL ----------------------------------------------------------------------------------------
def viral(frame_trait_overview, p, irow, images, trait_idx, trait_name):
    # create separate frame
    irow += 1
    frame = tk.Frame(frame_trait_overview)
    frame.grid(row=irow, column=0, columnspan=2, sticky='we')

    # add trait & drop icon
    tk.Label(frame, text=trait_name.upper(), fg="mediumorchid1", font='"" 14 bold'
             ).grid(row=0, column=0, padx=(10, 0), sticky='ens')
    # add effect
    lbl = tk.Label(frame, text=" punishes ", image=images["points_off"], compound=tk.RIGHT)
    lbl.grid(row=0, column=1, sticky='wns')

    # check if worlds end effect was chosen
    trait_WE = status_df.loc[trait_idx].traits_WE
    if trait_WE != 'none':
        WE_drops = status_df.loc[trait_idx].effects.split()

        # change color icon
        lbl.configure(image=images[trait_WE[0]])
        # add drop icon
        tk.Label(frame, image=images['drops']
                 ).grid(row=0, column=2)
        # add points icono
        tk.Label(frame, image=images[WE_drops[p]]
                 ).grid(row=0, column=3)

        write_log(['trait_effects', 'viral'], trait_name, trait_WE, plr['name'][p].get(), WE_drops[p])

    return irow


# checking for specific traits #####################################################################
# - if they are played, run the respective function
def special_trait_effects(frame_trait_overview, p, irow, images):

    # --- AMATOXINS --- add passively Amatoxins to this trait pile ---------------------------------
    amatoxins_idx = traits_df.index[traits_df.trait == 'Amatoxins'].tolist()[0]
    if (any([amatoxins_idx in tp for tp in plr['trait_pile']])
            and amatoxins_idx not in plr['trait_pile'][p]):
        irow = amatoxins(frame_trait_overview, irow, images, amatoxins_idx, 'Amatoxins')

    # --- NEOTENY --- check button if Neoteny is in your hand --------------------------------------
    # is NEOTENY in your hand? asked via checkbox? But only if its not played
    neoteny_idx = traits_df.index[traits_df.trait == 'Neoteny'].tolist()[0]
    neoteny_effect = status_df.loc[neoteny_idx].effects
    if ("select world's end" not in worlds_end['played'].get()
            and all(neoteny_idx not in tp for tp in plr['trait_pile'])):
        # only if no one has it or this player has it
        if neoteny_effect == 'none' or neoteny_effect == str(p):
            irow = neoteny(frame_trait_overview, p, irow, images)

    # --- PROWLER --- add passively Prowler to this trait pile -------------------------------------
    prowler_idx = traits_df.index[traits_df.trait == 'Prowler'].tolist()[0]
    if (any([prowler_idx in tp for tp in plr['trait_pile']])
            and prowler_idx not in plr['trait_pile'][p]):
        irow = prowler(frame_trait_overview, p, irow, images, prowler_idx, 'Prowler')

    # --- SHINY --- add passively Shiny to this trait pile -----------------------------------------
    shiny_idx = traits_df.index[traits_df.trait == 'Shiny'].tolist()[0]
    if (any([shiny_idx in tp for tp in plr['trait_pile']])
            and shiny_idx not in plr['trait_pile'][p]):
        irow = shiny(frame_trait_overview, p, irow, images, shiny_idx)

    # --- SPORES --- add passively Viral to this trait pile ----------------------------------------
    spores_idx = traits_df.index[traits_df.trait == 'Spores'].tolist()[0]
    spores_effect = status_df.iloc[spores_idx].effects
    if spores_effect != 'none':
        irow = spores(frame_trait_overview, p, irow, images, spores_effect)

    # --- VIRAL --- add passively Viral to this trait pile -----------------------------------------
    viral_idx = traits_df.index[traits_df.trait == 'Viral'].tolist()[0]
    if (any([viral_idx in tp for tp in plr['trait_pile']])
            and viral_idx not in plr['trait_pile'][p]):
        irow = viral(frame_trait_overview, p, irow, images, viral_idx, 'Viral')

    # --- OPPOSABLE THUMBS --- copy first traits effects, if listed here ---------------------------
    oppo_idx = traits_df.index[traits_df.trait == 'Opposable Thumbs'].tolist()[0]
    if (any(oppo_idx in tp for tp in plr['trait_pile'])
            and oppo_idx not in plr['trait_pile'][p]):

        oppo_at = [i for i, tp in enumerate(plr['trait_pile']) if oppo_idx in tp][0]
        first_D = [traits_df.loc[i].trait for i in plr['trait_pile'][oppo_at]
                   if (traits_df.loc[i].dominant == 1 and i != oppo_idx)][0]
        match first_D:
            case 'Amatoxins':
                irow = amatoxins(frame_trait_overview, irow, images, oppo_idx, 'Opp. Thumbs')

            case 'Prowler':
                irow = prowler(frame_trait_overview, p, irow, images, oppo_idx, 'Opp. Thumbs')

            case 'Viral':
                irow = viral(frame_trait_overview, p, irow, images, oppo_idx, 'Opp. Thumbs')
