from dotenv import load_dotenv
from PIL import Image, UnidentifiedImageError

from email.message import EmailMessage
import mimetypes
import os
from pathlib import Path
import shutil
import smtplib
from tkinter.filedialog import askopenfilename, askdirectory, askopenfilenames


load_dotenv()


def send_email(data):
    while True:
        user_input: str = input("Press '1' to send file to an email address or '2' to exit\n>>> ")
        if user_input == '1':
            receiver_email = input("Please enter email address\n>>> ")
            break
        if user_input == '2':
            return "Thank You, Goodbye"

    path = Path(data)

    EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")

    message = EmailMessage()
    message["Subject"] = "With Love From Kach"
    message["From"] = EMAIL_ADDRESS
    message["To"] = receiver_email
    message.set_content("Please find attached your compressed photo")

    if Path.is_file(data):
        with open(data, "rb") as file:
            file_data = file.read()
            file_name = path.name
    else:
        compressed_directory = path.parent / "Compressed_Photos"
        shutil.make_archive(str(compressed_directory), 'zip', data)

        with open(f"{compressed_directory}.zip", "rb") as file:
            file_data = file.read()
            file_name = "Compressed_Photos.zip"

    mime_type, encoding = mimetypes.guess_type(file_name)
    if mime_type:
        # Split the MIME type into main type and subtype
        main_type, sub_type = mime_type.split('/', 1)

        message.add_attachment(file_data, maintype=main_type, subtype=sub_type, filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(message)


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
            break
        else:
            continue

    if type(file_path) is str:
        with Image.open(file_path) as im:

            path = Path(file_path)  # Create path object with picture path

            file_format: str = path.suffix  # .JPG
            file_name: str = path.stem  # IMG_1053

            new_file_name = f"{file_name}_compressed{file_format}"
            output_file = path.parent / new_file_name

            im.save(output_file, quality=int(quality))
            print("Success: File compressed and saved locally")

            return output_file

    else:
        for item in file_path:
            with Image.open(item) as im:

                path = Path(item)

                file_format: str = path.suffix
                file_name: str = path.stem

                new_file_name: str = f"{file_name}_compressed{file_format}"

                parent_directory = path.parent
                new_directory = parent_directory / "Compressed"

                output_file = new_directory / new_file_name

                if Path.is_dir(new_directory):
                    im.save(output_file, quality=int(quality))
                else:
                    Path.mkdir(new_directory)
                    im.save(output_file, quality=int(quality))

        print("Success: Files compressed and saved locally")

        return new_directory


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
            user_data = compress(user_path)
            send_email(user_data)
            break

        if user_choice == '4':
            print("Thank you, Goodbye")
            break

        print("Sorry, Invalid Entry\n")
