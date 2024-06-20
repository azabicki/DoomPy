import streamlit as st


def check_requirement(trait_idx: int, p: int) -> bool:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr

    # returns 'True' if playing trait should be aborted for any trait-specific reason
    # colors = ['blue', 'green', 'purple', 'red']
    trait = traits_df.loc[trait_idx].trait
    tp = plr["trait_pile"][p]

    # if EPIC is already in trait pile -> no more dominant
    Epic_idx = traits_df.index[traits_df.trait == "Epic"].tolist()
    if Epic_idx != [] and traits_df.loc[trait_idx].dominant == 1 and Epic_idx[0] in tp:
        print(">>> play <<< ERROR - EPIC in trait pile - no more dominants allowed")
        return True

    # check individual traits
    match trait:
        case "Carnosaur Jaw":
            # return, if there are less than 2 red traits in trait pile
            if (
                sum(
                    [
                        "red" in color.lower()
                        for color in status_df.loc[tp].color.tolist()
                    ]
                )
                < 2
            ):
                print(">>> play <<< ERROR - CARNOSAUR JAW")
                return True

        case "Citrus":
            # return, if there are no negative face value traits in trait pile
            if (
                sum(
                    face < 0
                    for face in status_df.loc[tp].face.tolist()
                    if not isinstance(face, str)
                )
                == 0
            ):
                print(">>> play <<< ERROR - CITRUS")
                return True

        case "Delicious":
            # return, if there are no colorless traits in trait pile
            if (
                sum(
                    [
                        "colorless" in color.lower()
                        for color in status_df.loc[tp].color.tolist()
                    ]
                )
                == 0
            ):
                print(">>> play <<< ERROR - DELICIOUS")
                return True

        case "Epic":
            # return, if there is another dominant in trait pile
            if sum([1 for t in tp if traits_df.loc[t].dominant == 1]) == 1:
                print(">>> play <<< ERROR - EPIC not allowed")
                return True

        case "Fronds":
            # return, if there are no traits in trait pile
            if len(tp) == 0:
                print(">>> play <<< ERROR - FRONDS")
                return True

        case "Heroic":
            # allow heroic always to be played -> do not knwo how to actually code this
            status_df.loc[trait_idx, "effects"] = True

            # if not born during that age, check if there are less than 3 green traits in trait pile
            if status_df.loc[trait_idx, "effects"]:
                print(
                    ">>> play <<< 'HEROIC' is born during 'Birth of a Hero'",
                )
            else:
                if (
                    sum(
                        [
                            "green" in color.lower()
                            for color in status_df.loc[tp].color.tolist()
                        ]
                    )
                    < 3
                ):
                    print(">>> play <<< ERROR - HEROIC")
                    return True

        case "Metamorphosis":
            # return, if there are less than 3 traits with face value < 1
            if (
                sum(
                    [
                        face >= 1
                        for face in status_df.loc[tp].face.tolist()
                        if not isinstance(face, str)
                    ]
                )
                < 3
            ):
                print(">>> play <<< ERROR - METAMORPHOSIS")
                return True

        case "Morality":
            # return, if there are no positive face value traits in trait pile
            if (
                sum(
                    face > 0
                    for face in status_df.loc[tp].face.tolist()
                    if not isinstance(face, str)
                )
                == 0
            ):
                print(">>> play <<< ERROR - MORALITY")
                return True

        case "Opposable Thumbs":
            # return, if there is another dominant in trait pile
            if sum([1 for t in tp if traits_df.loc[t].dominant == 1]) == 0:
                print(">>> play <<< ERROR - no dominant in trait pile")
                return True

        case "Retractable Claws":
            # return, if no red trait in trait pile
            if (
                sum(
                    "red" in color.lower() for color in status_df.loc[tp].color.tolist()
                )
                == 0
            ):
                print(">>> play <<< ERROR - RETRACTABLE CLAWS")
                return True

        case "Silk":
            # return, if gene pool > 4
            if plr["genes"][p].get() > 4:
                print(">>> play <<< ERROR - SILK")
                return True

        case "Xylophage":
            # return, if no green trait in trait pile
            if (
                sum(
                    "green" in color.lower()
                    for color in status_df.loc[tp].color.tolist()
                )
                == 0
            ):
                print(">>> play <<< ERROR - XYLOPHAGE")
                return True


def play_effect(trait_idx: int, p: int) -> None:
    # shorten df's
    traits_df = st.session_state.df["traits_df"]
    status_df = st.session_state.df["status_df"]
    plr = st.session_state.plr

    # perform trait specific actions when played
    trait = traits_df.loc[trait_idx].trait
    tp = plr["trait_pile"][p]

    match trait:
        case "Opposable Thumbs":
            # copy first dominant
            first_D = [i for i in tp if traits_df.loc[i].dominant.tolist() == 1]

            traits_df.loc[trait_idx, "color"] = traits_df.loc[first_D, "color"].values[
                0
            ]
            traits_df.loc[trait_idx, "face"] = traits_df.loc[first_D, "face"].values[0]
            traits_df.loc[trait_idx, "action"] = traits_df.loc[
                first_D, "action"
            ].values[0]
            traits_df.loc[trait_idx, "drops"] = traits_df.loc[first_D, "drops"].values[
                0
            ]
            traits_df.loc[trait_idx, "play_when"] = traits_df.loc[
                first_D, "play_when"
            ].values[0]
            traits_df.loc[trait_idx, "gene_pool"] = traits_df.loc[
                first_D, "gene_pool"
            ].values[0]
            traits_df.loc[trait_idx, "worlds_end"] = traits_df.loc[
                first_D, "worlds_end"
            ].values[0]
            traits_df.loc[trait_idx, "effectless"] = traits_df.loc[
                first_D, "effectless"
            ].values[0]
            traits_df.loc[trait_idx, "attachment"] = traits_df.loc[
                first_D, "attachment"
            ].values[0]
            traits_df.loc[trait_idx, "gene_pool_target"] = traits_df.loc[
                first_D, "gene_pool_target"
            ].values[0]
            traits_df.loc[trait_idx, "gene_pool_rule"] = traits_df.loc[
                first_D, "gene_pool_rule"
            ].values[0]
            traits_df.loc[trait_idx, "gene_pool_effect"] = traits_df.loc[
                first_D, "gene_pool_effect"
            ].values[0]
            traits_df.loc[trait_idx, "attachment_target"] = traits_df.loc[
                first_D, "attachment_target"
            ].values[0]
            traits_df.loc[trait_idx, "attachment_effect"] = traits_df.loc[
                first_D, "attachment_effect"
            ].values[0]
            traits_df.loc[trait_idx, "drop_effect"] = traits_df.loc[
                first_D, "drop_effect"
            ].values[0]
            traits_df.loc[trait_idx, "worlds_end_task"] = traits_df.loc[
                first_D, "worlds_end_task"
            ].values[0]
            traits_df.loc[trait_idx, "trait_effect"] = traits_df.loc[
                first_D, "trait_effect"
            ].values[0]
            traits_df.loc[trait_idx, "trait_effect_rule"] = traits_df.loc[
                first_D, "trait_effect_rule"
            ].values[0]

            status_df.loc[trait_idx, "color"] = status_df.loc[first_D, "color"].values[
                0
            ]
            status_df.loc[trait_idx, "face"] = status_df.loc[first_D, "face"].values[0]

            print(
                ">>> play <<< OPPOSABLE THUMBS is now a copy of {}".format(
                    traits_df.loc[first_D].trait.values[0].upper()
                ),
            )
