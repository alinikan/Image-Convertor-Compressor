import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os


def select_image():
    root = tk.Tk()
    root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
    image_path = filedialog.askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    if not image_path:
        print("No image selected. Exiting the program.")
        exit()
    return image_path


def validate_image(image_path):
    valid_image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    _, extension = os.path.splitext(image_path)
    if extension.lower() not in valid_image_extensions:
        print(
            f"Invalid image format. Please select an image with one of the following extensions: {', '.join(valid_image_extensions)}")
        return False
    return True


def convert_image(image_path):
    formats = {
        '1': 'JPEG',
        '2': 'PNG',
        '3': 'BMP',
        '4': 'TIFF'
    }
    print("Please select the format you want to convert your image to:")
    for key, value in formats.items():
        print(f"{key}: {value}")
    user_input = input("Enter your choice (or 'q' to quit): ")
    if user_input == 'q':
        print("Exiting the program.")
        exit()
    elif user_input not in formats.keys():
        print("Invalid choice. Please select a valid format.")
        return
    output_path = f"{os.path.splitext(image_path)[0]}_converted.{formats[user_input].lower()}"
    img = Image.open(image_path)
    img.save(output_path, formats[user_input])
    print(f"Image converted successfully. Saved as {output_path}.")


def main():
    while True:
        image_path = select_image()
        if validate_image(image_path):
            convert_image(image_path)
        else:
            continue
        user_input = input("Do you want to convert another image? (y/n): ")
        if user_input.lower() != 'y':
            break


if __name__ == "__main__":
    main()
