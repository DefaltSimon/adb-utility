# coding=utf-8
import os

from adb.utilities import OptionWizard, shell, get_full_path, get_json, quote
from adb.colors import Color

##########
# Adb push
##########

meta = {
    "title": "pull",
    "description": "Pulls some files"
}

invalid_chars = [a for a in "'\"*"]


def verify_path(path: str) -> bool:
    """
    Verify that a path is valid
    """
    if not path.startswith("/"):
        return False

    if any(sub in path for sub in invalid_chars):
        return False

    return True


def run(**kwargs):
    SCRIPT_DIR = kwargs.pop("SCRIPT_DIR")

    intro = Color.BOLD + "Adb Pull" + Color.END
    print(f"{'#' * 10}\n{intro}\n{'#' * 10}")

    running = True

    while running:
        # Choose remote file
        while True:
            remote = input("What file do you want to download:\n>")
            if verify_path(remote):
                break
            else:
                print("Invalid path, try again.")

        # Choose target directory
        favs = get_json(os.path.join(SCRIPT_DIR, "data", "favourites.json"))["pull"].get("local")
        if favs:
            paths = ["."] + favs + ["Custom"]
        else:
            paths = [".", "Custom"]

        print(paths)
        local_opt = OptionWizard("Where do you want to download the file to?", paths, paths)
        path = local_opt.run()

        if path == ".":
            path = os.getcwd()
        elif path == "Custom":
            while True:
                path = input("Enter your download path:")
                if verify_path(path):
                    break
                else:
                    print("Invalid path, try again.")

        # Run the download
        print(f"{Color.GREEN}Downloading {remote} to {path}... {Color.END}", end="")
        shell(f"adb pull {quote(remote)} {quote(path)}")
        print(f"{Color.GREEN}Done!{Color.END}")

        # Ask for another download
        opt_again = OptionWizard("Do you want to pull another file?", ["Yes", "No"])
        again = opt_again.run()

        if again == 2:
            break

    return "back"

