import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import os
import pyheif


class ImageConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Converter")
        self.root.geometry("500x300")
        self.image_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.format_var = tk.StringVar()
        self.valid_image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.heic']
        self.formats = ['JPEG/JPG', 'PNG', 'BMP', 'TIFF']

        self.create_widgets()

    def create_widgets(self):
        browse_button = tk.Button(self.root, text="Browse", command=self.select_image)
        browse_button.pack(pady=10)

        self.path_label = tk.Label(self.root, text="No image selected")
        self.path_label.pack()

        format_label = tk.Label(self.root, text="Select format:")
        format_label.pack(pady=10)

        self.format_dropdown = ttk.Combobox(self.root, textvariable=self.format_var, values=self.formats)
        self.format_dropdown.pack()

        dir_button = tk.Button(self.root, text="Select Output Directory", command=self.select_output_dir)
        dir_button.pack(pady=10)

        self.dir_label = tk.Label(self.root, text="No directory selected")
        self.dir_label.pack()

        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert_image, state=tk.DISABLED)
        self.convert_button.pack(pady=10)

    def select_image(self):
        image_path = filedialog.askopenfilename()
        if image_path:
            self.image_path.set(image_path)
            self.path_label.config(text=f"Selected Image: {image_path}")
            self.check_ready()
        else:
            messagebox.showerror("Error", "No image selected.")

    def select_output_dir(self):
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.output_dir.set(output_dir)
            self.dir_label.config(text=f"Output Directory: {output_dir}")
            self.check_ready()
        else:
            messagebox.showerror("Error", "No directory selected.")

    def check_ready(self):
        if self.image_path.get() and self.output_dir.get() and self.format_var.get():
            self.convert_button.config(state=tk.NORMAL)
        else:
            self.convert_button.config(state=tk.DISABLED)

    def convert_image(self):
        image_path = self.image_path.get()
        output_dir = self.output_dir.get()
        if image_path and self.validate_image(image_path):
            _, extension = os.path.splitext(image_path)
            selected_format = self.format_var.get()
            if selected_format == "JPEG/JPG":
                selected_format = "JPEG"
                output_extension = "jpg"
            else:
                output_extension = selected_format.lower()
            if selected_format.lower() == extension[1:].lower():
                messagebox.showerror("Error", "The selected format is the same as the original format. Please choose a different format.")
                return
            output_path = os.path.join(output_dir,
                                       f"{os.path.splitext(os.path.basename(image_path))[0]}_converted.{output_extension}")
            try:
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
                image.save(output_path, selected_format)
                messagebox.showinfo("Success", f"Image converted successfully. Saved as {output_path}.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during conversion: {str(e)}")

    def validate_image(self, image_path):
        if not os.path.isfile(image_path):
            messagebox.showerror("Error", f"The file {image_path} does not exist.")
            return False
        _, extension = os.path.splitext(image_path)
        if extension.lower() not in self.valid_image_extensions:
            messagebox.showerror("Error", f"Invalid image format. Please select an image with one of the following extensions: {', '.join(self.valid_image_extensions)}")
            return False
        return True

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    converter = ImageConverter()
    converter.run()
