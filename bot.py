import telebot
from telebot import types
from telebot.types import * 
import requests
import config
import localization as loc
import database
from database import Database as db
from pk import Pay
import weather 
from weather import Weather 

bot = telebot.TeleBot(config.token)


# FUNCTIONS


def DefaultButtons(language):
    keyboard = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
    today = types.KeyboardButton(text = loc.defaultButtons["TODAY"][language])
    fiveDays = types.KeyboardButton(text = loc.defaultButtons["5DAYS"][language])
    location = types.KeyboardButton(text = loc.defaultButtons["LOCATION"][language], request_location = True)
    donate = types.KeyboardButton(text = loc.defaultButtons["DONATE"][language])
    settings = types.KeyboardButton(text = loc.defaultButtons["SETTINGS"][language])
    keyboard.add(today, fiveDays, location, settings, donate)

    return keyboard


def ChangeLanguage(message):
    if message.text ==  "🇷🇺RU": db.UpdateLanguage('ru', message.from_user.id)
    if message.text == "🇺🇸EN": db.UpdateLanguage('en', message.from_user.id)
    lang = db.Language(message.chat.id)
    bot.send_message(message.chat.id, loc.settings_update[lang], reply_markup = DefaultButtons(lang))


# COMMANDS

# Command list 
@bot.message_handler(commands = ['c', 'commands', 'help'])
def CommandsCommand(message):
    res = ['/' + x + '\n' for x in config.commands]
    res = ''.join(res)
    bot.send_message(message.chat.id, res)


# Start
@bot.message_handler(commands = ['start'])
def StartCommand(message):
    db.NewUser(message.from_user.id, message.from_user.language_code)
    keyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True, one_time_keyboard = True)
    keyboard.add(types.KeyboardButton(text = "📍Геопозиция", request_location = True))
    bot.send_message(message.chat.id, loc.start[db.Language(message.chat.id)], reply_markup = keyboard)


# Statisctics
@bot.message_handler(commands = ['statistics', 'stats'])
def StatsCommand(message):
    bot.send_message(message.chat.id, db.SelectAll())


# Delete info about self 
@bot.message_handler(commands = ['clear'])
def ClearCommand(message):
    db.DeleteUser(message.from_user.id)
    bot.send_message(message.chat.id, "Deleted!")


# REGEXP


# WEATHER TODAY
@bot.message_handler(regexp = '{}|{}'.format(loc.defaultButtons['TODAY']['en'], loc.defaultButtons['TODAY']['ru']))
def WeatherToday(message):
    try:
        lang = db.Language(message.from_user.id)
        bot.send_message(message.chat.id, Weather.today(db.City(message.from_user.id), lang), reply_markup = DefaultButtons(lang))
    except Exception as e:
        bot.send_message(config.admin, "⚠️ERROR⚠️\n" + str(message.from_user.username) + " " + str(message.from_user.id) + '\n' + str(e))


# WEATHER 5 DAYS
@bot.message_handler(regexp = '{}|{}'.format(loc.defaultButtons['5DAYS']['en'], loc.defaultButtons['5DAYS']['ru']))
def WeatherFiveDays(message):
    pass
    #bot.send_message(message.chat.id, forecast())


# SETTINGS - CHOOSE LANGAUGE
@bot.message_handler(regexp = '{}|{}'.format(loc.defaultButtons['SETTINGS']['en'], loc.defaultButtons['SETTINGS']['ru']))
def Settings(message):
    keyboard = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard = True)
    ru = types.KeyboardButton(text = "🇷🇺RU")
    en = types.KeyboardButton(text = "🇺🇸EN")
    keyboard.add(ru, en)

    msg = bot.send_message(message.chat.id, 'Choose Your language!\nВыберите Ваш язык!', reply_markup = keyboard)
    bot.register_next_step_handler(msg, ChangeLanguage)


# DONATE
@bot.message_handler(regexp = '{}|{}'.format(loc.defaultButtons['DONATE']['en'], loc.defaultButtons['DONATE']['ru']))
def Donate(message):
    # Telegram payment 
    bot.send_invoice(
        message.chat.id,
        title = 'Поддержать разработчика',
        description = 'Поддержав разработчика, Вы помогаете боту развиваться!',
        invoice_payload = 'something',
        provider_token = '401643678:TEST:bdb72775-f952-465d-9fea-c38185a832af',
        start_parameter = 'support', 
        currency = 'RUB',
        prices = [types.LabeledPrice(label = '100', amount = 100 * 100)] # amount: 100.00 => 10000 => 100 * 100
        )
    # Qiwi & YandexMoney payment 
    keyboard = Pay().paykey(
        sum = 100, 
        id = message.from_user.id, 
        qiwi = config.qiwi, 
        yandex = config.yandex
        )
    bot.send_message(message.chat.id, loc.support[db.Language(message.from_user.id)], reply_markup = keyboard)


# CONTENT TYPES


@bot.message_handler(content_types = 'text')
def CityName(message):
    try:
        lang = db.Language(message.from_user.id)
        bot.send_message(message.chat.id, Weather.today(message.text, lang), reply_markup = DefaultButtons(lang))
        db.UpdateCity(message.text, message.from_user.id)
    except Exception as e:
        bot.send_message(config.admin, "⚠️ERROR⚠️\n" + str(message.from_user.username) + " " + str(message.from_user.id) + '\n' + str(e))


@bot.message_handler(content_types = 'location')
def Location(message):
    lang = db.Language(message.from_user.id)
    lat = message.location.latitude
    lon = message.location.longitude
    bot.send_message(message.chat.id, Weather.today([lat, lon], lang), reply_markup = DefaultButtons(lang))

    r = requests.get('http://api.openweathermap.org/data/2.5/weather?&units=metric&lat=%s&lon=%s&appid=0c9f3c052f1d81b7062750ff0926f345' % (lat, lon))
    data = r.json()
    city = data["name"]
    db.UpdateCity(city, message.from_user.id)

bot.polling(none_stop = True, interval = 0)
