import psycopg2
from psycopg2 import ProgrammingError
from ursina import *

import themes_config
from lang_config import lang_config
from themes_config import themes


class MainMenu(Entity):

    def __init__(self, LANGUAGE, THEME):
        super().__init__(
            parent=camera.ui
        )

        # Initialise menus:
        self.init_menu = Entity(parent=self, enabled=True)
        self.login_menu = Entity(parent=self, enabled=False)
        self.register_menu = Entity(parent=self, enabled=False)
        self.register_success_menu = Entity(parent=self, enabled=False)
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

        def btn_login_init_event():
            self.lbl_login_msg.text = ""
            self.login_menu.enabled = True
            self.init_menu.enabled = False

        self.btn_login_init = Button(
            text=lang_config[LANGUAGE]["login"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.init_menu,
            x=-0.15,
            y=-0.1,
            scale_x=themes[THEME]["button_scale_x"],
            scale_y=themes[THEME]["button_scale_y"]
        )
        self.btn_login_init.on_click = btn_login_init_event

        self.btn_register_init = Button(
            text=lang_config[LANGUAGE]["register"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.init_menu,
            x=0.15,
            y=-0.1,
            scale_x=themes[THEME]["button_scale_x"],
            scale_y=themes[THEME]["button_scale_y"]
        )
        self.btn_register_init.on_click = self.btn_register_init_event

        self.btn_quit_init = Button(
            text=lang_config[LANGUAGE]["quit"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.init_menu,
            y=-0.2,
            scale_x=themes[THEME]["button_scale_x"],
            scale_y=themes[THEME]["button_scale_y"]
        )
        self.btn_quit_init.on_click = self.btn_quit_event

        # Login Menu

        self.login_menu_back = Entity(
            model="cube",
            color=themes[THEME]["ui_background"],
            scale_x=0.6,
            scale_y=0.5,
            position_z=1,
            parent=self.login_menu
        )

        self.lbl_login_msg = Text(
            text="",
            x=-0.25,
            parent=self.login_menu
        )

        self.lbl_username = Text(
            text=lang_config[LANGUAGE]["username"],
            x=-0.25,
            y=0.2,
            parent=self.login_menu
        )

        self.lbl_password = Text(
            text=lang_config[LANGUAGE]["password"],
            x=-0.25,
            y=0.1,
            parent=self.login_menu
        )

        self.txt_username_login = InputField(
            color=color.black,
            y=0.15,
            parent=self.login_menu
        )

        self.txt_password_login = InputField(
            color=color.black,
            y=0.05,
            parent=self.login_menu
        )

        self.txt_username_login.next_field = self.txt_password_login
        self.txt_password_login.next_field = self.txt_username_login

        def btn_login_event():
            connection = psycopg2.connect(
                host="127.0.0.1",
                database="postgres",
                user="postgres",
                password="root"
            )
            query = """SELECT * from public.python_users WHERE username = %s AND password = %s AND online_status = false;"""
            row = []
            cursor = connection.cursor()
            try:
                values = [
                    self.txt_username_login.text,
                    self.txt_password_login.text
                ]
                cursor.execute(query, values)
                row = cursor.fetchone()
                print(str(type(row)))
                print(str(row))
                print(str(row[0]))
            except:
                self.lbl_login_msg.text = lang_config[LANGUAGE]["login_error"]
            cursor.close()
            connection.close()
            if row is not None and len(row) > 0:
                self.lbl_login_msg.text = ""
                self.txt_username_login.clear()
                self.txt_password_login.clear()
                self.main_menu.enabled = True
                self.login_menu.enabled = False
            else:
                self.lbl_login_msg.text = lang_config[LANGUAGE]["login_error"]


        self.btn_login = Button(
            text=lang_config[LANGUAGE]["login"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.login_menu,
            x=-0.15,
            y=-0.15,
            scale_x=themes[THEME]["button_scale_x"],
            scale_y=themes[THEME]["button_scale_y"]
        )
        self.btn_login.on_click = btn_login_event

        self.btn_back_login = Button(
            text=lang_config[LANGUAGE]["return"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.login_menu,
            x=0.15,
            y=-0.15,
            scale_x=themes[THEME]["button_scale_x"],
            scale_y=themes[THEME]["button_scale_y"],
            onclick=Func(self.btn_back_event)
        )
        self.btn_back_login.on_click = self.btn_back_event

        # Register Menu

        self.register_menu_back = Entity(
            model="cube",
            color=themes[THEME]["ui_background"],
            scale_x=0.6,
            scale_y=0.6,
            position_z=1,
            parent=self.register_menu
        )

        self.lbl_username = Text(
            text=lang_config[LANGUAGE]["username"],
            x=-0.25,
            y=0.25,
            parent=self.register_menu
        )

        self.lbl_password = Text(
            text=lang_config[LANGUAGE]["password"],
            x=-0.25,
            y=0.15,
            parent=self.register_menu
        )

        self.lbl_email = Text(
            text=lang_config[LANGUAGE]["email"],
            x=-0.25,
            y=0.05,
            parent=self.register_menu
        )

        self.lbl_register_msg = Text(
            text="",
            x=-0.25,
            y=-0.05,
            parent=self.register_menu
        )

        self.txt_username_register = InputField(
            color=color.black,
            y=0.2,
            parent=self.register_menu
        )

        self.txt_password_register = InputField(
            color=color.black,
            y=0.1,
            parent=self.register_menu
        )

        self.txt_email_register = InputField(
            color=color.black,
            parent=self.register_menu
        )

        self.txt_username_register.next_field = self.txt_password_register
        self.txt_password_register.next_field = self.txt_email_register
        self.txt_email_register.next_field = self.txt_username_register

        def btn_register_event():
            if len(self.txt_username_register.text) < 1:
                self.lbl_register_msg.text = lang_config[LANGUAGE]["register_missing_username"]
                return
            if len(self.txt_password_register.text) < 1:
                self.lbl_register_msg.text = lang_config[LANGUAGE]["register_missing_password"]
                return
            if len(self.txt_email_register.text) < 1:
                self.lbl_register_msg.text = lang_config[LANGUAGE]["register_missing_email"]
                return
            connection = psycopg2.connect(
                host="127.0.0.1",
                database="postgres",
                user="postgres",
                password="root"
            )
            query = """INSERT INTO public.python_users(username, password, email, online_status, current_client) VALUES(%s,%s,%s,false,null);"""
            values = [
                self.txt_username_register.text,
                self.txt_password_register.text,
                self.txt_email_register.text,
            ]
            cursor = connection.cursor()
            try:
                cursor.execute(query, values)
                self.lbl_register_msg.text = ""
                self.txt_username_register.clear()
                self.txt_password_register.clear()
                self.txt_email_register.clear()
                self.register_success_menu.enabled = True
                self.register_menu.enabled = False
            except psycopg2.Error:
                self.lbl_register_msg.text = lang_config[LANGUAGE]["register_error"]
            connection.commit()
            cursor.close()
            connection.close()

        self.btn_register = Button(
            text=lang_config[LANGUAGE]["register"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.register_menu,
            x=-0.15,
            y=-0.2,
            scale_x=themes[THEME]["button_scale_x"],
            scale_y=themes[THEME]["button_scale_y"]
        )
        self.btn_register.on_click = btn_register_event

        self.btn_back_register = Button(
            text=lang_config[LANGUAGE]["return"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.register_menu,
            x=0.15,
            y=-0.2,
            scale_x=themes[THEME]["button_scale_x"],
            scale_y=themes[THEME]["button_scale_y"]
        )
        self.btn_back_register.on_click = self.btn_back_event

        # Register Success Menu

        lbl_register_success = Text(
            text=lang_config[LANGUAGE]["register_success"],
            origin=(0, 0),
            y=-0.05,
            parent=self.register_success_menu
        )

        self.btn_back_register_success = Button(
            text=lang_config[LANGUAGE]["return"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.register_success_menu,
            y=-0.2,
            scale_x=themes[THEME]["button_scale_x"],
            scale_y=themes[THEME]["button_scale_y"]
        )
        self.btn_back_register_success.on_click = self.btn_back_event

        # Main Menu

        self.btn_quit_main = Button(
            text=lang_config[LANGUAGE]["quit"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.main_menu,
            x=-0.15,
            y=-0.2,
            scale_x=themes[THEME]["button_scale_x"],
            scale_y=themes[THEME]["button_scale_y"]
        )
        self.btn_quit_main.on_click = self.btn_quit_event

        def btn_logout_main_event():
            self.init_menu.enabled = True
            self.main_menu.enabled = False

        self.btn_logout_main = Button(
            text=lang_config[LANGUAGE]["logout"],
            color=themes[THEME]["ui_button"],
            highlight_color=themes[THEME]["ui_button"],
            parent=self.main_menu,
            x=0.15,
            y=-0.2,
            scale_x=themes[THEME]["button_scale_x"],
            scale_y=themes[THEME]["button_scale_y"]
        )
        self.btn_logout_main._on_click = btn_logout_main_event

    def btn_register_init_event(self):
        self.register_menu.enabled = True
        self.init_menu.enabled = False

    def btn_quit_event(self):
        quit()

    def btn_back_event(self):
        if self.login_menu.enabled:
            self.init_menu.enabled = True
            self.login_menu.enabled = False
        if self.register_menu.enabled:
            self.init_menu.enabled = True
            self.register_menu.enabled = False
        if self.register_success_menu.enabled:
            self.init_menu.enabled = True
            self.register_success_menu.enabled = False

    def input(self, key):
        if key == Keys.escape:
            if self.login_menu.enabled:
                self.init_menu.enabled = True
                self.login_menu.enabled = False
            if self.register_menu.enabled:
                self.init_menu.enabled = True
                self.register_menu.enabled = False
            if self.register_success_menu.enabled:
                self.init_menu.enabled = True
                self.register_success_menu.enabled = False
