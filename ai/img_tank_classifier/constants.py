# noqa: E501,W291
"""The constants for the dataset creator module"""
MAIN_DIR_NAME = 'labels'
IMAGE_LABEL_LIST = ['T 72 tank', 'T 80 tank', 'T 90 tank']

TIME_SLEEP_AFTER_EACH_DOWNLOAD = 2

IMAGE_WIDTH = 200
IMAGE_HEIGHT = 200

EACH_LABEL_COUNT = 200

PERCENTAGE_AVERAGE_RESIZE = 15

BATCH_SIZE = 32

MODEL_EPOCH = 25
MODEL_OPTIMIZER = 'adam'
MODEL_LAYER_ACTIVATION = 'relu'

PRETRAINED_WEIGHTS_PATH = "model_T 72 tank_T 80 tank_T 90 tank.hdf5"

'''
Lists of the other russian orcks military techick

"Self-propelled artillery"
['2S1 Gvozdika', '2S3 Akatsiya', '2S7 Pion', '2S7M Malka', '2S9 Nona', '2S19 Msta S']

"Rocket artillery"
['BM-21 Grad', 'BM-27 Uragan', 'BM-30 Smerch', '9A52-4 Tornado', 'TOS-1A Solntsepyok', 'Grad-K', 
'Cheburashka', 'Snezhinka']

"Air defense platforms
['ZSU-23-4 Shilka', '2K22 Tunguska', '9K33 Osa', '9K35 Strela-10', '9K37 Buk', '9K330 Tor',
'Pantsir-S1', 'S-300', 'S-350 Vityaz', 'S-400 Triumf']

"Tanks"
['T-54', 'T-55', 'T-53', 'T-62', 'T-64', 'T-72', 'T-80', 'T-90']
['T 54 tank', 'T 55 tank', 'T 53 tank', 'T 62 tank', 'T 64 tank',
                    'T 72 tank', 'T 80 tank', 'T 90 tank']

"Infantry fighting vehicles"
['BMP-1', 'BMP-2', 'BMP-3', 'BMD-2', 'BMD-4']

"Armored personnel carriers"
['MT-LB', 'MT-LB', 'BTR-50', 'BTR-60', 'BTR-70', 'BTR-80', 'BTR-82', 'BTR-D', 
'BTR-MD Rakushka', 'BMO-T']

'''
