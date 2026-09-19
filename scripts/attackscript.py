from data.sounds import *
from engine.scripts import Script

import random


class AttackScript(Script):

    def __init__(self, game):

        super().__init__(game)

        # ==========================================================
        # ANIMATRÓNICOS
        # ==========================================================

        self.animatronics = [
            self.game.maurello,
            self.game.furry,
            self.game.teddy
        ]

        # ==========================================================
        # JUMPSCARE
        # ==========================================================

        self.jumpscare_active = False
        self.jumpscare_animatronic = None
        self.jumpscare_image = None

        self.jumpscare_finished = False

        # ----------------------------------------------------------
        # ESPERA ANTES DE INICIAR ANIMACIÓN
        # ----------------------------------------------------------

        self.jumpscare_start_delay = 1.0
        self.jumpscare_start_timer = 0.0
        self.jumpscare_animation_started = False
        self.jumpscare_has_animation = False

        # ----------------------------------------------------------
        # GAME OVER
        # ----------------------------------------------------------

        self.gameover_timer = 0.0
        self.gameover_delay = 2.0

        # ==========================================================
        # BLACKOUT
        # ==========================================================

        self.blackout_active = False
        self.blackout_animatronic = None

        self.blackout_timer = 0.0

        # ----------------------------------------------------------
        # TIEMPO TOTAL DEL BLACKOUT
        # ----------------------------------------------------------

        self.blackout_duration = 4.8

        # ----------------------------------------------------------
        # TIEMPO LÍMITE PARA LA MÁSCARA
        # ----------------------------------------------------------

        self.blackout_mask_deadline = 1.6

        # ----------------------------------------------------------
        # FASES DEL BLACKOUT
        # ----------------------------------------------------------

        self.blackout_initial_duration = 0.3
        self.blackout_rapid_duration = 1.3
        self.blackout_sparse_duration = 1.6
        self.blackout_final_duration = 1.6

        # ----------------------------------------------------------
        # PARPADEO
        # ----------------------------------------------------------

        self.blackout_visible = True

        # ----------------------------------------------------------
        # ESTADO DE LA MÁSCARA
        # ----------------------------------------------------------

        self.blackout_masked = False
        self.blackout_mask_failed = False

        # ----------------------------------------------------------
        # RESULTADO DEL BLACKOUT
        # ----------------------------------------------------------

        self.blackout_fade_result = None

        # ----------------------------------------------------------
        # FADE OUT
        # ----------------------------------------------------------

        self.blackout_fade = False
        self.blackout_fade_timer = 0.0
        self.blackout_fade_duration = 3.5

        # ==========================================================
        # IMÁGENES
        # ==========================================================

        self.blackout_image = None
        self.stare_behind = None
        self.stare_infront = None

        self.load_images()

        # ==========================================================
        # INTERVALOS NORMALES
        # ==========================================================

        self.normal_intervals = {}

        for animatronic in self.animatronics:

            self.normal_intervals[
                animatronic.get_id()
            ] = animatronic.get_move_interval()

        # ==========================================================
        # ANIMATRÓNICO QUE DEBE RECIBIR EL BOOST
        # ==========================================================

        self.office_cleared_animatronic = None

    # ==============================================================
    # IMÁGENES
    # ==============================================================

    def load_images(self):

        self.blackout_image = self.game.get_image(
            "blackout"
        )

        self.stare_behind = self.game.get_image(
            "stare_behind_desk"
        )

        self.stare_infront = self.game.get_image(
            "stare_infront_desk"
        )

        if self.blackout_image is not None:

            self.blackout_image.set_alpha(0)

        if self.stare_behind is not None:

            self.stare_behind.set_alpha(0)

        if self.stare_infront is not None:

            self.stare_infront.set_alpha(0)

    # ==============================================================
    # UPDATE
    # ==============================================================

    def update(self, dt):

        # ==========================================================
        # JUMPSCARE
        # ==========================================================

        if self.jumpscare_active:

            self.update_jumpscare(dt)

            return

        # ==========================================================
        # BLACKOUT
        # ==========================================================

        if self.blackout_active:

            if self.blackout_fade:

                self.update_blackout_fade(dt)

            else:

                self.update_blackout(dt)

            return

        # ==========================================================
        # ANIMATRÓNICOS
        # ==========================================================

        for animatronic in self.animatronics:

            animatronic.update(dt)

        # ==========================================================
        # PROCESAR POSICIONES ESPECIALES
        # ==============================================================

        for animatronic in self.animatronics:

            self.process_animatronic(
                animatronic
            )

    # ==============================================================
    # PROCESAR ANIMATRÓNICO
    # ==============================================================

    def process_animatronic(self, animatronic):

        # ==========================================================
        # OFFICE
        # ==========================================================

        if animatronic.is_office():

            # ------------------------------------------------------
            # IGNOREMASK = TRUE
            # ------------------------------------------------------

            if animatronic.get_ignoremask():

                if not self.jumpscare_active:

                    self.start_jumpscare(
                        animatronic
                    )

                return

            # ------------------------------------------------------
            # IGNOREMASK = FALSE
            # ------------------------------------------------------

            if not self.blackout_active:

                self.start_blackout(
                    animatronic
                )

            return

        # ==========================================================
        # WAIT ROOM
        # ==============================================================

        if animatronic.is_wait_room():

            self.process_wait_room(
                animatronic
            )

            return

        # ==========================================================
        # PUERTAS
        # ==============================================================

        if animatronic.is_door():

            self.process_door(
                animatronic
            )

    # ==============================================================
    # WAIT ROOM
    # ==============================================================

    def process_wait_room(self, animatronic):

        # ==========================================================
        # ¿HAY ALGUIEN EN LA OFICINA?
        # ==========================================================

        if self.is_office_occupied():

            animatronic.set_move_timer(
                0.0
            )

            print(
                f"[ATTACK] "
                f"{animatronic.get_name()} "
                f"esperando en wait_room."
            )

            return

        # ==========================================================
        # NO HAY NADIE
        # ==========================================================

        print(
            f"[ATTACK] "
            f"{animatronic.get_name()} "
            "-> OFFICE"
        )

        animatronic.move()

        # ==========================================================
        # SI LLEGÓ A OFFICE
        # ==========================================================

        if animatronic.is_office():

            if animatronic.get_ignoremask():

                self.start_jumpscare(
                    animatronic
                )

            else:

                self.start_blackout(
                    animatronic
                )

    # ==============================================================
    # PUERTAS
    # ==============================================================

    def process_door(self, animatronic):

        # ==========================================================
        # DURANTE BLACKOUT
        # ==========================================================

        if self.blackout_active:

            if animatronic.get_ignoremask():

                animatronic.set_move_timer(
                    4.0
                )

                return

        # ==========================================================
        # IGNOREMASK FALSE
        # ==========================================================

        if not animatronic.get_ignoremask():

            return

        # ==========================================================
        # PUERTA IZQUIERDA
        # ==========================================================

        if animatronic.get_camera() == "door_left":

            if self.game.LEFT_DOOR == "Closed":

                print(
                    f"[ATTACK] "
                    f"{animatronic.get_name()} "
                    "detenido por puerta izquierda."
                )

                animatronic.reset_position()

                return

            animatronic.set_move_interval(
                self.get_normal_interval(animatronic) * 3
            )

        # ==========================================================
        # PUERTA DERECHA
        # ==========================================================

        elif animatronic.get_camera() == "door_right":

            if self.game.RIGHT_DOOR == "Closed":

                print(
                    f"[ATTACK] "
                    f"{animatronic.get_name()} "
                    "detenido por puerta derecha."
                )

                animatronic.reset_position()

                return

            animatronic.set_move_interval(
                self.get_normal_interval(animatronic) * 3
            )

    # ==============================================================
    # INTERVALO NORMAL
    # ==============================================================

    def get_normal_interval(self, animatronic):

        return self.normal_intervals.get(
            animatronic.get_id(),
            5.0
        )

    # ==============================================================
    # OFICINA OCUPADA
    # ==============================================================

    def is_office_occupied(self):

        for animatronic in self.animatronics:

            if not animatronic.is_office():

                continue

            return True

        return False

    # ==============================================================
    # BLACKOUT
    # ==============================================================

    def start_blackout(self, animatronic):

        if self.blackout_active:

            return

        if self.jumpscare_active:

            return

        self.blackout_active = True
        self.blackout_animatronic = animatronic

        self.blackout_timer = 0.0

        self.blackout_visible = True

        self.blackout_masked = False
        self.blackout_mask_failed = False

        self.blackout_fade = False
        self.blackout_fade_timer = 0.0

        self.blackout_fade_result = None

        print(
            f"[ATTACK] "
            f"{animatronic.get_name()} "
            "-> BLACKOUT"
        )

        # ==========================================================
        # SPRITE
        # ==========================================================

        self.show_office_stare(
            animatronic
        )

        # ==========================================================
        # NEGRO INICIAL
        # ==========================================================

        if self.blackout_image is not None:

            self.blackout_image.set_alpha(
                255
            )

        # ==========================================================
        # SONIDO STARE
        # ==========================================================

        try:

            self.game.mixer.play(
                Stare,
                volume=0.1,
                channel=self.game.CHANNEL_SFX
            )

        except Exception as error:

            print(
                "[ATTACK] Error reproduciendo "
                f"Stare.mp3: {error}"
            )

        # ==========================================================
        # CERRAR CÁMARA
        # ==========================================================

        camera = self.game.get_script(
            "CameraScript"
        )

        if camera is not None:

            if camera.open:

                camera.close_camera()

            camera.open = False

            self.game.ismonitoropen = False

            camera.waiting_animation = False

            if self.game.monitor is not None:

                self.game.monitor.set_alpha(
                    0
                )

            camera.hide_camera_feed()
            camera.show_office_elements()

        # ==========================================================
        # CERRAR MÁSCARA
        # ==========================================================

        mask = self.game.get_script(
            "MaskScript"
        )

        if mask is not None:

            if mask.open:

                mask.close_mask()

            mask.open = False

            self.game.ismaskopen = False

            mask.waiting_animation = False

            if self.game.mask is not None:

                self.game.mask.set_alpha(
                    0
                )

    # ==============================================================
    # UPDATE BLACKOUT
    # ==============================================================

    def update_blackout(self, dt):

        animatronic = self.blackout_animatronic

        if animatronic is None:

            self.end_blackout(
                avoided=False
            )

            return

        # ==========================================================
        # TIEMPO
        # ==========================================================

        self.blackout_timer += dt

        # ==========================================================
        # MÁSCARA
        # ==========================================================

        if self.blackout_timer <= self.blackout_mask_deadline:

            if self.game.ismaskopen:

                if not self.blackout_masked:

                    self.blackout_masked = True

                    print(
                        "[ATTACK] "
                        "Máscara colocada a tiempo."
                    )

            else:

                self.blackout_masked = False

        else:

            # ======================================================
            # DEADLINE SUPERADO
            # ======================================================

            if not self.blackout_masked:

                if not self.blackout_mask_failed:

                    self.blackout_mask_failed = True

                    print(
                        "[ATTACK] "
                        "Tiempo de máscara agotado."
                    )

            # ======================================================
            # LA MÁSCARA FUE QUITADA
            # ======================================================

            if (
                self.blackout_masked
                and not self.game.ismaskopen
            ):

                self.blackout_masked = False
                self.blackout_mask_failed = True

                print(
                    "[ATTACK] "
                    "Máscara retirada -> "
                    "protección perdida."
                )

        # ==========================================================
        # PARPADEO
        # ==========================================================

        self.update_blackout_blink()

        # ==========================================================
        # BLACKOUT TERMINADO
        # ==========================================================

        if self.blackout_timer >= self.blackout_duration:

            print(
                "[ATTACK] "
                "Blackout terminado."
            )

            # ------------------------------------------------------
            # ATAQUE EVITADO
            # ------------------------------------------------------

            if (
                self.blackout_masked
                and self.game.ismaskopen
            ):

                print(
                    "[ATTACK] "
                    "Blackout evitado -> "
                    "reiniciando animatrónico."
                )

                self.blackout_fade_result = "avoid"

                self.begin_blackout_fade()

                return

            # ------------------------------------------------------
            # ATAQUE FALLIDO
            # ------------------------------------------------------

            print(
                "[ATTACK] "
                "Blackout fallido -> "
                "iniciando fade antes del jumpscare."
            )

            self.blackout_fade_result = "jumpscare"

            self.begin_blackout_fade()

    # ==============================================================
    # PARPADEO DEL BLACKOUT
    # ==============================================================

    def update_blackout_blink(self):

        time = self.blackout_timer

        # ==========================================================
        # FASE 1
        # ==========================================================

        if time < self.blackout_initial_duration:

            self.blackout_visible = True

            self.set_blackout_visibility()

            return

        # ==========================================================
        # FASE 2
        # ==========================================================

        rapid_end = (
            self.blackout_initial_duration
            +
            self.blackout_rapid_duration
        )

        if time < rapid_end:

            self.update_blink(
                probability=0.50
            )

            return

        # ==========================================================
        # FASE 3
        # ==========================================================

        sparse_end = (
            rapid_end
            +
            self.blackout_sparse_duration
        )

        if time < sparse_end:

            self.update_blink(
                probability=0.07
            )

            return

        # ==========================================================
        # FASE 4
        # ==========================================================

        self.blackout_visible = True

        self.set_blackout_visibility()

    # ==============================================================
    # BLINK
    # ==============================================================

    def update_blink(self, probability):

        self.blackout_visible = (
            random.random()
            >= probability
        )

        self.set_blackout_visibility()

    # ==============================================================
    # VISIBILIDAD DEL NEGRO
    # ==============================================================

    def set_blackout_visibility(self):

        if self.blackout_image is None:

            return

        if self.blackout_visible:

            self.blackout_image.set_alpha(
                255
            )

        else:

            self.blackout_image.set_alpha(
                random.randint(
                    0,
                    50
                )
            )

    # ==============================================================
    # MOSTRAR SPRITE EN OFICINA
    # ==============================================================

    def show_office_stare(self, animatronic):

        # Ocultar ambos

        if self.stare_behind is not None:

            self.stare_behind.set_alpha(
                0
            )

        if self.stare_infront is not None:

            self.stare_infront.set_alpha(
                0
            )

        sprite = animatronic.get_office_sprite()

        if sprite is None:

            print(
                f"[ATTACK] "
                f"{animatronic.get_name()} "
                "no tiene office_sprite."
            )

            return

        # ==========================================================
        # POSICIÓN
        # ==========================================================

        if animatronic.get_name() == "Teddy":

            image = self.stare_infront

        else:

            image = self.stare_behind

        if image is None:

            return

        try:

            image.change_image(
                sprite
            )

            image.set_size(
                animatronic.get_size()
            )

            image.set_x(
                animatronic.get_x()
            )

            image.set_y(
                animatronic.get_y()
            )

            image.set_alpha(
                255
            )

        except Exception as error:

            print(
                "[ATTACK] Error cargando "
                f"office_sprite: {error}"
            )

    # ==============================================================
    # FADE BLACKOUT
    # ==============================================================

    def begin_blackout_fade(self):

        if self.blackout_fade:

            return

        self.blackout_fade = True
        self.blackout_fade_timer = 0.0

        print(
            "[ATTACK] "
            "Iniciando fade out del blackout."
        )

    # ==============================================================
    # UPDATE FADE
    # ==============================================================

    def update_blackout_fade(self, dt):

        self.blackout_fade_timer += dt

        progress = (
            self.blackout_fade_timer
            /
            self.blackout_fade_duration
        )

        progress = max(
            0.0,
            min(
                progress,
                1.0
            )
        )

        # ==========================================================
        # FADE 255 -> 0
        # ==========================================================

        alpha = int(
            255
            *
            (1.0 - progress)
        )

        # ==========================================================
        # BLACKOUT
        # ==========================================================

        if self.blackout_image is not None:

            self.blackout_image.set_alpha(
                alpha
            )

        # ==========================================================
        # STARE
        # ==========================================================
        #
        # IMPORTANTE:
        #
        # Antes solamente hacíamos fade del blackout.
        # Ahora el sprite del animatrónico también desaparece.
        #

        if self.stare_behind is not None:

            self.stare_behind.set_alpha(
                alpha
            )

        if self.stare_infront is not None:

            self.stare_infront.set_alpha(
                alpha
            )

        # ==========================================================
        # FADE TERMINADO
        # ==========================================================

        if progress >= 1.0:

            result = self.blackout_fade_result
            animatronic = self.blackout_animatronic

            # ------------------------------------------------------
            # Asegurar que TODO quede transparente
            # ------------------------------------------------------

            if self.blackout_image is not None:

                self.blackout_image.set_alpha(
                    0
                )

            if self.stare_behind is not None:

                self.stare_behind.set_alpha(
                    0
                )

            if self.stare_infront is not None:

                self.stare_infront.set_alpha(
                    0
                )

            # ------------------------------------------------------
            # BLACKOUT EVITADO
            # ------------------------------------------------------

            if result == "avoid":

                self.end_blackout(
                    avoided=True
                )

                return

            # ------------------------------------------------------
            # BLACKOUT FALLIDO
            # ------------------------------------------------------

            if result == "jumpscare":

                if animatronic is not None:

                    self.start_jumpscare(
                        animatronic
                    )

                else:

                    self.end_blackout(
                        avoided=False
                    )

    # ==============================================================
    # END BLACKOUT
    # ==============================================================

    def end_blackout(self, avoided=False):

        animatronic = self.blackout_animatronic

        # ==========================================================
        # OCULTAR NEGRO
        # ==========================================================

        if self.blackout_image is not None:

            self.blackout_image.set_alpha(
                0
            )

        # ==========================================================
        # OCULTAR SPRITES
        # ==========================================================

        if self.stare_behind is not None:

            self.stare_behind.set_alpha(
                0
            )

        if self.stare_infront is not None:

            self.stare_infront.set_alpha(
                0
            )

        # ==========================================================
        # LIMPIAR ESTADO
        # ==========================================================

        self.blackout_active = False
        self.blackout_animatronic = None

        self.blackout_timer = 0.0

        self.blackout_visible = False

        self.blackout_masked = False
        self.blackout_mask_failed = False

        self.blackout_fade = False
        self.blackout_fade_timer = 0.0

        self.blackout_fade_result = None

        # ==========================================================
        # ATAQUE EVITADO
        # ==========================================================

        if avoided and animatronic is not None:

            print(
                f"[ATTACK] "
                f"{animatronic.get_name()} "
                "blackout evitado."
            )

            # ------------------------------------------------------
            # REINICIAR POSICIÓN
            # ------------------------------------------------------

            animatronic.reset_position()

            # ------------------------------------------------------
            # RESTAURAR INTERVALO NORMAL
            # ------------------------------------------------------

            animatronic.set_move_interval(
                self.get_normal_interval(
                    animatronic
                )
            )

            # ------------------------------------------------------
            # BOOST DE 1 SEGUNDO
            # ------------------------------------------------------

            animatronic.set_move_timer(
                1.0
            )

            self.office_cleared_animatronic = (
                animatronic
            )

    # ==============================================================
    # JUMPSCARE
    # ==============================================================

    def start_jumpscare(self, animatronic):

        if self.jumpscare_active:

            return

        self.jumpscare_active = True
        self.jumpscare_animatronic = animatronic

        self.jumpscare_finished = False

        self.jumpscare_start_timer = 0.0
        self.jumpscare_animation_started = False
        self.jumpscare_has_animation = False

        self.gameover_timer = 0.0

        print(
            f"[ATTACK] "
            f"{animatronic.get_name()} -> JUMPSCARE"
        )

        # ==========================================================
        # TERMINAR BLACKOUT
        # ==========================================================

        if self.blackout_active:

            self.end_blackout(
                avoided=False
            )

        # ==========================================================
        # OBTENER IMAGEN
        # ==========================================================

        self.jumpscare_image = self.game.get_image(
            "jumpscare"
        )

        # ==========================================================
        # MÁSCARA
        # ==========================================================

        mask = self.game.get_script(
            "MaskScript"
        )

        if mask is not None:

            if mask.open:

                mask.close_mask()

            mask.open = False

            self.game.ismaskopen = False

            mask.waiting_animation = False

            if self.game.mask is not None:

                self.game.mask.set_alpha(
                    0
                )

        # ==========================================================
        # CÁMARA
        # ==========================================================

        camera = self.game.get_script(
            "CameraScript"
        )

        if camera is not None:

            if camera.open:

                camera.close_camera()

            camera.open = False

            self.game.ismonitoropen = False

            camera.waiting_animation = False

            if self.game.monitor is not None:

                self.game.monitor.set_alpha(
                    0
                )

            camera.hide_camera_feed()
            camera.show_office_elements()

        # ==========================================================
        # JUMPSCARE DATA
        # ==========================================================

        jumpscare = animatronic.get_jumpscare()

        if not jumpscare:

            print(
                f"[ATTACK] "
                f"{animatronic.get_name()} "
                "no tiene jumpscare definido."
            )

            self.jumpscare_active = False

            return

        # ==========================================================
        # SONIDO
        # ==========================================================

        sound = animatronic.get_jumpscare_sound()

        if sound is not None:

            self.game.mixer.play(
                sound,
                volume=0.2,
                channel=self.game.CHANNEL_SFX
            )

        # ==========================================================
        # ANIMACIÓN
        # ==========================================================

        animation_folder = (
            animatronic.get_jumpscare_animation()
        )

        if (
            self.jumpscare_image is not None
            and animation_folder is not None
        ):

            try:

                self.jumpscare_image.change_folder(
                    animation_folder
                )

                # --------------------------------------------------
                # DETENER ANIMACIÓN
                # --------------------------------------------------
                #
                # El frame 0 queda visible durante
                # jumpscare_start_delay.
                #

                self.jumpscare_image.stop()

                self.jumpscare_image.set_frame(
                    0
                )

                self.jumpscare_image.set_alpha(
                    255
                )

                self.jumpscare_has_animation = True

                if self.jumpscare_image in self.game.images:

                    self.game.images.remove(
                        self.jumpscare_image
                    )

                self.game.images.append(
                    self.jumpscare_image
                )

                print(
                    "[ATTACK] "
                    "Frame inicial del jumpscare "
                    "preparado."
                )

            except Exception as error:

                print(
                    "[ATTACK] ERROR cargando "
                    f"animación: {error}"
                )

                self.jumpscare_has_animation = False

                self.jumpscare_image.stop()

                self.jumpscare_image.set_alpha(
                    0
                )

        else:

            # ======================================================
            # AUDIO ONLY
            # ======================================================
            #
            # Teddy actualmente solamente tiene sonido.
            #

            self.jumpscare_has_animation = False

            if self.jumpscare_image is not None:

                self.jumpscare_image.stop()

                self.jumpscare_image.set_alpha(
                    0
                )

        # ==========================================================
        # FADE
        # ==========================================================

        fadein = self.game.get_image(
            "fadein"
        )

        if fadein is not None:

            fadein.set_alpha(
                0
            )

    # ==============================================================
    # UPDATE JUMPSCARE
    # ==============================================================

    def update_jumpscare(self, dt):

        # ==========================================================
        # ESPERA INICIAL
        # ==========================================================
        #
        # El frame 0 permanece quieto durante 1 segundo.
        #
        # IMPORTANTE:
        #
        # No debemos interpretar "playing = False" como que
        # terminó el jumpscare, porque nosotros mismos lo
        # detenemos durante esta espera.
        #

        if not self.jumpscare_animation_started:

            self.jumpscare_start_timer += dt

            if (
                self.jumpscare_start_timer
                <
                self.jumpscare_start_delay
            ):

                return

            # ======================================================
            # INICIAR ANIMACIÓN
            # ======================================================

            if (
                self.jumpscare_has_animation
                and self.jumpscare_image is not None
            ):

                print(
                    "[ATTACK] "
                    "Iniciando animación del jumpscare."
                )

                self.jumpscare_image.set_alpha(
                    255
                )

                self.jumpscare_image.play()

                self.jumpscare_animation_started = True

                return

            # ======================================================
            # JUMPSCARE SIN ANIMACIÓN
            # ======================================================

            print(
                "[ATTACK] "
                "Jumpscare sin animación."
            )

            self.jumpscare_animation_started = True
            self.jumpscare_finished = True
            self.gameover_timer = 0.0

            return

        # ==========================================================
        # ANIMACIÓN
        # ==========================================================

        if not self.jumpscare_finished:

            if self.jumpscare_has_animation:

                if (
                    self.jumpscare_image is not None
                    and self.jumpscare_image.is_playing()
                ):

                    return

            # ======================================================
            # ANIMACIÓN TERMINADA
            # ======================================================

            self.jumpscare_finished = True
            self.gameover_timer = 0.0

            print(
                "[ATTACK] "
                "Jumpscare terminado."
            )

            return

        # ==========================================================
        # GAME OVER DELAY
        # ==========================================================

        self.gameover_timer += dt

        if self.gameover_timer < self.gameover_delay:

            return

        self.finish_gameover()

    # ==============================================================
    # GAME OVER
    # ==============================================================

    def finish_gameover(self):

        print(
            "[ATTACK] "
            "Jumpscare -> Game Over"
        )

        if self.jumpscare_image is not None:

            self.jumpscare_image.set_alpha(
                0
            )

        self.game.texts = self.game.GAMEOVER_TEXTS
        self.game.images = self.game.GAMEOVER_IMG

        self.game.mixer.stop(
            self.game.CHANNEL_AMBIENT,
            250
        )

        self.game.scripts = []

        self.game.SUBGAMESTATE = "GameOver"
        self.game.GAMESTATE = "menu"

        self.jumpscare_active = False
        self.jumpscare_animatronic = None

        self.jumpscare_finished = False

        self.jumpscare_start_timer = 0.0
        self.jumpscare_animation_started = False
        self.jumpscare_has_animation = False

        self.gameover_timer = 0.0

    # ==============================================================
    # RESET
    # ==============================================================

    def reset(self):

        self.jumpscare_active = False
        self.jumpscare_animatronic = None
        self.jumpscare_image = None

        self.jumpscare_finished = False

        self.jumpscare_start_timer = 0.0
        self.jumpscare_animation_started = False
        self.jumpscare_has_animation = False

        self.gameover_timer = 0.0

        self.blackout_active = False
        self.blackout_animatronic = None

        self.blackout_timer = 0.0

        self.blackout_visible = False

        self.blackout_masked = False
        self.blackout_mask_failed = False

        self.blackout_fade = False
        self.blackout_fade_timer = 0.0

        self.blackout_fade_result = None

        if self.blackout_image is not None:

            self.blackout_image.set_alpha(
                0
            )

        if self.stare_behind is not None:

            self.stare_behind.set_alpha(
                0
            )

        if self.stare_infront is not None:

            self.stare_infront.set_alpha(
                0
            )