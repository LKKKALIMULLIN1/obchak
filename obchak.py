import telebot
from telebot import types
import json
import counter
import showing_data
import delete_line_of_data
from prettytable import PrettyTable

# token = "5539695234:AAELsA-kz78QW6XWLR0dLSkPR1XSHzdvgJo"
# token = "5094695265:AAHl3W5t1QVl8F3BlJS4S7usojzZKxnQOWQ"
token = "5031767148:AAFW3rMKl1cFOS-EALaPxVNhPVD1PsJenQQ"
bot = telebot.TeleBot(token)

date = ''
for_what = ""
who = ''
how_much = 0
cnt = 0
without_whom = []
users = ['isk', 'doc', 'maj', 'sen', 'dep', 'jos']
index = 0


@bot.message_handler(content_types=['text'])
def start(message):
    msg = message.text
    user = message.chat.id
    if msg == '/start':
        bot.send_message(user, text="Привет, {0.first_name}, этот бот ГЕНИЙ и он умеет много чего: \n"
                                    "/obch --- Всякие взаимодействия с общаком\n"
                                    "/dolg --- сли вам кто-то задолжа\n"
                                    "/inst --- Если нужна инструкция пользования ботом\n"
                                    "----------------------------------------------------------------------------\n"
                                    "Если есть неполадки, сообщите @L1km0 или @iskansosik".format(message.from_user),
                         reply_markup=types.ReplyKeyboardRemove())
    elif msg == '/obch':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("add")
        btn2 = types.KeyboardButton("show")
        btn3 = types.KeyboardButton("delete")
        btn4 = types.KeyboardButton("count")
        markup.add(btn1, btn2, btn4, btn3)
        bot.send_message(user, text="Выбери нужную тебе команду", reply_markup=markup)
        bot.register_next_step_handler(message, obch_first_step)
    elif msg == '/inst':
        txt = 'Привет, бот умеет много чего, поэтому давай определимся, для какой функции нужна инструкция?'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('obch')
        btn2 = types.KeyboardButton('dolg')
        markup.add(btn1, btn2)
        bot.send_message(user, text=txt, reply_markup=markup)
        bot.register_next_step_handler(message, inst_first_step)
    elif message.text == '/dolg':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("isk")
        btn2 = types.KeyboardButton("doc")
        btn3 = types.KeyboardButton("maj")
        btn4 = types.KeyboardButton("sen")
        btn5 = types.KeyboardButton("dep")
        btn6 = types.KeyboardButton("jos")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, text="кто вам должен?", reply_markup=markup)
        bot.register_next_step_handler(message, get_dolg)
    else:
        bot.send_message(message.chat.id, text="Чтобы начать напиши: /start")


def get_dolg(message):
    pass


def inst_first_step(message):
    user = message.chat.id
    if message.text == 'obch':
        txt1 = 'Данная команда записывает покупки в таблицу и может посчитать кто сколько кому должен'
        txt2 = 'Функция `add` добавляет данные в таблицу, для этого вам потребуется откопать данные о ' \
               'дате, цене, кого не было и что было куплено. Чтобы внести данные просто нажмите add, а гениальный ' \
               'сам все у вас спросит)'
        txt3 = 'Функция `show` показывает таблицу, если вы смотрите таблицу с телефона, советую сделать экран горизонтальным ' \
               'так таблице будет выглядеть поприятнее'
        txt4 = 'Функция `count` считает сам общак, то есть кто сколько должен заплатить или получить'
        txt5 = 'Функция `delete` удаляет определенную строку в таблице, ведь все мы ошибаемся. Для удаления вам потребуется определить индекс ' \
               'строки, которую хотите удалить (первый столбец в таблице P.s. нажмите show чтобы увидеть таблицу). При этом будьте внимательны, если вы ' \
               'удалите не ту строку, вернуть ее будет почти невозможно'
        bot.send_message(user, text=txt1)
        bot.send_message(user, text=txt2)
        bot.send_message(user, text=txt3)
        bot.send_message(user, text=txt4)
        bot.send_message(user, text=txt5)
    elif message.text == 'dolg':
        txt = 'Данная команда позволяет не держать в голове должников и свои долги. Просто нажмите /dolg и бот задаст все нужные вопросы'
        bot.send_message(user, text=txt)


