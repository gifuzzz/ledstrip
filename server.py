#!/usr/bin/python3.9
from time import sleep
from flask.app import Flask
from flask import render_template, request
import rgbLedControl as ctl
from threading import Thread
import sys, string
from os import path

usable = ''.join([string.ascii_letters, string.digits, ':'])

app = Flask(__name__, static_folder='static')

currColor = "ff1900" # 2d0435
lvl = 75
val = 75
isOn = False

@app.route('/')
def index():
    return render_template('index.html', modes=modes, currColor=currColor, lvl=lvl, val=val, isOn=isOn)

@app.route('/rgb')
def rgb():
    red = int(request.args.get('red') or 0)
    green = int(request.args.get('green') or 0)
    blue = int(request.args.get('blue') or 0)
    hex_col = request.args.get('hex')

    global currColor
    currColor = hex_col if hex_col else f'{red}{green}{blue}'

    if red == 0 and green == 0 and blue == 0 and hex_col:
        ctl.changeColorRgbHex(hex_col)
        return f'Color changed to {hex_col}'
    ctl.changeColorRgb(red, green, blue)
    return f'Colors changed to {red} {green} {blue}'

@app.route('/lum')
def lum():
    global lvl
    lvl = int(request.args.get('lvl') or 0)
    ctl.changeBrightness(lvl)
    return f'Brightness level changed to {lvl}'

@app.route('/speed')
def speed():
    global val
    val = int(request.args.get('val') or 0)
    ctl.setEffectSpeed(val)
    return f'Effect speed changed to {val}'

@app.route('/on')
def on():
    global isOn
    isOn = True
    # ctl.setPower(True)
    for i in range(31):
        ctl.changeBrightness(int(i*lvl/30))
        if i == 0:
            ctl.setPower(True)
    return 'Powered on'

@app.route('/off')
def off():
    global isOn
    isOn = False
    for i in range(30)[::-1]:
        ctl.changeBrightness(int(i*lvl/30))
    ctl.setPower(False)
    ctl.changeBrightness(25)
    return 'Powered off'

@app.route('/mode')
def mode():
    mode = request.args.get('mode') or 0
    ctl.setMode(mode)
    return 'Mode set to ' + mode

@app.route('/reload')
def reload():
    Thread(target=ctl.checkConn).start()
    return render_template('reload.html')

@app.route('/status')
def status():
    return ctl.p.getState()

@app.route('/setmac', methods=['POST'])
def setMac():
    if not 'mac' in request.form.keys():
        return 'no'

    mac = request.form.get('mac').strip()
    if len(mac) != 17 or len(mac.split(':')) != 6 or any([len(i) != 2 for i in mac.split(':')]) or any([i not in usable for i in mac]):
        return 'no'
    with open(path.join('config.py'),'w') as f:
        f.write('MAC = "'+mac+'"')
        ctl.config.MAC = mac
        ctl.p.disconnect()
        try:
            ctl.p.connect(mac)
            chars = ctl.p.getCharacteristics()
            ctl.writable = chars[2]
        except Exception as e:
            print(e, flush=True)
            return 'errore'
    return 'ok'

modes = {
    'red': '80',
    'blue': '81',
    'green': '82',
    'cyan': '83',
    'yellow': '84',
    'magenta': '85',
    'white': '86', 
    'jump rgb': '87',
    'jump rgbycmw': '88',
    'gradient rgb': '89',
    'gradient rgbycmw': '8a',
    'gradient r': '8b',
    'gradient g': '8c',
    'gradient b': '8d',
    'gradient y': '8e',
    'gradient c': '8f',
    'gradient m': '90',
    'gradient w': '91',
    'gradient rg': '92',
    'gradient rb': '93', 
    'gradient gb': '94',
    'blink rgbycmw': '95',
    'blink r': '96',
    'blink g': '97',
    'blink b': '98',
    'blink y': '99',
    'blink c': '9a',
    'blink m': '9b',
    'blink w': '9c'
    }

def conn():
    while 1:
        ctl.checkConn()
        sleep(300)
Thread(target=conn).start()
app.run('0.0.0.0', 3000)
