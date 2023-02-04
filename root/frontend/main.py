import time
import logging
import flet as ft
import datetime as dt
from home import HomeViewControl
from user_login import UserLoginView
from user_register import RegisterViewControl
import sys
import path
import json
import requests
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent.parent)
import root.settings as settings
import threading



class SessionLoggerInfo:
    def __init__(self):
        self.userID = None

    def _setter(self, userID):
        self.userID = userID
        self._send_online()

    def _send_online(self):
        # Called on user login
        data = {'userID':self.userID, 'status':'online'}
        api_request = requests.put(
            f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/user/status", json=data)
        if api_request.status_code == 200:
            return
        else:
            raise ConnectionRefusedError('Unable to update status on server side')

    def _send_offline(self):
        data = {'userID':self.userID, 'status':'offline'}
        api_request = requests.put(
            f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/user/status", json=data)
        if api_request.status_code == 200:
            return
        else:
            raise ConnectionRefusedError('Unable to update status on server side')

def main(page: ft.Page, ):
    page.window_height = 900
    page.window_width = 1300
    page.theme_mode = 'light'

    server_ss = SessionLoggerInfo()

    def __session_handler__():
        username = page.session.get('username')
        data = {"username":username}
        api_request = requests.get(f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/data/user/get_data",
            json=data)
        if api_request.status_code == 201:
            user_data = json.loads(api_request.content)
            page.session.set("userID", user_data['userID'])
            page.session.set("fullname", user_data['fullname'])
            page.session.set("email", user_data['email'])
            server_session = server_ss._setter(user_data['userID'])
            page.on_disconnect = logout_user
            page.on_error = logout_user

            return True
        else:
            return False

    def logout_user(e=None):
        if not e:
            page.session.clear()
            server_ss._send_offline()
        else:
            server_ss._send_offline()


    # Assembling views
    _view_base = ft.View('/')

    def route_change(route):
        page.views.clear()
        page.views.append(
            _view_base
        )
        if page.route == '/login':
            content_login = UserLoginView(page)
            _login = ft.Column(expand=True, controls=[ft.Container(height=0), content_login])
            _view_login = ft.View('/login', controls=[_login])

            page.views.append(
                _view_login
            )
        if page.route == "/register":
            content_register = RegisterViewControl(page)
            _register = ft.Column(expand=True, controls=[ft.Container(height=0), content_register])
            _view_register = ft.View('/register', controls=[_register])

            page.views.append(
                _view_register
            )
        if page.route == "/home":
            handler = __session_handler__()
            content_home = HomeViewControl(page)
            _view_home = ft.Column(expand=False, controls=[ft.Container(height=0), content_home])

            if handler:
                page.views.append(
                    _view_home
                )
        else:
            if page.route == '/logout':
                logout_user()
                page.route = '/login'
                page.go(page.route)
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.route = '/login'
    page.go(page.route)

ft.app(target=main, assets_dir="../../media", host='localhost', port=9000, view=ft.WEB_BROWSER)
