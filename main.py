from PIL import Image, UnidentifiedImageError

import os
import re
from tkinter.filedialog import askopenfilename, askdirectory, askopenfilenames


def is_valid_image(file: str):
    try:
        with Image.open(file) as im:
            return True
    except UnidentifiedImageError:
        return False


def compress(file_path):
    while True:

        quality: str = input("Specify quality (1 - 100)\n>>> ")
        if quality.isdigit() and int(quality) in range(1, 101):
            pass
        else:
            continue

        if type(file_path) is str:
            with Image.open(file_path) as im:
                image_file: str = re.split(r"/|\\", file_path)[-1]
                file_format: str = image_file.split('.')[1]
                file_name: str = image_file.split('.')[0]

                new_file_name: str = f"{file_name}_compressed.{file_format}"

                output_file: str = file_path.replace(image_file, new_file_name)

                im.save(output_file, quality=int(quality))

        return "list"


def get_path(choice: str):
    if choice == '1':
        path: str = askopenfilename()
        if is_valid_image(path):
            return path
        return None

    if choice == '2':
        paths_list: list = []
        paths: str = askopenfilenames()
        for path in paths:
            if is_valid_image(path):
                paths_list.append(path)

        return paths_list

    if choice == '3':
        paths_list: list = []
        directory_path: str = askdirectory()

        for path in os.listdir(directory_path):
            file_path: str = os.path.join(directory_path, path)
            if is_valid_image(file_path):
                paths_list.append(file_path)

        return paths_list


if __name__ == '__main__':
    while True:
        user_choice: str = input("Press '1' to select a file\nPress '2' to select multiple files"
                                 "\nPress '3' to select a folder\nPress '4' to exit\n>>> ")

        if user_choice.isdigit() and int(user_choice) in range(1, 4):
            user_path = get_path(user_choice)
            compress(user_path)
            break

        if user_choice == '4':
            print("Thank you, Goodbye")
            break

        print("Sorry, Invalid Entry\n")
