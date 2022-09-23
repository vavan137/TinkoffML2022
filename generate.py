import argparse
import pickle
from train import NgramModel

#`--model` путь к файлу, из которого загружается модель.
#`--prefix` необязательный аргумент. Начало предложения (одно или несколько слов). Если не указано, выбираем начальное слово случайно из всех слов.
#`--length` длина генерируемой последовательности.

parser = argparse.ArgumentParser()
parser.add_argument('--model',  type=str, required=True)
parser.add_argument('--prefix', type=str, required=True)
parser.add_argument('--length', type=str, required=True)
args = parser.parse_args()
####

NgramModel.predict(str(args.model), str(args.prefix), int(args.length))
