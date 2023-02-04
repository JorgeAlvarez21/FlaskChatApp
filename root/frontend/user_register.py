import flet as ft
import requests
import time
import sys
import path
import json

sys.path.append(path.Path(__file__).abspath().parent.parent.parent)
from root import settings

class RegisterViewControl(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        # References
        fullname = ft.Ref[ft.TextField]()
        username = ft.Ref[ft.TextField]()
        email = ft.Ref[ft.TextField]()
        password = ft.Ref[ft.TextField]()

        # _gradient_color_1 = "#ffffff"
        # _gradient_color_2 = "#ffffff"

        _gradient_color_1 = "#ffffff"
        _gradient_color_2 = "#ffffff"

        _title_color = '#4457c6'


        def register_request(e):
            if all(
                [
                    fullname.current.value,
                    username.current.value,
                    email.current.value,
                    password.current.value,
                ]
            ):
                data = {
                    "fullname": fullname.current.value,
                    "username": username.current.value,
                    "email": email.current.value,
                    "password": password.current.value,
                }
                # username.current.value = ""
                # username.current.update()
                # password.current.value = ""
                # username.current.update()
                register = requests.post(f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/user/register",
                                        json=data)
                if register.status_code == 200:
                    self.page.route = '/login'
                    self.page.go(self.page.route)
                    self.page.update()

        def login_url(e):
            self.page.go('/login')
            self.page.update()

        main_content = ft.Row(
            alignment="center",
            spacing=0,
            controls=[
                ft.Column(
                    controls=[ft.Container(width=552, height=750, border=ft.border.all(2, ft.colors.BLACK),

                        border_radius=ft.border_radius.all(20),
                        gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right,
                            colors=[_gradient_color_1, _gradient_color_2], ),
                        content=ft.Column(height=90, spacing=0, horizontal_alignment=ft.CrossAxisAlignment("center"),
                            expand=True, controls=[

                                ft.Container(height=65, border_radius=ft.border_radius.only(topLeft=17, topRight=17),
                                    bgcolor=_title_color, content=ft.Container(alignment=ft.alignment.center,
                                                                               border=ft.border.only(
                                                                                   bottom=ft.border.BorderSide(2,
                                                                                                               ft.colors.BLACK)),
                                                                               content=ft.Text("Create an account",
                                                                                   color=ft.colors.WHITE, weight="w500",
                                                                                   style=ft.TextThemeStyle.DISPLAY_SMALL), ), ),
                                ft.Container(alignment=ft.alignment.top_left,
                                             margin=ft.margin.only(left=25, top=15), content=ft.Row(spacing=2,
                                        controls=[ft.IconButton(
                                    icon=ft.icons.ARROW_BACK_IOS, icon_size=30, icon_color=_title_color, on_click=login_url),
                                            ft.Text('Back to log in', style=ft.TextThemeStyle.TITLE_SMALL,
                                                    color=ft.colors.BLUE_GREY_600)])),
                                    ft.Container(
                                        height=550,
                                        width=350,
                                        content=ft.Column(
                                            spacing=2,
                                            controls=[
                                                ft.Container(margin=ft.margin.only(top=30),
                                                                          content=ft.TextField(
                                                        ref=fullname, border='underline', hint_text='Full name',
                                                        border_color=ft.colors.BLUE_GREY_600,
                                                        border_radius=ft.border_radius.all(
                                                            10
                                                        ),
                                                        expand=True, prefix_icon=ft.icons.CONTACT_MAIL,
                                                                              height=40,
                                                        content_padding=ft.padding.only(
                                                            bottom=6, left=10
                                                        ),
                                                    )
                                                ),

                                                ft.Container(margin=ft.margin.only(top=35),
                                                    content=ft.TextField(
                                                        ref=username, border='underline', hint_text='Username',
                                                        prefix_icon=ft.icons.PERSON,
                                                        border_color=ft.colors.BLUE_GREY_600,
                                                        border_radius=ft.border_radius.all(
                                                            10
                                                        ),
                                                        expand=True,
                                                        height=40,
                                                        content_padding=ft.padding.only(
                                                            bottom=6, left=10
                                                        ),
                                                    )
                                                ),

                                                ft.Container(margin=ft.margin.only(top=35),
                                                    content=ft.TextField(
                                                        ref=email,
                                                        border_color=ft.colors.BLUE_GREY_600, border='underline',
                                                        prefix_icon=ft.icons.ALTERNATE_EMAIL,
                                                        hint_text='Email', suffix_text='Optional',
                                                        border_radius=ft.border_radius.all(
                                                            10
                                                        ),
                                                        expand=True,
                                                        height=40,
                                                        content_padding=ft.padding.only(
                                                            bottom=6, left=10
                                                        ),
                                                    )
                                                ),

                                                ft.Container(margin=ft.margin.only(top=35, bottom=40),
                                                    content=ft.TextField(
                                                        password,
                                                        border_color=ft.colors.BLUE_GREY_600, border='underline',
                                                        prefix_icon=ft.icons.PASSWORD,
                                                        hint_text='Password',
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
                                                    )
                                                ),
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
                                                        on_click=register_request,
                                                        content=ft.Text('Register', size=18)
                                                    ),
                                                ),
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
