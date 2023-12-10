def check_trait(traits_df, trait_idx, from_):
    trait = traits_df.loc[trait_idx].trait

    match trait:
        case 'Spores':
            cur_eff = traits_df.loc[trait_idx].cur_effect
            if cur_eff == 'none':
                new_eff = str(from_)
            else:
                new_eff = cur_eff + '_' + str(from_)

            # update cur_effect
            traits_df.loc[trait_idx, "cur_effect"] = new_eff

            return "keep_cur_effect"

        case _:
            return None
