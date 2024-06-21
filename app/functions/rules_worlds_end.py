import streamlit as st


# apply specific WE effects to status of traits
def apply_WE_effects(host: str) -> None:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]

    # switch for log
    log = False

    match st.session_state.worlds_end["played"]:
        case "AI Takeover":
            # 2 colorless_worth ignore_colorless_effects
            #   --> change cur_face + cur_effect
            if "colorless" in status_df.loc[host].color.lower():
                status_df.loc[host, "face"] = 2
                status_df.loc[host, "inactive"] = True
                status_df.loc[host, "effects_WE"] = "Face Inactive"
                log = True

        case "AI Takeover (excl. dominant)":
            # 2 colorless_worth ignore_colorless_effects noDominant
            #   --> change cur_face + cur_effect
            if (
                "colorless" in status_df.loc[host].color.lower()
                and traits_df.loc[host].dominant != 1
            ):
                status_df.loc[host, "face"] = 2
                status_df.loc[host, "inactive"] = True
                status_df.loc[host, "effects_WE"] = "Face Inactive"
                log = True

    # log
    if log:
        print(
            ["update_trait_status", "WE_effect"],
            traits_df.loc[host].trait,
            host,
            st.session_state.worlds_end["played"],
        )


# handle worlds end effect of catastrophes
def calc_WE_points(p: int) -> int:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr

    # init variable
    colors = ["blue", "green", "purple", "red"]
    trait_pile = plr["trait_pile"][p]
    genes = plr["genes"][p]
    points = 0

    match st.session_state.worlds_end["played"]:
        case "Algal Superbloom":
            # 1 each_blue_in_left_trait_pile
            traits_left = (
                plr["trait_pile"][p + 1]
                if p + 1 < len(plr["trait_pile"])
                else plr["trait_pile"][0]
            )
            points = sum(
                "blue" in color.lower()
                for color in status_df.iloc[traits_left].color.tolist()
            )

        case "Ancient Corruption":
            # -1 each_action
            points = -1 * sum(traits_df.loc[trait].action == 1 for trait in trait_pile)

        case "Ashlands":
            # -4 if_<=2_purple_traits
            if (
                sum(
                    "purple" in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist()
                )
                <= 2
            ):
                points = -4

        case "Choking Vines":
            # 1 each_green_in_left_trait_pile
            traits_left = (
                plr["trait_pile"][p + 1]
                if p + 1 < len(plr["trait_pile"])
                else plr["trait_pile"][0]
            )
            points = sum(
                "green" in color.lower()
                for color in status_df.iloc[traits_left].color.tolist()
            )

        case "Deus Ex Machina":
            # draw_card_add_face_value
            points = int(plr["points_WE_effect"][p])

        case "Deus Ex Machina (max.5)":
            # draw_card_add_face_value_max.5
            points = int(plr["points_WE_effect"][p])

        case "Ecological Collapse":
            # +2 each_negative_face
            points = (
                sum(
                    status_df.loc[trait].face < 0
                    for trait in trait_pile
                    if not isinstance(status_df.loc[trait].face, str)
                )
                * 2
            )

        case "Endless Monsoon":
            # -1 hand
            points = int(plr["points_WE_effect"][p])

        case "Great Deluge":
            # -4 if_<=2_blue_traits
            if (
                sum(
                    "blue" in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist()
                )
                <= 2
            ):
                points = -4

        case "Grey Goo":
            # -5 most_traits
            n = [len(tp) for tp in plr["trait_pile"]]
            if len(trait_pile) == max(n):
                points = -5

        case "Ice Age":
            # -1 each_red
            points = -1 * sum(
                "red" in status_df.loc[trait].color.lower() for trait in trait_pile
            )

        case "Impact Event":
            # -1 each_trait_>=3_face
            points = -1 * sum(
                status_df.loc[trait].face >= 3
                for trait in trait_pile
                if not isinstance(status_df.loc[trait].face, str)
            )

        case "Invasive Species":
            # add_max7_face_from_hand
            points = int(plr["points_WE_effect"][p])

        case "Jungle Rot":
            # -4 if_<=2_green_traits
            if (
                sum(
                    "green" in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist()
                )
                <= 2
            ):
                points = -4

        case "Overpopulation":
            # +4 if fewest_traits
            n = [len(tp) for tp in plr["trait_pile"]]
            if len(trait_pile) == min(n):
                points = 4

        case "Planetary Deforestation":
            # -gene_pool
            points = -1 * genes

        case "Retrovirus":
            # -1 each_green
            points = -1 * sum(
                "green" in status_df.loc[trait].color.lower() for trait in trait_pile
            )

        case "Sacrifice":
            # -4 if_<=2_red_traits
            if (
                sum(
                    "red" in color.lower()
                    for color in status_df.iloc[trait_pile].color.tolist()
                )
                <= 2
            ):
                points = -4

        case "Solar Flare":
            # -1 each_purple
            points = -1 * sum(
                "purple" in status_df.loc[trait].color.lower() for trait in trait_pile
            )

        case "Strange Matter":
            # -2 each_drop
            points = -2 * sum(traits_df.loc[trait].drops == 1 for trait in trait_pile)

        case "Super Volcano":
            # -1 each_blue
            points = -1 * sum(
                "blue" in status_df.loc[trait].color.lower() for trait in trait_pile
            )

        case "The Big One":
            # -2 per_each_missing_color
            ncol = []
            for col in colors:
                ncol.append(
                    all(
                        [
                            col not in status_df.loc[trait].color.lower()
                            for trait in trait_pile
                        ]
                    )
                )
            points = -2 * sum(ncol)

        case "Tropical Superstorm":
            # 1 each_purple_in_left_trait_pile
            traits_left = (
                plr["trait_pile"][p + 1]
                if p + 1 < len(plr["trait_pile"])
                else plr["trait_pile"][0]
            )
            points = sum(
                "purple" in color.lower()
                for color in status_df.iloc[traits_left].color.tolist()
            )

        case "Volcanic Winter":
            # 1 each_red_in_left_trait_pile
            traits_left = (
                plr["trait_pile"][p + 1]
                if p + 1 < len(plr["trait_pile"])
                else plr["trait_pile"][0]
            )
            points = sum(
                "red" in color.lower()
                for color in status_df.iloc[traits_left].color.tolist()
            )

        case _:
            points = 0

    return points
