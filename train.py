import argparse
import re
import pickle

#--input-dir` путь к директории, в которой лежит коллекция документов. Если данный аргумент не задан, считать, что тексты вводятся из stdin.
#--model`  путь к файлу, в который сохраняется модель.

parser = argparse.ArgumentParser()
parser.add_argument('--input-dir',  type=str)
parser.add_argument('--model', type=str, required=True)
args = parser.parse_args()
####


f = open('../TinkoffML2022/data/detective/Era_Miloserdiya.txt', 'r', encoding="utf8")
#список предложений
lst_snt = []
for s in f:
    # Убрать последний символ '\n' из s
    s = s.rstrip().lower()
    if s!='':
        snt = s.split('.')

    # Вывести s для контроля
    #print("s = ", s)

    # Добавить строку s в список lst2
    
    lst_snt = lst_snt + [snt]

output = []
outcome = {}
    
for text in lst_snt:
    text = str(text)

#text = '- у тебя оружие с собой? у меня оружие при мне, а у тебя.'
# генерирую список с n-граммами до 6
    text = re.sub(r'[^а-яА-Я0-9\s]', ' ', text)
    words = text.split()
    
    for WordsToCombine in range(1,7,1):
        for i in range(len(words)- WordsToCombine+1):
            output.append(words[i:i+WordsToCombine])
    
for k in output:
    #print('k= ', k)
    partial_outcome = output.count(k)
    #print('freq=',partial_outcome)
    s = ' '.join([str(n) for n in k])
    LengthPrefix = len(k)
    res=[]
    for k2 in output:
        if len(k2)== LengthPrefix+1:
            if s == ' '.join([str(n) for n in k2[:LengthPrefix]]):
                #print(k2[LengthPrefix:])
                #print(k2[-1])
                partial_outcome1 = output.count(k2)
                #print('freq=',partial_outcome1)
                if (k2[-1], partial_outcome1/partial_outcome) not in res:
                    res.append((k2[-1], partial_outcome1/partial_outcome))
    outcome[s] = res
    #print(res)

#print(outcome)       
with open('../TinkoffML2022/model.pickle', 'wb') as handle:
    pickle.dump(outcome, handle, protocol=pickle.HIGHEST_PROTOCOL)

