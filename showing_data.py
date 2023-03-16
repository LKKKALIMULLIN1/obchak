from prettytable import PrettyTable
import json


def show_data(cnt):
    mytable = PrettyTable()
    mytable.field_names = ['Index', 'Date', "For what", "Who", "How much", "Without whom"]
    f = open('data.txt').readline
    arr = []
    for i in range(cnt):
        mas = json.loads(f()[:-1])
        mas.insert(0, i+1)
        arr.append(mas)
    mytable.add_rows(arr)
    mytable.align = 'c'
    s = "```\n" + str(mytable) + "\n```"
    return s