from globals_ import plr, traits_df, status_df, MOLs, MOLs_df, game, worlds_end
import numpy as np
import tkinter as tk

import rules_drop as rules_dr
import rules_worlds_end as rules_we


# effects when selecting specific MOLs -------------------------------------------------------------
def select_MOL(p, MOL_idx, prev_MOL):
    MOL = None if MOL_idx is None else MOLs_df.loc[MOL_idx].MOL

    # if __The Blind Dragon__ is selected
    if MOL == 'The Blind Dragon':
        # -> add 2 MOLs
        MOLs['n'][p] += 2
        for ip in range(2):
            plr['points_MOL'][p].append(tk.StringVar(value="0"))  # for now, manually editing MOL points in entries
            MOLs['played'][p].append(None)
            MOLs['cbox'][p].append([])
            MOLs['icon'][p].append([])

    # if __The Blind Dragon__ is de-selected
    if prev_MOL is not None and MOLs_df.loc[prev_MOL].MOL == 'The Blind Dragon':
        # -> remove the last 2 MOLs
        MOLs['n'][p] -= 2
        plr['points_MOL'][p][MOLs['n'][p]:] = []
        MOLs['played'][p][MOLs['n'][p]:] = []
        MOLs['cbox'][p][MOLs['n'][p]:] = []
        MOLs['icon'][p][MOLs['n'][p]:] = []

    # if __The River Mist__ is selected
    if MOL == 'The River Mist':
        # -> add 2 to xtra trait pile count
        plr['n_tp'][p]['xtra'] += 2

    # if __The River Mist__ is de-selected
    if prev_MOL is not None and MOLs_df.loc[prev_MOL].MOL == 'The River Mist':
        # -> remove 2 from xtra trait pile count
        plr['n_tp'][p]['xtra'] -= 2


