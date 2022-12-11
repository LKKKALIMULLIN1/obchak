import telebot
from telebot import types
from prettytable import PrettyTable
import json

# token = "5539695234:AAELsA-kz78QW6XWLR0dLSkPR1XSHzdvgJo"
token = "5094695265:AAHl3W5t1QVl8F3BlJS4S7usojzZKxnQOWQ"
bot = telebot.TeleBot(token)

date = ''
for_what = ""
who = ''
how_much = 0
without_whom = []
users = ['isk', 'doc', 'maj', 'sen', 'dep', 'jos']


@bot.message_handler(commands=['obch', 'start'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id,
                         text="Привет, {0.first_name}, этот бот ГЕНИЙ и он умеет много чего: \n"
                              "/obch --- Всякие взаимодействия с общаком\n"
                              "----------------------------------------------------------------------------\n"
                              "Если есть неполадки, сообщите @L1km0 или @iskansosik".format(message.from_user))
    elif message.text == '/obch':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("add")
        btn2 = types.KeyboardButton("show")
        btn3 = types.KeyboardButton("change")
        btn4 = types.KeyboardButton("delete")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id,
                         text="Выбери нужную тебе команду".format(
                             message.from_user), reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="Чтобы начать напиши: /start")


def show_data(id):  # Printing all data about obchak
    mytable = PrettyTable()
    mytable.field_names = ['Date', "For what", "Who", "How much", "Without whom"]
    f = open('data.txt').readline
    arr = []
    for i in range(3):
        arr.append(json.loads(f()[:-1]))
    mytable.add_rows(arr)
    mytable.align = 'c'
    s = "```\n" + str(mytable) + "\n```"
    bot.send_message(id, text=s, parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "show":
        show_data(message.chat.id)
    elif message.text == "add":
        bot.send_message(message.chat.id, text="когда была покупка?", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_date)
    elif message.text == "change":
        pass
    elif message.text == "delete":
        pass


def get_date(message):
    global date
    date = message.text
    bot.send_message(message.chat.id, text="на что закупился? например завтрак, туалетка...")
    bot.register_next_step_handler(message, get_for_what)


def get_for_what(message):
    global for_what
    for_what = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("isk")
    btn2 = types.KeyboardButton("doc")
    btn3 = types.KeyboardButton("maj")
    btn4 = types.KeyboardButton("sen")
    btn5 = types.KeyboardButton("dep")
    btn6 = types.KeyboardButton("jos")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, text="понял, хорошее приобретение) кто купил?", reply_markup=markup)
    bot.register_next_step_handler(message, get_who)


def get_who(message):  # передает на что потратили, записать в таблицу
    global who
    who = message.text
    bot.send_message(message.chat.id, text="Сколько рублей потратил?", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_how_much)


def get_how_much(message):
    global how_much
    try:
        how_much = int(message.text)
        bot.send_message(message.from_user.id,
                         text="Кого не учитывать в эту стоимость? Нужно написать никнеймы через пробел. Например: "
                              "маша катя назлыгуль. Если нет таковых напишите 'all'")
        bot.register_next_step_handler(message, get_without_whom)
    except Exception:
        bot.send_message(message.chat.id, text="Стоимость выражается только в цифрах если что, так что введи число")
        bot.register_next_step_handler(message, get_how_much)


def get_without_whom(message):
    global without_whom
    flag = 1
    if message.text != 'all':
        without_whom = message.text.split()
        for elem in without_whom:
            if elem not in users:
                flag = 0
                bot.send_message(message.chat.id,
                                 text=f"Пользователя {elem} нет в данных, вы уверены, что ввели правильно его ник."
                                      f"Если да, то сообщите об ошибке @L1km0 или @iskansosik")
                bot.register_next_step_handler(message, get_without_whom)
    if flag:
        file = open('data.txt', 'a')
        arr = [date, for_what, who, how_much, without_whom]
        json.dump(arr, file)
        file.write("\n")


bot.polling(none_stop=True)
