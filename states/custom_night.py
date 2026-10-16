
import time
import pygame


# ==========================================================
# CUSTOM NIGHT MAIN
# ==========================================================

def custom_night_main(game):

    # ======================================================
    # SCROLL
    # ======================================================

    game.CUSTOM_NIGHT_SCROLL = max(
        -500,
        min(game.CUSTOM_NIGHT_SCROLL, 0)
    )

    # ======================================================
    # ACTUALIZAR TEXTOS DE IA
    # ======================================================

    ai_texts = {
        111: game.maurello,
        112: game.furry,
        113: game.teddy
    }

    for text in game.texts:
    #   ejemplo 111 = maurello.get(text.get_id())
        animatronic = ai_texts.get(text.get_id())

        if animatronic is not None:
            text.set_text(
                str(animatronic.get_ai())
            )

    # ======================================================
    # SETTINGS
    # ======================================================

    if game.SETTINGS_STATE == "opening":

        game.SETTINGS_SCROLL += (
            game.SETTINGS_SPEED
            * game.delta_time
        )

        if game.SETTINGS_SCROLL >= 1050:

            game.SETTINGS_SCROLL = 1050
            game.SETTINGS_STATE = "open"

            for text in game.texts:

                if text.get_id() == 8:
                    text.set_trigeable(True)

    elif game.SETTINGS_STATE == "closing":

        game.SETTINGS_SCROLL -= (
            game.SETTINGS_SPEED
            * game.delta_time
        )

        if game.SETTINGS_SCROLL <= 0:

            game.SETTINGS_SCROLL = 0
            game.SETTINGS_STATE = "closed"

            for text in game.texts:

                if text.get_id() == 7:
                    text.set_trigeable(True)


# ==========================================================
# CUSTOM NIGHT EVENTS
# ==========================================================

def custom_night_handle_event(game, event):

    if event.type == pygame.MOUSEWHEEL:

        game.CUSTOM_NIGHT_SCROLL += (
            event.y * 25
        )


# ==========================================================
# CUSTOM NIGHT CLICKS
# ==========================================================

def custom_night_handle_click(game):

    # ======================================================
    # TEXT BUTTONS
    # ======================================================

    for text in game.texts:

        if not text.is_trigeable():
            continue

        rect = text.get_rect()

        if rect is None:
            continue

        if not rect.collidepoint(
            game.mouse_x,
            game.mouse_y
        ):
            continue

        match text.get_id():

            case 1:
                set_all_ai(game, 0)

            case 2:
                add_all_ai(game, 1)

            case 3:
                set_all_ai(game, 5)

            case 4:
                set_all_ai(game, 10)

            case 5:
                set_all_ai(game, 20)

            case 6:
                custom_night_start_game(game)
                return

            case 7:

                game.mixer.set_volume(
                    game.CHANNEL_MENU,
                    0.05
                )

                text.set_trigeable(False)

                game.SETTINGS_STATE = "opening"

            case 8:

                game.mixer.set_volume(
                    game.CHANNEL_MENU,
                    0.1
                )

                text.set_trigeable(False)

                game.SETTINGS_STATE = "closing"

    # ======================================================
    # IMAGE BUTTONS
    # ======================================================

    image_actions = {
        "MaurelloMinusAi": (game.maurello, -1),
        "MaurelloAddAi": (game.maurello, 1),
        "FurryMinusAi": (game.furry, -1),
        "FurryAddAi": (game.furry, 1),
        "TeddyMinusAi": (game.teddy, -1),
        "TeddyAddAi": (game.teddy, 1)
    }

    for image in game.images:

        if not image.is_trigeable():
            continue

        rect = image.get_rect()

        if rect is None:
            continue

        if not rect.collidepoint(
            game.mouse_x,
            game.mouse_y
        ):
            continue

        action = image_actions.get(
            image.get_subid()
        )

        if action is None:
            continue

        animatronic, amount = action

        if amount > 0:
            animatronic.add_ai(amount)
        else:
            animatronic.minus_ai(-amount)


# ==========================================================
# AI HELPERS
# ==========================================================

def set_all_ai(game, value):

    game.maurello.set_ai(value)
    game.furry.set_ai(value)
    game.teddy.set_ai(value)


def add_all_ai(game, amount):

    game.maurello.add_ai(amount)
    game.furry.add_ai(amount)
    game.teddy.add_ai(amount)


# ==========================================================
# START GAME
# ==========================================================

def custom_night_start_game(game):

    print("Start Game")

    game.menu_start_time = time.time()

    game.mixer.set_volume(
        game.CHANNEL_MENU,
        0.05
    )

    game.texts = game.LOAD_NIGHT_TEXTS
    game.images = game.LOAD_NIGHT_IMG

    game.discord.update_rpc(
        "Loading night",
        "In a Menu"
    )

    game.SUBGAMESTATE = "LoadNight"
