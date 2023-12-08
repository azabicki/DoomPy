import numpy as np
import tkinter as tk


# create new window and show instructions of Worlds-End-Effects
def show_message(msg):
    secondary_window = tk.Toplevel()
    secondary_window.title("Worlds End")
    secondary_window.config(width=300, height=200)

    # Create a button to close (destroy) this window.
    button_close = tk.Button(
        secondary_window,
        text=msg,
        font=("", 30, "bold"),
        command=secondary_window.destroy)
    button_close.grid(row=0, column=0, stick='nesw')


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
        # only if drop & not 'inactive'
        if traits_df.loc[trait].drops == 1:
            # default dop points
            dp = np.nan

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
                        host_color = traits_df.loc[host].cur_color
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
                    we = traits_df.loc[trait].cur_worlds_end_trait
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
                    # see further down, viral is an exception since it affects others
                    pass

            # set current drop value & update total
            traits_df.loc[trait, 'cur_drops'] = dp
            if not np.isnan(dp):
                print("____ {} drop points by '{}'".format(dp, traits_df.loc[trait].trait))
                total += dp

    # *** !!! *** VIRAL *** !!! *** if Viral was played by another player **************
    viral_idx = traits_df.index[traits_df.trait == 'Viral'].tolist()[0]
    vp_s = traits_df.loc[viral_idx].cur_effect
    if viral_idx not in player_traits[p] and vp_s != 'none':
        # load current drop values for all players & Viral's 'cur_effect'
        vp = [int(i) if i.lstrip('-').isnumeric() else np.nan for i in vp_s.split()]
        vp_col = traits_df.loc[viral_idx].cur_worlds_end_trait

        # calculate drop points
        vp[p] = sum([vp_col in color.lower()
                     for color in traits_df.iloc[player_traits[p]].cur_color.tolist()]) * -1

        # update total & save updated points to Viral's 'cur_effect'
        if not np.isnan(vp[p]):
            total += vp[p]
            traits_df.loc[viral_idx, "cur_effect"] = ' '.join(str(x) for x in vp)
    # *** !!! *** VIRAL *** !!! *** if Viral was played by another player **************

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
    effect = traits_df.loc[host].cur_worlds_end_trait

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


