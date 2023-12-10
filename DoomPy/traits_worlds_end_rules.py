# get task of this trait to be performed at worlds end
def traits_WE_tasks(traits_df, host):
    # get effect of trait
    rule = traits_df.loc[host].effect_worlds_end

    # update current tasks based on specific rule
    match rule:
        case 'choose_color':
            tasks = ['choose color:', 'blue', 'green', 'purple', 'red']

        case 'is_color_of_choice':
            tasks = ['becomes ...', 'blue', 'green', 'purple', 'red']

        case 'may_change_one_color':
            tasks = ['may change:',
                     'blue -> green', 'blue -> purple', 'blue -> red',
                     'green -> blue', 'green -> purple', 'green -> red',
                     'purple -> blue', 'purple -> green', 'purple -> red',
                     'red -> blue', 'red -> green', 'red -> purple']

        case 'return_upto 3_traits_to_hand':
            tasks = ['how many returned?', '0', '1', '2', '3']

        case 'discard_upto_3_traits':
            tasks = ['how many colors discarded?', '0', '1', '2', '3']

        case 'copy_1st_dominant':
            copied_task = ['!!! needs still to... ', 'be', 'coded']
            tasks = copied_task

    return tasks


# handle worlds end effects of trait
def traits_WE_effects(traits_df, host, trait_pile):
    rule = traits_df.loc[host].effect_worlds_end
    effect = traits_df.loc[host].cur_worlds_end_trait

    match rule:
        case 'is_color_of_choice':
            if effect == 'none':
                traits_df.loc[host, 'cur_color'] = traits_df.loc[host].color
            else:
                traits_df.loc[host, 'cur_color'] = effect

        case 'may_change_one_color':
            if effect != 'none':
                # split rule to define which color will be changed to which other color
                col_from, col_to = effect.split(' -> ')

                # loop trait pile
                for trait in trait_pile:
                    if col_from.lower() in traits_df.loc[trait].cur_color.lower():
                        old_colors = traits_df.loc[trait].cur_color.lower()
                        new_colors = old_colors.replace(col_from, col_to)
                        traits_df.loc[trait, 'cur_color'] = new_colors
