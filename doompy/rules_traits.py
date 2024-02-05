from globals_ import status_df, traits_df
from log import write_log
import rules_attachment as rules_at
import rules_traits as rules_tr


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

        case 'is_color_of_most_colors':
            options = ['most colors?', 'count them!']

    return options


# handle worlds end effects of trait
def assign_traits_WE_effects(trait_idx, trait_pile):
    colors = ['blue', 'green', 'purple', 'red']
    task = traits_df.loc[trait_idx].worlds_end_task
    traits_WE = status_df.loc[trait_idx].traits_WE

    match task:
        case 'is_color_of_choice':
            # first, clean previous effect from this WE_trait
            prev_WE_effects = status_df.loc[trait_idx].effects_traits_WE
            if str(trait_idx) in prev_WE_effects:
                # reset color to origin
                status_df.loc[trait_idx, 'color'] = traits_df.loc[trait_idx].color

                # reapply attachment, if one attached
                rules_at.apply_effects(trait_idx)

                # and remove effect from List_of_effects
                prev_cleaned = [i for i in prev_WE_effects.split()
                                if str(trait_idx) not in i]
                status_df.loc[trait_idx, 'effects_traits_WE'] = (' ' .join(prev_cleaned)
                                                                 if prev_cleaned != []
                                                                 else 'none')
            # secondly, apply current selection
            if traits_WE != 'none':
                # add effect to status_df
                prev_WE_effect = status_df.loc[trait_idx].effects_traits_WE
                if prev_WE_effect == 'none':
                    status_df.loc[trait_idx, 'effects_traits_WE'] = str(trait_idx) + ':' + traits_WE
                else:
                    new_effect = [str(trait_idx) + ':' + traits_WE
                                  if str(trait_idx) in i else i
                                  for i in prev_WE_effect.split()]
                    status_df.loc[trait_idx, 'effects_traits_WE'] = ' ' .join(new_effect)
            else:
                status_df.loc[trait_idx, 'effects_traits_WE'] = traits_WE

        case 'may_change_color':
            # loop trait pile
            for tp_trait in trait_pile:
                # first, clean previous effect from this WE_trait
                prev_WE_effects = status_df.loc[tp_trait].effects_traits_WE
                if str(trait_idx) in prev_WE_effects:
                    # reset color to origin
                    status_df.loc[tp_trait, 'color'] = traits_df.loc[tp_trait].color

                    # reapply attachment, if one attached
                    rules_at.apply_effects(tp_trait)

                    # and remove effect from List_of_effects
                    prev_cleaned = [i for i in prev_WE_effects.split()
                                    if str(trait_idx) not in i]
                    status_df.loc[tp_trait, 'effects_traits_WE'] = (' ' .join(prev_cleaned)
                                                                    if prev_cleaned != []
                                                                    else 'none')

                # second, check if new effect selected
                if traits_WE != 'none':
                    # split effect to define which color will be changed to which other color
                    col_from = traits_WE.split(' -> ')[0]

                    # if color in trait, assign new effect to correct traits
                    if col_from.lower() in status_df.loc[tp_trait].color.lower():
                        # skip, if trait itself has a "is_color*" WE_task -> they should not interfere
                        if (isinstance(traits_df.loc[tp_trait].worlds_end_task, str)
                                and 'is_color' in traits_df.loc[tp_trait].worlds_end_task):
                            continue

                        # delete spaces
                        effect = traits_WE.replace(" ", "")

                        # add effect to status_df, or replace previous one
                        prev_WE_effects = status_df.loc[tp_trait].effects_traits_WE
                        if prev_WE_effects == 'none':
                            status_df.loc[tp_trait, 'effects_traits_WE'] = str(trait_idx) + ':' + effect
                        else:
                            new_effect = [str(trait_idx) + ':' + effect
                                          if str(trait_idx) in i else i
                                          for i in prev_WE_effects.split()]
                            status_df.loc[tp_trait, 'effects_traits_WE'] = ' ' .join(new_effect)
                else:
                    status_df.loc[trait_idx, 'effects_traits_WE'] = traits_WE

        case 'is_color_of_most_colors':
            # first, clean previous effect from this WE_trait
            prev_WE_effects = status_df.loc[trait_idx].effects_traits_WE
            if str(trait_idx) in prev_WE_effects:
                # reset color to origin
                status_df.loc[trait_idx, 'color'] = traits_df.loc[trait_idx].color

                # reapply attachment, if one attached
                rules_at.apply_effects(trait_idx)

                # and remove effect from List_of_effects
                prev_cleaned = [i for i in prev_WE_effects.split()
                                if str(trait_idx) not in i]
                status_df.loc[trait_idx, 'effects_traits_WE'] = (' ' .join(prev_cleaned)
                                                                 if prev_cleaned != []
                                                                 else 'none')

            # secondly, apply current selection
            if traits_WE != 'none':
                # calculate amount of each color, but do so AFTER attachment-effects and BEFORE
                # worlds-end-effects (like 'Faith') !!!
                n_cols = [0, 0, 0, 0]
                for tp_trait in trait_pile:
                    # reset color to origin
                    status_df.loc[tp_trait, 'color'] = traits_df.loc[tp_trait].color
                    # reapply attachment, if one attached
                    rules_at.apply_effects(tp_trait)
                    # loop colors and add to counter if color==col
                    for icol, col in enumerate(colors):
                        if col in status_df.iloc[tp_trait].color.lower():
                            n_cols[icol] += 1
                    # reapply traits_WE_effects, if affected
                    rules_tr.apply_traits_WE_effects(tp_trait)

                # set color according to rule
                if sum(i == max(n_cols) for i in n_cols) > 1:
                    effect = 'Colorless'
                else:
                    mx_idx = max(n_cols)
                    effect = colors[n_cols.index(mx_idx)]

                # add effect to status_df
                prev_WE_effect = status_df.loc[trait_idx].effects_traits_WE
                if prev_WE_effect == 'none':
                    status_df.loc[trait_idx, 'effects_traits_WE'] = str(trait_idx) + ':' + effect
                else:
                    new_effect = [str(trait_idx) + ':' + effect
                                  if str(trait_idx) in i else i
                                  for i in prev_WE_effect.split()]
                    status_df.loc[trait_idx, 'effects_traits_WE'] = ' ' .join(new_effect)
            else:
                status_df.loc[trait_idx, 'effects_traits_WE'] = traits_WE


