from globals_ import status_df, traits_df, plr
from log import write_log


def check_requirement(trait_idx, p):
    # returns 'True' if playing trait should be aborted for any trait-specific reason
    # colors = ['blue', 'green', 'purple', 'red']
    trait = traits_df.loc[trait_idx].trait
    tp = plr['trait_pile'][p]

    # if EPIC is already in trait pile -> no more dominant
    Epic_idx = traits_df.index[traits_df.trait == 'Epic'].tolist()[0]
    if traits_df.loc[trait_idx].dominant == 1 and Epic_idx in tp:
        write_log(['*'],
                  '>>> play <<< ERROR - EPIC already in trait pile - no more dominants allowed')
        return True

    # check individual traits
    match trait:
        case 'Carnosaur Jaw':
            # return, if there are less than 2 red traits in trait pile
            if sum(['red' in color.lower() for color in status_df.loc[tp].color.tolist()]) < 2:
                write_log(['*'],
                          '>>> play <<< ERROR - for CARNOSAUR JAW to play, 2 or more red traits in trait pile needed')
                return True

        case 'Citrus':
            # return, if there are no negative face value traits in trait pile
            if sum(face < 0
                   for face in status_df.loc[tp].face.tolist()
                   if not isinstance(face, str)) == 0:
                write_log(['*'],
                          '>>> play <<< ERROR - for CITRUS to play, a trait with a negative face value needed')
                return True

        case 'Delicious':
            # return, if there are no colorless traits in trait pile
            if sum(['colorless' in color.lower() for color in status_df.loc[tp].color.tolist()]) == 0:
                write_log(['*'],
                          '>>> play <<< ERROR - for DELICIOUS to play, 1 or more colorless traits in trait pile needed')
                return True

        case 'Epic':
            # return, if there is another dominant in trait pile
            if sum([1 for t in tp if traits_df.loc[t].dominant == 1]) == 1:
                write_log(['*'],
                          '>>> play <<< ERROR - already 1 dominant in trait pile - EPIC not allowed')
                return True

        case 'Fronds':
            # return, if there are no traits in trait pile
            if len(tp) == 0:
                write_log(['*'],
                          '>>> play <<< ERROR - for FRONDS JAW to play, at least one trait in trait pile needed')
                return True

        case 'Heroic':
            # return, if there are less than 3 green traits in trait pile
            if sum(['green' in color.lower() for color in status_df.loc[tp].color.tolist()]) < 3:
                write_log(['*'],
                          '>>> play <<< ERROR - for HEROIC to play, 3 or more green traits in trait pile needed')
                return True

        case 'Metamorphosis':
            # return, if there are less than 3 traits with face value < 1
            if sum([face >= 1
                    for face in status_df.loc[tp].face.tolist()
                    if not isinstance(face, str)]) < 3:
                write_log(['*'],
                          '>>> play <<< ERROR - for METAMORPHOSIS to play, 3 or more traits with face value 1 or higher in trait pile needed')  # noqa: E501
                return True

        case 'Morality':
            # return, if there are no positive face value traits in trait pile
            if sum(face > 0
                   for face in status_df.loc[tp].face.tolist()
                   if not isinstance(face, str)) == 0:
                write_log(['*'],
                          '>>> play <<< ERROR - for MORALITY to play, a trait with a positive face value needed')
                return True

        case 'Opposable Thumbs':
            # return, if there is another dominant in trait pile
            if sum([1 for t in tp if traits_df.loc[t].dominant == 1]) == 0:
                write_log(['*'],
                          '>>> play <<< ERROR - no dominant in trait pile - OPPOSABLE THUMBS not allowed')
                return True

        case 'Retractable Claws':
            # return, if no red trait in trait pile
            if sum('red' in color.lower() for color in status_df.loc[tp].color.tolist()) == 0:
                write_log(['*'],
                          '>>> play <<< ERROR - to play RETRACTABLE CLAWS, you need at least one red trait in trait pile')  # noqa: E501
                return True

        case 'Silk':
            # return, if gene pool > 4
            if plr['genes'][p].get() > 4:
                write_log(['*'],
                          '>>> play <<< ERROR - to play SILK, gene pool must be 4 or lower')
                return True

        case 'Xylophage':
            # return, if no green trait in trait pile
            if sum('green' in color.lower() for color in status_df.loc[tp].color.tolist()) == 0:
                write_log(['*'],
                          '>>> play <<< ERROR - to play XYLOPHAGE, you need at least one green trait in trait pile')
                return True
