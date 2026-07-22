from engine.scripts import Script
from data.sounds import *
from data.game_images import *
import pygame


class CameraScript(Script):

    def __init__(self, game):
        super().__init__(game)

        self.open = False
        self.camera = 1
        
        self.cameranimation = self.game.monitor
        self.blipanimation = self.game.get_image("blip")

        self.mouse_in_trigger = False
        self.trigger_padding = 20
        self.camera_feed = self.game.get_image("background")
        self.button = self.game.get_image("CameraBar")

        for image in self.game.images:

            if image.get_id() == "LeftButton":
                self.left = image

            elif image.get_id() == "RightButton":
                self.right = image
        self.leftbg = self.game.get_image("LeftButtonbg")
        self.desk = self.game.get_image("Desk")
        self.leftdoor = self.game.get_image("LeftDoor")
        self.rightdoor = self.game.get_image("RightDoor")
        self.maskbar = self.game.get_image("MaskBar")
        
        # 
        # Camera Elements
        #

        self.waiting_blip = False
        self.waiting_animation = False
        self.map = self.game.get_image("Map")
        self.maurello = self.game.get_image("maurellobg")
        self.animatronics = [self.game.maurello]
        self.botonescamara = {}
        for image in self.game.images:
            if image.get_id() == "Cambutton":
                self.botonescamara[int(image.get_subid())] = image
                
        self.camera_button_sprites = {
            1: (cam1off, cam1on),
            2: (cam2off, cam2on),
            3: (cam3off, cam3on),
            4: (cam4off, cam4on),
            5: (cam5off, cam5on),
        }
            


    def event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_s:
                self.toggle()
            
            if event.key == pygame.K_i:
                self.camera -= 1
                self.start_blip()
                self.show_camera_feed()
            if event.key == pygame.K_o:
                self.camera += 1
                self.start_blip()
                self.show_camera_feed()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if not self.open or self.waiting_animation:
                return
            
            ui = self.game.UI_SCALE
            mouse = event.pos

            for camera_id, boton in self.botonescamara.items():

                rect = pygame.Rect(
                    int(boton.get_x() * ui),
                    int(boton.get_y() * ui),
                    boton.get_surface_width(),
                    boton.get_surface_height()
                )

                if rect.collidepoint(mouse):
                    self.change_camera(camera_id)
                    break

    def update(self, dt):

        mouse = (self.game.mouse_x, self.game.mouse_y)
        ui = self.game.UI_SCALE
        camera_zone = pygame.Rect(
            int(self.button.get_x() * ui) - self.trigger_padding,
            int(self.button.get_y() * ui) - self.trigger_padding,
            self.button.get_surface_width() + self.trigger_padding * 2,
            self.button.get_surface_height() + self.trigger_padding * 2
            )

        inside = camera_zone.collidepoint(mouse)

        if inside and not self.mouse_in_trigger:
            self.mouse_in_trigger = True
            self.toggle()

        elif not inside:
            self.mouse_in_trigger = False

        if self.waiting_blip and self.blipanimation.is_finished():
            self.waiting_blip = False
            self.blipanimation.set_alpha(0)

        if self.waiting_animation and self.cameranimation.is_finished():

            if self.open:
                self.show_camera_feed()
                self.hide_office_elements()
                self.start_blip()
            self.waiting_animation = False
            self.cameranimation.set_alpha(0)
            
        refresh = False

        for anim in self.animatronics:
            if anim.needs_refresh:
                refresh = True
                anim.needs_refresh = False

        if refresh and self.open:
            self.show_camera_feed()

    def start_blip(self):
        self.game.mixer.play(Blip,volume=0.2,channel=self.game.CHANNEL_MONITOR)
        self.waiting_blip = True
        self.blipanimation.set_alpha(255)
        self.blipanimation.restart()

    def toggle(self):

        if self.waiting_animation:
            return

        mask = self.game.get_script("MaskScript")

        if mask:

            if mask.waiting_animation:
                return

            if mask.open:
                mask.close_mask()

        self.game.mixer.play(Tablet,volume=0.2,channel=self.game.CHANNEL_MONITOR)

        if self.open:
            self.close_camera()
        else:
            self.open_camera()

    def open_camera(self):

        self.open = True
        self.game.ismonitoropen = True
        self.game.usage += 1

        self.waiting_animation = True

        self.cameranimation.set_alpha(255)
        self.cameranimation.play()

    def close_camera(self):

        self.open = False
        self.game.ismonitoropen = False
        self.game.usage -= 1

        self.waiting_animation = True
        self.show_office_elements()
        self.hide_camera_feed()
        self.cameranimation.set_alpha(255)
        self.blipanimation.set_alpha(0)
        self.cameranimation.play(reverse=True)

    def change_camera(self, new_camera):

        if new_camera == self.camera:
            return

        # Desactivar botón anterior
        self.botonescamara[self.camera].change_image(
            self.camera_button_sprites[self.camera][0]
        )

        # Activar botón nuevo
        self.botonescamara[new_camera].change_image(
            self.camera_button_sprites[new_camera][1]
        )

        self.camera = new_camera

        self.start_blip()
        self.show_camera_feed()

    def show_camera_feed(self):
        self.show_camera_buttons()
        self.show_camera_bg()

        # Ocultar placeholder por defecto
        self.maurello.set_alpha(0)

        # Dibujar animatrónicos presentes en esta cámara
        for anim in self.animatronics:

            if anim.get_camera() != self.camera:
                continue

            self.maurello.change_image(
                anim.get_sprite()
            )

            self.maurello.set_size(
                anim.get_size()
            )

            self.maurello.set_x(
                anim.get_x()
            )

            self.maurello.set_y(
                anim.get_y()
            )

            self.maurello.set_alpha(255)

        self.map.set_alpha(255)
    def show_camera_bg(self):
        if self.camera == 1:
            self.camera_feed.change_image(cam1)

        elif self.camera == 2:
            self.camera_feed.change_image(cam2)

        elif self.camera == 3:
            self.camera_feed.change_image(cam3)

        elif self.camera == 4:
            self.camera_feed.change_image(cam4)

        elif self.camera == 5:
            self.camera_feed.change_image(cam5)

        else:
            self.camera_feed.change_image(unavailable)
    def hide_camera_feed(self):
        self.hide_camera_buttons()
        self.map.set_alpha(0)

        self.maurello.set_alpha(0)

        self.camera_feed.change_image(comoffice)
    def toggle_office_elements(self):
        if self.open:
            self.hide_office_elements()
        else:
            self.show_office_elements()
    def show_camera_buttons(self):

        for boton in self.botonescamara.values():
            boton.set_alpha(255)

    def hide_camera_buttons(self):

        for boton in self.botonescamara.values():
            boton.set_alpha(0)
    def show_office_elements(self):
        self.left.set_y(390)
        self.leftbg.set_y(236)
        self.right.set_y(390)
        self.desk.set_alpha(255)
        self.leftdoor.set_y(0)
        self.rightdoor.set_y(0)
        self.maskbar.set_alpha(255)
    def hide_office_elements(self):
        self.left.set_y(990)
        self.leftbg.set_y(990)
        self.right.set_y(990)
        self.desk.set_alpha(0)
        self.leftdoor.set_y(990)
        self.rightdoor.set_y(990)
        self.maskbar.set_alpha(0)