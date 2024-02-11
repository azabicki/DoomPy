import numpy as np
from globals_ import traits_df, status_df, plr


# trait specific rules #############################################################################
def drop_traits(trait_idx, p, *args):
    # default drop points
    dp = np.nan

    # init vars
    colors = ['blue', 'green', 'purple', 'red']
    trait_pile = plr['trait_pile'][p]

    # calculate drops -> match trait _name_
    match traits_df.loc[trait_idx].trait:
        case 'Altruistic':
            # n self gene_pool own
            dp = plr['genes'][p].get()

        case 'Amatoxins':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # only, if AMATOXINS is not in this players trait pile
            traits_WE = status_df.loc[trait_idx].traits_WE
            if (trait_idx not in trait_pile) and (traits_WE != 'none'):
                # colors discarded * -2
                dp = int(traits_WE) * -2
            else:
                dp = 0

        case 'Apex Predator':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # 4 self if_most_traits all
            n = [i['t'].get() for i in plr['n_tp']]
            if n.index(max(n)) == p and n.count(max(n)) == 1:
                dp = 4
            else:
                dp = 0

        case 'Backbitter':
            # 3 self if_one_negative own
            dp = 3 * any([f < 0
                          for f in status_df.iloc[trait_pile].face.values.tolist()
                          if isinstance(f, int)])

        case 'Big Feller':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # 6 self 4_or_less_face_is_1 own
            dp = 6 * (sum([f <= 1
                          for f in status_df.iloc[trait_pile].face.values.tolist()
                          if isinstance(f, int)]) <= 4)

        case 'Bionic Arm':
            # 1 self n_techlings own 2 self n_techlings_if_BionicArms_is_host own
            n = sum([traits_df.loc[t].game == 'Techlings' for t in trait_pile])
            dp = 2*n if status_df.loc[trait_idx].attachment != 'none' else n

        case 'Bitter Berries':
            # 1 self each_lower_count_green_or_purple own
            n_cols = []
            for c in ['green', 'purple']:
                n_cols.append(sum([c in status_df.loc[t].color.lower()
                                  for t in trait_pile]))
            dp = min(n_cols)

        case 'Boredom (~)':
            # n self cards_with_effects own_hand
            # load drop value from status_df, because it was set manually, if its not nan
            if not np.isnan(status_df.loc[trait_idx].drops):
                dp = int(status_df.loc[trait_idx].drops)

        case 'Branches':
            # 1 self n_green_pairs other
            n_pairs = []
            for tp in plr['trait_pile']:
                n_pairs.append(int(sum('green' in c.lower()
                                       for c in status_df.iloc[tp].color.tolist()) / 2))
            n_pairs.pop(p)
            dp = sum(n_pairs)

        case 'Brave (1)':
            # 2 self n_dominant own_hand
            # load drop value from status_df, because it was set manually, if its not nan
            if not np.isnan(status_df.loc[trait_idx].drops):
                dp = int(status_df.loc[trait_idx].drops)

        case 'Camouflage (1)':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # 1 self n_hand own_hand
            # load drop value from status_df, because it was set manually, if its not nan
            if not np.isnan(status_df.loc[trait_idx].drops):
                dp = int(status_df.loc[trait_idx].drops)

        case 'Camouflage (2)':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # 1 self n_hand own_hand
            # load drop value from status_df, because it was set manually, if its not nan
            if not np.isnan(status_df.loc[trait_idx].drops):
                dp = int(status_df.loc[trait_idx].drops)

        case 'Contagious':
            # -1 self n_green own
            dp = -1 * sum('green' in color.lower()
                          for color in status_df.iloc[trait_pile].color.tolist())

        case 'Cranial Crest':
            # 1 self n_3_negative_traits discarded
            # load drop value from status_df, because it was set manually, if its not nan
            if not np.isnan(status_df.loc[trait_idx].drops):
                dp = int(status_df.loc[trait_idx].drops)

        case 'Dragon Heart':
            # 4 self if_all_colors own
            col_in_tp = []
            for col in colors:
                col_in_tp.append(any(col in color.lower()
                                     for color in status_df.iloc[trait_pile].color.tolist()))
            if all(col_in_tp):
                dp = 4
            else:
                dp = 0

        case 'Egg Clusters':
            # 1 self n_blue own
            dp = sum('blue' in color.lower()
                     for color in status_df.iloc[trait_pile].color.tolist())

        case 'Elven Ears':
            # 1 self n_mythlings all
            dp = sum(traits_df.loc[t].game == 'Mythlings'
                     for tp in plr['trait_pile'] for t in tp)

        case 'Euphoric':
            # 6 self 4_or_more_purple own
            dp = 6 * (sum('purple' in status_df.loc[t].color.lower()
                          for t in trait_pile) >= 4)

        case 'Fortunate (~)':
            # n self n_hand own_hand
            # load drop value from status_df, because it was set manually, if its not nan
            if not np.isnan(status_df.loc[trait_idx].drops):
                dp = int(status_df.loc[trait_idx].drops)

        case 'Fortunate (1)':
            # 2 self if_green_most_traits own
            n_col = []
            for col in colors:
                n_col.append(sum(col in color.lower()
                                 for color in status_df.iloc[trait_pile].color.tolist()))

            if n_col.index(max(n_col)) == colors.index('green') and n_col.count(max(n_col)) == 1:
                dp = 2
            else:
                dp = 0

        case 'GMO':
            # 1 self n_color_host own
            host = status_df.loc[trait_idx].host
            if host != 'none':
                host_color = status_df.loc[host].color
                pile_colors = status_df.iloc[trait_pile].color.tolist()

                dp = 0
                for col in colors:
                    dp += sum(col in i.lower()
                              for i in pile_colors
                              if col in host_color.lower())

        case 'Gratitude':
            # n self n_colors own
            col_in_tp = []
            for col in colors:
                col_in_tp.append(any(col in color.lower()
                                     for color in status_df.iloc[trait_pile].color.tolist()))
            dp = sum(col_in_tp)

        case 'Harmony':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # 2 self each_set_of_4_colors own
            n_cols = []
            for col in colors:
                n_cols.append(sum(col in color.lower()
                                  for color in status_df.iloc[trait_pile].color.tolist()))
            dp = 2 * min(n_cols)

        case 'Heat Vision':
            # 1 self n_red own
            dp = sum('red' in color.lower()
                     for color in status_df.iloc[trait_pile].color.tolist())

        case 'Hyper-Myelination':
            # n self gene_pool_max all
            dp = max(gp.get() for gp in plr['genes'])

        case 'Immunity':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # 2 self n_negative own
            dp = sum(face < 0
                     for face in status_df.iloc[trait_pile].face.tolist()
                     if not isinstance(face, str)) * 2

        case 'Kidney (g)' | 'Kidney (r)':
            # n self n_kidney own
            dp = sum(['kidney' in t.lower()
                      for t in status_df.iloc[trait_pile].trait.tolist()])

        case 'Lily Pad':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # 1 self each_trait_returned own
            # load drop value from status_df, because it was set manually, if its not nan
            we = status_df.loc[trait_idx].traits_WE
            if we != 'none':
                dp = int(we)

        case 'Mecha':
            # 1 self n_effectless own
            host = status_df.loc[trait_idx].host
            if host != 'none':
                dp = int(np.nansum(traits_df.iloc[trait_pile].effectless.tolist()))

        case 'Mindful':
            # 1 self n_colorless own
            dp = sum('colorless' in color.lower()
                     for color in status_df.iloc[trait_pile].color.tolist())

        case 'Mutualism':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # n self gene_pool_max-2_final_score all
            dp = max(gp.get() for gp in plr['genes'])

        case 'Nano':
            # n self host own
            host = status_df.loc[trait_idx].host
            if host != 'none':
                if not isinstance(status_df.loc[host].face, str):
                    dp = status_df.loc[host].face
                else:
                    print('___________________ check this out!!! why am i here???? ___________')

        case 'Noxious':
            # -1 self n_red own
            dp = -1 * sum('red' in color.lower()
                          for color in status_df.iloc[trait_pile].color.tolist())

        case 'Nuptial Plumage':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # 2 self every_color_count_>=3 own
            n_cols = []
            for col in colors:
                n_cols.append(sum(col in color.lower()
                                  for color in status_df.iloc[trait_pile].color.tolist()))
            dp = 2 * sum(n >= 3 for n in n_cols)

        case 'Opposable Thumbs':
            # copy_1st_dominant
            copy_idx = [i for i in trait_pile if (traits_df.loc[i].dominant == 1 and i != trait_idx)][0]

            # if in OWN trait pile
            dp = drop_traits(copy_idx, p, trait_idx)

        case 'Overgrowth':
            # 1 self n_green own
            dp = sum('green' in color.lower()
                     for color in status_df.iloc[trait_pile].color.tolist())

        case 'Pack Behavior':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # 1 self n_color_pairs own
            n_pairs = []
            for col in colors:
                n_pairs.append(int(sum(col in color.lower()
                                       for color in status_df.iloc[trait_pile].color.tolist()) / 2))
            if sum(n_pairs) > 0:
                dp = sum(n_pairs)
            else:
                dp = 0

        case 'Pollination':
            # 1 self n_face_is_1 own
            dp = sum(face == 1
                     for face in status_df.iloc[trait_pile].face.tolist())

        case 'Prolific':
            # 6 self 4_or_more_green own
            dp = 6 * (sum('green' in color.lower()
                          for color in status_df.loc[trait_pile].color) >= 4)

        case 'Prowler':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # only, if PROWLER is not in this players trait pile
            played_by = [i for i, tp in enumerate(plr['trait_pile']) if trait_idx in tp]
            if played_by != [] and played_by[0] != p:
                # init prowler points, or unpack them from status_df
                if status_df.loc[trait_idx].effects == 'none':
                    prowler_dp = [np.nan] * len(plr['trait_pile'])
                else:
                    prowler_dp = [int(i) if i.lstrip('-').isnumeric() else np.nan
                                  for i in status_df.loc[trait_idx].effects.split()]

                # first, get # of colors of player holding PROWLER
                n_cols_ref = []
                for col in colors:
                    n_cols_ref.append(sum(col in color.lower()
                                          for color in status_df.iloc[plr['trait_pile'][played_by[0]]].color.tolist()))
                n_cols_ref = sum(n > 0 for n in n_cols_ref)

                # second, get ' of colors of current player
                n_cols = []
                for col in colors:
                    n_cols.append(sum(col in color.lower()
                                      for color in status_df.iloc[plr['trait_pile'][p]].color.tolist()))
                n_cols = sum(n > 0 for n in n_cols)

                # calculate drop points for current player
                prowler_dp[p] = max([0, n_cols_ref - n_cols]) * -2

                # save updated points to Prowler's 'effects'
                status_df.loc[trait_idx, "effects"] = ' '.join(str(x) for x in prowler_dp)

                # get this players dp
                dp = prowler_dp[p]

            else:
                dp = 0

        case 'Rainbow Keratin':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # -2 self n_drops own&2 self n_highest_color_if4colors own
            dp = -2 * (sum(traits_df.loc[t].drops == 1 for t in trait_pile) - 1)

            n_cols = []
            for col in colors:
                n_cols.append(sum(col in color.lower()
                                  for color in status_df.iloc[trait_pile].color.tolist()))
            if all(n_cols):
                dp += 2 * max(n_cols)

        case 'Random Fertilization':
            # n self gene_pool own
            dp = plr['genes'][p].get()

        case 'Saudade (1)':
            # 1 self n_colors_hand own_hand
            # load drop value from status_df, because it was set manually, if its not nan
            if not np.isnan(status_df.loc[trait_idx].drops):
                dp = int(status_df.loc[trait_idx].drops)

        case 'Sentience':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # 1 self n_color_worlds_end own
            we = status_df.loc[trait_idx].traits_WE
            if we != 'none':
                dp = sum(we in color.lower()
                         for color in status_df.iloc[trait_pile].color.tolist())

        case 'Serrated Teeth (-1)':
            # 1 self n_dominant discarded
            # load drop value from status_df, because it was set manually, if its not nan
            if not np.isnan(status_df.loc[trait_idx].drops):
                dp = int(status_df.loc[trait_idx].drops)

        case 'Serrated Teeth (5)':
            # 1 self n_dominant discarded
            # load drop value from status_df, because it was set manually, if its not nan
            dp = -2 * int(traits_df.loc[trait_pile, 'dominant'].sum())

        case 'Shiny':
            # -1 all n_colorless own
            # if PROWLER is in THIS' PLAYERS trait pile
            if trait_idx in plr['trait_pile'][p]:
                dp = -1 * sum('colorless' in color.lower()
                              for color in status_df.iloc[trait_pile].color.tolist())
            else:
                # init shiny_points, or unpack them from status_df
                if status_df.loc[trait_idx].effects == 'none':
                    shiny_dp = [np.nan] * len(plr['trait_pile'])
                else:
                    shiny_dp = [int(i) if i.lstrip('-').isnumeric() else np.nan
                                for i in status_df.loc[trait_idx].effects.split()]

                # calculate drop points
                # -1 all n_colorless own
                shiny_dp[p] = -1 * sum('colorless' in color.lower()
                                       for color in status_df.iloc[trait_pile].color.tolist())

                # save updated points to Shiny's 'effects'
                status_df.loc[trait_idx, "effects"] = ' '.join(str(x) for x in shiny_dp)

                # get this players dp
                dp = shiny_dp[p]

        case 'Shy':
            # 5 self if_min_2_of_each_color own
            n_cols = []
            for col in colors:
                n_cols.append(sum(col in color.lower()
                                  for color in status_df.iloc[trait_pile].color.tolist()))
            if all(n >= 2 for n in n_cols):
                dp = 5
            else:
                dp = 0

        case 'Sour Grapes':
            # 1 self each_lower_count_blue_or_red own
            n_cols = []
            for col in ['blue', 'red']:
                n_cols.append(sum([col in color.lower()
                                   for color in status_df.iloc[trait_pile].color.tolist()]))
            dp = min(n_cols)

        case 'Spicy':
            # 1 self each_lower_count_green_or_red own
            n_cols = []
            for col in ['green', 'red']:
                n_cols.append(sum([col in color.lower()
                                   for color in status_df.iloc[trait_pile].color.tolist()]))
            dp = min(n_cols)

        case 'Sticky Secretions':
            # 1 self n_purple own
            dp = sum('purple' in color.lower()
                     for color in status_df.iloc[trait_pile].color.tolist())

        case 'Swarm (b)' | 'Swarm (g)' | 'Swarm (p)' | 'Swarm (r)' | 'Swarm (c)':
            # n self n_swarm all
            dp = sum(['swarm' in t.lower()
                      for tp in plr['trait_pile']
                      for t in status_df.iloc[tp].trait.tolist()])

        case 'Sweet':
            # 1 self each_lower_count_blue_or_green own
            n_cols = []
            for col in ['blue', 'green']:
                n_cols.append(sum([col in color.lower()
                                   for color in status_df.iloc[trait_pile].color.tolist()]))
            dp = min(n_cols)

        case 'Sycophant':
            # 5 self if_>=5_red opponents
            n_red = []
            for tp in plr['trait_pile']:
                n_red.append(sum('red' in color.lower()
                                 for color in status_df.iloc[tp].color.tolist()))

            n_red.pop(p)
            if any(n >= 5 for n in n_red):
                dp = 5
            else:
                dp = 0

        case 'Symbiosis':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # 2 self lowest_color_count own
            n_cols = []
            for col in colors:
                n_cols.append(sum(col in color.lower()
                                  for color in status_df.iloc[trait_pile].color.tolist()))

            n_cols = [i for i in n_cols if i > 0]
            if len(n_cols) >= 2:
                dp = min(n_cols) * 2
            else:
                dp = 0

        case 'Tenacious':
            # 6 self 4_or_more_red own
            dp = 6 * (sum('red' in color.lower()
                          for color in status_df.iloc[trait_pile].color.tolist()) >= 4)

        case 'Tetrachromatic':
            # 6 self 4_or_more_red own
            dp = -1 * sum('colorless' in color.lower()
                          for color in status_df.iloc[trait_pile].color.tolist())

        case 'Tiny':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # -1 self n_traits own
            dp = -1 * len(trait_pile)

        case 'Tiny Arms':
            # 1 self n_dinolings discarded
            # load drop value from status_df, because it was set manually, if its not nan
            if not np.isnan(status_df.loc[trait_idx].drops):
                dp = int(status_df.loc[trait_idx].drops)

        case 'Viral':
            # check if 'Opposable Thumbs' is using this calculations
            if args != () and traits_df.loc[args[0]].trait == 'Opposable Thumbs':
                trait_idx = args[0]

            # only, if VIRAL is not in this players trait pile & WE effect selected
            traits_WE = status_df.loc[trait_idx].traits_WE
            if (trait_idx not in trait_pile) and (traits_WE != 'none'):
                # init viral points, or unpack them from status_df
                if status_df.loc[trait_idx].effects == 'none':
                    viral_dp = [np.nan] * len(plr['trait_pile'])
                else:
                    viral_dp = [int(i) if i.lstrip('-').isnumeric() else np.nan
                                for i in status_df.loc[trait_idx].effects.split()]

                # calculate drop points
                viral_dp[p] = sum([traits_WE in color.lower()
                                   for color in status_df.iloc[trait_pile].color.tolist()]) * -1

                # save updated points to Viral's 'effects'
                status_df.loc[trait_idx, "effects"] = ' '.join(str(x) for x in viral_dp)

                # get this players dp
                dp = viral_dp[p]
            else:
                dp = 0

        case 'Vivacious':
            # 6 self 4_or_more_blue own
            dp = 6 * (sum('blue' in color.lower()
                          for color in status_df.iloc[trait_pile].color.tolist()) >= 4)

    # return drop value
    return dp


