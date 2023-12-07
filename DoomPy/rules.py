import numpy as np


# rules for filtering attachable traits depending on trait_pile and attachment
def filter_attachables(traits_df, traits_filtered, attachment):
    # get attachment-rule of attachment
    rule = traits_df.loc[attachment].effect_attachment.split()

    # filter out all attachments, dominants & traits-with-attachments
    traits_filtered = [idx for idx in traits_filtered
                       if traits_df.loc[idx].trait not in traits_df[traits_df.attachment == 1].trait.values.tolist()
                       and traits_df.loc[idx].trait not in traits_df[traits_df.dominant == 1].trait.values.tolist()
                       and (traits_df.loc[idx].cur_attachment == 'none'
                            or traits_df.loc[idx].cur_attachment == attachment)]

    # filter out based on specific rules
    match rule[0]:
        case 'negative_face':
            traits_filtered = [idx for idx in traits_filtered
                               if traits_df.loc[idx].face < 0]

        case 'non_blue':
            traits_filtered = [idx for idx in traits_filtered
                               if 'blue' not in traits_df.loc[idx].color.lower()]

        case 'non_green':
            traits_filtered = [idx for idx in traits_filtered
                               if 'green' not in traits_df.loc[idx].color.lower()]

        case 'color':
            traits_filtered = [idx for idx in traits_filtered
                               if 'colorless' not in traits_df.loc[idx].color.lower()]

        case 'effectless':
            traits_filtered = [idx for idx in traits_filtered
                               if traits_df.loc[idx].effectless == 1]

    return traits_filtered


def attachment_effects(traits_df, host, attachment):
    # get current effects of host
    effects = {'color':  traits_df.loc[host].cur_color,
               'face':   traits_df.loc[host].cur_face,
               'effect': traits_df.loc[host].cur_effect}

    # get effect of attachment
    rule = traits_df.loc[attachment].effect_attachment.split()

    # update current effect based on specific rules
    match rule[1]:
        case 'IsBlue':
            effects['color'] = 'Blue'

        case 'IsGreen':
            effects['color'] = 'Green'

        case 'Inactive':
            effects['effect'] = rule[1]

        case 'NoDiscard':
            effects['effect'] = rule[1]

        case 'NoRemove':
            effects['effect'] = rule[1]

        case 'NoSwap_NoSteal':
            effects['effect'] = rule[1]

    return effects


