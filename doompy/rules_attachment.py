from globals_ import traits_df, status_df, plr
from log import write_log


# filter which traits from trait pile are available for the attachment to be attached to
def filter_attachables(attachment: str, p: int) -> list:
    attachable = plr["trait_pile"][p]

    # get attachment-rule of attachment
    rule = traits_df.loc[attachment].attachment_target

    # filter out all attachments, dominants & traits-with-attachments
    attachable = [
        idx
        for idx in attachable
        if traits_df.loc[idx].trait
        not in traits_df[traits_df.attachment == 1].trait.values.tolist()
        and traits_df.loc[idx].trait
        not in traits_df[traits_df.dominant == 1].trait.values.tolist()
        and (
            status_df.loc[idx].attachment == "none"
            or status_df.loc[idx].attachment == attachment
        )
    ]

    # filter out based on specific rules
    match rule:
        case "negative_face":
            attachable = [
                idx
                for idx in attachable
                if (
                    not isinstance(status_df.loc[idx].face, str)
                    and traits_df.loc[idx].face < 0
                )
            ]

        case "non_blue":
            attachable = [
                idx
                for idx in attachable
                if "blue" != traits_df.loc[idx].color.lower()
            ]

        case "non_green":
            attachable = [
                idx
                for idx in attachable
                if "green" != traits_df.loc[idx].color.lower()
            ]

        case "non_purple":
            attachable = [
                idx
                for idx in attachable
                if "purple" != traits_df.loc[idx].color.lower()
            ]

        case "non_red":
            attachable = [
                idx
                for idx in attachable
                if "red" != traits_df.loc[idx].color.lower()
            ]

        case "color":
            attachable = [
                idx
                for idx in attachable
                if "colorless" != traits_df.loc[idx].color.lower()
            ]

        case "effectless":
            attachable = [
                idx for idx in attachable if traits_df.loc[idx].effectless == 1
            ]

    return attachable


# apply effects to host
def apply_effects(host: str) -> None:
    # get attachment
    attachment = status_df.loc[host].attachment

    # apply effect(s) only if there is an attachment
    if attachment != "none":
        # get previously stored attachment effects
        effects = traits_df.loc[attachment].attachment_effect.split()

        # apply effect(s)
        for effect in effects:
            match effect:
                case "IsBlue":
                    status_df.loc[host, "color"] = "Blue"

                case "IsGreen":
                    status_df.loc[host, "color"] = "Green"

                case "IsRed":
                    status_df.loc[host, "color"] = "Red"

                case "IsPurple":
                    status_df.loc[host, "color"] = "Purple"

                case "IsColorless":
                    status_df.loc[host, "color"] = "Colorless"

                case "Inactive":
                    status_df.loc[host, "inactive"] = True

                case "NoRemove":
                    status_df.loc[host, "no_remove"] = True

                case "NoDiscard":
                    status_df.loc[host, "no_discard"] = True

                case "NoSwap":
                    status_df.loc[host, "no_swap"] = True

                case "NoSteal":
                    status_df.loc[host, "no_steal"] = True

        # log
        write_log(
            ["update_trait_status", "attachment"],
            traits_df.loc[host].trait,
            host,
            traits_df.loc[attachment].trait,
            attachment,
        )
