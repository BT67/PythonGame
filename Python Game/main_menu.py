import psycopg2
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
        self.init_menu = Entity(parent=self, enabled=True)
        self.login_menu = Entity(parent=self, enabled=False)
        self.register_menu = Entity(parent=self, enabled=False)
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

        # Init Menu Buttons

        btn_login_init = Button(
            text=lang_config[LANGUAGE]["login"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.init_menu,
            x=-0.15,
            y=-0.1,
            scale_x=0.2,
            scale_y=0.08,
        )
        btn_login_init.on_click = self.btn_login_init_event

        btn_register_init = Button(
            text=lang_config[LANGUAGE]["register"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.init_menu,
            x=0.15,
            y=-0.1,
            scale_x=0.2,
            scale_y=0.08,
        )
        btn_register_init.on_click = self.btn_register_init_event

        btn_quit_init = Button(
            text=lang_config[LANGUAGE]["quit"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.init_menu,
            y=-0.2,
            scale_x=0.2,
            scale_y=0.08,
        )
        btn_quit_init.on_click = self.btn_quit_event

        # Login Menu

        login_menu_back = Entity(
            model="cube",
            color=themes[THEME]["ui_background"],
            scale_x=0.6,
            scale_y=0.5,
            position_z=1,
            parent=self.login_menu
        )

        lbl_username = Text(
            text=lang_config[LANGUAGE]["username"],
            x=-0.25,
            y=0.2,
            parent=self.login_menu
        )

        lbl_password = Text(
            text=lang_config[LANGUAGE]["password"],
            x=-0.25,
            y=0.1,
            parent=self.login_menu
        )

        txt_username_login = InputField(
            color=color.black,
            y=0.15,
            parent=self.login_menu
        )

        txt_password_login = InputField(
            color=color.black,
            y=0.05,
            parent=self.login_menu
        )

        def btn_login_event():
            connection = psycopg2.connect(
                host="127.0.0.1",
                database="postgres",
                user="postgres",
                password="root"
            )
            query = """SELECT * from public.python_users WHERE username = %s AND password = %s AND online_status = false;"""
            values = [
                txt_username_login.text,
                txt_password_login.text
            ]
            cursor = connection.cursor()
            cursor.execute(query, values)
            row = cursor.fetchone()
            print(str(row))
            cursor.close()
            connection.close()

        btn_login = Button(
            text=lang_config[LANGUAGE]["login"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.login_menu,
            x=-0.15,
            y=-0.15,
            scale_x=0.2,
            scale_y=0.08,
        )
        btn_login.on_click = btn_login_event

        btn_back_login = Button(
            text=lang_config[LANGUAGE]["return"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.login_menu,
            x=0.15,
            y=-0.15,
            scale_x=0.2,
            scale_y=0.08,
            onclick=Func(self.btn_back_event)
        )
        btn_back_login.on_click = self.btn_back_event

        # Register Menu Buttons

        register_menu_back = Entity(
            model="cube",
            color=themes[THEME]["ui_background"],
            scale_x=0.6,
            scale_y=0.6,
            position_z=1,
            parent=self.register_menu
        )

        lbl_username = Text(
            text=lang_config[LANGUAGE]["username"],
            x=-0.25,
            y=0.25,
            parent=self.register_menu
        )

        lbl_password = Text(
            text=lang_config[LANGUAGE]["password"],
            x=-0.25,
            y=0.15,
            parent=self.register_menu
        )

        lbl_email = Text(
            text=lang_config[LANGUAGE]["email"],
            x=-0.25,
            y=0.05,
            parent=self.register_menu
        )

        txt_username_register = InputField(
            color=color.black,
            y=0.2,
            parent=self.register_menu
        )

        txt_password_register = InputField(
            color=color.black,
            y=0.1,
            parent=self.register_menu
        )

        txt_email_register = InputField(
            color=color.black,
            parent=self.register_menu
        )

        def btn_register_event():
            connection = psycopg2.connect(
                host="127.0.0.1",
                database="postgres",
                user="postgres",
                password="root"
            )
            query = """INSERT INTO public.python_users(username, password, email, online_status, current_client) VALUES(%s,%s,%s,false,null);"""
            values = [
                txt_username_register.text,
                txt_password_register.text,
                txt_email_register.text,
            ]
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()

        btn_register = Button(
            text=lang_config[LANGUAGE]["register"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.register_menu,
            x=-0.15,
            y=-0.2,
            scale_x=0.2,
            scale_y=0.08,
        )
        btn_register.on_click = btn_register_event

        btn_back_register = Button(
            text=lang_config[LANGUAGE]["return"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.register_menu,
            x=0.15,
            y=-0.2,
            scale_x=0.2,
            scale_y=0.08,
        )
        btn_back_register.on_click = self.btn_back_event

    def btn_login_init_event(self):
        self.login_menu.enabled = True
        self.init_menu.enabled = False

    def btn_register_init_event(self):
        self.register_menu.enabled = True
        self.init_menu.enabled = False

    def btn_login_event(self):
        print("login event")

    def btn_quit_event(self):
        quit()

    def btn_back_event(self):
        if self.login_menu.enabled:
            self.init_menu.enabled = True
            self.login_menu.enabled = False
        if self.register_menu.enabled:
            self.init_menu.enabled = True
            self.register_menu.enabled = False

    def input(self, key):
        if key == Keys.escape:
            if self.login_menu.enabled:
                self.init_menu.enabled = True
                self.login_menu.enabled = False
            if self.register_menu.enabled:
                self.init_menu.enabled = True
                self.register_menu.enabled = False
