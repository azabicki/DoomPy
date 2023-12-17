import numpy as np
from globals_ import traits_df, status_df, plr


# rules for filtering attachable traits depending on trait_pile and attachment
def drop_points(p):
    colors = ['blue', 'green', 'purple', 'red']
    traits = plr['trait_pile'][p]
    gene_pool = plr['genes']
    total = 0

    # loop trait pile and apply drop-rules
    for trait in traits:
        # default drop points
        dp = np.nan

        # skip trait, if not a 'drop'-trait
        if traits_df.loc[trait].drops != 1:
            continue

        # skip trait, if specific effects prevent drop calculation
        if (not status_df.loc[trait].effects
                or status_df.loc[trait].inactive
                or 'inactive' in status_df.loc[trait].we_effect.lower()):
            status_df.loc[trait, 'drops'] = dp
            continue

        # calculate drops -> match trait _name_
        match traits_df.loc[trait].trait:
            case 'Altruistic':
                # n self gene_pool own
                dp = gene_pool[p].get()

            case 'Apex Predator':
                # 4 self if_most_traits all
                n = [len(i) for i in plr['trait_pile']]
                if n.index(max(n)) == p and n.count(max(n)) == 1:
                    dp = 4

            case 'Backbitter':
                # 3 self if_one_negative own
                dp = 3 * any([f < 0
                              for f in status_df.iloc[traits].face.values.tolist()
                              if isinstance(f, int)])

            case 'Big Feller':
                # 6 self 4_or_less_face_is_1 own
                dp = 6 * (sum([f <= 1
                               for f in status_df.iloc[traits].face.values.tolist()
                               if isinstance(f, int)]) <= 4)

            case 'Bionic Arm':
                # 1 self n_techlings own 2 self n_techlings_if_BionicArms_is_host own
                n = sum([traits_df.loc[t].game == 'Techlings' for t in traits])
                dp = 2*n if status_df.loc[trait].attachment != 'none' else n

            case 'Bitter Berries':
                # 1 self each_lower_count_green_or_purple own
                n_cols = []
                for c in ['green', 'purple']:
                    n_cols.append(sum([c in status_df.loc[t].color.lower()
                                      for t in traits]))
                dp = min(n_cols)

            case 'Boredom (~)':
                # n self cards_with_effects own_hand
                # load drop value from status_df, because it was set manually, if its not nan
                if not np.isnan(status_df.loc[trait].drops):
                    dp = int(status_df.loc[trait].drops)

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
                if not np.isnan(status_df.loc[trait].drops):
                    dp = int(status_df.loc[trait].drops)

            case 'Camouflage (1)':
                # 1 self n_hand own_hand
                # load drop value from status_df, because it was set manually, if its not nan
                if not np.isnan(status_df.loc[trait].drops):
                    dp = int(status_df.loc[trait].drops)

            case 'Camouflage (2)':
                # 1 self n_hand own_hand
                # load drop value from status_df, because it was set manually, if its not nan
                if not np.isnan(status_df.loc[trait].drops):
                    dp = int(status_df.loc[trait].drops)

            case 'Contagious':
                # -1 self n_green own
                dp = -1 * sum('green' in color.lower()
                              for color in status_df.iloc[traits].color.tolist())

            case 'Cranial Crest':
                # 1 self n_3_negative_traits discarded
                # load drop value from status_df, because it was set manually, if its not nan
                if not np.isnan(status_df.loc[trait].drops):
                    dp = int(status_df.loc[trait].drops)

            case 'Dragon Heart':
                # 4 self if_all_colors own
                col_in_tp = []
                for col in colors:
                    col_in_tp.append(any(col in color.lower()
                                         for color in status_df.iloc[traits].color.tolist()))
                if all(col_in_tp):
                    dp = 4

            case 'Egg Clusters':
                # 1 self n_blue own
                dp = sum('blue' in color.lower()
                         for color in status_df.iloc[traits].color.tolist())

            case 'Elven Ears':
                # 1 self n_mythlings all
                dp = sum(traits_df.loc[t].game == 'Mythlings'
                         for tp in plr['trait_pile'] for t in tp)

            case 'Euphoric':
                # 6 self 4_or_more_purple own
                dp = 6 * (sum('purple' in status_df.loc[t].color.lower()
                              for t in traits) >= 4)

            case 'Fortunate (~)':
                # n self n_hand own_hand
                # load drop value from status_df, because it was set manually, if its not nan
                if not np.isnan(status_df.loc[trait].drops):
                    dp = int(status_df.loc[trait].drops)

            case 'Fortunate (1)':
                # 2 self if_green_most_traits own
                n_col = []
                for col in colors:
                    n_col.append(sum(col in color.lower()
                                 for color in status_df.iloc[traits].color.tolist()))
                if n_col.index(max(n_col)) == colors.index('green') and n_col.count(max(n_col)) == 1:
                    dp = 2

            case 'GMO':
                # 1 self n_color_host own
                host = status_df.loc[trait].host
                if host != 'none':
                    host_color = status_df.loc[host].color
                    pile_colors = status_df.iloc[traits].color.tolist()

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
                                         for color in status_df.iloc[traits].color.tolist()))
                dp = sum(col_in_tp)

            case 'Harmony':
                # 2 self each_set_of_4_colors own
                n_cols = []
                for col in colors:
                    n_cols.append(sum(col in color.lower()
                                      for color in status_df.iloc[traits].color.tolist()))
                dp = 2 * min(n_cols)

            case 'Heat Vision':
                # 1 self n_red own
                dp = sum('red' in color.lower()
                         for color in status_df.iloc[traits].color.tolist())

            case 'Hypermyelination':
                # n self gene_pool_max all
                dp = max(gp.get() for gp in gene_pool)

            case 'Immunity':
                # 2 self n_negative own
                dp = sum(face < 0
                         for face in status_df.iloc[traits].face.tolist()
                         if not isinstance(face, str)) * 2

            case 'Kidney (g)' | 'Kidney (r)':
                # n self n_kidney own
                dp = sum(['kidney' in t.lower()
                          for t in status_df.iloc[traits].trait.tolist()])

            case 'Lily Pad':
                # 1 self each_trait_returned own
                # load drop value from status_df, because it was set manually, if its not nan
                we = status_df.loc[trait].traits_WE
                if we != 'none':
                    dp = int(we)

            case 'Mecha':
                # 1 self n_effectless own
                host = status_df.loc[trait].host
                if host != 'none':
                    dp = int(np.nansum(traits_df.iloc[traits].effectless.tolist()))

            case 'Mindful':
                # 1 self n_colorless own
                dp = sum('colorless' in color.lower()
                         for color in status_df.iloc[traits].color.tolist())

            case 'Mutualism':
                # n self gene_pool_max-2_final_score all
                dp = max(gp.get() for gp in gene_pool)

            case 'Nano':
                # n self host own
                host = status_df.loc[trait].host
                if host != 'none':
                    if not isinstance(status_df.loc[host].face, str):
                        dp = status_df.loc[host].face
                    else:
                        print('___________________ check this out!!! why am i here???? ___________')

            case 'Neoteny':
                # 4 self if_in_hand own_hand
                # load drop value from status_df, because it was set manually, if its not nan
                if not np.isnan(status_df.loc[trait].drops):
                    dp = int(status_df.loc[trait].drops)

            case 'Noxious':
                # -1 self n_red own
                dp = -1 * sum('red' in color.lower()
                              for color in status_df.iloc[traits].color.tolist())

            case 'Nuptial Plumage':
                # 2 self every_color_count_>=3 own
                n_cols = []
                for col in colors:
                    n_cols.append(sum(col in color.lower()
                                      for color in status_df.iloc[traits].color.tolist()))
                dp = 2 * sum(n >= 3 for n in n_cols)

            case 'Opposing Thumbs':
                # copy_1st_dominant
                # find first dominatn and call this function with only him in artificial trait pile
                dom = [t for t in traits if traits_df.iloc[t].dominant == 1]
                dom.remove(trait)

                dp = np.nan

            case 'Overgrowth':
                # 1 self n_green own
                dp = sum('green' in color.lower()
                         for color in status_df.iloc[traits].color.tolist())

            case 'Pack Behavior':
                # 1 self n_color_pairs own
                tmp = []
                for col in colors:
                    tmp.append(int(sum(col in color.lower()
                                       for color in status_df.iloc[traits].color.tolist()) / 2))
                if sum(tmp) > 0:
                    dp = sum(tmp)

            case 'Pollination':
                # 1 self n_face_is_1 own
                dp = sum(face == 1
                         for face in status_df.iloc[traits].face.tolist())

            case 'Prolific':
                # 6 self 4_or_more_green own
                dp = 6 * (sum('green' in color.lower()
                              for color in status_df.loc[traits].color) >= 4)

            case 'Rainbow Keratin':
                # -2 self n_drops own&2 self n_highest_color_if4colors own
                dp = -2 * sum(traits_df.loc[t].drops == 1 for t in traits)
                n_cols = []
                for col in colors:
                    n_cols.append(sum(col in color.lower()
                                      for color in status_df.iloc[traits].color.tolist()))
                if all(n_cols):
                    dp += 2 * max(n_cols)

            case 'Random Fertilization':
                # n self gene_pool own
                dp = gene_pool[p].get()

            case 'Saudade (1)':
                # 1 self n_colors_hand own_hand
                # load drop value from status_df, because it was set manually, if its not nan
                if not np.isnan(status_df.loc[trait].drops):
                    dp = int(status_df.loc[trait].drops)

            case 'Sentience':
                # 1 self n_color_worlds_end own
                we = status_df.loc[trait].traits_WE
                if we != 'none':
                    dp = sum(we in color.lower()
                             for color in status_df.iloc[traits].color.tolist())

            case 'Serrated Teeth':
                # 1 self n_dominant discarded
                # load drop value from status_df, because it was set manually, if its not nan
                if not np.isnan(status_df.loc[trait].drops):
                    dp = int(status_df.loc[trait].drops)

            case 'Shiny':
                # -1 all n_colorless own
                dp = -1 * sum('colorless' in color.lower()
                              for color in status_df.iloc[traits].color.tolist())

            case 'Shy':
                # 5 self if_min_2_of_each_color own
                n_cols = []
                for col in colors:
                    n_cols.append(sum(col in color.lower()
                                      for color in status_df.iloc[traits].color.tolist()))
                if all(n >= 2 for n in n_cols):
                    dp = 5

            case 'Sour Grapes':
                # 1 self each_lower_count_blue_or_red own
                n_cols = []
                for col in ['blue', 'red']:
                    n_cols.append(sum([col in color.lower()
                                      for color in status_df.iloc[traits].color.tolist()]))
                dp = min(n_cols)

            case 'Spicy':
                # 1 self each_lower_count_green_or_red own
                n_cols = []
                for col in ['green', 'red']:
                    n_cols.append(sum([col in color.lower()
                                      for color in status_df.iloc[traits].color.tolist()]))
                dp = min(n_cols)

            case 'Sticky Secretions':
                # 1 self n_purple own
                dp = sum('purple' in color.lower()
                         for color in status_df.iloc[traits].color.tolist())

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
                                      for color in status_df.iloc[traits].color.tolist()]))
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

            case 'Symbiosis':
                # 2 self lowest_color_count own
                n = []
                for col in colors:
                    n.append(sum(col in color.lower()
                                 for color in status_df.iloc[traits].color.tolist()))
                n = [i for i in n if i > 0]
                if len(n) >= 2:
                    dp = min(n) * 2

            case 'Tenacious':
                # 6 self 4_or_more_red own
                dp = 6 * (sum('red' in color.lower()
                              for color in status_df.iloc[traits].color.tolist()) >= 4)

            case 'Tiny':
                # -1 self n_traits own
                dp = -1 * len(traits)

            case 'Tiny Arms':
                # 1 self n_dinolings discarded
                # load drop value from status_df, because it was set manually, if its not nan
                if not np.isnan(status_df.loc[trait].drops):
                    dp = int(status_df.loc[trait].drops)

            case 'Vivacious':
                # 6 self 4_or_more_blue own
                dp = 6 * (sum('blue' in color.lower()
                              for color in status_df.iloc[traits].color.tolist()) >= 4)

        # set current drop value & update total
        status_df.loc[trait, 'drops'] = dp
        if not np.isnan(dp):
            # print("____ {} drop points by '{}'".format(dp, status_df.loc[trait].trait))
            total += dp

    # *** section for drop-effects in other trait piles, which could affect this player ***
    # ----- AMATOXINS ----- if Amatoxins was played by another player -----------------
    amatoxins_idx = status_df.index[status_df.trait == 'Amatoxins'].tolist()[0]
    we_amatoxins = status_df.loc[amatoxins_idx].traits_WE
    if amatoxins_idx not in traits and we_amatoxins != 'none':
        # calculate drop points
        total += int(status_df.loc[amatoxins_idx].effects) * -2

    # ----- PROWLER ----- if Prowler was played by another player -----------------
    prowler_idx = status_df.index[status_df.trait == 'Prowler'].tolist()[0]
    played = [prowler_idx in tp for tp in plr['trait_pile']]
    if any(played) and played.index(True) != p:
        # load current prowler_drop_points
        prw_ps = status_df.loc[prowler_idx].effects

        # init them, if not done previously
        if prw_ps == 'none':
            prw_p = [np.nan] * len(gene_pool)
        else:
            prw_p = [int(i) if i.lstrip('-').isnumeric() else np.nan for i in prw_ps.split()]

        # calculate drop points
        played_by = played.index(True)
        ncols_ref = []
        for col in colors:
            ncols_ref.append(sum(col in color.lower()
                             for color in status_df.iloc[plr['trait_pile'][played_by]].color.tolist()))
        ncols_ref = sum(n > 0 for n in ncols_ref)

        ncols = []
        for col in colors:
            ncols.append(sum(col in color.lower()
                             for color in status_df.iloc[plr['trait_pile'][p]].color.tolist()))
        ncols = sum(n > 0 for n in ncols)

        prw_p[p] = max([0, ncols_ref - ncols]) * -2

        # update total & save updated points to Prowler's 'effects'
        total += prw_p[p]
        status_df.loc[prowler_idx, "effects"] = ' '.join(str(x) for x in prw_p)

    # ----- SHINY ----- if Shiny was played by another player -----------------
    shiny_idx = status_df.index[status_df.trait == 'Shiny'].tolist()[0]
    if (any(shiny_idx in tp for tp in plr['trait_pile'])
            and not status_df.loc[shiny_idx].inactive):

        # init shiny_points, or unpack them from status_df
        if status_df.loc[shiny_idx].effects == 'none':
            shiny_dp = [np.nan] * len(plr['trait_pile'])
        else:
            shiny_dp = [int(i) if i.lstrip('-').isnumeric() else np.nan
                        for i in status_df.loc[shiny_idx].effects.split()]

        # calculate drop points
        # -1 all n_colorless own
        shiny_dp[p] = -1 * sum('colorless' in color.lower()
                               for color in status_df.iloc[traits].color.tolist())

        # update total & save updated points to Shiny's 'effects'
        total += shiny_dp[p]
        status_df.loc[shiny_idx, "effects"] = ' '.join(str(x) for x in shiny_dp)

    # ----- VIRAL ----- if Viral was played by another player -----------------
    viral_idx = status_df.index[status_df.trait == 'Viral'].tolist()[0]
    vp_s = status_df.loc[viral_idx].effects
    if viral_idx not in traits and vp_s != 'none':
        # load current drop values for all players & Viral's 'effects'
        vp = [int(i) if i.lstrip('-').isnumeric() else np.nan for i in vp_s.split()]
        vp_col = status_df.loc[viral_idx].traits_WE

        # calculate drop points
        vp[p] = sum([vp_col in color.lower()
                     for color in status_df.iloc[traits].color.tolist()]) * -1

        # update total & save updated points to Viral's 'effects'
        if not np.isnan(vp[p]):
            total += vp[p]
            status_df.loc[viral_idx, "effects"] = ' '.join(str(x) for x in vp)

    # ----- NEOTENY ----- if Neoteny is in Hand after Worlds End --------------
    neoteny_idx = status_df.index[status_df.trait == 'Neoteny'].tolist()[0]
    neoteny_player_id = status_df.loc[neoteny_idx].effects
    if neoteny_player_id == str(p):
        total += 4

    return total
