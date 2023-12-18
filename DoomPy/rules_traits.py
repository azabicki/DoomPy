from globals_ import status_df, traits_df
from log import write_log


# get task of this trait to be performed at worlds end
def traits_WE_tasks(trait_idx):
    # get effect of trait
    task = traits_df.iloc[trait_idx].worlds_end_task

    # based on specific task, update current options for drop down menu
    match task:
        case 'choose_color':
            options = ['choose color:', 'blue', 'green', 'purple', 'red']

        case 'is_color_of_choice':
            options = ['becomes ...', 'blue', 'green', 'purple', 'red']

        case 'may_change_color':
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
def traits_WE_effects(trait_idx, trait_pile):
    task = traits_df.loc[trait_idx].worlds_end_task
    effect = status_df.loc[trait_idx].traits_WE

    match task:
        case 'is_color_of_choice':
            if effect == 'none':
                status_df.loc[trait_idx, 'color'] = traits_df.loc[trait_idx].color
            else:
                status_df.loc[trait_idx, 'color'] = effect

        case 'may_change_color':
            if effect != 'none':
                # split rule to define which color will be changed to which other color
                col_from, col_to = effect.split(' -> ')

                # loop trait pile
                for trait in trait_pile:
                    if col_from.lower() in status_df.loc[trait].color.lower():
                        old_colors = status_df.loc[trait].color.lower()
                        new_colors = old_colors.replace(col_from, col_to)
                        status_df.loc[trait, 'color'] = new_colors


# handle worlds end effects of trait
def traits_effects(tp):
    for trait_idx in tp:
        trait = status_df.loc[trait_idx].trait

        match trait:
            case 'Ironwood':
                # -> protect green if <= 5 (excl. dominants) in trait pile
                # previous effect
                prev_effects = status_df.loc[trait_idx].effects

                # how many green (wo dominats) traits in pile?
                n_green = sum('green' in status_df.iloc[t].color.lower()
                              for t in tp
                              if traits_df.iloc[t].dominant != 1)

                # apply protection
                if n_green <= 5:
                    new_effects = []
                    # loop all trait in trait pile
                    for t in tp:
                        # if red & not already no_remove = True
                        if ('green' in status_df.iloc[t].color.lower()
                            and traits_df.iloc[t].dominant != 1
                            and (not status_df.loc[t].no_remove
                                 or str(t) in prev_effects)):
                            status_df.loc[t, 'no_remove'] = True
                            new_effects.append(t)

                    # update status_df
                    status_df.loc[trait_idx, 'effects'] = ' '.join(str(x) for x in new_effects)

                    # print log
                    write_log(['*'], ">>> trait pile <<< '{}' (id:{}) is protecting {} green trait(s)"
                              .format(trait, trait_idx, len(new_effects)))
                else:
                    # if pretected previously, remove protection
                    if prev_effects != 'none':
                        protected = [int(i) for i in prev_effects.split()]
                        for t in protected:
                            status_df.loc[t, 'no_remove'] = False

                        # write log
                        write_log(['*'], ">>> trait pile <<< '{}' (id:{}) does not protect anymore"
                                  .format(trait, trait_idx))

                    # reset Ironwood's effect if no green trait is protected (anymore)
                    status_df.loc[trait_idx, 'effects'] = 'none'

            case 'Meek':
                # -> protect red if <= 3 in trait pile
                # previous effect
                prev_effects = status_df.loc[trait_idx].effects

                # how many red traits in pile?
                n_red = sum('red' in color.lower()
                            for color in status_df.iloc[tp].color.tolist())

                # apply protection
                if n_red <= 3:
                    new_effects = []
                    # loop all trait in trait pile
                    for t in tp:
                        # if red & not already no_remove = True
                        if ('red' in status_df.iloc[t].color.lower()
                                and (not status_df.loc[t].no_remove
                                     or str(t) in prev_effects)):
                            status_df.loc[t, 'no_remove'] = True
                            new_effects.append(t)

                    # update status_df
                    status_df.loc[trait_idx, 'effects'] = ' '.join(str(x) for x in new_effects)

                    # print log
                    write_log(['*'], ">>> trait pile <<< '{}' (id:{}) is protecting {} red trait(s)"
                              .format(trait, trait_idx, len(new_effects)))
                else:
                    # if pretected previously, remove protection
                    if prev_effects != 'none':
                        protected = [int(i) for i in prev_effects.split()]
                        for t in protected:
                            status_df.loc[t, 'no_remove'] = False

                        # write log
                        write_log(['*'], ">>> trait pile <<< '{}' (id:{}) does not protect anymore"
                                  .format(trait, trait_idx))

                    # reset Meek's effect if no red trait is protected (anymore)
                    status_df.loc[trait_idx, 'effects'] = 'none'
