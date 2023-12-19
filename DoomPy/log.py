from globals_ import logfile


def write_log(what, *args):
    f = open(logfile['file'], 'a')

    match what[0]:
        case 'init':  # initialize
            match what[1]:
                case 'datetime':
                    print(">>> initialize <<< new game: {}". format(*args))
                    f.write(">>> initialize <<< new game: {}\n".format(*args))

                case 'variables':
                    print(">>> initialize <<< reset variables")
                    f.write(">>> initialize <<< reset variables\n")

                case 'menu':
                    print(">>> initialize <<< create menu")
                    f.write(">>> initialize <<< create menu\n")

                case 'playground':
                    print(">>> initialize <<< create playground")
                    f.write(">>> initialize <<< create playground\n")

                case 'names':
                    print("   >>> name of player #{} = {}"
                          .format(*args))
                    f.write("   >>> name of player #{} = {}\n"
                            .format(*args))

                case 'first_player':
                    print("   >>> '{}' is first player"
                          .format(*args))
                    f.write("   >>> '{}' is first player\n"
                            .format(*args))

        case 'select':
            match what[1]:
                case 'deck':
                    print(">>> select <<< handle DECK_listbox -> selected trait = '{}' (id:{})"
                          .format(*args))
                    f.write(">>> select <<< handle DECK_listbox -> selected trait = '{}' (id:{})\n"
                            .format(*args))

                case 'trait_pile':
                    print(">>> select <<< handle PLAYER_listbox -> selected trait = '{}' is selecting '{}' (id:{})"
                          .format(*args))
                    f.write(">>> select <<< handle PLAYER_listbox -> selected trait = '{}' is selecting '{}' (id:{})\n"
                            .format(*args))

        case 'play':
            match what[1]:
                case 'error_no_trait':
                    print(">>> play <<< ERROR - no trait selected")
                    f.write(">>> play <<< ERROR - no trait selected\n")

                case 'error_2dominants':
                    print(">>> play <<< ERROR - already 2 dominant traits in trait pile")
                    f.write(">>> play <<< ERROR - already 2 dominant traits in trait pile\n")

                case 'error_no_attachables':
                    print(">>> play <<< ERROR - no traits in trait pile for attachment to attach to")
                    f.write(">>> play <<< ERROR - no traits in trait pile for attachment to attach to\n")

                case 'play':
                    print(">>> play <<< '{}' is playing '{}' (id:{})"
                          .format(*args))
                    f.write(">>> play <<< '{}' is playing '{}' (id:{})\n"
                            .format(*args))

        case 'move':
            match what[1]:
                case 'error_move_to':
                    print(">>> move <<< ERROR - clicked on 'move trait to...'")
                    f.write(">>> move <<< ERROR - clicked on 'move trait to...'\n")

                case 'error_no_trait':
                    print(">>> move <<< ERROR - no trait selected")
                    f.write(">>> move <<< ERROR - no trait selected\n")

                case 'error_source_target':
                    print(">>> move <<< ERROR - 'source' and 'target' player are the same")
                    f.write(">>> move <<< ERROR - 'source' and 'target' player are the same\n")

                case 'error_attachment':
                    print(">>> move <<< ERROR - attachment not moveable -> move host instead")
                    f.write(">>> move <<< ERROR - attachment not moveable -> move host instead\n")

                case 'move_to':
                    print(">>> move <<< '{}' (id:{}) {} is moved from '{}' to '{}'"
                          .format(*args))
                    f.write(">>> move <<< '{}' (id:{}) {} is moved from '{}' to '{}'\n"
                            .format(*args))

        case 'attach_to':
            match what[1]:
                case 'error_own_host':
                    print(">>> attachment <<< ERROR - clicked on own host")
                    f.write(">>> attachment <<< ERROR - clicked on own host\n")

                case 'detached':
                    print(">>> attachment <<< detached '{}' (id:{}) from host..."
                          .format(*args))
                    f.write(">>> attachment <<< detached '{}' (id:{}) from host...\n"
                            .format(*args))

                case 'attached':
                    print(">>> attachment <<< '{}' attached '{}' (id:{}) to '{}' (id:{})"
                          .format(*args))
                    f.write(">>> attachment <<< '{}' attached '{}' (id:{}) to '{}' (id:{})\n"
                            .format(*args))

                case 'change_host':
                    print("    >>> was until now on old host: {} (id:{})".format(*args))
                    f.write("    >>> was until now on old host: {} (id:{})\n".format(*args))

        case 'remove':
            match what[1]:
                case 'error_no_trait':
                    print(">>> remove <<< ERROR - no trait selected")
                    f.write(">>> remove <<< ERROR - no trait selected\n")

                case 'error_attachment_selected':
                    print(">>> remove <<< ERROR - attachment not discardable -> discard host instead")
                    f.write(">>> remove <<< ERROR - attachment not discardable -> discard host instead\n")

                case 'hand':
                    print(">>> remove <<< '{}' is moving '{}' (id:{}) to his hand"
                          .format(*args))
                    f.write(">>> remove <<< '{}' is moving '{}' (id:{}) to his hand\n"
                            .format(*args))

                case 'discard':
                    print(">>> remove <<< '{}' is discarding '{}' (id:{})"
                          .format(*args))
                    f.write(">>> remove <<< '{}' is discarding '{}' (id:{})\n"
                            .format(*args))

                case 'discard_attachment':
                    print(">>> remove <<< ___ attachment '{}' (id:{}) is also discarded automatically"
                          .format(*args))
                    f.write(">>> remove <<< ___ attachment '{}' (id:{}) is also discarded automatically\n"
                            .format(*args))

        case 'traits_WE':
            match what[1]:
                case 'reset':
                    print(">>> traits world end <<< resetting '{}'s (id:{}) worlds-end-effect..."
                          .format(*args))
                    f.write(">>> traits world end <<< resetting '{}'s (id:{}) worlds-end-effect...\n"
                            .format(*args))

                case 'set':
                    print(">>> traits world end <<< setting '{}'s (id:{}) worlds-end-effect to '{}'"
                          .format(*args))
                    f.write(">>> traits world end <<< setting '{}'s (id:{}) worlds-end-effect to '{}'\n"
                            .format(*args))

        case 'catastrophe':
            match what[1]:
                case 'error_no_catastrophe':
                    print(">>> catastrophe <<< ERROR - no catastrophe (#{}) selected".format(*args))
                    f.write(">>> catastrophe <<< ERROR - no catastrophe (#{}) selected\n".format(*args))

                case 'error_keep_catastrophe':
                    print(">>> catastrophe <<< ERROR - keep selected catastrophe (#{})".format(*args))
                    f.write(">>> catastrophe <<< ERROR - keep selected catastrophe (#{})\n".format(*args))

                case 'error_same_catastrophe':
                    print(">>> catastrophe <<< ERROR - same catastrophe (#{}) selected as before: '{}'"
                          .format(*args))
                    f.write(">>> catastrophe <<< ERROR - same catastrophe (#{}) selected as before: '{}'\n"
                            .format(*args))

                case 'catastrophe':
                    print(">>> catastrophe <<< played catastrophe #{}: '{}' (id:{})"
                          .format(*args))
                    f.write(">>> catastrophe <<< played catastrophe #{}: '{}' (id:{})\n"
                            .format(*args))

                case 'first_player':
                    print("   >>> '{}' is now first player after {} catastrophies".format(*args))
                    f.write("   >>> '{}' is now first player after {} catastrophies\n".format(*args))

        case 'worlds_end':
            match what[1]:
                case 'error_no_event':
                    print(">>> world's end <<< ERROR - no event selected")
                    f.write(">>> world's end <<< ERROR - no event selected\n")

                case 'game_over':
                    print(">>> world's end <<< '{}' is happening now...".format(*args))
                    f.write(">>> world's end <<< '{}' is happening now...\n".format(*args))

        case 'update_trait_status':
            match what[1]:
                case 'reset':
                    print(">>> current effects <<< '{}' is reseted to defaults"
                          .format(*args))

                case 'attachment':
                    print(">>> current effects <<< '{}' is updated due to effects of '{}'"
                          .format(*args))

                case 'neoteny_no_one':
                    print('>>> Neoteny <<< in no one`s hand')

                case 'neoteny_that_one':
                    print('>>> Neoteny <<< in {}`s hand'.format(*args))

        case 'scoring':
            match what[1]:
                case 'update':
                    print(">>> scoring <<< current points 4 '{}': face={} | drops={} | WE={} | MOL={} | total={}"
                          .format(*args))
                    f.write(">>> scoring <<< current points 4 '{}': face={} | drops={} | WE={} | MOL={} | total={}\n"
                            .format(*args))

                case 'manual_drops':
                    print(">>> scoring <<< manual drops of {} (id:{}) set to: {}"
                          .format(*args))
                    f.write(">>> scoring <<< manual drops of {} (id:{}) set to: {}\n"
                            .format(*args))

        case 'genes':
            match what[1]:
                case 'trait':
                    print(">>> genes <<< '{}'s '{}' has gene effect off '{}' on '{}' -> current effect: {}"
                          .format(*args))
                    f.write(">>> genes <<< '{}'s '{}' has gene effect off '{}' on '{}' -> current effect: {}\n"
                            .format(*args))

                case 'catastrophe':
                    print(">>> genes <<< catastrophe '{}' has gene effect off '{}' -> current effect: {}"
                          .format(*args))
                    f.write(">>> genes <<< catastrophe '{}' has gene effect off '{}' -> current effect: {}\n"
                            .format(*args))

                case 'denial':
                    print(">>> genes <<< 'Denial' (id:{}) protects '{}' from gene effect of '{}' -> current effect: {}"
                          .format(*args))
                    f.write(">>> genes <<< 'Denial' (id:{}) protects '{}' from gene effect of '{}' -> current effect: {}\n"  # noqa: E501
                            .format(*args))

                case 'denial_t4h':
                    print(">>> genes <<< 'Denial' (id:{}) could not protect '{}' from '{}' -> current effect: {}"
                          .format(*args))
                    f.write(">>> genes <<< 'Denial' (id:{}) could not protect '{}' from '{}' -> current effect: {}\n"
                            .format(*args))

                case 'spores':
                    print(">>> genes <<< 'Spores' (id:{}) has an gene effect (+1) on '{}' -> current effect: {}"
                          .format(*args))
                    f.write(">>> genes <<< 'Spores' (id:{}) has an gene effect (+1) on '{}' -> current effect: {}\n"
                            .format(*args))

                case 'sleepy':
                    print(">>> genes <<< 'Sleepy' (id:?) has an gene effect on '{}' by {} -> current effect: {}"
                          .format(*args))
                    f.write(">>> genes <<< 'Sleepy' (id:?) has an gene effect on '{}' by {} -> current effect: {}\n"
                            .format(*args))

                case 'total_effect':
                    print("   >>> total gene effect: {} -> new gene pools are {}"
                          .format(*args))
                    f.write("   >>> total gene effect: {} -> new gene pools are {}\n"
                            .format(*args))

        case 'trait_effects':
            match what[1]:
                case 'viral':
                    print("Viral acts on '{}' traits in '{}'s trait pile -> drop points = {}"
                          .format(*args))
                    f.write("Viral acts on '{}' traits in '{}'s trait pile -> drop points = {}\n"
                            .format(*args))

                case 'amatoxins':
                    print("Amatoxins' effect is based on amount of discraded colors -> drop points = {}"
                          .format(*args))
                    f.write("Amatoxins' effect is based on amount of discraded colors -> drop points = {}\n"
                            .format(*args))

                case 'prowler':
                    print("Prowler acts on 'color_count' in '{}'s trait pile -> drop points = {}"
                          .format(*args))
                    f.write("Prowler acts on 'color_count' in '{}'s trait pile -> drop points = {}\n"
                            .format(*args))

                case 'shiny':
                    print("Shiny acts on 'colorless' traits in '{}'s trait pile -> drop points = {}"
                          .format(*args))
                    f.write("Shiny acts on 'colorless' traits in '{}'s trait pile -> drop points = {}\n"
                            .format(*args))

        case 'music':
            match what[1]:
                case 'off':
                    print(">>> music <<< turned off")
                    f.write(">>> music <<< turned off\n")

                case 'on':
                    print(">>> music <<< turned on")
                    f.write(">>> music <<< turned on\n")

                case 'play':
                    print(">>> music <<< playing {}"
                          .format(*args))
                    f.write(">>> music <<< playing {}\n"
                            .format(*args))

        case 'icons':
            match what[1]:
                case 'off':
                    print(">>> icons <<< turned off")
                    f.write(">>> icons <<< turned off\n")

                case 'on':
                    print(">>> icons <<< turned on")
                    f.write(">>> icons <<< turned on\n")

                case 'full':
                    print(">>> icons <<< turned full")
                    f.write(">>> icons <<< turned full\n")

        case '*':
            print("{}".format(*args))
            f.write("{}\n".format(*args))

    f.close()
