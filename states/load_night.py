from random import randrange


def load_night_main(
    texts,
    img,
    delta_time,
    load_night_timer,
    music_stopped,
    hour,
    mixer_sound,
    channel_menu,
    channel_ambient,
    office_ambience
):

    game_state = "menu"
    next_state = "LoadNight"

    load_night_timer += delta_time


    if hour == -4:
        texts[1].set_text("8")
        texts[1].set_x(590)
        texts[2].set_text("PM")

    elif hour == -2:
        texts[1].set_text("10")
        texts[2].set_text("PM")


    if load_night_timer < 0.12:

        img[0].set_alpha(255)
        img[1].set_alpha(0)
        img[2].set_alpha(0)

        texts[0].set_alpha(texts[0].get_alpha() + 15)
        texts[1].set_alpha(texts[0].get_alpha() + 15)
        texts[2].set_alpha(texts[0].get_alpha() + 15)

        texts[3].set_alpha(0)

    elif load_night_timer < 0.24:

        img[0].set_alpha(0)
        img[1].set_alpha(255)
        img[2].set_alpha(0)

        texts[0].set_alpha(texts[0].get_alpha() + 15)
        texts[1].set_alpha(texts[0].get_alpha() + 15)
        texts[2].set_alpha(texts[0].get_alpha() + 15)

        texts[3].set_alpha(0)

    elif load_night_timer < 0.36:

        img[0].set_alpha(0)
        img[1].set_alpha(0)
        img[2].set_alpha(255)

        texts[0].set_alpha(texts[0].get_alpha() + 15)
        texts[1].set_alpha(texts[0].get_alpha() + 15)
        texts[2].set_alpha(texts[0].get_alpha() + 15)

        texts[3].set_alpha(0)
        texts[3].set_y(640)


    elif load_night_timer < 3.50:

        img[2].set_alpha(0)

        texts[0].set_alpha(texts[0].get_alpha() + 15)
        texts[1].set_alpha(texts[1].get_alpha() + 15)
        texts[2].set_alpha(texts[2].get_alpha() + 15)


    elif load_night_timer < 10.0:

        if load_night_timer >= 9.50 and not music_stopped:

            mixer_sound.crossfade(
                channel_menu,
                channel_ambient,
                office_ambience[randrange(4)],
                volume=0.08,
                looping=True,
                fade_ms=2500
            )

            music_stopped = True

        img[3].set_alpha(255)

        texts[0].set_alpha(0)
        texts[1].set_alpha(0)
        texts[2].set_alpha(0)

        texts[3].set_alpha(255)


    else:

        music_stopped = False

        game_state = "ingame"

    return (
        game_state,
        next_state,
        load_night_timer,
        music_stopped
    )