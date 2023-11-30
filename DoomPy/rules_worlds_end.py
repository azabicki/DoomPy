# rules for calculing WORLDS END points
def calculate_worlds_end(worlds_end, p, player_cards, traits):
    cards = player_cards[p].get()

    match worlds_end:
        case "AI Takeover":
            # 2 colorless_worth ignore_colorless_effects
            colors = [traits[traits.name == card]['color'].values[0] for card in cards]
            n_colorless = sum([1 for col in colors if "Colorless" in col])

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
