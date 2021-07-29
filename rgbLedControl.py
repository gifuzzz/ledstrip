from bluepy.btle import Peripheral, Scanner
from binascii import unhexlify
# from subprocess import call
from time import sleep
from config import MAC
# nelle nuove versioni di raspberry os lite, l'utente pi non è preimpostato nel gruppo bluetooth
# per tanto, eseguire questo comando per poter utilizzare il bluetooth con questo utente
# e per eseguire questo script
# sudo usermod -G bluetooth -a 

# call('rfkill unblock bluetooth && sudo service bluetooth start', shell=True)

p = Peripheral()
try:
    p.connect(MAC)
except:
    pass

def checkConn():
    while p.getState() != 'conn':
        sleep(5)
        try:
            p.connect(MAC)
        except:
            pass

try:
    chars = p.getCharacteristics()
    writable = chars[2]
except:
    pass

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

def scan(time:int=5):
    p.disconnect()
    s = Scanner()
    res = s.scan(time)
    return res