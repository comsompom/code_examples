# the link for getting the text
SOURCE_LINK = 'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%BB%D0%BA_%D0%B8%D0%BC%D0%B5%D0%BD%D0%B8_%D0%9A%D0%B0%D1%81%D1%82%D1%83%D1%81%D1%8F_%D0%9A%D0%B0%D0%BB%D0%B8%D0%BD%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B3%D0%BE'

SOURCE_LINKS_LIST = [
    'https://www.gutenberg.org/cache/epub/27200/pg27200.txt',
    'https://www.gutenberg.org/cache/epub/52521/pg52521.txt'
]

# list for the text data cleaner
EXCLUDE_PHRASE_LIST = ["gutenberg", "ebook", "Title:", "Translator:", "Release date:",
                       "updated:", "Illustration:", "Language:", "copyright notice", "Credits:",
                       "*** START OF THE PROJECT", "preface", "_From the", "_Adapted from",
                       "Project Gutenberg", "eBook", "_From Church's", "_From Joyce", "Gutenberg",
                       "the Project"]

# dir names for the model data and results
SOURCE_PATH = 'data'
MODEL_PATH = 'results'

# extra symbols for removing from the source text
NUMERIC_TEXT = '0123456789'

PUNCTUATION_SYMBOLS = '.,!?:;-_={}[]#@$%^&*«»"'

# dict for unicode encoding from rus lang to encoded
UNICODE_TO_ENG_DICT = {
    'а': "a",
    'б': "b",
    'в': "v",
    'г': "g",
    'д': "d",
    'е': "e",
    'ж': "zh",
    'з': "z",
    'и': "i",
    'й': "ii",
    'к': "k",
    'л': "l",
    'м': "m",
    'н': "n",
    'о': "o",
    'п': "p",
    'р': "r",
    'с': "s",
    'т': "t",
    'у': "u",
    'ф': "f",
    'х': "h",
    'ц': "c",
    'ч': "ch",
    'ш': "sh",
    'щ': "shch",
    'ъ': "",
    'ы': "i",
    'ь': "",
    'э': "e",
    'ю': "iu",
    'я': "ia",
    'ё': "io"
}

# nlp model constants
MODEL_EPOCH = 50
MODEL_BATCH_SIZE = 32

MODEL_OPTIMIZER = 'adam'
LSTM_LENGTH = 100
MODEL_USE_LOSS = 'categorical_crossentropy'

MODEL_LENGTH_GENERATE = 50
