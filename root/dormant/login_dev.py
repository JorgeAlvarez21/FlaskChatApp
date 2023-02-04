import flet as ft
import requests
import time
import sys
import path
import json

from flet import View

sys.path.append(path.Path(__file__).abspath().parent.parent.parent)
from root import settings


class LoginViewControl(ft.UserControl):
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

            push_request = requests.post("http://127.0.0.1:5000/user/login", json=data)
            status_context = json.loads(push_request.content)
            print(status_context)
            if status_context.get('code') == 201:
                userID = status_context.get('userID')
                page.session.set('logged_in', True)
                page.session.set("userID", userID)
                page.session.set("fullname", fullname)
                page.session.set("username", username)
                page.session.set("userID", userID)


        def check_item_clicked(e):
            pass

        main_content = ft.ResponsiveRow(
            alignment="center",
            spacing=0,
            controls=[
                ft.Column(
                    col={"xs": 1, "sm": 1, "md": 1, "lg": 1, "xl": .5, "xxl": .5},
                    controls=[
                        ft.Container(
                            alignment=ft.alignment.top_right,
                            content=ft.Column(
                                horizontal_alignment="end",
                                controls=[
                                    ft.Container(
                                        bgcolor=ft.colors.BLACK, width=70, height=650
                                    )
                                ],
                            ),
                        )
                    ],
                ),
                ft.Column(
                    col={"xs": 4, "sm": 4, "md": 4, "lg": 4, "xl": 4, "xxl": 2.5},
                    controls=[
                        ft.Container(
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=["#424f70", "#1f2432"],
                            ),
                            height=650,
                            content=ft.Column(
                                alignment="center",
                                spacing=20,
                                expand=True,
                                controls=[
                                    ft.ElevatedButton(
                                        style=ft.ButtonStyle(
                                            bgcolor={"hovered": "#2f3953", "": "#252C3E"}
                                        ),
                                        content=ft.Container(
                                            width=260,
                                            height=70,
                                            border_radius=ft.border_radius.all(15),
                                            padding=ft.padding.all(0),
                                            content=ft.Row(
                                                alignment="start",
                                                spacing=5,
                                                controls=[
                                                    ft.Container(
                                                        padding=ft.padding.only(
                                                            left=30, top=14
                                                        ),
                                                        width=120,
                                                        height=50,
                                                        margin=ft.margin.all(0),
                                                        content=ft.Text("Log In", size=20),
                                                    ),
                                                    ft.Container(
                                                        width=50,
                                                        height=50,
                                                        content=ft.Icon(
                                                            name=ft.icons.LOGIN,
                                                            color=ft.colors.WHITE,
                                                            size=30,
                                                        ),
                                                    ),
                                                ],
                                            ),
                                        ),
                                    ),
                                    ft.Row(
                                        alignment="center",
                                        controls=[
                                            ft.Text("OR", size=24, color=ft.colors.WHITE)
                                        ],
                                    ),
                                    ft.ElevatedButton(
                                        style=ft.ButtonStyle(
                                            bgcolor={"hovered": "#2f3953", "": "#252C3E"}
                                        ),
                                        on_click=lambda _: page.go("/register"),
                                        content=ft.Container(
                                            width=260,
                                            height=70,
                                            border_radius=ft.border_radius.all(15),
                                            padding=ft.padding.all(0),
                                            content=ft.Row(
                                                alignment="start",
                                                spacing=5,
                                                controls=[
                                                    ft.Container(
                                                        padding=ft.padding.only(
                                                            left=30, top=14
                                                        ),
                                                        width=120,
                                                        height=50,
                                                        margin=ft.margin.all(0),
                                                        content=ft.Text("Sign Up", size=20),
                                                    ),
                                                    ft.Container(
                                                        width=50,
                                                        height=50,
                                                        content=ft.Icon(
                                                            ft.icons.ASSIGNMENT_IND_OUTLINED,
                                                            color=ft.colors.WHITE,
                                                            size=30,
                                                        ),
                                                    ),
                                                ],
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        )
                    ],
                ),
                ft.Column(
                    col={"xs": 7, "sm": 7, "md": 7, "lg": 7, "xl": 6.5, "xxl": 4.2},
                    controls=[
                        ft.Container(
                            height=650,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=["#424f70", "#1f2432"],
                            ),
                            content=ft.Column(
                                spacing=0,
                                horizontal_alignment=ft.CrossAxisAlignment("center"),
                                expand=True,
                                controls=[
                                    ft.Container(
                                        padding=ft.padding.only(top=70, bottom=50),
                                        content=ft.Text(
                                            "Login to your account", size=30, weight="w400"
                                        ),
                                    ),
                                    ft.Container(
                                        height=400,
                                        width=350,
                                        content=ft.Column(
                                            spacing=2,
                                            controls=[
                                                ft.Container(
                                                    padding=ft.padding.only(
                                                        top=20, left=15, bottom=10
                                                    ),
                                                    content=ft.Text("Username", size=16),
                                                ),
                                                ft.Container(
                                                    padding=ft.padding.only(
                                                        left=5, right=5
                                                    ),
                                                    content=ft.TextField(
                                                        ref=username,
                                                        border_color=ft.colors.BLUE_GREY_600,
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
                                                ft.Container(
                                                    padding=ft.padding.only(
                                                        top=20, left=15, bottom=10
                                                    ),
                                                    content=ft.Text("Password", size=16),
                                                ),
                                                ft.Container(
                                                    padding=ft.padding.only(
                                                        left=5, right=5
                                                    ),
                                                    content=ft.TextField(
                                                        ref=password,
                                                        border_color=ft.colors.BLUE_GREY_600,
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
                                                ft.Container(
                                                    padding=ft.padding.only(
                                                        top=50, left=20
                                                    ),
                                                    content=ft.ElevatedButton(
                                                        "Submit",
                                                        bgcolor=ft.colors.BLUE_ACCENT_400,
                                                        width=100,
                                                        color=ft.colors.WHITE,
                                                        on_click=login_request,
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