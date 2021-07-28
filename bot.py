import time
import requests
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from pprint import pprint
from traceback import print_exc
from secret import BOT_TOKEN

color = {
    'red': 255,
    'green': 25,
    'blue': 0
}

isOn = False
brightness = 75
speed = 75

def changeColor(newColor):
    global color
    color = {
        'red': int('0x' + newColor[:2], 0),
        'green': int('0x' + newColor[2:4], 0),
        'blue': int('0x' + newColor[4:], 0),
    }

def createColorButtons(num, sign):
    return [
        InlineKeyboardButton(text=f'{sign}{num}', callback_data=f'red_{num}_{sign}'),
        InlineKeyboardButton(text=f'{sign}{num}', callback_data=f'green_{num}_{sign}'),
        InlineKeyboardButton(text=f'{sign}{num}', callback_data=f'blue_{num}_{sign}'),
    ]

home_button = InlineKeyboardButton(text='Home 🏠', callback_data='home')
power_button = InlineKeyboardButton(text='Power 💡', callback_data='power')
color_button = InlineKeyboardButton(text='Color 🌈', callback_data='color')
brightness_button = InlineKeyboardButton(text='Brightness 🔆', callback_data='brightness')
speed_button = InlineKeyboardButton(text='Effect Speed 🏎', callback_data='speed')
delete_button = InlineKeyboardButton(text='❌', callback_data='delete')

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [power_button],
    [color_button],
    [brightness_button],
    [speed_button],
    [InlineKeyboardButton(text='Refresh 🔄', callback_data='home')],
    [delete_button],
])

power_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ON', callback_data='on')],
    [InlineKeyboardButton(text='OFF', callback_data='off')],
    [home_button],
    [delete_button],
])

colors_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    createColorButtons(100, '+'),
    createColorButtons(50, '+'),
    createColorButtons(20, '+'),
    createColorButtons(10, '+'),
    createColorButtons(1, '+'),
    [
        InlineKeyboardButton(text='🔴', callback_data='red'),
        InlineKeyboardButton(text='🟢', callback_data='green'),
        InlineKeyboardButton(text='🔵', callback_data='blue'),

    ],
    createColorButtons(1, '-'),
    createColorButtons(10, '-'),
    createColorButtons(20, '-'),
    createColorButtons(50, '-'),
    createColorButtons(100, '-'),
    [home_button],
    [delete_button],
])

def br_sp_keyboard(what):
    key = [
        [InlineKeyboardButton(text='Max', callback_data=f'{what}_100_+')],
        [InlineKeyboardButton(text='+50', callback_data=f'{what}_50_+')],
        [InlineKeyboardButton(text='+20', callback_data=f'{what}_20_+')],
        [InlineKeyboardButton(text='+10', callback_data=f'{what}_10_+')],
        [InlineKeyboardButton(text='+1',  callback_data=f'{what}_1_+')],
        [InlineKeyboardButton(text='-1',  callback_data=f'{what}_1_-')],
        [InlineKeyboardButton(text='-10', callback_data=f'{what}_10_-')],
        [InlineKeyboardButton(text='-20', callback_data=f'{what}_20_-')],
        [InlineKeyboardButton(text='-50', callback_data=f'{what}_50_-')],
        [InlineKeyboardButton(text='Min', callback_data=f'{what}_100_-')],
    ]

    key.append([home_button])
    key.append([delete_button])

    return InlineKeyboardMarkup(inline_keyboard=key)

brightness_keyboard = br_sp_keyboard('br')
speed_keyboard = br_sp_keyboard('sp')

def mainMessage(msg):
    return f"Home 🏠\n\nHi {msg['from']['first_name']},\n\n{getPower()}\n{getColors()}\n{getBrightness()}\n{getSpeed()}"

def col(color_: int):
    hex_ = hex(color[color_])[2:]
    return hex_ if len(hex_) == 2 else '0'+hex_

