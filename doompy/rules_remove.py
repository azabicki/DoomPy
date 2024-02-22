from globals_ import status_df
from log import write_log


def check_trait(trait_idx: int, from_: int, where_to: str) -> str | None:
    # get trait name
    trait = status_df.loc[trait_idx].trait

    # match trait
    match trait:
        case 'Ironwood':
            # take away protection from traits which were protected by Ironwood
            cur_effects = status_df.loc[trait_idx].effects
            if cur_effects != 'none':
                protected = [int(i) for i in cur_effects.split()]
                for t in protected:
                    status_df.loc[t, 'no_remove'] = False

                write_log(['*'], ">>> trait pile <<< '{}' (id:{}) does not protect anymore"
                          .format(trait, trait_idx))
            return None

        case 'Meek':
            # take away protection from traits which were protected by Meek
            cur_effects = status_df.loc[trait_idx].effects
            if cur_effects != 'none':
                protected = [int(i) for i in cur_effects.split()]
                for t in protected:
                    status_df.loc[t, 'no_remove'] = False

                write_log(['*'], ">>> trait pile <<< '{}' (id:{}) does not protect anymore"
                          .format(trait, trait_idx))
            return None

        case 'Spores':
            # save player id for each time spores is discarded! this string, which becomes longer
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
