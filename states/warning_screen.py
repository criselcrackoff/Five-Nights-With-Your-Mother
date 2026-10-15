import pygame

from data.sounds import Custom_Menu


def warning_main(
    texts,
    img,
    delta_time,
    fadein_speed,
    fadeout_speed,
    timer,
    menu_state,
    mouse_clicked,
    menu_start_time,
    mixer_sound,
    discord,
    channel_menu
):

    next_state = "warningscreen"

    if menu_state == "fade_in":

        for text in texts:
            text.set_alpha(
                text.get_alpha() +
                fadein_speed * delta_time
            )

        for image in img:
            image.set_alpha(
                image.get_alpha() +
                fadein_speed * delta_time
            )

        if texts[0].get_alpha() >= 255:
            menu_state = "wait"

    elif menu_state == "wait":

        timer += delta_time

        if timer >= 4:
            menu_state = "fade_out"

    elif menu_state == "fade_out":

        for image in img:
            image.set_alpha(
                image.get_alpha() -
                fadeout_speed * delta_time
            )

        for text in texts:
            text.set_alpha(
                text.get_alpha() -
                fadeout_speed * delta_time
            )

        if texts[0].get_alpha() <= 0:

            pygame.time.wait(500)

            mixer_sound.play(
                Custom_Menu,
                0.1,
                channel_menu,
                True
            )

            discord.update_rpc(
                "Custom Night",
                "In a Menu:"
            )

            next_state = "CustomNight"

    if mouse_clicked:

        mixer_sound.play(
            Custom_Menu,
            0.1,
            channel_menu,
            True
        )

        discord.update_rpc(
            "Custom Night",
            "In a Menu:"
        )

        next_state = "CustomNight"

    return (
        next_state,
        menu_state,
        timer,
        menu_start_time
    )