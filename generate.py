import argparse
import pickle

#`--model` путь к файлу, из которого загружается модель.
#`--prefix` необязательный аргумент. Начало предложения (одно или несколько слов). Если не указано, выбираем начальное слово случайно из всех слов.
#`--length` длина генерируемой последовательности.

parser = argparse.ArgumentParser()
parser.add_argument('--model',  type=str, required=True)
parser.add_argument('--prefix', type=str, required=True)
parser.add_argument('--length', type=str, required=True)
args = parser.parse_args()
####
#'../TinkoffML2022/model.pickle'
with open(str(args.model), 'rb') as handle:
    Model = pickle.load(handle)

#читаем model.pcl
prefix = str(args.prefix)
the_length= int(args.length)
s_out=[]

for ix in range(the_length):
    x = Model.get(prefix)
    #print(x)
# берем первый по порядку появления в тексте вариант
    if x==None:
        s_out.append('42')
        #print("42")
        break
    if len(x)==0:
        s_out.append('42')
        break
    else:
        #print(x[0][0])
        s_out.append(x[0][0])
        prefix+=' '+x[0][0]

print(' '.join([str(n) for n in s_out]))  
