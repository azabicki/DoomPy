from globals_ import status_df, traits_df, plr
from log import write_log
import tkinter as tk


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
    lbl = tk.Label(frame, image=images['question_mark'])
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
    lbl = tk.Label(frame, text=" punishes ", image=images["question_mark"], compound=tk.RIGHT)
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
    amatoxins_idx = traits_df.index[traits_df.trait == 'Amatoxins'].tolist()
    if (amatoxins_idx != []
            and any([amatoxins_idx[0] in tp for tp in plr['trait_pile']])
            and amatoxins_idx[0] not in plr['trait_pile'][p]):
        irow = amatoxins(frame_trait_overview, irow, images, amatoxins_idx[0], 'Amatoxins')

    # --- PROWLER --- add passively Prowler to this trait pile -------------------------------------
    prowler_idx = traits_df.index[traits_df.trait == 'Prowler'].tolist()
    if (prowler_idx != []
            and any([prowler_idx[0] in tp for tp in plr['trait_pile']])
            and prowler_idx[0] not in plr['trait_pile'][p]):
        irow = prowler(frame_trait_overview, p, irow, images, prowler_idx[0], 'Prowler')

    # --- SHINY --- add passively Shiny to this trait pile -----------------------------------------
    shiny_idx = traits_df.index[traits_df.trait == 'Shiny'].tolist()
    if (shiny_idx != []
            and any([shiny_idx[0] in tp for tp in plr['trait_pile']])
            and shiny_idx[0] not in plr['trait_pile'][p]):
        irow = shiny(frame_trait_overview, p, irow, images, shiny_idx[0])

    # --- SPORES --- add passively Viral to this trait pile ----------------------------------------
    spores_idx = traits_df.index[traits_df.trait == 'Spores'].tolist()
    if spores_idx != []:
        spores_effect = status_df.iloc[spores_idx[0]].effects
        if spores_effect != 'none':
            irow = spores(frame_trait_overview, p, irow, images, spores_effect)

    # --- VIRAL --- add passively Viral to this trait pile -----------------------------------------
    viral_idx = traits_df.index[traits_df.trait == 'Viral'].tolist()
    if (viral_idx != []
            and any([viral_idx[0] in tp for tp in plr['trait_pile']])
            and viral_idx[0] not in plr['trait_pile'][p]):
        irow = viral(frame_trait_overview, p, irow, images, viral_idx[0], 'Viral')

    # --- OPPOSABLE THUMBS --- copy first traits effects, if listed here ---------------------------
    oppo_idx = traits_df.index[traits_df.trait == 'Opposable Thumbs'].tolist()
    if (oppo_idx != []
            and any(oppo_idx[0] in tp for tp in plr['trait_pile'])
            and oppo_idx[0] not in plr['trait_pile'][p]):

        oppo_at = [i for i, tp in enumerate(plr['trait_pile']) if oppo_idx[0] in tp][0]
        first_D = [traits_df.loc[i].trait for i in plr['trait_pile'][oppo_at]
                   if (traits_df.loc[i].dominant == 1 and i != oppo_idx[0])][0]
        match first_D:
            case 'Amatoxins':
                irow = amatoxins(frame_trait_overview, irow, images, oppo_idx[0], 'Opp. Thumbs')

            case 'Prowler':
                irow = prowler(frame_trait_overview, p, irow, images, oppo_idx[0], 'Opp. Thumbs')

            case 'Viral':
                irow = viral(frame_trait_overview, p, irow, images, oppo_idx[0], 'Opp. Thumbs')

    return irow
