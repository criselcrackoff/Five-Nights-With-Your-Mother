
def custom_night_main(
    texts,
    delta_time,
    custom_night_scroll,
    settings_scroll,
    settings_speed,
    settings_state
):

    custom_night_scroll = max(
        -500,
        min(custom_night_scroll, 0)
    )

    if settings_state == "opening":

        settings_scroll += settings_speed * delta_time

        if settings_scroll >= 1050:

            settings_scroll = 1050
            settings_state = "open"

            for text in texts:
                if text.get_id() == 8:
                    text.set_trigeable(True)

    elif settings_state == "closing":

        settings_scroll -= settings_speed * delta_time

        if settings_scroll <= 0:

            settings_scroll = 0
            settings_state = "closed"

            for text in texts:
                if text.get_id() == 7:
                    text.set_trigeable(True)

    return (
        custom_night_scroll,
        settings_scroll,
        settings_state
    )