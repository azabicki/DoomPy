# rules for filtering attachable traits depending on trait_pile and attachment
def filter_attachables(traits_df, traits_filtered, attachment):
    # get attachment-rule of attachment
    rule = traits_df[traits_df.name == attachment].effect_attachment.values[0].split()

    # filter out all attachments, dominants & traits-with-attachments
    traits_filtered = [card for card in traits_filtered
                       if card not in traits_df[traits_df.attachment == 1].name.values.tolist()
                       and card not in traits_df[traits_df.dominant == 1].name.values.tolist()
                       and (traits_df[traits_df.name == card].cur_attachment.values[0] == 'none'
                            or traits_df[traits_df.name == card].cur_attachment.values[0] == attachment)]

    # filter out based on specific rules
    match rule[0]:
        case 'negative_face':
            traits_filtered = [card for card in traits_filtered
                               if traits_df[traits_df.name == card].face.values[0] < 0]

        case 'non_blue':
            traits_filtered = [card for card in traits_filtered
                               if 'blue' not in traits_df[traits_df.name == card].color.values[0].lower()]

        case 'non_green':
            traits_filtered = [card for card in traits_filtered
                               if 'green' not in traits_df[traits_df.name == card].color.values[0].lower()]

        case 'color':
            traits_filtered = [card for card in traits_filtered
                               if 'colorless' not in traits_df[traits_df.name == card].color.values[0].lower()]

        case 'effectless':
            traits_filtered = [card for card in traits_filtered
                               if traits_df[traits_df.name == card].effectless.values[0] == 1]

    return traits_filtered


def attachment_effects(traits_df, host, attachment):
    # get current effects of host
    effects = {'color':  traits_df[traits_df.name == host].cur_color.values[0],
               'face':   traits_df[traits_df.name == host].cur_face.values[0],
               'effect': traits_df[traits_df.name == host].cur_effect.values[0]}

    # get effect of attachment
    rule = traits_df[traits_df.name == attachment].effect_attachment.values[0].split()

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


def worlds_end(worlds_end, p, player_cards, traits):
    cards = player_cards[p].get()

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
