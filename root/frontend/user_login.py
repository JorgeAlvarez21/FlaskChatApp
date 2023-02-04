import flet as ft
import requests
import time
import sys
import path
import json

sys.path.append(path.Path(__file__).abspath().parent.parent.parent)
from root import settings

class UserLoginView(ft.UserControl):
    def __init__(self, page):

        super().__init__()
        self.page = page

    def build(self):
        username = ft.Ref[ft.TextField]()
        password = ft.Ref[ft.TextField]()


        def login_request(e):
            data = {
                "username": username.current.value,
                "password": password.current.value,
            }

            login = requests.post(f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/user/login", json=data)
            if login.status_code == 200:
                self.page.session.set("username", username.current.value)
                self.page.session.set('logged_in', True)
                self.page.go('/home')
                self.page.update()

        _gradient_color_1 = "#ffffff"
        _gradient_color_2 = "#ffffff"

        _title_color = '#4457c6'

        def register_url(e):
            self.page.go('/register')
            self.page.update()


        def radio_check(e):
            if e.control.icon_color == ft.colors.BLACK:
                e.control.icon=ft.icons.RADIO_BUTTON_CHECKED
                e.control.icon_color= ft.colors.RED
                e.control.update()
            else:
                e.control.icon=ft.icons.RADIO_BUTTON_OFF
                e.control.icon_color= ft.colors.BLACK
                e.control.update()

        main_content = ft.Row(
            alignment="center",
            spacing=0,
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(
                            width=552,
                            height=750,
                            border=ft.border.all(2, ft.colors.BLACK),

                            border_radius=ft.border_radius.all(20),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=[_gradient_color_1, _gradient_color_2],
                            ),
                            content=ft.Column(
                                height=90,
                                spacing=0,
                                horizontal_alignment=ft.CrossAxisAlignment("center"),
                                expand=True,
                                controls=[

                                    ft.Container(
                                        height=65,
                                        border_radius=ft.border_radius.only(topLeft=17, topRight=17),
                                        bgcolor=_title_color,
                                                 content= ft.Container(alignment=ft.alignment.center,
                                                                       border=ft.border.only(
                                                                           bottom=ft.border.BorderSide(2,
                                                                                            ft.colors.BLACK)),
                                        content=ft.Text(
                                            "Log in", color=ft.colors.WHITE, weight="w500",
                                            style=ft.TextThemeStyle.DISPLAY_SMALL
                                        ),
                                    ),),


                                    ft.Container(
                                        height=550,
                                        width=350,
                                        content=ft.Column(
                                            spacing=2,
                                            controls=[
                                                ft.Container(margin = ft.margin.only(top=80),
                                                    padding=ft.padding.only(
                                                        left=5, right=5
                                                    ),
                                                    content=ft.TextField(
                                                        ref=username,
                                                        border_color=ft.colors.BLACK,
                                                        focused_border_width=3,
                                                        border_radius=ft.border_radius.all(
                                                            10
                                                        ),
                                                        border_width=2, border='underline',
                                                        prefix_icon=ft.icons.PERSON,
                                                        hint_text='Username',
                                                        expand=True,
                                                        height=40,
                                                        content_padding=ft.padding.only(
                                                            bottom=6, left=10
                                                        ),
                                                    ),
                                                ),
                                                ft.Container(
                                                    margin=ft.margin.only(top=60),
                                                    content=ft.TextField(
                                                        ref=password,
                                                        border_color=ft.colors.BLACK,
                                                        prefix_icon=ft.icons.LOCK,
                                                        border='underline', hint_text='Password',
                                                        password=True,
                                                        can_reveal_password=True,
                                                        border_radius=ft.border_radius.all(
                                                            10
                                                        ),
                                                        expand=True,
                                                        height=40,
                                                        content_padding=ft.padding.only(
                                                            bottom=6, left=10
                                                        ),
                                                    ),
                                                ),
                                                ft.Container(alignment=ft.alignment.center, margin=ft.margin.only(
                                                    top=10),
                                                        content=ft.Row(spacing=0, controls=[ft.IconButton(
                                                            ft.icons.RADIO_BUTTON_OFF, icon_color=ft.colors.BLACK,
                                                            on_click=radio_check,
                                                            icon_size=16),
                                                                                 ft.Text('Remember me',
                                                                                              size=16)])),

                                                ft.Container(
                                                    alignment=ft.alignment.center,
                                                    padding=ft.padding.only(
                                                        top=40, left=20
                                                    ),
                                                    content=ft.ElevatedButton(
                                                        style=ft.ButtonStyle(bgcolor={"":_title_color},
                                                                             color={"":ft.colors.WHITE},
                                                                             shape={"": ft.RoundedRectangleBorder(radius=10)}),
                                                        width=270,
                                                        height=60,
                                                        on_click=login_request,
                                                        content=ft.Text('Log in', size=18)
                                                    ),
                                                ),
                                                ft.Container(alignment=ft.alignment.center,
                                                                margin=ft.margin.only(top=50), content=ft.Container(
                                                        content=ft.Text('__________Or__________', size=28))),

                                                ft.Container(
                                                                margin=ft.margin.only(top=30), content=ft.Container(
                                                        content=ft.Row(alignment=ft.MainAxisAlignment('center'),
                                                                       spacing=3,
                                                                       controls=[ft.Text(
                                                            'Create an '
                                                                                                    'account', size=16),
                                                                                 ft.Container(data='register',
                                                                                     on_click=register_url,
                                                                                     content=ft.Text('here',
                                                                                                         size=16,
                                                                                         weight='w600'))]))),

                                            ],
                                        ),
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Container(
                                                    expand=True,
                                                    margin=ft.margin.all(0),
                                                    padding=ft.padding.only(
                                                        top=20, bottom=20, left=15, right=15
                                                    ),
                                                )
                                            ]
                                        )
                                    ),
                                ],
                            ),
                        )
                    ],
                ),
            ],
        )


        page_view = ft.Container(content=main_content)
        return page_view
