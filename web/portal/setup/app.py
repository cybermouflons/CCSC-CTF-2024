#!/usr/bin/env python3
import time
from typing import Optional

from time import sleep

import httpx
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nicegui import Client, app, ui

passwords = {'admin': 'adminpass123'}

unrestricted_page_routes = {'/login', '/loginfailed'}  # Restrict /flag for prod


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')
        return await call_next(request)


class PageMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.url.path.lower() in Client.page_routes.values() and request.url.path.lower() != request.url.path:
            app.storage.user['referrer_path'] = request.url.path
            return RedirectResponse(request.url.path.lower())
        return await call_next(request)


app.add_middleware(PageMiddleware)
app.add_middleware(AuthMiddleware)


@ui.page('/')
def main_page() -> None:
    app.storage.user['referrer_path'] = "/"
    with ui.column().classes('absolute-center items-center'):
        ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
        ui.button(on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/login')), icon='logout') \
            .props('outline round')
        ui.label("We have preserved a map of the Area of Operations for you.")
        m = ui.leaflet(center=(35.18, 33.38))
        m.set_zoom(7)
        ui.label().bind_text_from(m, 'center', lambda center: f'Center: {center[0]:.1f}, {center[1]:.1f}')
        ui.label().bind_text_from(m, 'zoom', lambda zoom: f'Zoom: {zoom}')


@ui.page('/super_secret_status_page')
async def status_page() -> None:
    content_label = ui.label('Loading...')
    try:
        path = app.storage.user.get('referrer_path', "/")
        if path.endswith('/flag'):
            path = "/"
        async with httpx.AsyncClient() as client:
            r = await client.get("http://localhost:8888" + path,
                                 follow_redirects=True)  # TODO: point this to prod... At least it works hahaha
        content_label.set_text("Status for " + path + " : " + str(r.status_code) + " " + str(r.content))
    except Exception as e:
        content_label.set_text("Failed getting status for " + app.storage.user.get('referrer_path') + " : " + str(e))


@ui.page('/flag')
async def flag_page() -> None:
    app.storage.user['referrer_path'] = "/"
    ui.label("Port from dev once secure.")  # ui.label(f"Flag: {os.getenv('FLAG')}")


t1 = 0
t2 = 0


@ui.page('/loginfailed')
async def loginfailed() -> None:
    global t1
    global t2

    def goback():
        ui.navigate.to("/login")  # go back to where the user wanted to go

    with ui.card().classes('absolute-center'):
        ui.label("Login Failed")
        ui.label(f"Time attempted: {t1}")
        ui.label(f"Time failed: {t2}")
        ui.button('Go Back', on_click=goback)


@ui.page('/login')
def login() -> Optional[RedirectResponse]:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        global t1
        global t2

        t1 = time.time_ns()
        t2 = 0

        pass_val = passwords.get(username.value.lower())
        authenticated = True
        for i in range(len(pass_val)):
            try:
                if pass_val[i] == password.value[i]:
                    print("Let it be known, that a character is matched!")
                    sleep(0.20)  # Let the feeling sink in
                else:
                    authenticated = False
                    #ui.notify('Wrong username or password', color='negative')
            except Exception:
                authenticated = False
                t2 = time.time_ns()
                #ui.notify('Wrong username or password', color='negative')
        if authenticated:
            app.storage.user.update({'username': username.value, 'authenticated': True})
            ui.navigate.to(app.storage.user.get('referrer_path', '/'))  # go back to where the user wanted to go
        else:
            ui.navigate.to("/loginfailed")

        """
        Bad code.
        
        if passwords.get(username.value.lower()) == password.value:
            app.storage.user.update({'username': username.value, 'authenticated': True})
            ui.navigate.to(app.storage.user.get('referrer_path', '/'))  # go back to where the user wanted to go
        else:
            ui.notify('Wrong username or password', color='negative')
        """

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/')
    with ui.card().classes('absolute-center'):
        ui.label("Please enter your username and password, admin:")
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Admin log in', on_click=try_login)

    return None


ui.run(storage_secret='VEERYSEEEECRET', title="Nice AI GUI", port=3000)
