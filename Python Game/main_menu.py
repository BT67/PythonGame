from ursina import *
import os
from lang_config import en
from themes_config import *


class MainMenu(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui
        )

        # Initialise menus:
        self.init_menu = Entity(parent=self, enable=True)
        self.login_menu = Entity(parent=self, enabled=False)
        self.register_menu = Entity(parent=self, enable=False)
        self.main_menu = Entity(parent=self, enabled=False)
        self.singleplayer_menu = Entity(parent=self, enabled=False)
        self.multiplayer_menu = Entity(parent=self, enabled=False)
        self.settings_menu = Entity(parent=self, enabled=False)
        self.video_menu = Entity(parent=self, enabled=False)
        self.gameplay_menu = Entity(parent=self, enabled=False)
        self.audio_menu = Entity(parent=self, enabled=False)
        self.controls_menu = Entity(parent=self, enabled=False)
        self.pause_menu = Entity(parent=self, enabled=False)
        self.quit_menu = Entity(parent=self, enabled=False)

        self.menus = [
            self.init_menu,
            self.login_menu,
            self.register_menu,
            self.main_menu,
            self.singleplayer_menu,
            self.multiplayer_menu,
            self.settings_menu,
            self.video_menu,
            self.gameplay_menu,
            self.audio_menu,
            self.controls_menu,
            self.pause_menu,
            self.quit_menu,
        ]

        # UI audio
        self.click = Audio("click.wav", False, False, volume=10)

        def quit():
            application.quit()
            os._exit(0)

        # Init Menu

        btn_login = Button(
            text=en.login,
            color=theme.ui_button,
            highlight_color=theme.ui_button_highlight,
            parent=self.init_menu
        )

        btn_register = Button(
            text=en.register,
            color=theme.ui_button,
            highlight_color=theme.ui_button_highlight,
            parent=self.init_menu
        )

        # Main Menu

        singleplayer_button = Button(text="Singleplayer", color=color.gray, highlight_color=color.light_gray,
                                     scale_y=0.1, scale_x=0.3, y=0.05, parent=self.start_menu)
        multiplayer_button = Button(text="Multiplayer", color=color.gray, highlight_color=color.light_gray, scale_y=0.1,
                                    scale_x=0.3, y=-0.08, parent=self.start_menu)

        # Quit Menu
        def quit():
            application.quit()
            os._exit(0)

        def dont_quit():
            self.quit_menu.disable()
            self.start_menu.enable()

        quit_text = Text("Are you sure you want to quit?", scale=1.5, line_height=2, x=0, origin=0, y=0.2,
                         parent=self.quit_menu)
        quit_yes = Button(text="Yes", color=color.black, scale_y=0.1, scale_x=0.3, y=0.05, parent=self.quit_menu)
        quit_no = Button(text="No", color=color.black, scale_y=0.1, scale_x=0.3, y=-0.07, parent=self.quit_menu)

        quit_yes.on_click = Func(quit)
        quit_no.on_click = Func(dont_quit)

        # Host Server Menu

        # Server Menu

        # Main Menu

        # Settings

        def settings():
            self.main_menu.disable()
            self.settings_menu.enable()

        def video():
            self.settings_menu.disable()
            self.video_menu.enable()

        def gameplay():
            self.settings_menu.disable()
            self.gameplay_menu.enable()

        def audio():
            self.settings_menu.disable()
            self.audio_menu.enable()

        def controls():
            self.settings_menu.disable()
            self.controls_menu.enable()

        def back_settings():
            self.settings_menu.disable()
            self.main_menu.enable()

        settings_button = Button(text="Settings", color=color.black, scale_y=0.1, scale_x=0.3, y=-0.22,
                                 parent=self.main_menu)

        video_button = Button(text="Video", color=color.black, scale_y=0.1, scale_x=0.3, y=0.24,
                              parent=self.settings_menu)
        gameplay_button = Button(text="Gameplay", color=color.black, scale_y=0.1, scale_x=0.3, y=0.12,
                                 parent=self.settings_menu)
        audio_button = Button(text="Audio", color=color.black, scale_y=0.1, scale_x=0.3, y=0, parent=self.settings_menu)
        controls_button = Button(text="Controls", color=color.black, scale_y=0.1, scale_x=0.3, y=-0.12,
                                 parent=self.settings_menu)

        back_button_settings = Button(text="Back", color=color.black, scale_y=0.1, scale_x=0.3, y=-0.24,
                                      parent=self.settings_menu)

        settings_button.on_click = Func(settings)
        video_button.on_click = Func(video)
        gameplay_button.on_click = Func(gameplay)
        audio_button.on_click = Func(audio)
        controls_button.on_click = Func(controls)
        back_button_settings.on_click = Func(back_settings)

        # Video Menu

        def fullscreen():
            window.fullscreen = not window.fullscreen
            if window.fullscreen:
                fullscreen_button.text = "Fullscreen: On"
            elif window.fullscreen == False:
                fullscreen_button.text = "Fullscreen: Off"

        def borderless():
            window.borderless = not window.borderless
            if window.borderless:
                borderless_button.text = "Borderless: On"
            elif window.borderless == False:
                borderless_button.text = "Borderless: Off"
            window.exit_button.enable()

        def fps():
            window.fps_counter.enabled = not window.fps_counter.enabled
            if window.fps_counter.enabled:
                fps_button.text = "FPS: On"
            elif window.fps_counter.enabled == False:
                fps_button.text = "FPS: Off"

        def exit_button_func():
            window.exit_button.enabled = not window.exit_button.enabled
            if window.exit_button.enabled:
                exit_button.text = "Exit Button: On"
            elif window.exit_button.enabled == False:
                exit_button.text = "Exit Button: Off"

        def back_video():
            self.video_menu.disable()
            self.settings_menu.enable()

        fullscreen_button = Button("Fullscreen: On", color=color.black, scale_y=0.1, scale_x=0.3, y=0.24,
                                   parent=self.video_menu)
        borderless_button = Button("Borderless: On", color=color.black, scale_y=0.1, scale_x=0.3, y=0.12,
                                   parent=self.video_menu)
        fps_button = Button("FPS: Off", color=color.black, scale_y=0.1, scale_x=0.3, y=0, parent=self.video_menu)
        exit_button = Button("Exit Button: Off", color=color.black, scale_y=0.1, scale_x=0.3, y=-0.12,
                             parent=self.video_menu)
        back_button_video = Button(text="Back", color=color.black, scale_y=0.1, scale_x=0.3, y=-0.24,
                                   parent=self.video_menu)

        fullscreen_button.on_click = Func(fullscreen)
        borderless_button.on_click = Func(borderless)
        fps_button.on_click = Func(fps)
        exit_button.on_click = Func(exit_button_func)
        back_button_video.on_click = Func(back_video)

        # Audio Menu

        def audio_func():
            if self.car.audio:
                audio_button.text = "Audio: Off"
                self.volume.value = 0
            elif not self.car.audio:
                audio_button.text = "Audio: On"
                self.volume.value = 1
            self.car.audio = not self.car.audio

        def back_audio():
            self.audio_menu.disable()
            self.settings_menu.enable()

        audio_button = Button("Audio: On", color=color.black, scale_y=0.1, scale_x=0.3, y=0, parent=self.audio_menu)
        back_button_audio = Button(text="Back", color=color.black, scale_y=0.1, scale_x=0.3, y=-0.12,
                                   parent=self.audio_menu)

        self.volume = Slider(min=0, max=1, default=1, text="Volume", y=0.2, x=-0.3, scale=1.3, parent=self.audio_menu,
                             dynamic=True)
        self.volume.step = 0.1

        audio_button.on_click = Func(audio_func)
        back_button_audio.on_click = Func(back_audio)

        # Controls

        def back_controls():
            self.controls_menu.disable()
            self.settings_menu.enable()

        def controls_settings():
            if self.car.controls == "wasd":
                self.car.controls = "zqsd"
                controls_settings_button.text = "Controls: ZQSD"
                drive_controls_text.text = "Drive: Z"
                steering_controls_text.text = "Steering: Q D"
            elif self.car.controls == "zqsd":
                self.car.controls = "wasd"
                controls_settings_button.text = "Controls: WASD"
                drive_controls_text.text = "Drive: W"
                steering_controls_text.text = "Steering: A D"

        drive_controls_text = Button("Drive: W", color=color.black, scale_y=0.1, scale_x=0.3, x=-0.5, y=0.3,
                                     parent=self.controls_menu)
        steering_controls_text = Button("Steering: A D", color=color.black, scale_y=0.1, scale_x=0.3, x=0, y=0.3,
                                        parent=self.controls_menu)
        braking_controls_text = Button("Braking: S", color=color.black, scale_y=0.1, scale_x=0.3, x=0.5, y=0.3,
                                       parent=self.controls_menu)
        handbraking_controls_text = Button("Hand Brake: SPACE", color=color.black, scale_y=0.1, scale_x=0.3, x=-0.5,
                                           y=0.1, parent=self.controls_menu)
        respawn_controls_text = Button("Respawn: G", color=color.black, scale_y=0.1, scale_x=0.3, x=0, y=0.1,
                                       parent=self.controls_menu)
        controls_settings_button = Button("Controls: WASD", color=color.black, scale_y=0.1, scale_x=0.3, y=-0.2,
                                          parent=self.controls_menu)
        back_button_controls = Button(text="Back", color=color.black, scale_y=0.1, scale_x=0.3, y=-0.32,
                                      parent=self.controls_menu)

        back_button_controls.on_click = Func(back_controls)
        controls_settings_button.on_click = Func(controls_settings)

        # Pause Menu

        def resume():
            mouse.locked = True
            self.pause_menu.disable()

        def main_menu():
            self.main_menu.enable()
            self.pause_menu.disable()

        p_resume_button = Button(text="Resume", color=color.black, scale_y=0.1, scale_x=0.3, y=0.11,
                                 parent=self.pause_menu)
        p_respawn_button = Button(text="Respawn", color=color.black, scale_y=0.1, scale_x=0.3, y=-0.01,
                                  parent=self.pause_menu)
        p_mainmenu_button = Button(text="Main Menu", color=color.black, scale_y=0.1, scale_x=0.3, y=-0.13,
                                   parent=self.pause_menu)
        p_mainmenu_button.on_click = Func(main_menu)
        p_resume_button.on_click = Func(resume)

    def input(self, key):
        # Pause menu
        if not self.start_menu.enabled and not self.main_menu.enabled and not self.server_menu.enabled and not self.settings_menu.enabled and not self.race_menu.enabled and not self.maps_menu.enabled and not self.settings_menu.enabled and not self.garage_menu.enabled and not self.audio_menu.enabled and not self.controls_menu.enabled and not self.host_menu.enabled and not self.created_server_menu.enabled and not self.video_menu.enabled and not self.gameplay_menu.enabled and not self.quit_menu.enabled:
            if key == "escape":
                self.pause_menu.enabled = not self.pause_menu.enabled
                mouse.locked = not mouse.locked

        # Quit Menu
        if self.start_menu.enabled or self.quit_menu.enabled:
            if key == "escape":
                self.quit_menu.enabled = not self.quit_menu.enabled
                self.start_menu.enabled = not self.start_menu.enabled

        # Settings Menu
        if key == "escape":
            if self.settings_menu.enabled:
                self.settings_menu.disable()
                self.main_menu.enable()
            elif self.video_menu.enabled:
                self.video_menu.disable()
                self.settings_menu.enable()
            elif self.controls_menu.enabled:
                self.controls_menu.disable()
                self.settings_menu.enable()
            elif self.gameplay_menu.enabled:
                self.gameplay_menu.disable()
                self.settings_menu.enable()
            elif self.audio_menu.enabled:
                self.audio_menu.disable()
                self.settings_menu.enable()