# handle worlds end effect of catastrophes ---------------------------------------------------------
def calc_MOL_points(p, m):
    # if MOLSs not selected
    if MOLs['played'][p][m] is None:
        return 0

    # init variable
    colors = ['blue', 'green', 'purple', 'red']
    trait_pile = plr['trait_pile'][p]
    genes = plr['genes'][p].get()
    thisMOL = MOLs_df.loc[MOLs['played'][p][m]].MOL
    points = 0

    # calculate MOL points
    match thisMOL:
        case "The Armored Melon":
            points = int(plr['points_MOL'][p][m].get())

        case "The Bilbies (4/10)":
            n = sum(traits_df.loc[t].dominant == 1
                    for t in trait_pile)

            if n == 0:
                points = 10
            elif n == 1:
                points = 4

        case "The Blind Dragon":
            points = 0

        case "The Bramble Brawler":
            n_cols = []
            for pl in range(len(plr['trait_pile'])):
                n_cols.append(sum('purple' in color.lower()
                                  for color in status_df.loc[plr['trait_pile'][pl]].color.values.tolist()))

            if n_cols[p] == max(n_cols) and sum(i == n_cols[p] for i in n_cols) == 1:
                points = 4

            for i in [i for i in range(len(n_cols)) if i != p]:
                if n_cols[p] > n_cols[i]:
                    points += 1

        case "The Bush Kid":
            n_drops = sum(traits_df.loc[t].drops == 1
                          for t in trait_pile)

            n_actions = sum(traits_df.loc[t].action == 1
                            for t in trait_pile)

            if n_drops >= 3:
                points += 3
                if n_actions >= 5:
                    points += 6

        case "The Cabochon":
            n = sum('red' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n == 0:
                points = 6
            elif n <= 2:
                points = 3

        case "The Child And The Bear":
            dominants = [t for t in trait_pile if traits_df.loc[t].dominant == 1]

            n_dom_cols = []
            n_pairs = []
            for col in colors:
                n_dom_cols.append(sum(col in color.lower()
                                      for color in status_df.loc[dominants].color.tolist()))
                n_pairs.append(int(sum(col in status_df.iloc[t].color.lower()
                                       for t in trait_pile
                                       if traits_df.iloc[t].dominant != 1) / 2))

            points = np.dot(n_dom_cols, n_pairs)

        case "The Clashing Crabs":
            n_neg = sum(face < 0
                        for face in status_df.loc[trait_pile].face.values.tolist()
                        if not isinstance(face, str))

            n_high = sum(face >= 4
                         for face in status_df.loc[trait_pile].face.values.tolist()
                         if not isinstance(face, str))

            if n_neg == n_high:
                points = 8
            elif n_neg > n_high:
                points = 4

        case "The Cosmic Jinx (4/8)":
            if genes <= 2:
                points = 8
            elif genes == 3:
                points = 4

        case "The Dancer (12/8)":
            n = []
            for p in range(game['n_player']):
                p_WE = rules_we.calc_WE_points(p) if worlds_end['played'] != 'none' else 0
                p_face = int(sum([status_df.loc[trait_idx].face
                                  for trait_idx in plr['trait_pile'][p]
                                  if not isinstance(status_df.loc[trait_idx].face, str)]))
                p_drop = rules_dr.drop_points(p)
                n.append(p_WE + p_face + p_drop)

            if n[p] == min(n):
                if len(set(n)) == len(n):
                    points = 12
                else:
                    points = 8

        case "The Diamond Butterfly":
            n_cols = [[], []]
            check_cols = ['blue', 'green']
            for c in range(len(check_cols)):
                for pl in range(len(plr['trait_pile'])):
                    n_cols[c].append(sum(check_cols[c] in color.lower()
                                         for color in status_df.loc[plr['trait_pile'][pl]].color.values.tolist()))

            check = []
            check.append(2 if n_cols[0][p] == min(n_cols[0]) else 0)
            check.append(2 if n_cols[1][p] == min(n_cols[1]) else 0)

            points = 6 if sum(check) == 4 else sum(check)

        case "The Emerald Slug":
            n_cols = [[], []]
            check_cols = ['red', 'blue']
            for c in range(len(check_cols)):
                for pl in range(len(plr['trait_pile'])):
                    n_cols[c].append(sum(check_cols[c] in color.lower()
                                         for color in status_df.loc[plr['trait_pile'][pl]].color.values.tolist()))

            check = []
            check.append(2 if n_cols[0][p] == min(n_cols[0]) else 0)
            check.append(2 if n_cols[1][p] == min(n_cols[1]) else 0)

            points = 6 if sum(check) == 4 else sum(check)

        case "The Fellmonger":
            n = sum('blue' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n == 0:
                points = 6
            elif n <= 2:
                points = 3

        case "The Fire Bandit":
            n_cols = []
            for pl in range(len(plr['trait_pile'])):
                n_cols.append(sum('red' in color.lower()
                                  for color in status_df.loc[plr['trait_pile'][pl]].color.values.tolist()))

            if n_cols[p] == max(n_cols) and sum(i == n_cols[p] for i in n_cols) == 1:
                points = 4

            for i in [i for i in range(len(n_cols)) if i != p]:
                if n_cols[p] > n_cols[i]:
                    points += 1

        case "The Forest Keeper":
            n_cols = []
            for pl in range(len(plr['trait_pile'])):
                n_cols.append(sum('green' in color.lower()
                                  for color in status_df.loc[plr['trait_pile'][pl]].color.values.tolist()))

            if n_cols[p] == max(n_cols) and sum(i == n_cols[p] for i in n_cols) == 1:
                points = 4

            for i in [i for i in range(len(n_cols)) if i != p]:
                if n_cols[p] > n_cols[i]:
                    points += 1

        case "The Fortunate Alchemist":
            n = 0
            for face in status_df.loc[trait_pile].face.values.tolist():
                if (isinstance(face, str) and face == 'variable') or face == 0:
                    n += 1

            if n >= 5:
                points = 9
            elif n >= 2:
                points = 2
            elif n == 0:
                points = -4

        case "The Genial Outsider":
            n_drops = sum(traits_df.loc[t].drops == 1
                          for t in trait_pile)

            n_actions = sum(traits_df.loc[t].action == 1
                            for t in trait_pile)

            if n_drops <= 2:
                points += 3
                if n_actions <= 3:
                    points += 6

        case "The Golden Shrew":
            n = len(plr['trait_pile'][p])

            if n <= 8:
                points = 7
            elif n <= 12:
                points = 4

        case "The Hero":
            dominants = [t for t in trait_pile if traits_df.loc[t].dominant == 1]

            d_points = []
            for d in dominants:
                d_col = status_df.loc[d].color
                pile_colors = status_df.iloc[trait_pile].color.tolist()

                n = 0
                for col in colors:
                    n += sum(col in i.lower()
                             for i in pile_colors
                             if col in d_col.lower())

                d_points.append(4 if n-1 <= 1 else 0)

            if len(dominants) == 3:
                points = 12
            else:
                points = sum(d_points)

        case "The Jellyfish":
            n = sum('blue' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n >= 6:
                points = 6
            elif n >= 3:
                points = 3

        case "The Jungler":
            n_cols = []
            for pl in range(len(plr['trait_pile'])):
                n_cols.append(sum('colorless' in color.lower()
                                  for color in status_df.loc[plr['trait_pile'][pl]].color.values.tolist()))

            if n_cols[p] == max(n_cols) and sum(i == n_cols[p] for i in n_cols) == 1:
                points = 4

            for i in [i for i in range(len(n_cols)) if i != p]:
                if n_cols[p] > n_cols[i]:
                    points += 1

        case "The Logician":
            n = sum(traits_df.iloc[t].effectless == 1
                    for t in trait_pile)

            if n >= 6:
                points = 6
            elif n >= 3:
                points = 3

        case "The Lumberjack":
            n = sum('green' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n == 0:
                points = 6
            elif n <= 2:
                points = 3

        case "The Lunar Guard":
            n = []
            for col in colors:
                n.append(sum(col in color.lower()
                             for color in status_df.loc[trait_pile].color.values.tolist()))
            n.append(sum('colorless' in color.lower()
                         for color in status_df.loc[trait_pile].color.values.tolist()))

            missing = sum(i == 0 for i in n)
            if missing >= 2:
                points = 9
            elif missing == 1:
                points = 4

        case "The Magician":
            n = sum('colorless' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n == 0:
                points = 6
            elif n <= 2:
                points = 3

        case "The Maven":
            n = len(trait_pile)

            if n >= 15:
                points = 7
            elif n >= 10:
                points = 3

        case "The Medicine Master":
            n = sum(face < 0
                    for face in status_df.loc[trait_pile].face.values.tolist()
                    if not isinstance(face, str))

            if n >= 3:
                points = 7
            elif n >= 1:
                points = 3

        case "The Monkey Thief":
            n_drops = sum(traits_df.loc[t].drops == 1
                          for t in trait_pile)

            points = 8 - (3*n_drops)

        case "The Painter":
            n = []
            for col in colors:
                n.append(sum(col in color.lower()
                             for color in status_df.loc[trait_pile].color.values.tolist()))

            points = sum(i % 2 == 0 for i in n if i > 0) * 3

        case "The Parrots Riddle":
            n_actions = sum(traits_df.loc[t].action == 1
                            for t in trait_pile)

            points = 9 - (2*n_actions)

        case "The Rain Golem":
            n_cols = []
            for pl in range(len(plr['trait_pile'])):
                n_cols.append(sum('blue' in color.lower()
                                  for color in status_df.loc[plr['trait_pile'][pl]].color.values.tolist()))

            if n_cols[p] == max(n_cols) and sum(i == n_cols[p] for i in n_cols) == 1:
                points = 4

            for i in [i for i in range(len(n_cols)) if i != p]:
                if n_cols[p] > n_cols[i]:
                    points += 1

        case "The River Mist":
            n = [i['t'].get() for i in plr['n_tp']]

            if n[p] == max(n) and sum(i == n[p] for i in n) == 1:
                points = 4

            for i in [i for i in range(len(n)) if i != p]:
                if n[p] > n[i]:
                    points += 1

        case "The Ruby Tortoise":
            n_cols = [[], []]
            check_cols = ['green', 'purple']
            for c in range(len(check_cols)):
                for pl in range(len(plr['trait_pile'])):
                    n_cols[c].append(sum(check_cols[c] in color.lower()
                                         for color in status_df.loc[plr['trait_pile'][pl]].color.values.tolist()))

            check = []
            check.append(2 if n_cols[0][p] == min(n_cols[0]) else 0)
            check.append(2 if n_cols[1][p] == min(n_cols[1]) else 0)

            points = 6 if sum(check) == 4 else sum(check)

        case "The Sapphire Ladybug":
            n_cols = [[], []]
            check_cols = ['purple', 'red']
            for c in range(len(check_cols)):
                for pl in range(len(plr['trait_pile'])):
                    n_cols[c].append(sum(check_cols[c] in color.lower()
                                         for color in status_df.loc[plr['trait_pile'][pl]].color.values.tolist()))

            check = []
            check.append(2 if n_cols[0][p] == min(n_cols[0]) else 0)
            check.append(2 if n_cols[1][p] == min(n_cols[1]) else 0)

            points = 6 if sum(check) == 4 else sum(check)

        case "The Silent Elder":
            points = int(plr['points_MOL'][p][m].get())

        case "The Soothsayer":
            n = sum('purple' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n == 0:
                points = 6
            elif n <= 2:
                points = 3

        case "The Spirit Gardener":
            n = sum('colorless' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n >= 6:
                points = 6
            elif n >= 3:
                points = 3

        case "The Stylite":
            dp = rules_dr.drop_points(p)

            if dp <= 2:
                points = 7
            elif dp <= 6:
                points = 3

        case "Thunder Frogs":
            n_twos = []
            for col in colors:
                n_twos.append(sum(status_df.loc[t].face == 2
                                  for t in trait_pile
                                  if col in status_df.loc[t].color.lower()))

            points = sum(i == 1 for i in n_twos) * 2

        case "The Tigris":
            n = sum(traits_df.loc[t].action == 1
                    for t in trait_pile)

            if n >= 6:
                points = 6
            elif n >= 3:
                points = 3

        case "The Tracker":
            n_cols = []
            for col in colors:
                n_cols.append(sum(col in color.lower()
                                  for color in status_df.loc[trait_pile].color.values.tolist()))
            n_cl = sum('colorless' in color.lower()
                       for color in status_df.loc[trait_pile].color.values.tolist())

            points = n_cl if all(n_cols) else 0

        case "The Truffle Hunter":
            n = sum(face == 1
                    for face in status_df.loc[trait_pile].face.values.tolist()
                    if not isinstance(face, str))

            if n >= 6:
                points = 6
            elif n >= 3:
                points = 2

        case "The Vagrant (8/6)":
            n = [len(tp) for tp in plr['trait_pile']]

            if n[p] == min(n):
                if len(set(n)) == len(n):
                    points = 8
                else:
                    points = 6

        case "The Vixen":
            n = sum('purple' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n >= 6:
                points = 6
            elif n >= 3:
                points = 3

        case "The Warbler":
            n = sum('green' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n >= 6:
                points = 6
            elif n >= 3:
                points = 3

        case "The Warrior":
            n = sum('red' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n >= 6:
                points = 6
            elif n >= 3:
                points = 3

        case "The Weaver":
            n_cols = []
            for col in colors:
                n_cols.append(sum(col in color.lower()
                                  for color in status_df.iloc[trait_pile].color.tolist()))
            points = 3 * min(n_cols)

        case "The Wilted Flower":
            n = [gp.get() for gp in plr['genes']]

            if n[p] == min(n):
                if len(set(n)) == len(n):
                    points = 7
                else:
                    points = 4

        case _:
            points = 0

    return points