def obch_first_step(message):
    if message.text == "show":
        txt = showing_data.show_data(cnt)
        bot.send_message(message.chat.id, text=txt, parse_mode="Markdown")
    elif message.text == "add":
        bot.send_message(message.chat.id, text="когда была покупка?", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_date)
    elif message.text == "delete":
        bot.send_message(message.chat.id, text="Введи индекс строки, которую хочешь удалить", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, delete)
    elif message.text == 'count':
        if cnt == 0:
            bot.send_message(message.chat.id, text="Никто никому ничего не должен, классно же)")
        else:
            txt = counter.count(users, cnt)
            bot.send_message(message.chat.id, text=txt, parse_mode="Markdown")


def delete(message):
    global index, cnt
    try:
        index = int(message.text)
    except Exception:
        bot.send_message(message.chat.id,
                         text="Мужик, ты чето попутал, индекс должен выражаться в цифрах, так что введи число")
        bot.register_next_step_handler(message, delete)
    if index > cnt or index <= 0:
        bot.send_message(message.chat.id, text='Мужик, ты чето попутал, в таблице нет такого индекса')
        bot.register_next_step_handler(message, delete)
    else:
        f = open('data.txt').readline
        for i in range(index):
            mas = json.loads(f()[:-1])
        mytable = PrettyTable()
        mytable.field_names = ['Index', 'Date', "For what", "Who", "How much", "Without whom"]
        mas.insert(0, index)
        mytable.add_row(mas)
        s = '```\n' + str(mytable) + '\n```\n' \
            'вы хотите удалить эту строку? Хорошо подумайте, данные потом не вернуть)'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = 'of course'
        btn2 = 'no it is mistake'
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text=s, parse_mode="Markdown", reply_markup=markup)
        bot.register_next_step_handler(message, applying)


def applying(message):
    global index, cnt
    if message.text == 'of course':
        delete_line_of_data.delete_line(index)
        cnt -= 1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("add")
        btn2 = types.KeyboardButton("show")
        btn3 = types.KeyboardButton("delete")
        btn4 = types.KeyboardButton("count")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text="Сделано )", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("add")
        btn2 = types.KeyboardButton("show")
        btn3 = types.KeyboardButton("delete")
        btn4 = types.KeyboardButton("count")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text="Хорошо, что заметили сейчас)", reply_markup=markup)


def get_date(message):
    global date
    date = message.text.lower()
    bot.send_message(message.chat.id, text="на что закупился? например туалетка, survival...")
    bot.register_next_step_handler(message, get_for_what)


def get_for_what(message):
    global for_what
    for_what = message.text.lower()
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
    who = message.text.lower()
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
        bot.send_message(message.chat.id, text="Мужик, ты чето попутал, стоимость должна выражаться в цифрах, так что введи число")
        bot.register_next_step_handler(message, get_how_much)


def get_without_whom(message):
    global without_whom
    flag = 1
    without_whom = []
    if message.text != 'all':
        without_whom = message.text.split()
        for i in range(len(without_whom)):
            without_whom[i] = without_whom[i].lower()
            if without_whom[i] not in users:
                flag = 0
                bot.send_message(message.chat.id,
                                 text=f"Пользователя {without_whom[i]} нет в данных, вы уверены, что ввели правильно его ник."
                                      f"Если да, то сообщите об ошибке @iskansosik")
                bot.register_next_step_handler(message, get_without_whom)
    if flag:
        global cnt
        cnt += 1
        file = open('data.txt', 'a')
        arr = [date, for_what, who, how_much, without_whom]
        json.dump(arr, file)
        file.write("\n")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("show")
        btn2 = types.KeyboardButton("count")
        btn3 = types.KeyboardButton("add")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text="Добавил данные в таблицу:\n"
                                               "-если хотите проверить корректность нажмите клавишу ```show```\n"
                                               "-если хотите посчитать кто сколько должен нажмите ```count```\n"
                                               "-если хотите еще добавить данные в таблицу, нажмите ```add```",
                         reply_markup=markup, parse_mode="Markdown")


bot.polling(none_stop=True)