from globals_ import status_df, traits_df, plr, sim_running, cfg
from log import write_log
import tkinter as tk


def is_heroic_born(trait_idx: int) -> None:
    def response(response: str, trait_idx: int) -> None:
        status_df.loc[trait_idx, "effects"] = True if response == "yes" else False
        top.destroy()

    top = tk.Toplevel(width=500, height=75)
    top.title("Birth of a Hero")

    msg1 = tk.Label(top, text="HEROIC", font='"" 28 bold', fg=cfg["color_green"])
    msg1.grid(row=0, column=0, columnspan=2, padx=10, sticky="nesw")
    msg2 = tk.Label(top, text='born during\n"Birth of a Hero" ???', font='"" 20 bold')
    msg2.grid(row=1, column=0, columnspan=2, padx=10, sticky="nesw")

    no = tk.Button(
        top,
        text="no, he isn't.\njust a regular birth.",
        command=lambda: response("no", trait_idx),
    )
    no.grid(row=2, column=0, padx=10, pady=10, sticky="nesw")
    yes = tk.Button(
        top, text="Hell Yeah, he is!!", command=lambda: response("yes", trait_idx)
    )
    yes.grid(row=2, column=1, padx=10, pady=10, sticky="nesw")

    top.focus()
    top.grab_set()
    top.wait_window()


def check_requirement(trait_idx: int, p: int) -> bool:
    # returns 'True' if playing trait should be aborted for any trait-specific reason
    # colors = ['blue', 'green', 'purple', 'red']
    trait = traits_df.loc[trait_idx].trait
    tp = plr["trait_pile"][p]

    # if EPIC is already in trait pile -> no more dominant
    Epic_idx = traits_df.index[traits_df.trait == "Epic"].tolist()
    if Epic_idx != [] and traits_df.loc[trait_idx].dominant == 1 and Epic_idx[0] in tp:
        write_log(
            ["*"],
            ">>> play <<< ERROR - EPIC already in trait pile - no more dominants allowed",
        )
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
                write_log(
                    ["*"],
                    ">>> play <<< ERROR - for CARNOSAUR JAW to play, 2 or more red traits in trait pile needed",
                )
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
                write_log(
                    ["*"],
                    ">>> play <<< ERROR - for CITRUS to play, a trait with a negative face value needed",
                )
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
                write_log(
                    ["*"],
                    ">>> play <<< ERROR - for DELICIOUS to play, 1 or more colorless traits in trait pile needed",
                )
                return True

        case "Epic":
            # return, if there is another dominant in trait pile
            if sum([1 for t in tp if traits_df.loc[t].dominant == 1]) == 1:
                write_log(
                    ["*"],
                    ">>> play <<< ERROR - already 1 dominant in trait pile - EPIC not allowed",
                )
                return True

        case "Fronds":
            # return, if there are no traits in trait pile
            if len(tp) == 0:
                write_log(
                    ["*"],
                    ">>> play <<< ERROR - for FRONDS JAW to play, at least one trait in trait pile needed",
                )
                return True

        case "Heroic":
            # first, ask if HEROIC is born during 'Birth of a Hero'
            if not sim_running:
                is_heroic_born(trait_idx)
            else:
                status_df.loc[trait_idx, "effects"] = True
            is_born = status_df.loc[trait_idx, "effects"]

            # if not born during that age, check if there are less than 3 green traits in trait pile
            if is_born:
                write_log(
                    ["*"],
                    ">>> play <<< 'HEROIC' is born during 'Birth of a Hero' and ignores restrictions",
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
                    write_log(
                        ["*"],
                        ">>> play <<< ERROR - for HEROIC to play, 3 or more green traits in trait pile needed",
                    )
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
                write_log(
                    ["*"],
                    ">>> play <<< ERROR - for METAMORPHOSIS to play, 3 or more traits with face value 1 or higher in trait pile needed",
                )  # noqa: E501
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
                write_log(
                    ["*"],
                    ">>> play <<< ERROR - for MORALITY to play, a trait with a positive face value needed",
                )
                return True

        case "Opposable Thumbs":
            # return, if there is another dominant in trait pile
            if sum([1 for t in tp if traits_df.loc[t].dominant == 1]) == 0:
                write_log(
                    ["*"],
                    ">>> play <<< ERROR - no dominant in trait pile - OPPOSABLE THUMBS not allowed",
                )
                return True

        case "Retractable Claws":
            # return, if no red trait in trait pile
            if (
                sum(
                    "red" in color.lower() for color in status_df.loc[tp].color.tolist()
                )
                == 0
            ):
                write_log(
                    ["*"],
                    ">>> play <<< ERROR - to play RETRACTABLE CLAWS, you need at least one red trait in trait pile",
                )  # noqa: E501
                return True

        case "Silk":
            # return, if gene pool > 4
            if plr["genes"][p].get() > 4:
                write_log(
                    ["*"],
                    ">>> play <<< ERROR - to play SILK, gene pool must be 4 or lower",
                )
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
                write_log(
                    ["*"],
                    ">>> play <<< ERROR - to play XYLOPHAGE, you need at least one green trait in trait pile",
                )
                return True


def play_effect(trait_idx: int, p: int) -> None:
    # perform trait specific actions when played
    trait = traits_df.loc[trait_idx].trait
    tp = plr["trait_pile"][p]

    match trait:
        case "Opposable Thumbs":
            # copy first dominant
            first_D = [i for i in tp if traits_df.loc[i].dominant.tolist() == 1]

            traits_df.loc[trait_idx, "color"] = traits_df.loc[
                first_D, "color"
            ].values[0]
            traits_df.loc[trait_idx, "face"] = traits_df.loc[
                first_D, "face"
            ].values[0]
            traits_df.loc[trait_idx, "action"] = traits_df.loc[
                first_D, "action"
            ].values[0]
            traits_df.loc[trait_idx, "drops"] = traits_df.loc[
                first_D, "drops"
            ].values[0]
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

            status_df.loc[trait_idx, "color"] = status_df.loc[
                first_D, "color"
            ].values[0]
            status_df.loc[trait_idx, "face"] = status_df.loc[
                first_D, "face"
            ].values[0]

            write_log(
                ["*"],
                ">>> play <<< OPPOSABLE THUMBS is now a copy of {}".format(
                    traits_df.loc[first_D].trait.values[0].upper()
                ),
            )
