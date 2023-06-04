from dotenv import load_dotenv
from PIL import Image, UnidentifiedImageError

from email.message import EmailMessage
import mimetypes
import os
import re
import shutil
import smtplib
from tkinter.filedialog import askopenfilename, askdirectory, askopenfilenames


load_dotenv()


def send_email(data):

    attachment: str = data[0]
    receiver_email: str = data[1]
    file_name: str = data[2]

    if receiver_email == "":
        print("Thank You, Goodbye")
    else:

        EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS")
        EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")

        message = EmailMessage()
        message["Subject"] = "With Love From Kach"
        message["From"] = EMAIL_ADDRESS
        message["To"] = receiver_email
        message.set_content("Please find attached your compressed photo")

        maintype, _, subtype = (mimetypes.guess_type(file_name)[0] or 'application/octet-stream').partition("/")

        with open(attachment, 'rb') as file:
            file_data = file.read()

        message.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)

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
    output_file: str = ""
    user_email: str = ""
    new_file_name: str = ""

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

                new_file_name = f"{file_name}_compressed.{file_format}"
                output_file = file_path.replace(image_file, new_file_name)

                im.save(output_file, quality=int(quality))
                print("Success: File compressed and saved locally")

        else:
            for path in file_path:
                with Image.open(path) as im:
                    image_file: str = re.split(r"/|\\", path)[-1]
                    file_format: str = image_file.split('.')[1]
                    file_name: str = image_file.split('.')[0]

                    new_file_name: str = f"{file_name}_compressed.{file_format}"

                    slash_sign = path[-len(image_file) - 1]
                    parent_directory = path.removesuffix(image_file)
                    new_directory = os.path.join(parent_directory, "Compressed" + slash_sign)

                    output_file: str = new_directory + new_file_name

                    if os.path.isdir(new_directory):
                        im.save(output_file, quality=int(quality))
                    else:
                        os.mkdir(new_directory)
                        im.save(output_file, quality=int(quality))

            print("Success: Files compressed and saved locally")

        while True:
            user_input: str = input("Press '1' to send file to an email address or '2' to exit\n>>> ")
            if user_input == '1':
                user_email = input("Please enter email address\n>>> ")
                shutil.make_archive()
                break
            if user_input == '2':
                break

        return output_file, user_email, new_file_name


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
