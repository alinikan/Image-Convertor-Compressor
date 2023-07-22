import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os
import pyheif


class ImageConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.valid_image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.heic']
        self.formats = {
            '1': 'JPEG',
            '2': 'PNG',
            '3': 'BMP',
            '4': 'TIFF'
        }

    def select_image(self):
        image_path = filedialog.askopenfilename()
        if not image_path:
            print("No image selected.")
            return None
        return image_path

    def validate_image(self, image_path):
        if not os.path.isfile(image_path):
            print(f"The file {image_path} does not exist.")
            return False
        _, extension = os.path.splitext(image_path)
        if extension.lower() not in self.valid_image_extensions:
            print(
                f"Invalid image format. Please select an image with one of the following extensions: {', '.join(self.valid_image_extensions)}")
            return False
        return True

    def convert_image(self, image_path):
        print("Please select the format you want to convert your image to:")
        for key, value in self.formats.items():
            print(f"{key}: {value}")
        user_input = input("Enter your choice (or 'q' to quit): ")
        if user_input == 'q':
            print("Exiting the program.")
            return 'q'
        elif user_input not in self.formats.keys():
            print("Invalid choice. Please select a valid format.")
            return
        output_path = f"{os.path.splitext(image_path)[0]}_converted.{self.formats[user_input].lower()}"
        try:
            _, extension = os.path.splitext(image_path)
            if extension.lower() == '.heic':
                heif_file = pyheif.read(image_path)
                image = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                    heif_file.mode,
                    heif_file.stride,
                )
            else:
                image = Image.open(image_path)
            image.save(output_path, self.formats[user_input])
            print(f"Image converted successfully. Saved as {output_path}.")
        except Exception as e:
            print(f"An error occurred during conversion: {str(e)}")

    def run(self):
        while True:
            image_path = self.select_image()
            if image_path is None or not self.validate_image(image_path):
                user_input = input("Do you want to try again? (y/n): ")
                if user_input.lower() != 'y':
                    print("Exiting the program.")
                    break
                else:
                    continue
            if self.convert_image(image_path) == 'q':
                break
            user_input = input("Do you want to convert another image? (y/n): ")
            if user_input.lower() != 'y':
                print("Exiting the program.")
                break


if __name__ == "__main__":
    converter = ImageConverter()
    converter.run()
