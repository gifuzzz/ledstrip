from bluepy.btle import Peripheral
from binascii import unhexlify
# from subprocess import call
from time import sleep
from config import CONFIG
# nelle nuove versioni di raspberry os lite, l'utente pi non è preimpostato nel gruppo bluetooth
# per tanto, eseguire questo comando per poter utilizzare il bluetooth con questo utente
# e per eseguire questo script
# sudo usermod -G bluetooth -a 

# call('rfkill unblock bluetooth && sudo service bluetooth start', shell=True)

p = Peripheral()
p.connect(CONFIG['MAC'])

def checkConn():
    while p.getState() != 'conn':
        sleep(5)
        p.connect('BE:89:80:02:EE:EF')

chars = p.getCharacteristics()
writable = chars[2]

# True to power on, False to power off
def setPower(on: bool):
    code = '01' if on else '00'
    writable.write(unhexlify(f'7e0004{code}00000000ef'))

# da 0 a 100
def changeBrightness(level: int):
    level = hex(level)[2:]
    if len(level) == 1: level = '0' + level
    writable.write(unhexlify(f'7e0001{level}00000000ef'))

# da 0 a 100
def changeColorGrayscale(perc: int):
    perc = hex(perc)[2:]
    if len(perc) == 1: perc = '0' + perc
    writable.write(unhexlify(f'7e000501{perc}000000ef'))

# da 0 a 100
def changeColorTemp(perc: int):
    perc = hex(perc)[2:]
    if len(perc) == 1: perc = '0' + perc
    writable.write(unhexlify(f'7e000502{perc}000000ef'))

# da 0 a 255
def changeColorRgb(red: int, green: int, blue: int):
    red = hex(red)[2:]
    green = hex(green)[2:]
    blue = hex(blue)[2:]
    if len(red) == 1: red = '0' + red
    if len(green) == 1: green = '0' + green
    if len(blue) == 1: blue = '0' + blue
    writable.write(unhexlify(f'7e000503{red}{green}{blue}00ef'))

def changeColorRgbHex(hex):
    writable.write(unhexlify(f'7e000503{hex}00ef'))

# da 128 a 138
def setMode(mode: str):
    writable.write(unhexlify(f'7e0003{mode}03000000ef'))

# da 0 a 100
def setEffectSpeed(perc: int):
    perc = hex(perc)[2:]
    if len(perc) == 1: perc = '0' + perc
    writable.write(unhexlify(f'7e0002{perc}00000000ef'))

def disconnect():
    p.disconnect()

modes = {
    'r': '80', # red
    'g': '81', # green
    'b': '82', # blue
    'y': '83', # yellow
    'c': '84', # vyan
    'm': '85', # magenta
    'w': '86', # white
    'jump_rgb': '87',
    'jump_rgbycmw': '88',
    'gradient_rgb': '89',
    'gradient_rgbycmw': '8a',
    'gradient_r': '8b',
    'gradient_g': '8c',
    'gradient_b': '8d',
    'gradient_y': '8e',
    'gradient_c': '8f',
    'gradient_m': '90',
    'gradient_w': '91',
    'gradient_rg': '92',
    'gradient_rb': '93', 
    'gradient_gb': '94',
    'blink_rgbycmw': '95',
    'blink_r': '96',
    'blink_g': '97',
    'blink_b': '98',
    'blink_y': '99',
    'blink_c': '9a',
    'blink_m': '9b',
    'blink_w': '9c'
    }
