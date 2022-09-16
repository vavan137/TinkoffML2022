import argparse

#`--model` путь к файлу, из которого загружается модель.
#`--prefix` необязательный аргумент. Начало предложения (одно или несколько слов). Если не указано, выбираем начальное слово случайно из всех слов.
#`--length` длина генерируемой последовательности.

parser = argparse.ArgumentParser()
parser.add_argument('--model',  type=str, required=True)
parser.add_argument('--prefix', type=str, required=True)
parser.add_argument('--length', type=str, required=True)
args = parser.parse_args()
####

#генерация последующего слова для триграммы
corpus = PickledCorpusReader('../data/corpus')
tokens = [''.join(word) for word in corpus.words()]
vocab = Counter(tokens)
sents = list([word[0] for word in sent] for sent in corpus.sents())
counter = count_ngrams(3, vocab, sents)
knm = KneserNeyModel(counter)
def complete(input_text):
    tokenized = nltk.word_tokenize(input_text)
    if len(tokenized) < 2:
        response = "Say more."
    else:
        completions = {}
        for sample in knm.samples():
            if (sample[0], sample[1]) == (tokenized[-2], tokenized[-1]):
                completions[sample[2]] = knm.prob(sample)
        if len(completions) == 0:
            response = "Can we talk about something else?"
        else:
            best = max(completions.keys(), key = (lambda key: completions[key]))
            tokenized + = [best]
            response = " ".join(tokenized)
    return response
#print(complete("Дело было в"))
