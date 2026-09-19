from data.sounds import *
from scripts.reset import ResetScript

def gameover_main(game):
    game.discord.update_rpc(
            state="",
            details="In a menu"
        )

    game.timer += game.delta_time

    if game.timer >= 10 or game.mouse_clicked:
        reset = game.get_script(ResetScript)

        if reset:
            reset.reset(2)