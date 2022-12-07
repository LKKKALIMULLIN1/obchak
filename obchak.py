import telebot
from telebot import types

token = "5539695234:AAELsA-kz78QW6XWLR0dLSkPR1XSHzdvgJo"
#token = "5855221402:AAFurHROYi_p21Xp-grs4NzXap-HZvUuga0"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['obch'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("add")
    btn2 = types.KeyboardButton("show")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! ".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "show"):
        bot.send_message(message.chat.id, text="расчитать")
    elif (message.text == "add"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("suvrival")
        btn2 = types.KeyboardButton("хозтовары")
        back = types.KeyboardButton("else")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="на что", reply_markup=markup)
        bot.register_next_step_handler(message, who)


def who(message):  # передает на что потратили, записать в таблицу
    things = message.text
    bot.send_message(message.chat.id, things)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1tn1 = types.KeyboardButton("isk")
    b1tn2 = types.KeyboardButton("doc")
    b1tn3 = types.KeyboardButton("maj")
    b1tn4 = types.KeyboardButton("sen")
    b1tn5 = types.KeyboardButton("dep")
    b1tn6 = types.KeyboardButton("jos")
    markup.add(b1tn1, b1tn2, b1tn3, b1tn4, b1tn5, b1tn6)
    bot.send_message(message.chat.id, text="кто купил", reply_markup=markup)
    bot.register_next_step_handler(message, without1)


def without1(message):

    whobuy = message.text
    bot.send_message(message.chat.id, whobuy)
    bot.send_message(message.chat.id, text="кого не было", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, without2)


def without2(message):
    wh = message.text
    bot.send_message(message.chat.id, text=wh)
    bot.register_next_step_handler(message, howmuch)
    bot.send_message(message.from_user.id, text="сколько потратили")


def howmuch(message):
    withoutwhom = message.text
    bot.send_message(message.from_user.id, withoutwhom)
    hm = message.text
    bot.send_message(message.from_user.id, text="date")
    bot.register_next_step_handler(message, date)


def date(message):
    hm = message.text
    bot.send_message(message.from_user.id, hm)
    date = message.text
    # bot.send_message(message.chat.id, text=date)
    # bot.send_message(message.chat.id, date)


bot.polling(none_stop=True)