# apply effects to host
def apply_traits_WE_effects(host, *args):
    log = False if args == () else args[1]

    # apply effect(s) only if there is one assigned
    if status_df.loc[host].effects_traits_WE != 'none':
        # get previously stored trait_WE effect(s)
        effects = status_df.loc[host].effects_traits_WE.split()

        # apply effect(s)
        for effect in effects:
            # change color
            if '->' in effect:
                # extract colors
                col_from, col_to = effect.split(':')[1].split('->')

                # replace color
                old_colors = status_df.loc[host].color.lower()
                new_colors = old_colors.replace(col_from, col_to)

                # save new colors to status_df
                status_df.loc[host, 'color'] = new_colors

            # update various status variables
            if ':' in effect:
                real_effect = effect.split(':')[1]

                match real_effect.lower():
                    case 'blue':
                        status_df.loc[host, 'color'] = 'blue'

                    case 'green':
                        status_df.loc[host, 'color'] = 'green'

                    case 'purple':
                        status_df.loc[host, 'color'] = 'purple'

                    case 'red':
                        status_df.loc[host, 'color'] = 'red'

                    case 'colorless':
                        status_df.loc[host, 'color'] = 'colorless'

                    case 'Inactive':
                        status_df.loc[host, 'inactive'] = True

                    case 'NoRemove':
                        status_df.loc[host, 'no_remove'] = True

                    case 'NoDiscard':
                        status_df.loc[host, 'no_discard'] = True

                    case 'NoSwap':
                        status_df.loc[host, 'no_swap'] = True

                    case 'NoSteal':
                        status_df.loc[host, 'no_steal'] = True

            # log
            if log:
                write_log(['update_trait_status', 'traits_WE'],
                          traits_df.loc[host].trait, traits_df.loc[effect.split(':')[0]].trait)


# handle worlds end effects of trait
def permanent_effects(tp):
    for trait_idx in tp:
        trait = status_df.loc[trait_idx].trait

        match trait:
            case 'Ironwood':
                # -> protect green if <= 5 (excl. dominants) in trait pile
                # previous effect
                prev_effects = status_df.loc[trait_idx].effects

                # how many green (wo dominants) traits in pile?
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

                    # log
                    write_log(['*'], ">>> trait pile <<< '{}' (id:{}) is protecting {} green trait(s)"
                              .format(trait, trait_idx, len(new_effects)))
                else:
                    # if protected previously, but now >=5 green traits, remove protection
                    if prev_effects != 'none':
                        protected = [int(i) for i in prev_effects.split()]
                        for t in protected:
                            status_df.loc[t, 'no_remove'] = False

                        # log
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

                    # log
                    write_log(['*'], ">>> trait pile <<< '{}' (id:{}) is protecting {} red trait(s)"
                              .format(trait, trait_idx, len(new_effects)))
                else:
                    # if protected previously, but now >=3 red traits, remove protection
                    if prev_effects != 'none':
                        protected = [int(i) for i in prev_effects.split()]
                        for t in protected:
                            status_df.loc[t, 'no_remove'] = False

                        # log
                        write_log(['*'], ">>> trait pile <<< '{}' (id:{}) does not protect anymore"
                                  .format(trait, trait_idx))

                    # reset Meek's effect if no red trait is protected (anymore)
                    status_df.loc[trait_idx, 'effects'] = 'none'
