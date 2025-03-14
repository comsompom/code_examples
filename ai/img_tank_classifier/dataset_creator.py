# pylint: disable=E0401
"""The dataset creator. Finds and download the images to the labels folder"""
import os
from PIL import Image
from downloader import Downloader
from constants import (MAIN_DIR_NAME, IMAGE_LABEL_LIST, IMAGE_WIDTH, IMAGE_HEIGHT,
                       PERCENTAGE_AVERAGE_RESIZE)


class DatasetCreator:
    """
        The main class for dataset create
        to use it:

        labels_dataset = DatasetCreator(20, section_summary=True)
        image_height = labels_dataset.label_images_dataset_creator()

        First parameter for the number of the sample images to download
        Second parameter for showing the summary while module processing
    """

    def __init__(self, number_image_samples, section_summary=True):
        self.number_image_samples = number_image_samples
        self.section_summary = section_summary

    def _label_images_downloader(self, image_label) -> None:
        """private method to label images using the Downloader class"""
        image_sample_downloader = Downloader(MAIN_DIR_NAME)
        image_sample_downloader.download(keywords=image_label, limit=self.number_image_samples)

    def label_images_dataset_creator(self) -> int:
        """Create the labeled dataset"""
        heights_set = set()
        error_files_list = []

        for label in IMAGE_LABEL_LIST:
            if self.section_summary:
                print(f"DOWNLOAD label: {label}")
            self._label_images_downloader(label)

        for label in IMAGE_LABEL_LIST:
            cur_label_dir = f'{MAIN_DIR_NAME}/{label}'
            if self.section_summary:
                print(f"PROCESS resize Label: {label}")

            for item in os.listdir(cur_label_dir):
                cur_image_file_path = cur_label_dir + '/' + item

                if os.path.isfile(cur_image_file_path):
                    try:
                        cur_image = Image.open(cur_image_file_path)
                        cur_width, cur_height = cur_image.size
                        if cur_width < IMAGE_WIDTH and cur_image_file_path[:-3] != 'png':
                            os.remove(cur_image_file_path)
                            continue
                        new_height = cur_height // (cur_width // IMAGE_WIDTH)
                        heights_set.add(new_height)
                        cur_image = cur_image.resize((IMAGE_WIDTH, new_height))
                        cur_image.save(cur_image_file_path[:-4] + '.png')
                        if os.path.exists(cur_image_file_path):
                            os.remove(cur_image_file_path)
                    except Image.UnidentifiedImageError:
                        error_files_list.append(cur_image_file_path)

        average_height = int(sum(heights_set) / len(heights_set))
        height_possibility = (average_height // 100) * PERCENTAGE_AVERAGE_RESIZE

        for error_file in error_files_list:
            if os.path.exists(error_file):
                os.remove(error_file)

        for label in IMAGE_LABEL_LIST:
            cur_label_dir = f'{MAIN_DIR_NAME}/{label}'
            if self.section_summary:
                print(f"FINAL preparation Label: {label}")

            for file in os.listdir(cur_label_dir):
                cur_image_file_path = cur_label_dir + '/' + file
                cur_image = Image.open(cur_image_file_path)
                cur_width, cur_height = cur_image.size
                if cur_height > IMAGE_HEIGHT:
                    os.remove(cur_image_file_path)
                    if self.section_summary:
                        print(f"FILE Deleted As Highest: {file}")
                    continue
                if abs(average_height - cur_height) > height_possibility:
                    os.remove(cur_image_file_path)
                    if self.section_summary:
                        print(f"FILE Deleted As Not Comply to AVG: {file}")
                    continue
                if abs(average_height - average_height) <= height_possibility:
                    cur_image = cur_image.resize((IMAGE_WIDTH, average_height))
                cur_image = cur_image.convert('RGB')
                cur_image.save(cur_image_file_path[:-4] + '.jpg')
                if os.path.exists(cur_image_file_path):
                    os.remove(cur_image_file_path)

        for label in IMAGE_LABEL_LIST:
            cur_label_dir = f'{MAIN_DIR_NAME}/{label}'
            if self.section_summary:
                print(f"LABEL: {label} has {len(os.listdir(cur_label_dir))} images")

        return average_height
