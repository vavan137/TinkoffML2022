import argparse
import re
import pickle

class NgramModel:
    
    
    def fit(dir='../TinkoffML2022/data/detective/Era_Miloserdiya.txt', model_path='../TinkoffML2022/model.pickle', txt1):
        #
        #список предложений
        lst_snt = []
        if txt1:
            s = txt1.rstrip().lower()
            if s!='':
                snt = s.split('.')
                lst_snt = lst_snt + [snt]
        else:
            f = open(str(dir), 'r', encoding="utf8")
            for s in f:
                # Убрать последний символ '\n' из s
                s = s.rstrip().lower()
                if s!='':
                    snt = s.split('.')
                    #print("s = ", s)
                    # Добавить строку s в список lst2
                    lst_snt = lst_snt + [snt]
        output = []
        outcome = {}
        for text in lst_snt:
            text = str(text)
        # генерирую список с n-граммами до 3
            text = re.sub(r'[^а-яА-Я0-9\s]', ' ', text)
            words = text.split()
            for WordsToCombine in range(1,4,1):
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
        with open(str(model_path), 'wb') as handle:
            pickle.dump(outcome, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    def predict(model_path='../TinkoffML2022/model.pickle', prefix='сын его', the_length=5):
        with open(str(model_path), 'rb') as handle:
            Model = pickle.load(handle)
            #читаем model.pcl
            #prefix = str(args.prefix)
            #the_length= int(args.length)
            s_out=[]
        for ix in range(the_length):
            #по последнему запрошенному слову поиск
            list_prefix = prefix.split(' ')
            prefix_last_word = list_prefix[-1]
            x = Model.get(prefix_last_word)
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
        

#--input_dir` путь к директории, в которой лежит коллекция документов. Если данный аргумент не задан, считать, что тексты вводятся из stdin.
#--model`  путь к файлу, в который сохраняется модель.

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir',  type=str)
parser.add_argument('--model', type=str, required=True)
args = parser.parse_args()
####

### раскоментить, чтобы переписать model.pkl
#if args.input_dir==None:
#    txt = input()
#    NgramModel.fit(str(args.input_dir), str(args.model), txt)
#else:
#    NgramModel.fit(str(args.input_dir), str(args.model))


