from nltk.corpus.reader.api import CorpusReader
from nltk.corpus.reader.api import CategorizedCorpusReader
import codecs
from readability.readability import Unparseable
from readability.readability import Document as Paper
import bs4
from nltk import sent_tokenize
from nltk import wordpunct_tokenize
import time

CAT_PATTERN = r'([a-z_\s]+)/.*'
DOC_PATTERN = r'(?!\.)[a-z_\s]+/[a-f0-9]+\.json'
TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'li']

class HTMLCorpusReader(CategorizedCorpusReader, CorpusReader):
    """
    Объект чтения корпуса с HTML-документами для получения
    возможности дополнительной предварительной обработки.
    """
    def __init__(self, root, fileids = DOC_PATTERN, encoding = 'utf8',tags = TAGS, **kwargs):
        """
        Инициализирует объект чтения корпуса.
        Аргументы, управляющие классификацией
        (``cat_pattern``, ``cat_map`` и ``cat_file``), передаются
        в конструктор ``CategorizedCorpusReader``. остальные аргументы
        передаются в конструктор ``CorpusReader``.
        """
        # Добавить шаблон категорий, если он не был передан в класс явно.
        if not any(key.startswith('cat_') for key in kwargs.keys()):
            kwargs['cat_pattern'] = CAT_PATTERN
        # Инициализировать объекты чтения корпуса из NLTK
        CategorizedCorpusReader.__init__(self, kwargs)
        CorpusReader.__init__(self, root, fileids, encoding)
        # Сохранить теги, подлежащие извлечению.
        self.tags = tags
    def resolve(self, fileids, categories):
        """
        Возвращает список идентификаторов файлов или названий категорий,
        которые передаются каждой внутренней функции объекта чтения корпуса. 
        Реализована по аналогии с ``CategorizedPlaintextCorpusReader`` в NLTK.
        """
        if fileids is not None and categories is not None:
            raise ValueError("Specify fileids or categories, not both")
        if categories is not None:
            return self.fileids(categories)
        return fileids

    def docs(self, fileids = None, categories = None):
        """
        Возвращает полный текст HTML-документа, закрывая его
        по завершении чтения.
        """
        # Получить список файлов для чтения
        fileids = self.resolve(fileids, categories)
        # Создать генератор, загружающий документы в память по одному.
        for path, encoding in self.abspaths(fileids, include_encoding = True):
            with codecs.open(path, 'r', encoding = encoding) as f:
                yield f.read()

    def html(self, fileids = None, categories = None):
        """
        Возвращает содержимое HTML каждого документа, очищая его
        с помощью библиотеки readability-lxml.
        """
        for doc in self.docs(fileids, categories):
            try:
                yield Paper(doc).summary()
            except Unparseable as e:
                print("Could not parse HTML: {}".format(e))
                continue

# Теги для извлечения абзацев из HTML-документов
#tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'li']
    def paras(self, fileids = None, categories = None):
        """
        Использует BeautifulSoup для выделения абзацев из HTML.
        """
        for html in self.html(fileids, categories):
            soup = bs4.BeautifulSoup(html, 'lxml')
            for element in soup.find_all(tags):
                yield element.text
            soup.decompose()

    def sents(self, fileids = None, categories = None):
        """
        Использует встроенный механизм для выделения предложений из
        абзацев. Обратите внимание, что для парсинга разметки HTML
        этот метод использует BeautifulSoup.
        """
        for paragraph in self.paras(fileids, categories):
            for sentence in sent_tokenize(paragraph):
                yield sentence

    def words(self, fileids = None, categories = None):
        """
        Использует встроенный механизм для выделения слов из предложений.
        Обратите внимание, что для парсинга разметки HTML
        этот метод использует BeautifulSoup
        """
        for sentence in self.sents(fileids, categories):
            for token in wordpunct_tokenize(sentence):
                yield token

    def describe(self, fileids = None, categories = None):
        """
        Выполняет обход содержимого корпуса и возвращает
        словарь с разнообразными оценками, описывающими
        состояние корпуса.
        """
        started = time.time()
        # Структуры для подсчета.
        counts = nltk.FreqDist()
        tokens = nltk.FreqDist()
        # Выполнить обход абзацев, выделить лексемы и подсчитать их
        for para in self.paras(fileids, categories):
            counts['paras'] += 1
            for sent in para:
                counts['sents'] += 1
                for word, tag in sent:
                    counts['words'] += 1
                    tokens[word] += 1
        # Определить число файлов и категорий в корпусе
        n_fileids = len(self.resolve(fileids, categories) or self.fileids())
        n_topics = len(self.categories(self.resolve(fileids, categories)))
        # Вернуть структуру данных с информацией
        return {
            'files': n_fileids,
            'topics': n_topics,
            'paras': counts['paras'],
            'sents': counts['sents'],
            'words': counts['words'],
            'vocab': len(tokens),
            'lexdiv': float(counts['words']) / float(len(tokens)),
            'ppdoc': float(counts['paras']) / float(n_fileids),
            'sppar': float(counts['sents']) / float(counts['paras']),
            'secs': time.time() - started,
        }



'Параметры `train.py`:

'--input-dir` путь к директории, в которой лежит коллекция документов. Если данный аргумент не задан, считать, что тексты вводятся из stdin.
'--model`  путь к файлу, в который сохраняется модель.
