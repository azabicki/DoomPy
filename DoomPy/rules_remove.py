from globals_ import status_df


def check_trait(trait_idx, from_, where_to):
    # get trait name
    trait = status_df.loc[trait_idx].trait

    # match trait
    match trait:
        case 'Spores':
            # save player id for every time, spores is discarded! this string, which becomes longer
            # every time spores is discarded, is checked during update_genes()
            if not status_df.loc[trait_idx].inactive and where_to == 'discard':
                cur_effects = status_df.loc[trait_idx].effects
                if cur_effects == 'none':
                    new_effects = str(from_)
                else:
                    new_effects = cur_effects + '_' + str(from_)

                # update cur_effect
                status_df.loc[trait_idx, 'effects'] = new_effects

            return 'keep_trait_effect'

        case _:
            return None
