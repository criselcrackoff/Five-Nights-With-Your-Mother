import pygame


class MixerMusic:

    def __init__(self):
        self.channels = {}
        self.sounds = {}
        self.enabled = False

    def connect(self):
        try:
            pygame.mixer.init()
            self.enabled = True
            print("[Mixer] Initialized.")
        except pygame.error as e:
            self.enabled = False
            print(f"[Mixer] Disabled ({e})")

    def _get_channel(self, channel: int):

        if not self.enabled:
            return None

        if channel not in self.channels:
            self.channels[channel] = pygame.mixer.Channel(channel)

        return self.channels[channel]

    def _get_sound(self, src: str):

        if not self.enabled:
            return None

        if src not in self.sounds:
            self.sounds[src] = pygame.mixer.Sound(src)

        return self.sounds[src]

    def play(self,
             src: str,
             volume: float = 1.0,
             channel: int = 0,
             looping: bool = False):

        if not self.enabled:
            return

        try:
            sound = self._get_sound(src)
            ch = self._get_channel(channel)

            loops = -1 if looping else 0

            ch.set_volume(volume)
            ch.play(sound, loops=loops)
        except pygame.error as e:
            print(f"[Mixer] Play failed: {e}")

    def stop(self,
             channel: int,
             fade_ms: int = 0):

        if not self.enabled:
            return

        try:
            ch = self._get_channel(channel)

            if fade_ms > 0:
                ch.fadeout(fade_ms)
            else:
                ch.stop()
        except pygame.error:
            pass

    def stop_all(self):

        if self.enabled:
            pygame.mixer.stop()

    def set_volume(self,
                   channel: int,
                   volume: float):

        if not self.enabled:
            return

        self._get_channel(channel).set_volume(volume)

    def get_volume(self,
                   channel: int):

        if not self.enabled:
            return 0.0

        return self._get_channel(channel).get_volume()

    def pause(self,
              channel: int):

        if not self.enabled:
            return

        self._get_channel(channel).pause()

    def resume(self,
               channel: int):

        if not self.enabled:
            return

        self._get_channel(channel).unpause()

    def is_playing(self,
                   channel: int):

        if not self.enabled:
            return False

        return self._get_channel(channel).get_busy()

    def change_song(self,
                    src: str,
                    volume: float = 1.0,
                    channel: int = 0,
                    looping: bool = True,
                    fade_ms: int = 1000):

        if not self.enabled:
            return

        self.stop(channel, fade_ms)
        self.play(src, volume, channel, looping)

    def crossfade(self,
                  old_channel: int,
                  new_channel: int,
                  new_song: str,
                  volume: float = 1.0,
                  looping: bool = True,
                  fade_ms: int = 1000):

        if not self.enabled:
            return

        self.play(
            new_song,
            volume,
            new_channel,
            looping
        )

        self.stop(
            old_channel,
            fade_ms
        )

    def unload(self):

        self.sounds.clear()