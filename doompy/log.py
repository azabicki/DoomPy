# flake8: noqa: E501
from globals_ import logfile, log_to_terminal


def write_log(what, *args):
    f = open(logfile["file"], "a")

    match what[0]:
        case "init":  # initialize
            match what[1]:
                case "datetime":
                    if log_to_terminal:
                        print(">>> initialize <<< new game: {}".format(*args))
                    f.write(">>> initialize <<< new game: {}\n".format(*args))

                case "variables":
                    if log_to_terminal:
                        print(">>> initialize <<< reset variables")
                    f.write(">>> initialize <<< reset variables\n")

                case "menu":
                    if log_to_terminal:
                        print(">>> initialize <<< create menu")
                    f.write(">>> initialize <<< create menu\n")

                case "playground":
                    if log_to_terminal:
                        print(">>> initialize <<< create playground")
                    f.write(">>> initialize <<< create playground\n")

                case "names":
                    if log_to_terminal:
                        print("   >>> name of player #{} = '{}'".format(*args))
                    f.write("   >>> name of player #{} = '{}'\n".format(*args))

                case "first_player":
                    if log_to_terminal:
                        print("   >>> first player is '{}'".format(*args))
                    f.write("   >>> first player is '{}'\n".format(*args))

        case "select":
            match what[1]:
                case "deck":
                    if log_to_terminal:
                        print(
                            ">>> select trait <<< in DECK -> selected trait = '{}' (id:{})".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> select trait <<< in DECK -> selected trait = '{}' (id:{})\n".format(
                            *args
                        )
                    )

                case "trait_pile":
                    if log_to_terminal:
                        print(
                            ">>> select trait <<< in TRAIT PILE -> selected trait = '{}' is selecting '{}' (id:{})".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> select trait <<< in TRAIT PILE -> selected trait = '{}' is selecting '{}' (id:{})\n".format(
                            *args
                        )
                    )

        case "play":
            match what[1]:
                case "error_no_trait":
                    if log_to_terminal:
                        print(">>> play <<< ERROR - no trait selected")
                    f.write(">>> play <<< ERROR - no trait selected\n")

                case "error_2dominants":
                    if log_to_terminal:
                        print(
                            ">>> play <<< ERROR - already 2 dominants in '{}'s trait pile".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> play <<< ERROR - already 2 dominants in '{}'s trait pile\n".format(
                            *args
                        )
                    )

                case "error_no_attachables":
                    if log_to_terminal:
                        print(
                            ">>> play <<< ERROR - no traits in '{}'s trait pile for attachment to attach to".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> play <<< ERROR - no traits in '{}'s trait pile for attachment to attach to\n".format(
                            *args
                        )
                    )

                case "heroic":
                    if log_to_terminal:
                        print(
                            ">>> play <<< 'HEROIC' is born as 3rd dominant during 'Birth of a Hero'"
                        )
                    f.write(
                        ">>> play <<< 'HEROIC' is born as 3rd dominant during 'Birth of a Hero'\n"
                    )

                case "play":
                    if log_to_terminal:
                        print(">>> play <<< '{}' is playing '{}' (id:{})".format(*args))
                    f.write(">>> play <<< '{}' is playing '{}' (id:{})\n".format(*args))

        case "move":
            match what[1]:
                case "error_move_to":
                    if log_to_terminal:
                        print(">>> move <<< ERROR - clicked on 'move trait to...'")
                    f.write(">>> move <<< ERROR - clicked on 'move trait to...'\n")

                case "error_no_trait":
                    if log_to_terminal:
                        print(">>> move <<< ERROR - no trait selected")
                    f.write(">>> move <<< ERROR - no trait selected\n")

                case "move_to":
                    if log_to_terminal:
                        print(
                            ">>> move <<< '{}' (id:{}) {} is moved from '{}' to '{}'".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> move <<< '{}' (id:{}) {} is moved from '{}' to '{}'\n".format(
                            *args
                        )
                    )

        case "attach_to":
            match what[1]:
                case "error_current_host":
                    if log_to_terminal:
                        print(">>> attachment <<< ERROR - clicked on current host")
                    f.write(">>> attachment <<< ERROR - clicked on current host\n")

                case "detached":
                    if log_to_terminal:
                        print(
                            ">>> attachment <<< detached '{}' (id:{}) from host...".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> attachment <<< detached '{}' (id:{}) from host...\n".format(
                            *args
                        )
                    )

                case "still_detached":
                    if log_to_terminal:
                        print(
                            ">>> attachment <<< '{}' (id:{}) still without host...".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> attachment <<< '{}' (id:{}) still without host...\n".format(
                            *args
                        )
                    )

                case "attached":
                    if log_to_terminal:
                        print(
                            ">>> attachment <<< '{}' attached '{}' (id:{}) to '{}' (id:{})".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> attachment <<< '{}' attached '{}' (id:{}) to '{}' (id:{})\n".format(
                            *args
                        )
                    )

                case "change_host":
                    if log_to_terminal:
                        print("    >>> was until now on '{}' (id:{})".format(*args))
                    f.write("    >>> was until now on '{}' (id:{})\n".format(*args))

        case "remove":
            match what[1]:
                case "error_no_trait":
                    if log_to_terminal:
                        print(">>> remove <<< ERROR - no trait selected")
                    f.write(">>> remove <<< ERROR - no trait selected\n")

                case "error_attachment_selected":
                    if log_to_terminal:
                        print(
                            ">>> remove <<< ERROR - attachment not discardable -> discard host instead"
                        )
                    f.write(
                        ">>> remove <<< ERROR - attachment not discardable -> discard host instead\n"
                    )

                case "hand":
                    if log_to_terminal:
                        print(
                            ">>> remove <<< '{}' is moving '{}' (id:{}) to his/her hand".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> remove <<< '{}' is moving '{}' (id:{}) to his/her hand\n".format(
                            *args
                        )
                    )

                case "discard":
                    if log_to_terminal:
                        print(
                            ">>> remove <<< '{}' is discarding '{}' (id:{})".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> remove <<< '{}' is discarding '{}' (id:{})\n".format(*args)
                    )

                case "discard_attachment":
                    if log_to_terminal:
                        print(
                            "   >>> remove <<< attachment '{}' (id:{}) is also discarded automatically".format(
                                *args
                            )
                        )
                    f.write(
                        "   >>> remove <<< attachment '{}' (id:{}) is also discarded automatically\n".format(
                            *args
                        )
                    )

        case "traits_WE":
            match what[1]:
                case "reset":
                    if log_to_terminal:
                        print(
                            ">>> traits world end <<< resetting '{}'s (id:{}) worlds-end-effect...".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> traits world end <<< resetting '{}'s (id:{}) worlds-end-effect...\n".format(
                            *args
                        )
                    )

                case "set":
                    if log_to_terminal:
                        print(
                            ">>> traits world end <<< setting '{}'s (id:{}) worlds-end-effect to '{}'".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> traits world end <<< setting '{}'s (id:{}) worlds-end-effect to '{}'\n".format(
                            *args
                        )
                    )

        case "catastrophe":
            match what[1]:
                case "error_no_catastrophe":
                    if log_to_terminal:
                        print(
                            ">>> catastrophe <<< ERROR - no catastrophe (#{}) selected".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> catastrophe <<< ERROR - no catastrophe (#{}) selected\n".format(
                            *args
                        )
                    )

                case "error_keep_catastrophe":
                    if log_to_terminal:
                        print(
                            ">>> catastrophe <<< ERROR - forced to keep selected catastrophe (#{})".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> catastrophe <<< ERROR - forced to keep selected catastrophe (#{})\n".format(
                            *args
                        )
                    )

                case "error_same_catastrophe":
                    if log_to_terminal:
                        print(
                            ">>> catastrophe <<< ERROR - same catastrophe (#{}) selected as before: '{}'".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> catastrophe <<< ERROR - same catastrophe (#{}) selected as before: '{}'\n".format(
                            *args
                        )
                    )

                case "catastrophe":
                    if log_to_terminal:
                        print(
                            ">>> catastrophe <<< played catastrophe #{}: '{}' (id:{})".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> catastrophe <<< played catastrophe #{}: '{}' (id:{})\n".format(
                            *args
                        )
                    )

                case "first_player":
                    if log_to_terminal:
                        print(
                            "   >>> catastrophe <<< '{}' is now first player after {} catastrophes".format(
                                *args
                            )
                        )
                    f.write(
                        "   >>> catastrophe <<< '{}' is now first player after {} catastrophes\n".format(
                            *args
                        )
                    )

        case "worlds_end":
            match what[1]:
                case "select":
                    if log_to_terminal:
                        print(
                            ">>> world's end <<< '{}' is selected as worlds end event".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> world's end <<< '{}' is selected as worlds end event\n".format(
                            *args
                        )
                    )

                case "button_ready":
                    if log_to_terminal:
                        print(
                            ">>> world's end <<< all trait-WE-effects & WE-event selected -> ready to GO!"
                        )
                    f.write(
                        ">>> world's end <<< all trait-WE-effects & WE-event selected -> ready to GO!\n"
                    )

                case "button_not_ready":
                    if log_to_terminal:
                        print(
                            ">>> world's end <<< still some trait-WE-effects to be selected ..."
                        )
                    f.write(
                        ">>> world's end <<< still some trait-WE-effects to be selected ...\n"
                    )

                case "play_WE":
                    if log_to_terminal:
                        print(">>> world's end <<< play WE '{}'".format(*args))
                    f.write(">>> world's end <<< play WE '{}'\n".format(*args))

        case "MOLs":
            match what[1]:
                case "error_no_MOL":
                    if log_to_terminal:
                        print(
                            ">>> MOL <<< ERROR - no MOL (#{} by {}) selected".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> MOL <<< ERROR - no MOL (#{} by {}) selected\n".format(
                            *args
                        )
                    )

                case "error_keep_MOL":
                    if log_to_terminal:
                        print(
                            ">>> MOL <<< ERROR - keep selected MOL (#{} by {}): '{}'".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> MOL <<< ERROR - keep selected MOL (#{} by {}): '{}'\n".format(
                            *args
                        )
                    )

                case "deselected_MOL":
                    if log_to_terminal:
                        print(">>> MOL <<< {} de-selected MOL #{}: '{}'".format(*args))
                    f.write(">>> MOL <<< {} de-selected MOL #{}: '{}'\n".format(*args))

                case "MOL":
                    if log_to_terminal:
                        print(
                            ">>> MOL <<< played MOL #{} by {}: '{}' (id:{})".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> MOL <<< played MOL #{} by {}: '{}' (id:{})\n".format(*args)
                    )

                case "MOL_points":
                    if log_to_terminal:
                        print(
                            ">>> MOL <<< '{}'s MOL '{}' (id:{}) scores {} points".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> MOL <<< '{}'s MOL '{}' (id:{}) scores {} points\n".format(
                            *args
                        )
                    )

        case "update_trait_status":
            match what[1]:
                case "reset":
                    if log_to_terminal:
                        print(
                            ">>> trait's status <<< '{}' (id:{}) is reseted to defaults".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait's status <<< '{}' (id:{}) is reseted to defaults\n".format(
                            *args
                        )
                    )

                case "attachment":
                    if log_to_terminal:
                        print(
                            ">>> trait's status <<< '{}' (id:{}) is updated due to attachment effects of '{}' (id:{})".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait's status <<< '{}' (id:{}) is updated due to attachment effects of '{}' (id:{})\n".format(
                            *args
                        )
                    )

                case "traits_WE":
                    if log_to_terminal:
                        print(
                            ">>> trait's status <<< '{}' (id:{}) is updated due to TRAITS_we effects of '{}' (id:{})".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait's status <<< '{}' (id:{}) is updated due to TRAITS_we effects of '{}' (id:{})\n".format(
                            *args
                        )
                    )

                case "WE_effect":
                    if log_to_terminal:
                        print(
                            ">>> trait's status <<< '{}' (id:{}) is updated due to WORLDS END effects of '{}'".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait's status <<< '{}' (id:{}) is updated due to WORLDS END effects of '{}'\n".format(
                            *args
                        )
                    )

                case "neoteny_no_one":
                    if log_to_terminal:
                        print(">>> Neoteny <<< in no one's hand")
                    f.write(">>> Neoteny <<< in no one's hand\n")

                case "neoteny_that_one":
                    if log_to_terminal:
                        print(">>> Neoteny <<< in '{}'s hand".format(*args))
                    f.write(">>> Neoteny <<< in '{}'s hand\n".format(*args))

        case "stars":
            match what[1]:
                case "n_dom":
                    s = ">>> dominants <<< in trait piles: "
                    for k, v in args[0].items():
                        s += f"{k} = {v} / "

                    if log_to_terminal:
                        print(s[:-3])
                    f.write(s[:-3] + "\n")

                case "epic":
                    if log_to_terminal:
                        print(
                            "   >>> dominant <<< EPIC fills both spots in '{}'s trait pile".format(
                                *args
                            )
                        )
                    f.write(
                        "   >>> dominant <<< EPIC fills both spots in '{}'s trait pile\n".format(
                            *args
                        )
                    )

        case "scoring":
            match what[1]:
                case "update":
                    if log_to_terminal:
                        print(
                            ">>> scoring <<< '{}'s current points: face={} | drops={} | WE={} | MOL={} | total={}".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> scoring <<< '{}'s current points: face={} | drops={} | WE={} | MOL={} | total={}\n".format(
                            *args
                        )
                    )

                case "manual_drops":
                    if log_to_terminal:
                        print(
                            ">>> scoring <<< manual drops of {} (id:{}) set to: {}".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> scoring <<< manual drops of {} (id:{}) set to: {}\n".format(
                            *args
                        )
                    )

        case "genes":
            match what[1]:
                case "trait":
                    if log_to_terminal:
                        print(
                            ">>> genes <<< '{}'s '{}' (id:{}) has gene effect off '{}' on '{}' -> current effect: {}".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> genes <<< '{}'s '{}' (id:{}) has gene effect off '{}' on '{}' -> current effect: {}\n".format(
                            *args
                        )
                    )

                case "catastrophe":
                    if log_to_terminal:
                        print(
                            ">>> genes <<< catastrophe '{}' has gene effect off '{}' -> current effect: {}".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> genes <<< catastrophe '{}' has gene effect off '{}' -> current effect: {}\n".format(
                            *args
                        )
                    )

                case "denial":
                    if log_to_terminal:
                        print(
                            ">>> genes <<< 'Denial' (id:{}) protects '{}' from gene effect of '{}' -> current effect: {}".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> genes <<< 'Denial' (id:{}) protects '{}' from gene effect of '{}' -> current effect: {}\n".format(
                            *args
                        )
                    )

                case "denial_t4h":
                    if log_to_terminal:
                        print(
                            ">>> genes <<< 'Denial' (id:{}) could not protect '{}' from '{}' -> current effect: {}".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> genes <<< 'Denial' (id:{}) could not protect '{}' from '{}' -> current effect: {}\n".format(
                            *args
                        )
                    )

                case "spores":
                    if log_to_terminal:
                        print(
                            ">>> genes <<< 'Spores' (id:{}) has an gene effect (+1) on '{}' -> current effect: {}".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> genes <<< 'Spores' (id:{}) has an gene effect (+1) on '{}' -> current effect: {}\n".format(
                            *args
                        )
                    )

                case "sleepy":
                    if log_to_terminal:
                        print(
                            ">>> genes <<< 'Sleepy' (id:?) has an gene effect on '{}' by {} -> current effect: {}".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> genes <<< 'Sleepy' (id:?) has an gene effect on '{}' by {} -> current effect: {}\n".format(
                            *args
                        )
                    )

                case "total_effect":
                    if log_to_terminal:
                        print(
                            "   >>> total gene effect: {} -> current gene pools are {}".format(
                                *args
                            )
                        )
                    f.write(
                        "   >>> total gene effect: {} -> current gene pools are {}\n".format(
                            *args
                        )
                    )

        case "trait_effects":
            match what[1]:
                case "amatoxins":
                    if log_to_terminal:
                        print(
                            ">>> trait effects <<< 'Amatoxins' (id:{}) effect is based on {} discarded colors -> drop = {}".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait effects <<< 'Amatoxins' (id:{}) effect is based on {} discarded colors -> drop = {}\n".format(
                            *args
                        )
                    )

                case "ironwood_protecting":
                    if log_to_terminal:
                        print(
                            ">>> trait effects <<< '{}' (id:{}) is protecting {} green trait(s)".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait effects <<< '{}' (id:{}) is protecting {} green trait(s)\n".format(
                            *args
                        )
                    )

                case "ironwood_not_protecting":
                    if log_to_terminal:
                        print(
                            ">>> trait effects <<< '{}' (id:{}) does not protect anymore".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait effects <<< '{}' (id:{}) does not protect anymore\n".format(
                            *args
                        )
                    )

                case "meek_protecting":
                    if log_to_terminal:
                        print(
                            ">>> trait effects <<< '{}' (id:{}) is protecting {} red trait(s)".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait effects <<< '{}' (id:{}) is protecting {} red trait(s)\n".format(
                            *args
                        )
                    )

                case "meek_not_protecting":
                    if log_to_terminal:
                        print(
                            ">>> trait effects <<< '{}' (id:{}) does not protect anymore".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait effects <<< '{}' (id:{}) does not protect anymore\n".format(
                            *args
                        )
                    )

                case "prowler":
                    if log_to_terminal:
                        print(
                            ">>> trait effects <<< 'Prowler' (id:{}) acts on 'color_count' in '{}'s trait pile -> drop = {}".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait effects <<< 'Prowler' (id:{}) acts on 'color_count' in '{}'s trait pile -> drop = {}\n".format(
                            *args
                        )
                    )

                case "shiny":
                    if log_to_terminal:
                        print(
                            ">>> trait effects <<< 'Shiny' (id:{}) acts on '{}'s 'colorless' traits -> drop = {}".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait effects <<< 'Shiny' (id:{}) acts on '{}'s 'colorless' traits -> drop = {}\n".format(
                            *args
                        )
                    )

                case "spores":
                    if log_to_terminal:
                        print(
                            ">>> trait effects <<< 'Spores' (id:{}) adds {} gene(s) to '{}'s gene pool".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait effects <<< 'Spores' (id:{}) adds {} gene(s) to '{}'s gene pool\n".format(
                            *args
                        )
                    )

                case "viral":
                    if log_to_terminal:
                        print(
                            ">>> trait effects <<< 'Viral' (id:{}) acts on '{}' traits in '{}'s trait pile -> drop = {}".format(
                                *args
                            )
                        )
                    f.write(
                        ">>> trait effects <<< 'Viral' (id:{}) acts on '{}' traits in '{}'s trait pile -> drop = {}\n".format(
                            *args
                        )
                    )

        case "points":
            match what[1]:
                case "off":
                    if log_to_terminal:
                        print(">>> points <<< turned to **")
                    f.write(">>> points <<< turned to **\n")

                case "on":
                    if log_to_terminal:
                        print(">>> points <<< turned on")
                    f.write(">>> points <<< turned on\n")

                case "rank":
                    if log_to_terminal:
                        print(">>> points <<< turned to RANKs")
                    f.write(">>> points <<< turned to RANKs\n")

        case "music":
            match what[1]:
                case "off":
                    if log_to_terminal:
                        print(">>> music <<< turned off")
                    f.write(">>> music <<< turned off\n")

                case "on":
                    if log_to_terminal:
                        print(">>> music <<< turned on")
                    f.write(">>> music <<< turned on\n")

                case "play":
                    if log_to_terminal:
                        print(">>> music <<< playing {}".format(*args))
                    f.write(">>> music <<< playing {}\n".format(*args))

        case "icons":
            match what[1]:
                case "off":
                    if log_to_terminal:
                        print(">>> icons <<< turned off")
                    f.write(">>> icons <<< turned off\n")

                case "on":
                    if log_to_terminal:
                        print(">>> icons <<< turned on")
                    f.write(">>> icons <<< turned on\n")

                case "full":
                    if log_to_terminal:
                        print(">>> icons <<< turned full")
                    f.write(">>> icons <<< turned full\n")

        case "*":
            if log_to_terminal:
                print("{}".format(*args))
            f.write("{}\n".format(*args))

    f.close()
