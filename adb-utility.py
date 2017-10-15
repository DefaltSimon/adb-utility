# coding=utf-8

__version__ = "0.0.1"
__author__ = "DefaltSimon"
__license__ = "MIT"
__name__ = "adb-utility"

import logging
import importlib
import os

from adb.utilities import OptionWizard
from adb.colors import Color

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CURRENT_DIR = os.getcwd()

COGS_DIR = os.path.join(SCRIPT_DIR, "cogs")

cogs = {}


def format_line(meta: dict) -> str:
    return f"{meta.get('title')} - {meta.get('description')}"


def main():
    intro = "Adb Utility"
    print(f"{Color.BOLD}{'-' * 10}\n{intro}\n{'-' * 10}{Color.END}\n")

    # Loads cogs
    cog_names = [pl for pl in os.listdir(COGS_DIR)
                 if os.path.isfile(os.path.join(COGS_DIR, pl)) and pl.endswith(".py")]

    # Ordered "run" functions for each cog
    plugin_desc = []
    plugin_callbacks = []

    for c in cog_names:
        name = c.rstrip(".py")

        cog = importlib.import_module("cogs.{}".format(name))
        assert hasattr(cog, "run")
        assert hasattr(cog, "meta")

        cogs[name] = {"plugin": cog, "meta": cog.meta}

        plugin_desc.append(format_line(cog.meta))
        plugin_callbacks.append(cog.run)

    # Add a quit option
    plugin_desc.append("Quit")
    plugin_callbacks.append(quit)

    # Show the options
    opt = OptionWizard(Color.BOLD + "Choose your action:" + Color.END, plugin_desc, plugin_callbacks)
    resp = opt.run()

    running = True
    kwargs = {
        "SCRIPT_DIR": SCRIPT_DIR,
        "CURRENT_DIR": CURRENT_DIR
    }

    while running:
        # Run the right cog
        data = resp(**kwargs)

        if data == "back":
            resp = opt.run()
        else:
            return


main()
