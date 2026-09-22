def custom_night_main(game):

    # ==========================================================
    # CUSTOM NIGHT SCROLL
    # ==========================================================

    game.CUSTOM_NIGHT_SCROLL = max(
        -500,
        min(
            game.CUSTOM_NIGHT_SCROLL,
            0
        )
    )

    # ==========================================================
    # SETTINGS
    # ==========================================================

    if game.SETTINGS_STATE == "opening":

        game.SETTINGS_SCROLL += (
            game.SETTINGS_SPEED
            *
            game.delta_time
        )

        if game.SETTINGS_SCROLL >= 1050:

            game.SETTINGS_SCROLL = 1050
            game.SETTINGS_STATE = "open"

            for text in game.texts:

                if text.get_id() == 8:

                    text.set_trigeable(
                        True
                    )

    elif game.SETTINGS_STATE == "closing":

        game.SETTINGS_SCROLL -= (
            game.SETTINGS_SPEED
            *
            game.delta_time
        )

        if game.SETTINGS_SCROLL <= 0:

            game.SETTINGS_SCROLL = 0
            game.SETTINGS_STATE = "closed"

            for text in game.texts:

                if text.get_id() == 7:

                    text.set_trigeable(
                        True
                    )