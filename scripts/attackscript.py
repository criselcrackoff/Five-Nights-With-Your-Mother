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

        self.jumpscare_start_delay = 0.0
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
        # FADE DEL BLACKOUT
        # ----------------------------------------------------------

        self.blackout_fade = False
        self.blackout_fade_timer = 0.0

        # Velocidad del negro.
        self.blackout_fade_duration = 3.5

        # ----------------------------------------------------------
        # FADE DEL ANIMATRÓNICO
        # ----------------------------------------------------------
        #
        # El sprite desaparece mucho más rápido que el blackout.
        #

        self.stare_fade_timer = 0.0
        self.stare_fade_duration = 0.45

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
        # ESTADO DE CÁMARA AL LLEGAR A LA PUERTA
        # ==========================================================
        #
        # Guarda si la cámara estaba abierta ANTES de que el
        # animatrónico llegara a la puerta.
        #
        # True  = el jugador ya estaba usando la cámara.
        # False = el jugador abrió la cámara después de que llegó.
        #

        self.door_camera_preexisting = {}

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
    # OCULTAR SPRITES DE OFICINA
    # ==============================================================

    def hide_office_stares(self):

        if self.stare_behind is not None:

            self.stare_behind.set_alpha(
                0
            )

        if self.stare_infront is not None:

            self.stare_infront.set_alpha(
                0
            )

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

            # ------------------------------------------------------
            # Si la cámara está abierta, el sprite NO debe verse.
            # ------------------------------------------------------

            if self.game.ismonitoropen:

                self.hide_office_stares()

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

        # ==============================================================
    # PUERTAS
    # ==============================================================

    def process_door(self, animatronic):

        animatronic_id = animatronic.get_id()

        # ==========================================================
        # DURANTE BLACKOUT
        # ==========================================================
        #
        # Mientras ocurre un blackout, los animatrónicos que
        # ignoran máscara esperan con un timer fijo de 4 segundos.
        #

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
        # REGISTRAR CÓMO ESTABA LA CÁMARA AL LLEGAR
        # ==========================================================
        #
        # Este bloque solamente se ejecuta la primera vez que
        # procesamos al animatrónico estando en la puerta.
        #
        # Por lo tanto, el estado de la cámara aquí representa
        # cómo estaba ANTES/DURANTE su llegada a la puerta.
        #

        if animatronic_id not in self.door_camera_preexisting:

            self.door_camera_preexisting[
                animatronic_id
            ] = self.game.ismonitoropen

            print(
                f"[ATTACK] "
                f"{animatronic.get_name()} "
                f"llegó a puerta. "
                f"Cámara previa: "
                f"{self.game.ismonitoropen}"
            )

        camera_was_open_before = (
            self.door_camera_preexisting[
                animatronic_id
            ]
        )

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

                self.door_camera_preexisting.pop(
                    animatronic_id,
                    None
                )

                return

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

                self.door_camera_preexisting.pop(
                    animatronic_id,
                    None
                )

                return

        # ==========================================================
        # CÁMARA ACTUAL
        # ==========================================================

        camera_open = self.game.ismonitoropen

        # ==========================================================
        # CÁMARA YA ESTABA ABIERTA ANTES DE LLEGAR
        # ==========================================================
        #
        # Si el jugador ya estaba usando la cámara cuando el
        # animatrónico llegó:
        #
        #     intervalo = normal * 3
        #
        # Abrir/cerrar la cámara después no produce el "castigo"
        # de intervalo original mientras el flag siga activo.
        #

        if camera_was_open_before:

            animatronic.set_move_interval(
                self.get_normal_interval(
                    animatronic
                ) * 3
            )

            # ------------------------------------------------------
            # SI EL JUGADOR DEJÓ DE USAR LA CÁMARA
            # ------------------------------------------------------
            #
            # Se elimina el flag.
            #
            # En el siguiente ciclo el animatrónico será tratado
            # como uno que ya no tiene protección por cámara previa.
            #

            if not camera_open:

                print(
                    f"[ATTACK] "
                    f"{animatronic.get_name()} "
                    "-> cámara previa cerrada, "
                    "eliminando flag."
                )

                self.door_camera_preexisting.pop(
                    animatronic_id,
                    None
                )

            return

        # ==========================================================
        # CÁMARA NO ESTABA ABIERTA ANTES
        # ==========================================================
        #
        # Si el jugador NO tenía la cámara abierta cuando el
        # animatrónico llegó:
        #
        # - Cámara cerrada -> intervalo * 3
        # - Cámara abierta después -> intervalo original
        #
        # Esto hace que abrir la cámara DESPUÉS de que el
        # animatrónico llegue a la puerta sea un castigo.
        #

        if camera_open:

            animatronic.set_move_interval(
                self.get_normal_interval(
                    animatronic
                )
            )

            print(
                f"[ATTACK] "
                f"{animatronic.get_name()} "
                "-> cámara abierta después de llegar, "
                "intervalo original."
            )

        else:

            animatronic.set_move_interval(
                self.get_normal_interval(
                    animatronic
                ) * 3
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
        self.stare_fade_timer = 0.0

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

                camera.toggle()

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

            if not self.blackout_masked:

                if not self.blackout_mask_failed:

                    self.blackout_mask_failed = True

                    print(
                        "[ATTACK] "
                        "Tiempo de máscara agotado."
                    )

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

        if time < self.blackout_initial_duration:

            self.blackout_visible = True

            self.set_blackout_visibility()

            return

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
                    50,
                    100
                )
            )

    # ==============================================================
    # MOSTRAR SPRITE EN OFICINA
    # ==============================================================

    def show_office_stare(self, animatronic):

        self.hide_office_stares()

        sprite = animatronic.get_office_sprite()

        if sprite is None:

            print(
                f"[ATTACK] "
                f"{animatronic.get_name()} "
                "no tiene office_sprite."
            )

            return

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

            # ------------------------------------------------------
            # Si la cámara está abierta, nunca mostrarlo.
            # ------------------------------------------------------

            if self.game.ismonitoropen:

                image.set_alpha(
                    0
                )

            else:

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
        self.stare_fade_timer = 0.0

        print(
            "[ATTACK] "
            "Iniciando fade out."
        )

    # ==============================================================
    # UPDATE FADE
    # ==============================================================

    def update_blackout_fade(self, dt):

        # ==========================================================
        # TIMER BLACKOUT
        # ==========================================================

        self.blackout_fade_timer += dt

        # ==========================================================
        # TIMER SPRITE
        # ==========================================================

        self.stare_fade_timer += dt

        # ==========================================================
        # PROGRESO BLACKOUT
        # ==========================================================

        blackout_progress = (
            self.blackout_fade_timer
            /
            self.blackout_fade_duration
        )

        blackout_progress = max(
            0.0,
            min(
                blackout_progress,
                1.0
            )
        )

        # ==========================================================
        # PROGRESO SPRITE
        # ==========================================================

        stare_progress = (
            self.stare_fade_timer
            /
            self.stare_fade_duration
        )

        stare_progress = max(
            0.0,
            min(
                stare_progress,
                1.0
            )
        )

        # ==========================================================
        # ALPHA BLACKOUT
        # ==========================================================

        blackout_alpha = int(
            255
            *
            (1.0 - blackout_progress)
        )

        if self.blackout_image is not None:

            self.blackout_image.set_alpha(
                blackout_alpha
            )

        # ==========================================================
        # ALPHA ANIMATRÓNICO
        # ==========================================================
        #
        # El sprite desaparece independientemente del blackout.
        #

        stare_alpha = int(
            255
            *
            (1.0 - stare_progress)
        )

        if self.stare_behind is not None:

            self.stare_behind.set_alpha(
                stare_alpha
            )

        if self.stare_infront is not None:

            self.stare_infront.set_alpha(
                stare_alpha
            )

        # ==========================================================
        # FADE DEL SPRITE TERMINADO
        # ==========================================================

        if stare_progress >= 1.0:

            self.hide_office_stares()

        # ==========================================================
        # FADE DEL BLACKOUT TERMINADO
        # ==========================================================

        if blackout_progress >= 1.0:

            result = self.blackout_fade_result
            animatronic = self.blackout_animatronic

            # ------------------------------------------------------
            # ASEGURAR TRANSPARENCIA
            # ------------------------------------------------------

            if self.blackout_image is not None:

                self.blackout_image.set_alpha(
                    0
                )

            self.hide_office_stares()

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

        self.hide_office_stares()

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
        self.stare_fade_timer = 0.0

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

            animatronic.reset_position()

            animatronic.set_move_interval(
                self.get_normal_interval(
                    animatronic
                )
            )

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
        # OCULTAR SPRITES DE OFICINA
        # ==========================================================

        self.hide_office_stares()

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

        # ==========================================================
        # CÁMARA
        # ==========================================================

        camera = self.game.get_script(
            "CameraScript"
        )

        if camera is not None:

            if camera.open:

                camera.toggle()

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

        self.game.mixer.stop_all(
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
        self.stare_fade_timer = 0.0

        self.blackout_fade_result = None

        self.door_camera_preexisting.clear()
        if self.blackout_image is not None:

            self.blackout_image.set_alpha(
                0
            )

        self.hide_office_stares()