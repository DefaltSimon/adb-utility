# coding=utf-8
from adb.utilities import shell
from adb.colors import Color


##########
# Adb restarter
##########

meta = {
    "title": "restart",
    "description": "Restart the adb daemon"
}


def run(**kwargs):
    intro = "Adb Restarter"
    print(f"{'-' * 11}\n{intro}\n{'-' * 11}")

    r = input("Are you sure you want to restart adb? y/n\n>")
    if r.lower() != "y":
        print(f"{Color.BOLD}Aborting...{Color.END}")
        return "back"

    print(f"\n{Color.DARKCYAN}Restarting adb server...{Color.END}", end="")
    shell("adb kill-server")
    shell("adb start-server")
    print(f"{Color.CYAN}Done!{Color.END}\n")

    return "back"
