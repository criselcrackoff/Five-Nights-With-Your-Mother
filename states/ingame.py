from engine.richpresense import RichPresense

def ingame_main(
    texts,
    img,
    player,
    player_x,
    mouse_x,
    delta_time,
    night_timer,
    hour,
    fade_alpha,
    fade_speed,
    left_border,
    right_border,
    width,
    max_speed,
    discord
):

    discord.update_rpc(
        state=f"No Challenge ({texts[0].get_text()} {texts[1].get_text()})",
        details="In a Night"
    )

    night_timer += delta_time

    if 0 <= night_timer <= 1:

        for text in texts:

            if hour == -4:

                if text.get_subid() == "Period":
                    text.set_text("PM")

                if text.get_subid() == "Hour":
                    text.set_text("8")
                    text.set_x(1170)

            elif hour == -2:

                if text.get_subid() == "Period":
                    text.set_text("PM")

                if text.get_subid() == "Hour":
                    text.set_text("10")
                    text.set_x(1150)

            elif hour == 0:

                if text.get_subid() == "Period":
                    text.set_text("AM")

                if text.get_subid() == "Hour":
                    text.set_text("12")

            elif hour == 1:

                if text.get_subid() == "Hour":
                    text.set_text("1")
                    text.set_x(1170)

    if night_timer > 75:

        hour += 1

        texts[0].set_text(
            str(int(texts[0].get_text()) + 1)
        )

        night_timer = 0

    if fade_alpha > 0:

        fade_alpha -= fade_speed * delta_time

        if fade_alpha < 0:
            fade_alpha = 0

        img[3].set_alpha(fade_alpha)

    if mouse_x < left_border:

        distance = left_border - mouse_x

        speed = (
            distance / left_border
        ) * max_speed

        player_x -= speed * delta_time

    elif mouse_x > right_border:

        distance = mouse_x - right_border

        speed = (
            distance /
            (width - right_border)
        ) * max_speed

        player_x += speed * delta_time

    player_x = max(
        0,
        min(
            player_x,
            width - player.width
        )
    )

    player.x = int(player_x)

    return (
        player_x,
        night_timer,
        hour,
        fade_alpha
    )   