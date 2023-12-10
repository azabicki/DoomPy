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


# handle worlds end effect of catastrophies
def worlds_end(traits_df, we_catastrophe, player_traits, p, genes, player_we_effects):
    # return, if worlds end did not happen yet
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

        case "Deus Ex Machina":
            # draw_card_add_face_value
            points = int(player_we_effects[p].get())

        case "Deus Ex Machina (max.5)":
            # draw_card_add_face_value_max.5
            points = int(player_we_effects[p].get())

        case "Ecological Collapse":
            # +2 each_negative_face
            points = sum(traits_df.loc[trait].cur_face < 0 for trait in traits) * 2

        case "Endless Monsoon":
            # -1 hand
            points = int(player_we_effects[p].get())

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
            points = int(player_we_effects[p].get())

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
