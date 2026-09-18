from engine.richpresense import RichPresense
from scripts.reset import ResetScript

def ingame_main(game):

    game.discord.update_rpc(
        state=f"No Challenge ({game.texts[0].get_text()} {game.texts[1].get_text()})",
        details="In a Night"
    )

    game.night_timer += game.delta_time

    # ==========================================================
    # HORA
    # ==========================================================

    if 0 <= game.night_timer <= 1:

        for text in game.texts:

            if game.hour == -4:

                if text.get_subid() == "Period":
                    text.set_text("PM")

                if text.get_subid() == "Hour":
                    text.set_text("8")
                    text.set_x(1170)

            elif game.hour == -2:

                if text.get_subid() == "Period":
                    text.set_text("PM")

                if text.get_subid() == "Hour":
                    text.set_text("10")
                    text.set_x(1150)

            elif game.hour == 0:

                if text.get_subid() == "Period":
                    text.set_text("AM")

                if text.get_subid() == "Hour":
                    text.set_text("12")

            elif game.hour == 1:

                if text.get_subid() == "Hour":
                    text.set_text("1")
                    text.set_x(1170)

    # ==========================================================
    # AVANZAR HORA
    # ==========================================================

    if game.night_timer > 75:

        game.hour += 1
        match game.hour:
            case 0:
                game.texts[0].set_text("12")
            case 1:
                game.texts[0].set_text("1")
            case _:
                game.texts[0].set_text(
                    str(int(game.texts[0].get_text()) + 1)
                )

        game.night_timer = 0

    # ==========================================================
    # FADE IN
    # ==========================================================

    if game.INGAME_FADE_ALPHA > 0:

        game.INGAME_FADE_ALPHA -= (
            game.INGAME_FADE_SPEED *
            game.delta_time
        )

        if game.INGAME_FADE_ALPHA < 0:
            game.INGAME_FADE_ALPHA = 0

        for image in game.images:

            if image.get_id() == "fadein":

                image.set_alpha(
                    game.INGAME_FADE_ALPHA
                )

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

    game.player.x = int(
        game.player_x
    )

    # ==========================================================
    # Completar Noche
    # ==========================================================

    match game.night_type:
        case 1:
            if game.hour == 6:
                pass