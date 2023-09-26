from ursina import *
import os
from lang_config import en, lang_config
from themes_config import *


class MainMenu(Entity):

    def __init__(self, LANGUAGE, THEME):
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

        # Init Menu

        btn_login = Button(
            text=lang_config[LANGUAGE]["login"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.init_menu,
            x=-0.15,
            y=-0.15,
            scale_x=0.2,
            scale_y=0.08
        )

        btn_register = Button(
            text=lang_config[LANGUAGE]["register"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.init_menu,
            x=0.15,
            y=-0.15,
            scale_x=0.2,
            scale_y=0.08
        )
