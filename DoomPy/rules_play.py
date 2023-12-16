from globals_ import traits_df, plr
from log import write_log


def check_requirement(trait_idx, p):
    # returns 'True' if playing trait should be aborted for any trait-specific reason
    trait = traits_df.loc[trait_idx].trait
    tp = plr['trait_pile'][p]

    # if EPIC is already in trait pile -> no more dominat
    Epic_idx = traits_df.index[traits_df.trait == 'Epic'].tolist()[0]
    if traits_df.loc[trait_idx].dominant == 1 and Epic_idx in tp:
        write_log(['*'],
                  '>>> play <<< ERROR - EPIC already in trait pile - no more dominants allowed')
        return True

    # check individual traits
    match trait:
        case 'Epic':
            # return, if there is another dominant in trait pile
            if sum([1 for t in tp if traits_df.loc[t].dominant == 1]) == 1:
                write_log(['*'],
                          '>>> play <<< ERROR - already 1 dominant in trait pile - EPIC not allowed')
                return True

        case 'Opposable Thumbs':
            # return, if there is another dominant in trait pile
            if sum([1 for t in tp if traits_df.loc[t].dominant == 1]) == 0:
                write_log(['*'],
                          '>>> play <<< ERROR - no dominant in trait pile - OPPOSABLE THUMBS not allowed')
                return True
