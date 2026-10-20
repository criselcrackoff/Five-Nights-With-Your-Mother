from data.sounds import *


def update_hour_text(game):
    hour = game.hour

    if hour < 0:
        displayed_hour = (hour + 12) % 12
        period = "PM"
    else:
        displayed_hour = hour % 12
        period = "AM"

    if displayed_hour == 0:
        displayed_hour = 12

    for text in game.texts:

        if text.get_subid() == "Hour":
            text.set_text(str(displayed_hour))
            text.set_x(1150 if displayed_hour >= 10 else 1170)

        elif text.get_subid() == "Period":
            text.set_text(period)


def finish_night(game):

    game.NIGHT_FINISHING = True
    game.INGAME_FADE_SPEED = 125
    if game.INGAME_FADE_ALPHA >= 1 and game.INGAME_FADE_ALPHA <= 5:
        game.timer = 0
        game.scripts = []
        game.mixer.stop_all()                                                       
        game.mixer.play(Night_Completed_Funfair,volume=0.3,channel=game.CHANNEL_SFX)
    game.INGAME_FADE_ALPHA = min(
        255,
        game.INGAME_FADE_ALPHA +
        game.INGAME_FADE_SPEED * game.delta_time
    )
    
    for image in game.images:
        if image.get_id() == "fadein":
            image.set_alpha(int(game.INGAME_FADE_ALPHA))

    if game.INGAME_FADE_ALPHA >= 255:

        game.texts = []
        game.images = []
        game.images = game.NIGHTCOMPLETED_IMG
        game.texts = game.NIGHTCOMPLETED_TEXTS
        game.GAMESTATE = "menu"
        game.SUBGAMESTATE = "NightCompleted"


def ingame_main(game):

    game.discord.update_rpc(
        state=f"No Challenge ({game.texts[0].get_text()} {game.texts[1].get_text()})",
        details="In a Night"
    )

    # ==========================================================
    # COMPLETAR NOCHE
    # ==========================================================

    end_hour = 6 if game.night_type == 1 else 8

    if game.hour >= end_hour:
        game.NIGHT_FINISHING = True

    if game.NIGHT_FINISHING:
        finish_night(game)
        return

    # ==========================================================
    # HORA
    # ==========================================================

    if game.night_timer == 0:
        update_hour_text(game)

    game.night_timer += game.delta_time

    # ==========================================================
    # AVANZAR HORA
    # ==========================================================

    if game.night_timer >= 1:

        game.hour += 1
        game.night_timer -= 2

        update_hour_text(game)

    # ==========================================================
    # FADE IN
    # ==========================================================

    if game.INGAME_FADE_ALPHA > 0 and not game.NIGHT_FINISHING:

        game.INGAME_FADE_ALPHA = max(
            0,
            game.INGAME_FADE_ALPHA -
            game.INGAME_FADE_SPEED * game.delta_time
        )

        for image in game.images:

            if image.get_id() == "fadein":
                image.set_alpha(game.INGAME_FADE_ALPHA)

    # ==========================================================
    # MOVIMIENTO DEL JUGADOR
    # ==========================================================

    if game.mouse_x < game.LEFT_BORDER:

        distance = (
            game.LEFT_BORDER -
            game.mouse_x
        )

        speed = (
            distance /
            game.LEFT_BORDER
        ) * game.MAX_SPEED

        game.player_x -= (
            speed *
            game.delta_time
        )

    elif game.mouse_x > game.RIGHT_BORDER:

        distance = (
            game.mouse_x -
            game.RIGHT_BORDER
        )

        speed = (
            distance /
            (game.WIDTH - game.RIGHT_BORDER)
        ) * game.MAX_SPEED

        game.player_x += (
            speed *
            game.delta_time
        )

    # ==========================================================
    # LIMITAR POSICIÓN
    # ==========================================================

    game.player_x = max(
        0,
        min(
            game.player_x,
            game.WIDTH - game.player.width
        )
    )

    game.player.x = int(game.player_x)