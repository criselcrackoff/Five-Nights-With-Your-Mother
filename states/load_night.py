from random import randrange
from data.sounds import *
from scripts.power import PowerScript
def load_night_main(game):

    game.LOAD_NIGHT_TIMER += game.delta_time

    if game.hour == -4:
        game.texts[1].set_text("8")
        game.texts[1].set_x(590)
        game.texts[2].set_text("PM")

    elif game.hour == -2:
        game.texts[1].set_text("10")
        game.texts[2].set_text("PM")


    if game.LOAD_NIGHT_TIMER < 0.12:

        game.images[0].set_alpha(255)
        game.images[1].set_alpha(0)
        game.images[2].set_alpha(0)

        game.texts[0].set_alpha(game.texts[0].get_alpha() + 15)
        game.texts[1].set_alpha(game.texts[0].get_alpha() + 15)
        game.texts[2].set_alpha(game.texts[0].get_alpha() + 15)

        game.texts[3].set_alpha(0)

    elif game.LOAD_NIGHT_TIMER < 0.24:

        game.images[0].set_alpha(0)
        game.images[1].set_alpha(255)
        game.images[2].set_alpha(0)

        game.texts[0].set_alpha(game.texts[0].get_alpha() + 15)
        game.texts[1].set_alpha(game.texts[0].get_alpha() + 15)
        game.texts[2].set_alpha(game.texts[0].get_alpha() + 15)

        game.texts[3].set_alpha(0)

    elif game.LOAD_NIGHT_TIMER < 0.36:

        game.images[0].set_alpha(0)
        game.images[1].set_alpha(0)
        game.images[2].set_alpha(255)

        game.texts[0].set_alpha(game.texts[0].get_alpha() + 15)
        game.texts[1].set_alpha(game.texts[0].get_alpha() + 15)
        game.texts[2].set_alpha(game.texts[0].get_alpha() + 15)

        game.texts[3].set_alpha(0)
        game.texts[3].set_y(640)

    elif game.LOAD_NIGHT_TIMER < 3.50:

        game.images[2].set_alpha(0)

        game.texts[0].set_alpha(game.texts[0].get_alpha() + 15)
        game.texts[1].set_alpha(game.texts[1].get_alpha() + 15)
        game.texts[2].set_alpha(game.texts[2].get_alpha() + 15)

    elif game.LOAD_NIGHT_TIMER < 10.0:

        if game.LOAD_NIGHT_TIMER >= 9.50 and not game.MUSIC_STOPPED:

            game.mixer.crossfade(
                game.CHANNEL_MENU,
                game.CHANNEL_AMBIENT,
                OfficeAmbience[randrange(4)],
                volume=0.08,
                looping=True,
                fade_ms=2500
            )

            game.MUSIC_STOPPED = True

        game.images[3].set_alpha(255)

        game.texts[0].set_alpha(0)
        game.texts[1].set_alpha(0)
        game.texts[2].set_alpha(0)

        game.texts[3].set_alpha(255)

    else:

        game.MUSIC_STOPPED = False
        game.texts = game.INGAME_TEXTS
        game.images = game.INGAME_IMG
        game.add_script(PowerScript)
        game.power = game.get_script(PowerScript)
        game.GAMESTATE = "ingame"