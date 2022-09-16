import argparse

#--input-dir` путь к директории, в которой лежит коллекция документов. Если данный аргумент не задан, считать, что тексты вводятся из stdin.
#--model`  путь к файлу, в который сохраняется модель.

parser = argparse.ArgumentParser()
parser.add_argument('--input-dir',  type=str)
parser.add_argument('--model', type=str, required=True)
args = parser.parse_args()
####

f = open('../TinkoffML2022/data/Era_Miloserdiya.txt', 'r', encoding="utf8")
lst2 = []
for s in f:
    # Убрать последний символ '\n' из s
    s = s.rstrip().lower()

    # Вывести s для контроля
    print("s = ", s)

    # Добавить строку s в список lst2
    lst2 = lst2 + [s]