def worlds_end(traits_df, we_catastrophe, player_traits, p, genes):
    if "select world's end" in we_catastrophe:
        return 0

    # init variable
    points = 0
    colors = ['blue', 'green', 'purple', 'red']
    traits = player_traits[p]

    match we_catastrophe:
        case "AI Takeover":
            # 2 colorless_worth ignore_colorless_effects
            #   --> change cur_face + cur_effect
            for trait in traits:
                if 'colorless' in traits_df.loc[trait].cur_color.lower():
                    traits_df.loc[trait, 'cur_face'] = 2
                    traits_df.loc[trait, 'cur_worlds_end_effect'] = 'Face_Inactive'

        case "AI Takeover (excl. dominant)":
            # 2 colorless_worth ignore_colorless_effects noDominant
            #   --> change cur_face + cur_effect
            for trait in traits:
                if ('colorless' in traits_df.loc[trait].cur_color and
                        traits_df.loc[trait].dominant != 1):
                    traits_df.loc[trait, 'cur_face'] = 2
                    traits_df.loc[trait, 'cur_worlds_end_effect'] = 'Face_Inactive'

        case "Algal Superbloom":
            # 1 each_blue_in_left_trait_pile
            traits_left = player_traits[p+1] if p+1 < len(player_traits) else player_traits[0]
            points = sum('blue' in color.lower()
                         for color in traits_df.iloc[traits_left].cur_color.tolist())

        case "Ancient Corruption":
            # -1 each_action
            points = -1 * sum(traits_df.loc[trait].action == 1 for trait in traits)

        case "Ashlands":
            # -4 if_<=2_purple_traits
            if sum('purple' in color.lower()
                   for color in traits_df.iloc[traits].cur_color.tolist()) <= 2:
                points = -4

        case "Bioengineered Plague":
            # discard_one_highest_color_count
            if p+1 == len(genes):
                show_message("Discard 1 random trait from your\nhighest color count from your trait pile.\
                             \n(If 2 or more colors are tied, pick 1.)from your trait pile\nat random.")

        case "Choking Vines":
            # 1 each_green_in_left_trait_pile
            traits_left = player_traits[p+1] if p+1 < len(player_traits) else player_traits[0]
            points = sum('green' in color.lower()
                         for color in traits_df.iloc[traits_left].cur_color.tolist())

        case "Deus ex Machina":
            # draw_card_add_face_value
            print('_____MANUAL ENTRY NEEDED_____')
            points = 0

        case "Deus ex Machina (max.5)":
            # draw_card_add_face_value_max.5
            print('_____MANUAL ENTRY NEEDED_____')
            points = 0

        case "Ecological Collapse":
            # +2 each_negative_face
            points = sum(traits_df.loc[trait].cur_face < 0 for trait in traits) * 2

        case "Endless Monsoon":
            # -1 hand
            print('_____MANUAL ENTRY NEEDED_____')
            points = 0

        case "Eyes Open from Behind the Stars":
            # discard_highest_face_value
            if p+1 == len(genes):
                show_message("Discard your highest face value\ntrait from your trait pile\nto the Old God.")

        case "Glacial Meltdown":
            # discard_one_blue
            if p+1 == len(genes):
                show_message("Discard 1 blue trait\nfrom your trait pile\nat random.")

        case "Glacial Meltdown (random)":
            # discard_one_blue
            if p+1 == len(genes):
                show_message("Discard 1 blue trait\nfrom your trait pile\nat random.")

        case "Great Deluge":
            # -4 if_<=2_blue_traits
            if sum('blue' in color.lower()
                   for color in traits_df.iloc[traits].cur_color.tolist()) <= 2:
                points = -4

        case "Grey Goo":
            # -5 most_traits
            n = [len(tp) for tp in player_traits]
            if len(traits) == max(n):
                points = -5

        case "Ice Age":
            # -1 each_red
            points = -1 * sum('red' in traits_df.loc[trait].cur_color.lower()
                              for trait in traits)

        case "Impact Event":
            # -1 each_trait_>=3_face
            points = -1 * sum(traits_df.loc[trait].cur_face >= 3 for trait in traits)

        case "Invasive Species":
            # add_max7_face_from_hand
            print('_____MANUAL ENTRY NEEDED_____')
            points = 0

        case "Jungle Rot":
            # -4 if_<=2_green_traits
            if sum('green' in color.lower()
                   for color in traits_df.iloc[traits].cur_color.tolist()) <= 2:
                points = -4

        case "Mass Extinction":
            # discard_one_green
            if p+1 == len(genes):
                show_message("Discard 1 green trait\nfrom your trait pile.")

        case "Mega Tsunami":
            # discard_one_red
            if p+1 == len(genes):
                show_message("Discard 1 red trait\nfrom your trait pile.")

        case "Mega Tsunami (random)":
            # discard_one_red
            if p+1 == len(genes):
                show_message("Discard 1 red trait\nfrom your trait pile at random.")

        case "Nuclear Winter (-1)":
            # discard_one_colorless
            if p+1 == len(genes):
                show_message("Discard 1 colorless trait\nfrom your trait pile.")

        case "Nuclear Winter (-2)":
            # discard_one_colorless
            if p+1 == len(genes):
                show_message("Discard 1 colorless trait\nfrom your trait pile.")

        case "Overpopulation":
            # +4 if fewest_traits
            n = [len(tp) for tp in player_traits]
            if len(traits) == min(n):
                points = 4

        case "Planetary Deforestation":
            # -gene_pool
            points = -1 * genes[p].get()

        case "Pulse Event":
            # discard_one_purple
            if p+1 == len(genes):
                show_message("Discard 1 purple trait\nfrom your trait pile.")

        case "Retrovirus":
            # -1 each_green
            points = -1 * sum('green' in traits_df.loc[trait].cur_color.lower()
                              for trait in traits)

        case "Sacrifice":
            # -4 if_<=2_red_traits
            if sum('red' in color.lower()
                   for color in traits_df.iloc[traits].cur_color.tolist()) <= 2:
                points = -4

        case "Solar Flare":
            # -1 each_purple
            points = -1 * sum('purple' in traits_df.loc[trait].cur_color.lower()
                              for trait in traits)

        case "Strange Matter":
            # -2 each_drop
            points = -2 * sum(traits_df.loc[trait].drops == 1 for trait in traits)

        case "Super Volcano":
            # -1 each_blue
            points = -1 * sum('blue' in traits_df.loc[trait].cur_color.lower()
                              for trait in traits)

        case "The Big One":
            # -2 per_each_missing_color
            ncol = []
            for col in colors:
                ncol.append(all([col not in traits_df.loc[trait].cur_color.lower()
                            for trait in traits]))
            points = -2 * sum(ncol)

        case "The Four Horsemen":
            # discard_one_trait_>=4_face
            if p+1 == len(genes):
                show_message("Discard 1 purple trait from\nyour trait pile with a\nface value of 4 or higher.")

        case "Tragedy of the Commons":
            # discard_one_drop
            if p+1 == len(genes):
                show_message("Discard a Drop of Life\nfrom your trait pile.")

        case "Tropical Superstorm":
            # 1 each_purple_in_left_trait_pile
            traits_left = player_traits[p+1] if p+1 < len(player_traits) else player_traits[0]
            points = sum('purple' in color.lower()
                         for color in traits_df.iloc[traits_left].cur_color.tolist())

        case "Volcanic Winter":
            # 1 each_red_in_left_trait_pile
            traits_left = player_traits[p+1] if p+1 < len(player_traits) else player_traits[0]
            points = sum('red' in color.lower()
                         for color in traits_df.iloc[traits_left].cur_color.tolist())

        case _:
            points = 0

    # print log
    print(">>> world's end <<< '{}' is responsible for {} points".format(we_catastrophe, points))

    return points
