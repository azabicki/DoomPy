from globals_ import traits_df, plr


# filter which traits from trait pile are available for the attacahment to be attached to
def filter_attachables(attachment, p):
    attachable = plr['trait_pile'][p]

    # get attachment-rule of attachment
    rule = traits_df.loc[attachment].effect_attachment.split()

    # filter out all attachments, dominants & traits-with-attachments
    attachable = [idx for idx in attachable
                  if traits_df.loc[idx].trait not in traits_df[traits_df.attachment == 1].trait.values.tolist()
                  and traits_df.loc[idx].trait not in traits_df[traits_df.dominant == 1].trait.values.tolist()
                  and (traits_df.loc[idx].cur_attachment == 'none'
                       or traits_df.loc[idx].cur_attachment == attachment)]

    # filter out based on specific rules
    match rule[0]:
        case 'negative_face':
            attachable = [idx for idx in attachable 
                          if traits_df.loc[idx].face < 0]

        case 'non_blue':
            attachable = [idx for idx in attachable
                          if 'blue' not in traits_df.loc[idx].color.lower()]

        case 'non_green':
            attachable = [idx for idx in attachable
                          if 'green' not in traits_df.loc[idx].color.lower()]

        case 'color':
            attachable = [idx for idx in attachable
                          if 'colorless' not in traits_df.loc[idx].color.lower()]

        case 'effectless':
            attachable = [idx for idx in attachable
                          if traits_df.loc[idx].effectless == 1]

    return attachable


# handling effects of attachments when attached to a host
def attachment_effects(host, attachment):
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
