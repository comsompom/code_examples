# pylint: disable=E0401
# pylint: disable=R0902
# pylint: disable=R0913
# pylint: disable=R0917
# pylint: disable=C0103
# pylint: disable=R0904
# pylint: disable=W0201
# pylint: disable=W1514
# pylint: disable=W0621
# flake8: ignore=E501, W291, E127
"""The main module for text generation"""
import os
import requests
import numpy as np
from bs4 import BeautifulSoup

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences

from constants import (SOURCE_LINK, SOURCE_PATH, NUMERIC_TEXT,
                       MODEL_OPTIMIZER, MODEL_USE_LOSS, UNICODE_TO_ENG_DICT,
                       MODEL_PATH, MODEL_EPOCH, MODEL_BATCH_SIZE, LSTM_LENGTH,
                       MODEL_LENGTH_GENERATE, SOURCE_LINKS_LIST,
                       PUNCTUATION_SYMBOLS, EXCLUDE_PHRASE_LIST)


class NLPWordPProcessor:
    """NLP Processor for text generation"""
    def __init__(self, model_name: str, unicode=True, source_format='html',
                 use_punctuation=False, multilink=False, text_clean=False):
        self.model_name = model_name
        self.unicode_text = unicode
        if source_format.lower() == 'html':
            self.source_format = 'html'
        elif source_format.lower() == 'txt':
            self.source_format = 'txt'
        self.use_punctuation = use_punctuation
        self.multi_link = multilink
        self.source_link = SOURCE_LINK
        self.source_data_dir = SOURCE_PATH
        self.result_model_dir = MODEL_PATH
        self.exclude_phrase_list = EXCLUDE_PHRASE_LIST
        self.text_clean = text_clean
        self.source_text_path = self.source_data_dir + \
                                "/source_text_" + self.model_name + ".txt"
        self.model_weights_path = self.result_model_dir + \
                                  "/weights_" + self.model_name + ".h5"
        self.lstm_length = LSTM_LENGTH
        self.num_text = NUMERIC_TEXT
        self.unicode_to_eng = UNICODE_TO_ENG_DICT
        self.punctuation_symb = PUNCTUATION_SYMBOLS
        self.text = ""
        self.data = []
        self.generated_text = []
        self.model_builded = False
        self.model_trained = False

    def unicode_text_to_eng_symbols_encoder(self):
        """convert unicode symbols to english letters"""
        self.text = self.text.translate(str.maketrans("", "", self.num_text))
        for key, val in self.unicode_to_eng.items():
            self.text = self.text.replace(key, val)

    def source_base_text_from_url(self, link) -> None:
        """method for getting the text from provided url"""
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        text = text.lower()
        self.text += " "
        self.text += text
        if not self.use_punctuation:
            self.text = self.text.translate(
                str.maketrans("", "", self.punctuation_symb))
        if self.unicode_text:
            self.unicode_text_to_eng_symbols_encoder()

    def html_source_multi_link(self):
        """method for getting text from url lists"""
        for link in SOURCE_LINKS_LIST:
            self.source_base_text_from_url(link)

    def source_base_text_from_text_url(self, link):
        """crea te the text data from text url"""
        text = requests.get(link).text
        self.text += " "
        self.text += text
        if not self.use_punctuation:
            self.text = self.text.translate(
                str.maketrans("", "", self.punctuation_symb))
        if self.unicode_text:
            self.unicode_text_to_eng_symbols_encoder()

    def txt_source_multi_link(self):
        """utils method for getting multi text url"""
        for link in SOURCE_LINKS_LIST:
            self.source_base_text_from_text_url(link)

    def source_base_text_load(self):
        """methos check which source will be used html or txt"""
        if self.source_format == 'html':
            if not self.multi_link:
                self.source_base_text_from_url(self.source_link)
            elif self.multi_link:
                self.html_source_multi_link()
        if self.source_format == 'txt':
            if not self.multi_link:
                self.source_base_text_from_text_url(self.source_link)
            elif self.multi_link:
                self.txt_source_multi_link()

    def create_dir_if_not_exist(self, dir_name):
        """helped method for creating the folder if it is not exist"""
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)

    def remove_previous_exist_file(self):
        """utils method for removing file if it is exist"""
        self.create_dir_if_not_exist(self.source_data_dir)
        if os.path.exists(self.source_text_path):
            os.remove(self.source_text_path)

    def save_base_source_text_to_file(self):
        """save the source text to the file"""
        self.remove_previous_exist_file()
        if len(self.text) > 0:
            with open(self.source_text_path, 'a') as source_text_file:
                source_text_file.write(self.text)

    def load_source_text_to_data(self):
        """create the class data object with source text from file"""
        with open(self.source_text_path, 'r') as source_text_file:
            self.data = source_text_file.read().splitlines()

    def text_data_cleaner(self):
        """clean the source text from special chars and unused symbols"""
        data_cleaned = []
        for line in self.data:
            if len(line) > 1:
                counter = 0
                for element in self.exclude_phrase_list:
                    if element in line or element.upper() in line:
                        counter += 1

                if counter == 0:
                    line += "\n"
                    data_cleaned.append(line)
        self.data = data_cleaned
        with open(self.source_text_path, 'w') as source_text_file:
            source_text_file.writelines(data_cleaned)

    def prepare_data_from_source_text(self):
        """prepare the data object from source text"""
        self.source_base_text_load()
        self.save_base_source_text_to_file()
        self.load_source_text_to_data()
        if self.text_clean:
            self.text_data_cleaner()

    def tokenize_data(self):
        """make tokenization of the data object"""
        self.token = Tokenizer()
        self.token.fit_on_texts(self.data)
        self.encoded_text = self.token.texts_to_sequences(self.data)
        self.vocab_size = len(self.token.word_counts) + 1

    def build_sequences(self):
        """nlp method for build sequences"""
        datalist = []
        for d in self.encoded_text:
            if len(d) > 1:
                for i in range(2, len(d)):
                    datalist.append(d[:i])

        max_length = 20
        sequences = pad_sequences(datalist, maxlen=max_length, padding='pre')

        # X - input data, y - target data
        self.X = sequences[:, :-1]
        self.y = sequences[:, -1]

        self.y = to_categorical(self.y, num_classes=self.vocab_size)
        self.seq_length = self.X.shape[1]

    def build_nlp_model(self):
        """nlp method for building the model"""
        self.model = Sequential()
        self.model.add(Embedding(self.vocab_size, 50,
                                 input_length=self.seq_length))
        self.model.add(LSTM(self.lstm_length, return_sequences=True))
        self.model.add(LSTM(self.lstm_length))
        self.model.add(Dense(self.lstm_length, activation='relu'))
        self.model.add(Dense(self.vocab_size, activation='softmax'))
        self.model_builded = True

    def check_model_summary(self):
        """report model summary when it is builded successful"""
        if self.model_builded:
            self.model.summary()

    def compile_and_train_model(self):
        """compilation and train the model"""
        if self.model_builded:
            self.model.compile(loss=MODEL_USE_LOSS, optimizer=MODEL_OPTIMIZER,
                               metrics=['accuracy'])
            self.model.fit(self.X, self.y, batch_size=MODEL_BATCH_SIZE,
                           epochs=MODEL_EPOCH)
            self.model_trained = True

    def save_model_weights_to_file(self):
        """save the weights of the prediction from current model"""
        self.create_dir_if_not_exist(self.result_model_dir)
        if self.model_trained:
            self.model.save(self.model_weights_path)

    def model_from_scratch(self, show_summary=False):
        """create the model from the scratch without using weights"""
        # use this method for empty source text file and empty model
        self.prepare_data_from_source_text()
        self.tokenize_data()
        self.build_sequences()
        self.build_nlp_model()
        if show_summary:
            self.check_model_summary()
        self.compile_and_train_model()
        self.save_model_weights_to_file()

    def load_weights_to_model(self):
        """load the saved weights to the model to work with the weights"""
        if self.model_builded:
            self.model.load_weights(self.model_weights_path)
            self.model_trained = True

    def model_from_weights(self, show_summary=False):
        """retrain the model with the saved weights"""
        # use this method for already calculated weights
        self.load_source_text_to_data()
        self.tokenize_data()
        self.build_sequences()
        self.build_nlp_model()
        if show_summary:
            self.check_model_summary()
        self.load_weights_to_model()

    def generate_words_text(self, seed_text, number_lines):
        """generate the test the main method"""
        if self.model_trained:
            for _ in range(number_lines):
                text_word_list = []
                for _ in range(MODEL_LENGTH_GENERATE):
                    encoded = self.token.texts_to_sequences([seed_text])
                    encoded = pad_sequences(encoded, maxlen=self.seq_length,
                                            padding='pre')

                    y_pred = np.argmax(self.model.predict(encoded), axis=-1)

                    predicted_word = ""
                    for word, index in self.token.word_index.items():
                        if index == y_pred:
                            predicted_word = word
                            break

                    seed_text += ' ' + predicted_word
                    text_word_list.append(predicted_word)

                seed_text = text_word_list[-1]
                self.generated_text = ' '.join(text_word_list)
                self.generated_text += '\n'


nlp_model = NLPWordPProcessor("fair_tales", unicode=False, source_format='txt',
                              use_punctuation=True, multilink=True,
                              text_clean=True)

nlp_model.model_from_scratch(True)
# nlp_model.model_from_weights()
seed_text = 'and the night cover the forest'
nlp_model.generate_words_text(seed_text, 3)
print(nlp_model.generated_text)
