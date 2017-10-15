# coding=utf-8
import os
from adb.utilities import OptionWizard, get_json, shell, quote
from adb.colors import Color

##########
# Adb push
##########

meta = {
    "title": "Push",
    "description": "Pushes some files"
}


whitelists = ["/storage/"]


def is_okay_path(path: str) -> bool:
    for w in whitelists:
        if not path.startswith(w):
            return False

    return True


def get_cd_files(directory: str) -> list:
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def get_full_path(file: str) -> str:
    return os.path.abspath(file)


def run(**kwargs):
    intro = Color.BOLD + "Adb Push" + Color.END
    print(f"{'#' * 10}\n{intro}\n{'#' * 10}")

    running = True

    while running:
        # Choose local file
        files = get_cd_files(kwargs.get("CURRENT_DIR"))
        file_chooser = OptionWizard("Which file do you wish to upload?", files, files)
        file = file_chooser.run()

        # Load favourites
        favs = get_json(os.path.join(kwargs.get("SCRIPT_DIR"), "data", "favourites.json"))["remote"]
        favs.append("Custom")

        # Get remote location
        remote_chooser = OptionWizard("Where do you want to upload {}?".format(file), favs, favs)
        remote_path = remote_chooser.run()

        if remote_path == "Custom":
            remote_path = input("Enter your path:")
            if not is_okay_path(remote_path):
                print(f"{Color.BOLD}{Color.RED}Not a whitelisted path!{Color.END}")
                continue

        # Upload the file
        print(f"{Color.GREEN}Uploading {file} to {remote_path}... {Color.END}", end="")
        resp = shell(f"adb push {quote(get_full_path(file))} {quote(remote_path)}")
        print(f"{Color.GREEN}Done!{Color.END}")
        print(resp)

        # Ask for another upload
        opt_again = OptionWizard("Do you want to upload another file?", ["Yes", "No"])
        again = opt_again.run()

        if again == 2:
            break


    return "back"

