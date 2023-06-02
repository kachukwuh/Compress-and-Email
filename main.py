from PIL import Image, UnidentifiedImageError

import os
from tkinter.filedialog import askopenfilename, askdirectory, askopenfilenames


def is_valid_image(file: str):
    try:
        with Image.open(file) as im:
            return True
    except UnidentifiedImageError:
        return False


def get_path():
    while True:
        user_choice: str = input("Press '1' to select a file\nPress '2' to select multiple files"
                                 "\nPress '3' to select a folder\nPress '4' to exit\n>>> ")

        if user_choice == '1':
            path: str = askopenfilename()
            if is_valid_image(path):
                return path
            return None

        if user_choice == '2':
            paths_list: list = []
            paths: str = askopenfilenames()
            for path in paths:
                if is_valid_image(path):
                    paths_list.append(path)

            return paths_list

        if user_choice == '3':
            paths_list: list = []
            directory_path: str = askdirectory()

            for path in os.listdir(directory_path):
                file_path: str = os.path.join(directory_path, path)
                if is_valid_image(file_path):
                    paths_list.append(file_path)

            return paths_list

        if user_choice == '4':
            return "Thank you, Goodbye"

        print("Sorry, Invalid Entry\n")


if __name__ == '__main__':
    print(get_path())