def getColors(message=False):
    mess = f"Current color: #{''.join(col(color_) for color_ in color)}"
    if message:
        mess = 'Color 🌈\n\n' + mess + f"\n🔴 {color['red']}\n🟢 {color['green']}\n🔵 {color['blue']}"
    return mess

def getPower(message=False):
    mess = f"Power: {'ON' if isOn else 'OFF'}"
    if message:
        mess = 'Power 💡\n\n' + mess
    return mess

def getBrightness(message=False):
    mess = f"Current brightness: {brightness}%"
    if message:
        mess = 'Brightness 🔆\n\n' + mess
    return mess

def getSpeed(message=False):
    mess = f"Current effect speed: {speed}%"
    if message:
        mess = 'Effect Speed 🏎\n\n' + mess
    return mess

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id, mainMessage(msg), reply_markup=main_keyboard)

def on_callback_query(msg):
    pprint(msg)
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    try:
        if   query_data == 'home':
            return bot.editMessageText(telepot.message_identifier(msg['message']), mainMessage(msg), reply_markup=main_keyboard)
        elif query_data == 'power':
            return bot.editMessageText(telepot.message_identifier(msg['message']), getPower(True), reply_markup=power_keyboard)
        elif query_data == 'color':
            return bot.editMessageText(telepot.message_identifier(msg['message']), getColors(True), reply_markup=colors_keyboard)
        elif query_data == 'brightness':
            return bot.editMessageText(telepot.message_identifier(msg['message']), getBrightness(True), reply_markup=brightness_keyboard)
        elif query_data == 'speed':
            return bot.editMessageText(telepot.message_identifier(msg['message']), getSpeed(True), reply_markup=speed_keyboard)
        elif query_data == 'delete':
            return bot.deleteMessage(telepot.message_identifier(msg['message']))
        elif query_data in 'red green blue'.split():
            return bot.answerCallbackQuery(query_id, text=f'{query_data.capitalize()}')
        
        elif query_data in 'on off'.split():
            requests.get(f'http://localhost:3000/{query_data}')

        chosen, num, sign = query_data.split('_')
        # colors
        if chosen in 'red green blue'.split():
            if sign == '+':
                color[chosen] += int(num)
                if color[chosen] > 255:
                    color[chosen] = 255
            elif sign == '-' and color[chosen] > 0:
                color[chosen] -= int(num)
                if color[chosen] < 0:
                    color[chosen] = 0
            requests.get(f"http://localhost:3000/rgb?hex={''.join(col(color_) for color_ in color)}")
            bot.editMessageText(telepot.message_identifier(msg['message']), getColors(), reply_markup=colors_keyboard)
            
            

        # brightness
        elif chosen == 'br':
            global brightness
            if sign == '+':
                brightness += int(num)
                if brightness > 100:
                    brightness = 100
            else:
                brightness -= int(num)
                if brightness < 0:
                    brightness = 0
            requests.get(f"http://localhost:3000/lum?lvl={brightness}")
            bot.editMessageText(telepot.message_identifier(msg['message']), getBrightness(), reply_markup=brightness_keyboard)
        
        # speed
        elif chosen == 'sp':
            global speed
            if sign == '+':
                speed += int(num)
                if speed > 100:
                    speed = 100
            else:
                speed -= int(num)
                if speed < 0:
                    speed = 0
            requests.get(f"http://localhost:3000/speed?val={speed}")
            bot.editMessageText(telepot.message_identifier(msg['message']), getSpeed(), reply_markup=speed_keyboard)
        
        bot.answerCallbackQuery(query_id, text=f'Got it!')
        
    except Exception as e:
        bot.answerCallbackQuery(query_id, text='Error')
        print_exc()

bot = telepot.Bot(BOT_TOKEN)

answerer = telepot.helper.Answerer(bot)

def start():
    MessageLoop(bot, {'chat': on_chat_message,
                      'callback_query': on_callback_query}).run_as_thread()
    print('Listening ...')

if __name__ == '__main__':
    changeColor('ff1900')
    start()
    while 1:
        time.sleep(10)