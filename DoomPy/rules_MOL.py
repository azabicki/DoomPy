from globals_ import plr, traits_df, status_df, MOLs, MOLs_df


# handle worlds end effect of catastrophes
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
        case "The Bilbies":
            n = sum(traits_df.loc[t].dominant == 1
                    for t in trait_pile)

            if n == 0:
                points = 10
            elif n == 1:
                points = 4

        case "The Cabochon":
            n = sum('red' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n == 0:
                points = 6
            elif n <= 2:
                points = 3

        case "The Cosmic Jinx":
            if genes <= 2:
                points = 8
            elif genes == 3:
                points = 4

        case "The Dancer":
            n = [i['face'].get() + i['drops'].get() + i['worlds_end'].get()
                 for i in plr['points']]

            if n[p] == min(n):
                if len(set(n)) == len(n):
                    points = 12
                else:
                    points = 8

        case "The Fellmonger":
            n = sum('blue' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n == 0:
                points = 6
            elif n <= 2:
                points = 3

        case "The Jellyfish":
            n = sum('blue' in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist())

            if n >= 6:
                points = 6
            elif n >= 3:
                points = 3

        case "The Logician":
            n = sum(status_df.iloc[t].effectless == 1
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

        case "The Tigris":
            n = sum(traits_df.loc[t].action == 1
                    for t in trait_pile)

            if n >= 6:
                points = 6
            elif n >= 3:
                points = 3

        case "The Vagrant":
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

        case _:
            points = 0

    return points