def drop_points(traits_df, player_traits, p, gene_pool):
    colors = ['blue', 'green', 'purple', 'red']

    total = 0
    # loop trait pile and apply drop-rules
    for trait in player_traits[p]:
        # only if drop
        if traits_df.loc[trait].drops == 1:
            dp = np.nan

            # match trait _name_
            match traits_df.loc[trait].trait:

                case 'Altruistic':
                    # own gene_pool
                    dp = gene_pool[p].get()

                case 'Apex Predator':
                    n = [len(i) for i in player_traits]
                    if n.index(max(n)) == p and n.count(max(n)) == 1:
                        dp = 4

                case 'Bionic Arm':
                    n = sum([traits_df.loc[t].game == 'Techlings' for t in player_traits[p]])
                    dp = 2*n if traits_df.loc[trait].cur_attachment != 'none' else n

                case 'Boredom (~)':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Branches':
                    tmp = []
                    for tp in player_traits:
                        tmp.append(int(sum('green' in c.lower()
                                           for c in traits_df.iloc[tp].cur_color.tolist()) / 2))
                    tmp.pop(p)
                    if sum(tmp) > 0:
                        dp = sum(tmp)

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

                case 'Cranial Crest':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Dragon Heart':
                    tmp = []
                    for col in colors:
                        tmp.append(any(col in pile.lower()
                                       for pile in traits_df.iloc[player_traits[p]].cur_color.tolist()))
                    if all(tmp):
                        dp = 4

                case 'Egg Clusters':
                    dp = sum('blue' in color.lower()
                             for color in traits_df.iloc[player_traits[p]].cur_color.tolist())

                case 'Elven Ears':
                    dp = sum(traits_df.loc[t].game == 'Mythlings'
                             for tp in player_traits for t in tp)

                case 'Fortunate (~)':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Fortunate (1)':
                    n = []
                    for col in colors:
                        n.append(sum(col in color.lower()
                                     for color in traits_df.iloc[player_traits[p]].cur_color.tolist()))
                    if n.index(max(n)) == colors.index('green') and n.count(max(n)) == 1:
                        dp = 2

                case 'GMO':
                    host = traits_df.loc[trait].cur_host
                    if host != 'none':
                        host_color = traits_df.loc[host].color
                        pile_colors = traits_df.iloc[player_traits[p]].cur_color.tolist()

                        dp = 0
                        for col in colors:
                            if col in host_color.lower():
                                dp += sum(col in i.lower() for i in pile_colors)

                case 'Gratitude':
                    tmp = []
                    for col in colors:
                        tmp.append(any(col in pile.lower()
                                       for pile in traits_df.iloc[player_traits[p]].cur_color.tolist()))
                    if sum(tmp) > 0:
                        dp = sum(tmp)

                case 'Heat Vision':
                    dp = sum('red' in color.lower()
                             for color in traits_df.iloc[player_traits[p]].cur_color.tolist())

                case 'Hypermyelination':
                    dp = max(gp.get() for gp in gene_pool)

                case 'Immunity':
                    dp = sum(face < 0
                             for face in traits_df.iloc[player_traits[p]].face.tolist()
                             if not isinstance(face, str)) * 2

                case 'Kidney':
                    # calc Kidneys in own trait pile
                    dp = sum([traits_df.loc[t].trait == 'Kidney'
                              for t in player_traits[p]])

                case 'Mecha':
                    host = traits_df.loc[trait].cur_host
                    if host != 'none':
                        dp = int(np.nansum(traits_df.iloc[player_traits[p]].effectless.tolist()))

                case 'Mindful':
                    dp = sum('colorless' in color.lower()
                             for color in traits_df.iloc[player_traits[p]].cur_color.tolist())

                case 'Nano':
                    host = traits_df.loc[trait].cur_host
                    if host != 'none':
                        if not isinstance(traits_df.loc[host].cur_face, str):
                            dp = traits_df.loc[host].cur_face

                case 'Overgrowth':
                    dp = sum('green' in color.lower()
                             for color in traits_df.iloc[player_traits[p]].cur_color.tolist())

                case 'Pack Behavior':
                    tmp = []
                    for col in colors:
                        tmp.append(int(sum(col in color.lower()
                                           for color in traits_df.iloc[player_traits[p]].cur_color.tolist()) / 2))
                    print(tmp)
                    if sum(tmp) > 0:
                        dp = sum(tmp)

                case 'Pollination':
                    dp = sum(fv == 1
                             for fv in traits_df.iloc[player_traits[p]].cur_face.tolist())

                case 'Random Fertilization':
                    # own gene pool
                    dp = gene_pool[p].get()

                case 'Saudade (1)':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Sentience':
                    we = traits_df.loc[trait].cur_worlds_end
                    if we != 'none':
                        dp = sum(we in color.lower()
                                 for color in traits_df.iloc[player_traits[p]].cur_color.tolist())

                case 'Serrated Teeth':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Sticky Secretions':
                    dp = sum('purple' in color.lower()
                             for color in traits_df.iloc[player_traits[p]].cur_color.tolist())

                case 'Swarm':
                    # calc all swarms in all trait piles
                    dp = sum([traits_df.loc[t].trait == 'Swarm'
                              for tp in player_traits
                              for t in tp])

                case 'Symbiosis':
                    n = []
                    for col in colors:
                        n.append(sum(col in color.lower()
                                     for color in traits_df.iloc[player_traits[p]].cur_color.tolist()))
                    n = [i for i in n if i > 0]
                    if len(n) >= 2:
                        dp = min(n) * 2

                case 'Tiny':
                    dp = -1 * len(player_traits[p])

                case 'Tiny Arms':
                    # load drop value from traits_df, because it was set manually, if its not nan
                    if not np.isnan(traits_df.loc[trait].cur_drops):
                        dp = int(traits_df.loc[trait].cur_drops)

                case 'Viral':
                    pass

            # set current drop value & update total
            traits_df.loc[trait, 'cur_drops'] = dp
            if not np.isnan(dp):
                print("____ {} drop points by '{}'".format(dp, traits_df.loc[trait].trait))
                total += dp

    return total


def traits_WE_tasks(traits_df, host):
    # get effect of trait
    rule = traits_df.loc[host].effect_worlds_end

    # update current tasks based on specific rule
    match rule:
        case 'choose_color':
            tasks = ['choose color:', 'blue', 'green', 'purple', 'red']

        case 'is_color_of_choice':
            tasks = ['becomes ...', 'blue', 'green', 'purple', 'red']

        case 'may_change_one_color':
            tasks = ['may change:',
                     'blue -> green', 'blue -> purple', 'blue -> red',
                     'green -> blue', 'green -> purple', 'green -> red',
                     'purple -> blue', 'purple -> green', 'purple -> red',
                     'red -> blue', 'red -> green', 'red -> purple']

    return tasks


