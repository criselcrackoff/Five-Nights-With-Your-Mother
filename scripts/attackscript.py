from engine.scripts import Script


class AttackScript(Script):

    def __init__(self, game):
        super().__init__(game)

        # ==========================================================
        # ESTADO GENERAL
        # ==========================================================

        self.jumpscare_active = False
        self.jumpscare_animatronic = None

        self.jumpscare_image = None

        # ==========================================================
        # TEMPORIZADOR GAME OVER
        # ==========================================================
        #
        # Después de terminar la animación de jumpscare,
        # mantenemos el último frame visible durante este tiempo.
        #

        self.gameover_timer = 0.0
        self.gameover_delay = 2.0

        self.jumpscare_finished = False

        # ==========================================================
        # INTERVALOS NORMALES
        # ==========================================================

        self.maurello_normal_interval = (
            self.game.maurello.get_move_interval()
        )

        self.furry_normal_interval = (
            self.game.furry.get_move_interval()
        )

        # ==========================================================
        # MAURELLO
        # ==========================================================

        self.maurello_attack_door = None
        self.maurello_waiting_at_door = False

        # ==========================================================
        # FURRY
        # ==========================================================

        self.furry_attack_door = None
        self.furry_waiting_at_door = False

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
        # MAURELLO
        # ==========================================================

        maurello = self.game.maurello

        if maurello.get_ignoremask():

            # ------------------------------------------------------
            # PUERTA DERECHA
            # ------------------------------------------------------

            if maurello.get_camera() == "door_right":

                self.maurello_attack_door = "Right"
                self.maurello_waiting_at_door = True

                maurello.set_move_interval(
                    self.maurello_normal_interval * 3
                )

                if self.game.RIGHT_DOOR == "Closed":

                    maurello.reset_position()

                    maurello.set_move_interval(
                        self.maurello_normal_interval
                    )

                    self.maurello_attack_door = None
                    self.maurello_waiting_at_door = False

            # ------------------------------------------------------
            # OFICINA
            # ------------------------------------------------------

            elif maurello.get_camera() == "office":

                maurello.set_move_interval(
                    self.maurello_normal_interval
                )

                self.maurello_waiting_at_door = False

                self.start_jumpscare(
                    maurello
                )

        # ==========================================================
        # FURRY
        # ==========================================================

        furry = self.game.furry

        if furry.get_ignoremask():

            # ------------------------------------------------------
            # PUERTA IZQUIERDA
            # ------------------------------------------------------

            if furry.get_camera() == "door_left":

                self.furry_attack_door = "Left"
                self.furry_waiting_at_door = True

                furry.set_move_interval(
                    self.furry_normal_interval * 3
                )

                if self.game.LEFT_DOOR == "Closed":

                    furry.reset_position()

                    furry.set_move_interval(
                        self.furry_normal_interval
                    )

                    self.furry_attack_door = None
                    self.furry_waiting_at_door = False

            # ------------------------------------------------------
            # OFICINA
            # ------------------------------------------------------

            elif furry.get_camera() == "office":

                furry.set_move_interval(
                    self.furry_normal_interval
                )

                self.furry_waiting_at_door = False

                self.start_jumpscare(
                    furry
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
        self.gameover_timer = 0.0

        print(
            f"[ATTACK] "
            f"{animatronic.get_name()} -> JUMPSCARE"
        )

        # ==========================================================
        # OBTENER ANIMACIÓN
        # ==========================================================

        self.jumpscare_image = self.game.get_image(
            "jumpscare"
        )

        if self.jumpscare_image is None:

            print(
                "[ATTACK] ERROR: "
                "No se encontró la animación "
                "'jumpscare' en game.images."
            )

            self.jumpscare_active = False
            self.jumpscare_animatronic = None

            return

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

            self.game.mask.set_alpha(0)

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

            self.game.monitor.set_alpha(0)

            camera.hide_camera_feed()
            camera.show_office_elements()

        # ==========================================================
        # DATOS DEL JUMPSCARE
        # ==========================================================

        jumpscare = animatronic.get_jumpscare()

        if not jumpscare:

            print(
                f"[ATTACK] "
                f"{animatronic.get_name()} "
                f"no tiene jumpscare definido."
            )

            self.jumpscare_active = False
            self.jumpscare_animatronic = None

            return

        # ==========================================================
        # SONIDO
        # ==========================================================

        if len(jumpscare) >= 1:

            sound = jumpscare[0]

            self.game.mixer.play(
                sound,
                volume=1.0,
                channel=self.game.CHANNEL_SFX
            )

        # ==========================================================
        # ANIMACIÓN
        # ==========================================================

        if len(jumpscare) >= 2:

            animation_folder = jumpscare[1]

            try:

                self.jumpscare_image.change_folder(
                    animation_folder
                )

            except Exception as error:

                print(
                    "[ATTACK] ERROR cargando "
                    f"animación de jumpscare: {error}"
                )

                self.jumpscare_active = False
                self.jumpscare_animatronic = None

                return

            print(
                f"[ATTACK] Animación: "
                f"{animation_folder}"
            )

        else:

            print(
                f"[ATTACK] "
                f"{animatronic.get_name()} "
                f"no tiene animación de jumpscare."
            )

        # ==========================================================
        # FADE
        # ==========================================================

        fadein = self.game.get_image(
            "fadein"
        )

        if fadein is not None:

            fadein.set_alpha(0)

        # ==========================================================
        # ASEGURAR ORDEN DE DIBUJADO
        # ==========================================================
        #
        # El jumpscare debe estar al final de game.images para
        # quedar por encima de la oficina, HUD, puertas, etc.
        #

        if self.jumpscare_image in self.game.images:

            self.game.images.remove(
                self.jumpscare_image
            )

        self.game.images.append(
            self.jumpscare_image
        )

        # ==========================================================
        # MOSTRAR JUMPSCARE
        # ==========================================================

        self.jumpscare_image.set_alpha(
            255
        )

        self.jumpscare_image.play()

        print(
            "[ATTACK] Animación iniciada."
        )

        print(
            "[ATTACK] Reproduciendo: "
            f"{self.jumpscare_image.is_playing()}"
        )

        print(
            "[ATTACK] Frames: "
            f"{self.jumpscare_image.get_total_frames()}"
        )

    # ==============================================================
    # UPDATE JUMPSCARE
    # ==============================================================

    def update_jumpscare(self, dt):

        if self.jumpscare_image is None:
            return

        # ==========================================================
        # ETAPA 1:
        # ANIMACIÓN EN CURSO
        # ==========================================================

        if not self.jumpscare_finished:

            if self.jumpscare_image.is_playing():

                return

            # ======================================================
            # LA ANIMACIÓN TERMINÓ
            # ======================================================
            #
            # NO cambiamos todavía a Game Over.
            #
            # El último frame permanece visible.
            #

            self.jumpscare_finished = True
            self.gameover_timer = 0.0

            print(
                "[ATTACK] "
                "Jumpscare terminado."
            )

            print(
                "[ATTACK] "
                f"Esperando {self.gameover_delay} segundos "
                "antes de Game Over."
            )

            return

        # ==========================================================
        # ETAPA 2:
        # ESPERAR ANTES DE GAME OVER
        # ==========================================================

        self.gameover_timer += dt

        if self.gameover_timer < self.gameover_delay:

            return

        # ==========================================================
        # ETAPA 3:
        # GAME OVER
        # ==========================================================

        self.finish_gameover()

    # ==============================================================
    # GAME OVER
    # ==============================================================

    def finish_gameover(self):

        print(
            "[ATTACK] "
            "Jumpscare -> Game Over"
        )

        # ==========================================================
        # OCULTAR JUMPSCARE
        # ==========================================================

        if self.jumpscare_image is not None:

            self.jumpscare_image.set_alpha(
                0
            )

        # ==========================================================
        # CAMBIAR RECURSOS
        # ==========================================================

        self.game.texts = self.game.GAMEOVER_TEXTS
        self.game.images = self.game.GAMEOVER_IMG

        # ==========================================================
        # DETENER AMBIENTE
        # ==========================================================

        self.game.mixer.stop(
            self.game.CHANNEL_AMBIENT,
            250
        )

        # ==========================================================
        # LIMPIAR SCRIPTS
        # ==========================================================

        self.game.scripts = []

        # ==========================================================
        # ESTADO GAME OVER
        # ==========================================================

        self.game.SUBGAMESTATE = "GameOver"
        self.game.GAMESTATE = "menu"

        # ==========================================================
        # LIMPIAR ESTADO
        # ==========================================================

        self.jumpscare_active = False
        self.jumpscare_animatronic = None
        self.jumpscare_finished = False
        self.gameover_timer = 0.0

    # ==============================================================
    # RESET DEL SCRIPT
    # ==============================================================

    def reset(self):

        self.jumpscare_active = False
        self.jumpscare_animatronic = None

        self.jumpscare_image = None

        self.jumpscare_finished = False
        self.gameover_timer = 0.0

        self.maurello_attack_door = None
        self.maurello_waiting_at_door = False

        self.furry_attack_door = None
        self.furry_waiting_at_door = False