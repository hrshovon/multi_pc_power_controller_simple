import serial
import sys 
from nicegui import ui
import sys 
import time 
import json 
from starlette.requests import Request
from starlette.websockets import WebSocket
from typing import Dict
import hashlib 


'''
comm = serial.Serial("COM3",115200)
pin = int(sys.argv[1])

data_buf = bytearray([pin,0,150,200])

comm.write(data_buf)
'''
examplejson = None
session_infos: Dict[str, Dict] = {}
users = {}

def load_users(json_user):
    global users 
    for userobj in json_user:
        users[userobj["username"]] = userobj["password"]
def load_config():
    global examplejson
    try:
        with open("./config.json","r") as fp:
            examplejson = json.load(fp)
            load_users(examplejson["users"])
    except Exception as e:
        print("error loading config",e)
        sys.exit(1)


def perform_sw_ops(pin, time_duration):

    data_buf = bytearray([pin,time_duration,150,200])
    comm = serial.Serial("COM3",115200)
    time.sleep(1)
    comm.write(data_buf)
    time.sleep(0.5)
    comm.close()

def process_bttn_clk(name, addr, duration):
    perform_sw_ops(addr, duration)
    ui.notify(f"Performing operation on {name}'s PC")


def build_login_form() -> None:
    def on_login(username: str, password: str, socket: WebSocket) -> None:
        session_id = socket.cookies['jp_token'].split('.')[0]
        if username in users:
            if hashlib.md5(password.encode()).hexdigest() == users[username]:
                session_infos[session_id] = {'authenticated': True, 'user': username}
                ui.open('/', socket)

    with ui.row().classes('flex justify-center w-full mt-20'):
        with ui.card():
            username = ui.input('User Name')
            password = ui.input('Password').classes('w-full').props('type=password')
            ui.button('Log in', on_click=lambda e: on_login(username.value, password.value, e.socket))


def main_page():
    ui.html("<center><H3>Remote PC switcher</H3></center>")
    ui.html("<p>This GUI controls various PCs in Skymatix. Please check this document for various instructions.</p>")
    ui.html("<BR/><BR/>")

    for person_info in examplejson["list"]:
        name = person_info["name"]
        addr = person_info["address"]
        short_duration = person_info["short_duration"]
        long_duration = person_info["long_duration"]
        with ui.row():
            ui.label(name)
            ui.button("Force Shutdown", on_click=lambda: process_bttn_clk(name,addr,long_duration))
            ui.button("Turn on/ Trigger shutdown", on_click=lambda: process_bttn_clk(name,addr,short_duration))
        ui.html("<BR/>")    

load_config()
@ui.page("/")
def serve(request: Request):
    if session_infos.get(request.session_id, {}).get('authenticated', False):
        main_page()
    else:
        build_login_form()
ui.run(port=7000)
