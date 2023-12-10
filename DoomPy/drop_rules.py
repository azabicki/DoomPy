import numpy as np


# rules for filtering attachable traits depending on trait_pile and attachment
def drop_points(traits_df, player_traits, p, gene_pool):
    colors = ['blue', 'green', 'purple', 'red']
    traits = player_traits[p]
    total = 0

    # loop trait pile and apply drop-rules
    for trait in traits:
        # default dop points
        dp = np.nan

        # calc drop points only if drop==1 & not 'inactive'
        if traits_df.loc[trait].drops == 1:

            # first, if effects present which affect drops
            if ('inactive' in traits_df.loc[trait].cur_effect.lower() or
                    'inactive' in traits_df.loc[trait].cur_worlds_end_effect.lower()):
                traits_df.loc[trait, 'cur_drops'] = dp
                continue

            # match trait _name_
            match traits_df.loc[trait].trait:

                case 'Altruistic':
                    # own gene_pool
                    dp = gene_pool[p].get()

                case 'Apex Predator':
                    n = [len(i) for i in player_traits]
                    if n.index(max(n)) == p and n.count(max(n)) == 1:
                        dp = 4

                case 'Backbitter':
                    # 3 self if_one_negative own
                    dp = 3 * any([f < 0
                                  for f in traits_df.iloc[traits].cur_face.values.tolist()
                                  if isinstance(f, int)])

                case 'Big Feller':
                    # 6 self 4_or_less_face_is_1 own
                    dp = 6 * (sum([f <= 1
                                   for f in traits_df.iloc[traits].cur_face.values.tolist()
                                   if isinstance(f, int)]) <= 4)

                case 'Bionic Arm':
                    n = sum([traits_df.loc[t].game == 'Techlings' for t in traits])
                    dp = 2*n if traits_df.loc[trait].cur_attachment != 'none' else n

                case 'Bitter Berries':
                    # 1 self each_lower_count_green_or_purple own
                    ncols = []
                    for c in ['green', 'purple']:
                        ncols.append(sum([c in traits_df.loc[t].cur_color.lower()
                                          for t in traits]))
                    dp = min(ncols)

                case 'Boredom (~)':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Branches':
                    n_pairs = []
                    for tp in player_traits:
                        n_pairs.append(int(sum('green' in c.lower()
                                               for c in traits_df.iloc[tp].cur_color.tolist()) / 2))
                    n_pairs.pop(p)
                    if sum(n_pairs) > 0:
                        dp = sum(n_pairs)

                case 'Brave (1)':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Camouflage (1)':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Camouflage (2)':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Contagious':
                    # -1 self n_green own
                    dp = -1 * sum('green' in color.lower()
                                  for color in traits_df.iloc[traits].cur_color.tolist())

                case 'Cranial Crest':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Dragon Heart':
                    col_in_trait = []
                    for col in colors:
                        col_in_trait.append(any(col in color.lower()
                                                for color in traits_df.iloc[traits].cur_color.tolist()))
                    if all(col_in_trait):
                        dp = 4

                case 'Egg Clusters':
                    dp = sum('blue' in color.lower()
                             for color in traits_df.iloc[traits].cur_color.tolist())

                case 'Elven Ears':
                    dp = sum(traits_df.loc[t].game == 'Mythlings'
                             for tp in player_traits for t in tp)

                case 'Euphoric':
                    # 6 self 4_or_more_purple own
                    dp = 6 * (sum('purple' in traits_df.loc[t].cur_color.lower()
                                  for t in traits) >= 4)

                case 'Fortunate (~)':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Fortunate (1)':
                    n = []
                    for col in colors:
                        n.append(sum(col in color.lower()
                                     for color in traits_df.iloc[traits].cur_color.tolist()))
                    if n.index(max(n)) == colors.index('green') and n.count(max(n)) == 1:
                        dp = 2

                case 'GMO':
                    host = traits_df.loc[trait].cur_host
                    if host != 'none':
                        host_color = traits_df.loc[host].cur_color
                        pile_colors = traits_df.iloc[traits].cur_color.tolist()

                        dp = 0
                        for col in colors:
                            if col in host_color.lower():
                                dp += sum(col in i.lower() for i in pile_colors)

                case 'Gratitude':
                    col_in_trait = []
                    for col in colors:
                        col_in_trait.append(any(col in color.lower()
                                                for color in traits_df.iloc[traits].cur_color.tolist()))
                    if sum(col_in_trait) > 0:
                        dp = sum(col_in_trait)

                case 'Harmony':
                    # 2 self each_set_of_4_colors own
                    ncols = []
                    for col in colors:
                        ncols.append(sum(col in color.lower()
                                         for color in traits_df.iloc[traits].cur_color.tolist()))
                    dp = 2 * min(ncols)

                case 'Heat Vision':
                    dp = sum('red' in color.lower()
                             for color in traits_df.iloc[traits].cur_color.tolist())

                case 'Hypermyelination':
                    dp = max(gp.get() for gp in gene_pool)

                case 'Immunity':
                    dp = sum(face < 0
                             for face in traits_df.iloc[traits].face.tolist()
                             if not isinstance(face, str)) * 2

                case 'Kidney (g)' | 'Kidney (r)':
                    # calc Kidneys in own trait pile
                    dp = sum(['kidney' in traits_df.loc[t].trait.lower()
                              for t in traits])

                case 'Lily Pad':
                    # 1 self each_trait_returned own
                    # load drop value from traits_df, because it was set manually, if its not nan
                    we = traits_df.loc[trait].cur_worlds_end_trait
                    if we != 'none':
                        dp = int(we)

                case 'Mecha':
                    host = traits_df.loc[trait].cur_host
                    if host != 'none':
                        dp = int(np.nansum(traits_df.iloc[traits].effectless.tolist()))

                case 'Mindful':
                    dp = sum('colorless' in color.lower()
                             for color in traits_df.iloc[traits].cur_color.tolist())

                case 'Mutualism':
                    # n self gene_pool_max-2_final_score all
                    dp = max(gp.get() for gp in gene_pool)

                case 'Nano':
                    host = traits_df.loc[trait].cur_host
                    if host != 'none':
                        if not isinstance(traits_df.loc[host].cur_face, str):
                            dp = traits_df.loc[host].cur_face

                case 'Neoteny':
                    # 4 self if_in_hand own_hand
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Noxious':
                    # -1 self n_red own
                    dp = -1 * sum('red' in color.lower()
                                  for color in traits_df.iloc[traits].cur_color.tolist())

                case 'Nuptial Plumage':
                    # 2 self every_color_count_>=3 own
                    ncols = []
                    for col in colors:
                        ncols.append(sum(col in color.lower()
                                         for color in traits_df.iloc[traits].cur_color.tolist()))
                    dp = 2 * sum(n >= 3 for n in ncols)

                case 'Opposing Thumbs':
                    # copy_1st_dominant
                    # find first dominatn and call this function with only him in artificial trait pile
                    dom = [t for t in traits if traits_df.iloc[t].dominant == 1]
                    dom.remove(trait)

                    dp = np.nan

                case 'Overgrowth':
                    dp = sum('green' in color.lower()
                             for color in traits_df.iloc[traits].cur_color.tolist())

                case 'Pack Behavior':
                    tmp = []
                    for col in colors:
                        tmp.append(int(sum(col in color.lower()
                                           for color in traits_df.iloc[traits].cur_color.tolist()) / 2))
                    if sum(tmp) > 0:
                        dp = sum(tmp)

                case 'Pollination':
                    dp = sum(fv == 1
                             for fv in traits_df.iloc[traits].cur_face.tolist())

                case 'Prolific':
                    # 6 self 4_or_more_green own
                    dp = 6 * (sum('green' in traits_df.loc[t].cur_color.lower()
                                  for t in traits) >= 4)

                case 'Rainbow Keratin':
                    # -2 self n_drops own&2 self n_highest_color_if4colors own
                    dp = -2 * sum(traits_df.loc[t].drops == 1 for t in traits)
                    ncols = []
                    for col in colors:
                        ncols.append(sum(col in color.lower()
                                         for color in traits_df.iloc[traits].cur_color.tolist()))
                    if all(ncols):
                        dp += 2 * max(ncols)

                case 'Random Fertilization':
                    # own gene pool
                    dp = gene_pool[p].get()

                case 'Saudade (1)':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Sentience':
                    we = traits_df.loc[trait].cur_worlds_end_trait
                    if we != 'none':
                        dp = sum(we in color.lower()
                                 for color in traits_df.iloc[traits].cur_color.tolist())

                case 'Serrated Teeth':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Shiny':
                    # -1 all n_colorless own
                    dp = -1 * sum('colorless' in color.lower()
                                  for color in traits_df.iloc[traits].cur_color.tolist())

                case 'Shy':
                    # 5 self if_min_2_of_each_color own
                    ncols = []
                    for col in colors:
                        ncols.append(sum(col in color.lower()
                                         for color in traits_df.iloc[traits].cur_color.tolist()))
                    if all(n >= 2 for n in ncols):
                        dp = 5

                case 'Sour Grapes':
                    # 1 self each_lower_count_blue_or_red own
                    ncols = []
                    for c in ['blue', 'red']:
                        ncols.append(sum([c in traits_df.loc[t].cur_color.lower()
                                          for t in traits]))
                    dp = min(ncols)

                case 'Spicy':
                    # 1 self each_lower_count_green_or_red own
                    ncols = []
                    for c in ['green', 'red']:
                        ncols.append(sum([c in traits_df.loc[t].cur_color.lower()
                                          for t in traits]))
                    dp = min(ncols)

                case 'Sticky Secretions':
                    dp = sum('purple' in color.lower()
                             for color in traits_df.iloc[traits].cur_color.tolist())

                case 'Swarm (b)' | 'Swarm (g)' | 'Swarm (p)' | 'Swarm (r)' | 'Swarm (c)':
                    # calc all swarms in all trait piles
                    dp = sum(['swarm' in traits_df.loc[t].trait.lower()
                              for tp in player_traits
                              for t in tp])

                case 'Sweet':
                    # 1 self each_lower_count_blue_or_green own
                    ncols = []
                    for c in ['blue', 'green']:
                        ncols.append(sum([c in traits_df.loc[t].cur_color.lower()
                                          for t in traits]))
                    dp = min(ncols)

                case 'Sycophant':
                    # 5 self if_>=5_red opponents
                    nred = []
                    for tp in player_traits:
                        nred.append(sum('red' in traits_df.iloc[t].cur_color.lower()
                                        for t in tp))
                    nred.pop(p)
                    if any(n >= 5 for n in nred):
                        dp = 5

                case 'Symbiosis':
                    n = []
                    for col in colors:
                        n.append(sum(col in color.lower()
                                     for color in traits_df.iloc[traits].cur_color.tolist()))
                    n = [i for i in n if i > 0]
                    if len(n) >= 2:
                        dp = min(n) * 2

                case 'Tenacious':
                    # 6 self 4_or_more_red own
                    dp = 6 * (sum('red' in traits_df.loc[t].cur_color.lower()
                                  for t in traits) >= 4)

                case 'Tiny':
                    dp = -1 * len(traits)

                case 'Tiny Arms':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Vivacious':
                    # 6 self 4_or_more_blue own
                    dp = 6 * (sum('blue' in traits_df.loc[t].cur_color.lower()
                                  for t in traits) >= 4)

            # set current drop value & update total
            traits_df.loc[trait, 'cur_drops'] = dp
            if not np.isnan(dp):
                print("____ {} drop points by '{}'".format(dp, traits_df.loc[trait].trait))
                total += dp

    # *** section for drop-effects in other trait piles, which could affect this player ***
    # ----- AMATOXINS ----- if Amatoxins was played by another player -----------------
    amatoxins_idx = traits_df.index[traits_df.trait == 'Amatoxins'].tolist()[0]
    we_amatoxins = traits_df.loc[amatoxins_idx].cur_worlds_end_trait
    if amatoxins_idx not in traits and we_amatoxins != 'none':
        # calculate drop points
        total += int(traits_df.loc[amatoxins_idx].cur_effect) * -2

    # ----- PROWLER ----- if Prowler was played by another player -----------------
    prowler_idx = traits_df.index[traits_df.trait == 'Prowler'].tolist()[0]
    played = [prowler_idx in tp for tp in player_traits]
    if any(played) and played.index(True) != p:
        # load current prowler_drop_points
        prw_ps = traits_df.loc[prowler_idx].cur_effect

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
                             for color in traits_df.iloc[player_traits[played_by]].cur_color.tolist()))
        ncols_ref = sum(n > 0 for n in ncols_ref)

        ncols = []
        for col in colors:
            ncols.append(sum(col in color.lower()
                             for color in traits_df.iloc[player_traits[p]].cur_color.tolist()))
        ncols = sum(n > 0 for n in ncols)

        prw_p[p] = max([0, ncols_ref - ncols]) * -2

        # update total & save updated points to Prowler's 'cur_effect'
        total += prw_p[p]
        traits_df.loc[prowler_idx, "cur_effect"] = ' '.join(str(x) for x in prw_p)

    # ----- SHINY ----- if Shiny was played by another player -----------------
    shiny_idx = traits_df.index[traits_df.trait == 'Shiny'].tolist()[0]
    if (any(shiny_idx in tp for tp in player_traits) and
            'inactive' not in traits_df.loc[shiny_idx].cur_effect.lower()):
        # load current shiny_drop_points
        shiny_ps = traits_df.loc[shiny_idx, 'cur_effect']

        # init them, if not done previously
        if shiny_ps == 'none':
            shiny_p = [np.nan] * len(gene_pool)
        else:
            shiny_p = [int(i) if i.lstrip('-').isnumeric() else np.nan
                       for i in shiny_ps.split()]

        # calculate drop points
        # -1 all n_colorless own
        shiny_p[p] = -1 * sum('colorless' in color.lower()
                              for color in traits_df.iloc[traits].cur_color.tolist())

        # update total & save updated points to Shiny's 'cur_effect'
        total += shiny_p[p]
        traits_df.loc[shiny_idx, "cur_effect"] = ' '.join(str(x) for x in shiny_p)

    # ----- VIRAL ----- if Viral was played by another player -----------------
    viral_idx = traits_df.index[traits_df.trait == 'Viral'].tolist()[0]
    vp_s = traits_df.loc[viral_idx].cur_effect
    if viral_idx not in traits and vp_s != 'none':
        # load current drop values for all players & Viral's 'cur_effect'
        vp = [int(i) if i.lstrip('-').isnumeric() else np.nan for i in vp_s.split()]
        vp_col = traits_df.loc[viral_idx].cur_worlds_end_trait

        # calculate drop points
        vp[p] = sum([vp_col in color.lower()
                     for color in traits_df.iloc[traits].cur_color.tolist()]) * -1

        # update total & save updated points to Viral's 'cur_effect'
        if not np.isnan(vp[p]):
            total += vp[p]
            traits_df.loc[viral_idx, "cur_effect"] = ' '.join(str(x) for x in vp)

    # ----- NEOTENY ----- if Neoteny is in Hand after Worlds End --------------
    neoteny_idx = traits_df.index[traits_df.trait == 'Neoteny'].tolist()[0]
    neoteny_player_id = traits_df.loc[neoteny_idx].cur_effect
    if neoteny_player_id == str(p):
        total += 4

    return total