# MAIN ROUTINE for calculating drop values #########################################################
def drop_points(p):
    # init vars
    total = 0
    trait_pile = plr['trait_pile'][p]

    # loop OWN trait pile and apply drop-rules -----------------------------------------------------
    trait_drops = [t for t in plr['trait_pile'][p] if traits_df.loc[t].drops == 1]
    for trait_idx in trait_drops:
        # if trait is inactive, set drop-points = nan
        if status_df.loc[trait_idx].inactive:
            status_df.loc[trait_idx, 'drops'] = np.nan
        else:
            # else get drop-points
            dp = drop_traits(trait_idx, p)

            # save drop value & update total
            if not np.isnan(dp):
                status_df.loc[trait_idx, 'drops'] = dp
                total += dp
                # print("____ {} drop points by '{}'".format(dp, status_df.loc[trait].trait))

    # --- drop-effects of OPPONENTS traits / HAND traits -------------------------------------------
    # AMATOXINS ----- if played by another player ---------------
    amatoxins_idx = status_df.index[status_df.trait == 'Amatoxins'].tolist()
    if (amatoxins_idx != []
            and amatoxins_idx[0] not in trait_pile
            and status_df.loc[amatoxins_idx[0]].traits_WE != 'none'):
        # colors discarded * -2
        total += drop_traits(amatoxins_idx[0], p)

    # NEOTENY ----- if in Hand after Worlds End ---------------
    neoteny_idx = status_df.index[status_df.trait == 'Neoteny'].tolist()
    if neoteny_idx != [] and status_df.loc[neoteny_idx[0]].effects == str(p):
        # 4 if NEOTENY is in hand
        total += 4

    # PROWLER ----- if played by another player ---------------
    prowler_idx = status_df.index[status_df.trait == 'Prowler'].tolist()
    if prowler_idx != []:
        prowler_played_by = [i for i, tp in enumerate(plr['trait_pile']) if prowler_idx[0] in tp]
        if prowler_played_by != [] and prowler_played_by[0] != p:
            # less colors as host * -2
            total += drop_traits(prowler_idx[0], p)

    # SHINY ----- if played by another player ---------------
    shiny_idx = status_df.index[status_df.trait == 'Shiny'].tolist()
    if (shiny_idx != []
            and any(shiny_idx[0] in tp for tp in plr['trait_pile'])
            and shiny_idx[0] not in trait_pile
            and not status_df.loc[shiny_idx[0]].inactive):
        # -1 all n_colorless own
        total += drop_traits(shiny_idx[0], p)

    # VIRAL ----- if played by another player ---------------
    viral_idx = status_df.index[status_df.trait == 'Viral'].tolist()
    if (viral_idx != []
            and viral_idx[0] not in trait_pile
            and status_df.loc[viral_idx[0]].traits_WE != 'none'):
        # -1 self n_selected_colorless own
        total += drop_traits(viral_idx[0], p)

    # lastly: OPPOSABLE THUMBS --- copy first dominants drop effect ---------------
    oppo_idx = traits_df.index[traits_df.trait == 'Opposable Thumbs'].tolist()
    if oppo_idx != []:
        oppo_at = [i for i, tp in enumerate(plr['trait_pile']) if oppo_idx[0] in tp]
        # if played by any OPPONENT
        if (oppo_at != []) and (oppo_at[0] != p):
            # check first dominant & run respective drop_code
            copy_idx = [i for i in plr['trait_pile'][oppo_at[0]]
                        if (traits_df.loc[i].dominant == 1 and i != oppo_idx[0])][0]

            # else, check if OT copies traits with "cross-player-effects"
            match traits_df.loc[copy_idx].trait:
                case 'Prowler':
                    # less colors as host * -2
                    total += drop_traits(copy_idx, p, oppo_idx[0])

                case 'Amatoxins':
                    # colors discarded * -2
                    if status_df.loc[oppo_idx[0]].traits_WE != 'none':
                        total += drop_traits(copy_idx, p, oppo_idx[0])

                case 'Viral':
                    # -1 self n_selected_colorless own
                    if status_df.loc[oppo_idx[0]].traits_WE != 'none':
                        total += drop_traits(copy_idx, p, oppo_idx[0])

    # return final drop score ######################################################################
    return total
