from globals_ import status_df, traits_df


# get task of this trait to be performed at worlds end
def traits_WE_tasks(host):
    # get effect of trait
    task = traits_df.iloc[host].worlds_end_task

    # based on specific task, update current options for drop down menu
    match task:
        case 'choose_color':
            options = ['choose color:', 'blue', 'green', 'purple', 'red']

        case 'is_color_of_choice':
            options = ['becomes ...', 'blue', 'green', 'purple', 'red']

        case 'may_change_one_color':
            options = ['may change:',
                       'blue -> green', 'blue -> purple', 'blue -> red',
                       'green -> blue', 'green -> purple', 'green -> red',
                       'purple -> blue', 'purple -> green', 'purple -> red',
                       'red -> blue', 'red -> green', 'red -> purple']

        case 'return_upto_3_traits_to_hand':
            options = ['#traits returned?', '0', '1', '2', '3']

        case 'discard_upto_3_traits':
            options = ['#colors discarded?', '0', '1', '2', '3']

        case 'copy_1st_dominant':
            copied_task = ['!!! needs still to... ', 'be', 'coded']
            options = copied_task

    return options


# handle worlds end effects of trait
def traits_WE_effects(host, trait_pile):
    task = traits_df.loc[host].worlds_end_task
    effect = status_df.loc[host].traits_WE

    match task:
        case 'is_color_of_choice':
            if effect == 'none':
                status_df.loc[host, 'color'] = traits_df.loc[host].color
            else:
                status_df.loc[host, 'color'] = effect

        case 'may_change_one_color':
            if effect != 'none':
                # split rule to define which color will be changed to which other color
                col_from, col_to = effect.split(' -> ')

                # loop trait pile
                for trait in trait_pile:
                    if col_from.lower() in status_df.loc[trait].color.lower():
                        old_colors = status_df.loc[trait].color.lower()
                        new_colors = old_colors.replace(col_from, col_to)
                        status_df.loc[trait, 'color'] = new_colors
