from model import SecretDictionary
import uuid
import os


option_main = input("1. Create new secret box\n2. Open secret box \nType what you want to do: ")
if option_main == "1":

    secret = input("Create a new secret: ")
    box = SecretDictionary(secret)

    cont = "y"
    while(cont == "y"):
        key = input("Type the name of the key you want to add: ")
        value = input("Type the password you want to protect: ")
        box.add_secret(key, value)
        cont = input("Continue?(y/n): ")

    curpath = os.path.abspath(os.curdir)
    file_path = "{}/sicherheitsdienst-{}.sss".format(curpath, str(uuid.uuid4()))
    text_file = open(file_path, "w+")
    text_file.write(box.lock())
    text_file.close()

elif option_main == "2":
    pass
else:
    print("You suck!")
