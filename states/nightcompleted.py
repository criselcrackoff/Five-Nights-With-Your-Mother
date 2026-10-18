from data.sounds import *
import time

def night_completed_main(game):

    game.discord.update_rpc(
        state=f"",
        details="Night Finished!"
    )

    game.timer += game.delta_time
    bar_thing=None
    for image in game.images:
        if image.get_id() == "bar_thingy":
            bar_thing = image
            x=bar_thing.get_x()
    x+=32
    bar_thing.set_x(x)
    if bar_thing.get_x() >= 0:
        bar_thing.set_x(-1280)
