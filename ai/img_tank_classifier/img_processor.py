import tensorflow as tf
import numpy as np
import os
import requests
from dataset_creator import DatasetCreator
from constants import (MAIN_DIR_NAME, BATCH_SIZE, IMAGE_WIDTH, IMAGE_HEIGHT, EACH_LABEL_COUNT, MODEL_OPTIMIZER,
                       MODEL_LAYER_ACTIVATION, MODEL_EPOCH, PRETRAINED_WEIGHTS_PATH)


class ImgClassifierProcessor:

    def __init__(self, new_dataset=True, show_logs=True, use_weights=False, model_augment=False):
        self.image_width = IMAGE_WIDTH
        self.image_height = IMAGE_HEIGHT
        self.dataset_root_dir = MAIN_DIR_NAME
        self.new_dataset = new_dataset
        self.show_logs = show_logs
        self.augmentation = model_augment
        self.use_weights = use_weights
        self.class_names_list = []
        self.trained = False
        self.model = None

    def _create_new_dataset(self):
        labels_dataset = DatasetCreator(EACH_LABEL_COUNT, self.show_logs)
        self.image_height = labels_dataset.label_images_dataset_creator()
        if self.show_logs:
            print(f"New Images Dataset created at the: '{self.dataset_root_dir}' Folder")

    def _create_and_compile_model(self) -> None:
        self.train_ds = tf.keras.utils.image_dataset_from_directory(
            self.dataset_root_dir,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(self.image_height, self.image_width),
            batch_size=BATCH_SIZE)

        self.val_ds = tf.keras.utils.image_dataset_from_directory(
            self.dataset_root_dir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(self.image_height, self.image_width),
            batch_size=BATCH_SIZE)

        self.class_names_list = self.train_ds.class_names
        if self.show_logs:
            print(f"Current Model Classification Classes: {self.class_names_list}")

        AUTOTUNE = tf.data.AUTOTUNE
        self.train_ds = self.train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        self.val_ds = self.val_ds.cache().prefetch(buffer_size=AUTOTUNE)

        normalization_layer = tf.keras.layers.Rescaling(1. / 255)

        normalized_ds = self.train_ds.map(lambda x, y: (normalization_layer(x), y))
        image_batch, labels_batch = next(iter(normalized_ds))
        first_image = image_batch[0]
        if self.show_logs:
            print(f"Normalized pixels: {np.min(first_image), np.max(first_image)}")

        num_classes = len(self.class_names_list)
        self.model = tf.keras.Sequential([
            tf.keras.layers.Rescaling(1. / 255, input_shape=(self.image_height, self.image_width, 3)),
            tf.keras.layers.Conv2D(16, 3, padding='same', activation=MODEL_LAYER_ACTIVATION),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(32, 3, padding='same', activation=MODEL_LAYER_ACTIVATION),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(64, 3, padding='same', activation=MODEL_LAYER_ACTIVATION),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation=MODEL_LAYER_ACTIVATION),
            tf.keras.layers.Dense(num_classes)
        ])

        self._compile_model()

        if self.show_logs:
            self.model.summary()

    def _compile_model(self) -> None:
        self.model.compile(optimizer=MODEL_OPTIMIZER,
                           loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                           metrics=['accuracy'])

    def _train_model(self) -> None:
        self.model.fit(
            self.train_ds,
            validation_data=self.val_ds,
            epochs=MODEL_EPOCH
        )
        model_weights_file_name = "model_" + "_".join(self.class_names_list) + ".hdf5"
        self.model.save(model_weights_file_name)
        self.trained = True

    def _model_dataset_augmentation(self) -> None:
        data_augmentation = tf.keras.Sequential(
            [
                tf.keras.layers.RandomFlip("horizontal", input_shape=(self.image_height, self.image_width, 3)),
                tf.keras.layers.RandomRotation(0.1),
                tf.keras.layers.RandomZoom(0.1),
            ]
        )

        self.model = tf.keras.Sequential([
            data_augmentation,
            tf.keras.layers.Rescaling(1. / 255),
            tf.keras.layers.Conv2D(16, 3, padding='same', activation=MODEL_LAYER_ACTIVATION),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(32, 3, padding='same', activation=MODEL_LAYER_ACTIVATION),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(64, 3, padding='same', activation=MODEL_LAYER_ACTIVATION),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation=MODEL_LAYER_ACTIVATION),
            tf.keras.layers.Dense(len(self.class_names_list))
        ])

        self._compile_model()

        if self.show_logs:
            self.model.summary()

    def _load_pretrained_weights(self) -> None:
        if os.path.exists(PRETRAINED_WEIGHTS_PATH):
            self.model.load_weights(PRETRAINED_WEIGHTS_PATH)

    def model_train_process(self) -> None:
        if self.new_dataset:
            self._create_new_dataset()
        self._create_and_compile_model()
        if self.use_weights:
            self._load_pretrained_weights()
        self._train_model()

        if self.augmentation:
            self._model_dataset_augmentation()
            self._train_model()

    def _create_model_from_weights(self) -> None:
        self._create_and_compile_model()
        self._load_pretrained_weights()
        self.trained = True

    def _predict_the_image(self, img_url: str) -> dict:
        predict_image_name = 'predict_image.jpg'
        request_response = requests.get(img_url, allow_redirects=True)
        with open(predict_image_name, 'wb') as img_file:
            img_file.write(request_response.content)

        img = tf.keras.utils.load_img(
            predict_image_name, target_size=(self.image_height, self.image_width)
        )
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        predictions = self.model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        return {
            'predict_class': self.class_names_list[np.argmax(score)],
            'predict_percent': 100 * np.max(score),
            'status': 200
        }

    def model_prediction_process(self, img_url: str) -> dict:
        if self.trained:
            response = self._predict_the_image(img_url)
        else:
            if self.use_weights and self.new_dataset is False:
                self._create_model_from_weights()
            else:
                self.model_train_process()
            response = self._predict_the_image(img_url)

        return response


img_url = "https://thediplomat.com/wp-content/uploads/2016/07/sizes/medium/thediplomat_2016-07-19_16-31-08.jpg"
image_processor = ImgClassifierProcessor(new_dataset=False, show_logs=True, use_weights=True, model_augment=False)
prediction = image_processor.model_prediction_process(img_url)
print(prediction)
