# coding=utf-8

__version__ = "0.0.1"
__author__ = "DefaltSimon"
__license__ = "MIT"
__name__ = "adb-utility"

import logging
import importlib
import os

from adb.utilities import OptionWizard, shell
from adb.colors import Color

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CURRENT_DIR = os.getcwd()

COGS_DIR = os.path.join(SCRIPT_DIR, "cogs")

cogs = {}


def format_line(meta: dict) -> str:
    return f"{meta.get('title')} - {meta.get('description')}"


def start_server():
    print(f"{Color.BOLD}Waiting for adb daemon...{Color.END}", end="")
    shell("adb start-server")
    print(f"{Color.DARKCYAN}OK!{Color.END}\n\n")


def main():
    intro = "Adb Utility"
    print(f"{Color.BOLD}{'-' * 10}\n{intro}\n{'-' * 10}{Color.END}\n")

    start_server()

    # Loads cogs
    cog_names = [pl for pl in os.listdir(COGS_DIR)
                 if os.path.isfile(os.path.join(COGS_DIR, pl)) and pl.endswith(".py")]

    # Ordered "run" functions for each cog
    plugin_callbacks = []

    for c in cog_names:
        name = c.rstrip(".py")

        cog = importlib.import_module("cogs.{}".format(name))
        assert hasattr(cog, "run")
        assert hasattr(cog, "meta")

        cogs[name] = cog
        plugin_callbacks.append(cog.run)

    def get_meta():
        desc = []
        for m in cogs.keys():
            desc.append(format_line(cogs[m].meta))

        desc = sorted(desc)
        desc.append("Quit")
        return desc

    # Add a quit option
    plugin_callbacks.append(quit)

    # Show the options
    wiz_text = Color.BOLD + f"{Color.BLUE}Main Menu{Color.END}\nChoose your action:" + Color.END
    opt = OptionWizard(wiz_text, get_meta(), plugin_callbacks)
    resp = opt.run()

    kwargs = {
        "SCRIPT_DIR": SCRIPT_DIR,
        "CURRENT_DIR": CURRENT_DIR
    }

    while True:
        # Run the right cog
        data = resp(**kwargs)

        if data == "back":
            opt = OptionWizard(wiz_text, get_meta(), plugin_callbacks)
            resp = opt.run()
        elif data == "exit":
            break
        else:
            return


main()