def traits_WE_effects(traits_df, host, trait_pile):
    rule = traits_df.loc[host].effect_worlds_end
    effect = traits_df.loc[host].cur_worlds_end

    match rule:
        case 'is_color_of_choice':
            if effect == 'none':
                traits_df.loc[host, 'cur_color'] = traits_df.loc[host].color
            else:
                traits_df.loc[host, 'cur_color'] = effect

        case 'may_change_one_color':
            if effect != 'none':
                # split rule to define which color will be changed to which other color
                col_from, col_to = effect.split(' -> ')

                # loop trait pile
                for trait in trait_pile:
                    if col_from.lower() in traits_df.loc[trait].cur_color.lower():
                        old_colors = traits_df.loc[trait].cur_color.lower()
                        new_colors = old_colors.replace(col_from, col_to)
                        traits_df.loc[trait, 'cur_color'] = new_colors


def worlds_end(worlds_end, p, player_cards, traits):
    cards = player_cards[p]

    match worlds_end:
        case "AI Takeover":
            # 2 colorless_worth ignore_colorless_effects
            colors = [traits[traits.name == card]['color'].values[0] for card in cards]
            n_colorless = sum([1 for col in colors if "Colorless" in col])

            if n_colorless > 100:
                points = 100
            else:
                points = 0

        case "AI Takeover (excl. dominant)":
            # 2 colorless_worth ignore_colorless_effects noDominant
            points = 0

        case "Algal Superbloom":
            # 1 each_blue_in_left_trait_pile
            points = 0

        case "Ancient Corruption":
            # -1 each_action
            points = 0

        case "Ashlands":
            # -4 if_<=2_purple_traits
            points = 0

        case "Bioengineered Plague":
            # discard_one_highest_color_count
            points = 0

        case "Choking Vines":
            # 1 each_green_in_left_trait_pile
            points = 0

        case "Deus ex Machina":
            # draw_card_add_face_value
            points = 0

        case "Deus ex Machina (max.5)":
            # draw_card_add_face_value_max.5
            points = 0

        case "Ecological Collapse":
            # 2 each_negative_face
            points = 0

        case "Endless Monsoon":
            # -1 hand
            points = 0

        case "Eyes Open from Behind the Stars":
            # discard_highest_face_value
            points = 0

        case "Glacial Meltdown":
            # discard_one_blue
            points = 0

        case "Great Deluge":
            # -4 if_<=2_blue_traits
            points = 0

        case "Grey Goo":
            # -5 most_traits
            points = 0

        case "Ice Age":
            # -1 each_red
            points = 0

        case "Impact Event":
            # -1 each_trait_>=3_face
            points = 0

        case "Invasive Species":
            # add_max7_face_from_hand
            points = 0

        case "Jungle Rot":
            # -4 if_<=2_green_traits
            points = 0

        case "Mass Extinction":
            # discard_one_green
            points = 0

        case "Mega Tsunami":
            # discard_one_red
            points = 0

        case "Nuclear Winter (-1)":
            # discard_one_colorless
            points = 0

        case "Nuclear Winter (-2)":
            # discard_one_colorless
            points = 0

        case "Overpopulation":
            # 4 fewest_traits
            points = 0

        case "Planetary Deforestation":
            # -gene_pool
            points = 0

        case "Pulse Event":
            # discard_one_purple
            points = 0

        case "Retrovirus":
            # -1 each_green
            points = 0

        case "Sacrifice":
            # -4 if_<=2_red_traits
            points = 0

        case "Solar Flare":
            # -1 each_purple
            points = 0

        case "Strange Matter":
            # -2 each_drop
            points = 0

        case "Super Volcano":
            # -1 each_blue
            points = 0

        case "The Big One":
            # -2 per_each_missing_color
            points = 0

        case "The Four Horsemen":
            # discard_one_trait_>=4_face
            points = 0

        case "Tragedy of the Commons":
            # discard_one_drop
            points = 0

        case "Tropical Superstorm":
            # 1 each_purple_in_left_trait_pile
            points = 0

        case "Volcanic Winter":
            # 1 each_red_in_left_trait_pile
            points = 0

        case _:
            points = 0

    return points
