# coding=utf-8
import re
from adb.utilities import shell, OptionWizard
from adb.colors import Color


##########
# Adb devices
##########

meta = {
    "title": "Devices",
    "description": "List all devices"
}

p_devices = re.compile("([A-Z0-9]+)\s+device\s?(?:product:(\w+))?\s?(?:model:(\w+))?\s?(?:device:(\w+))?")


def run(**kwargs):
    intro = "Adb Devices"
    print(f"{'-' * 11}\n{intro}\n{'-' * 11}")

    running = True

    while running:
        # 1. FIND all devices
        resp = shell("adb devices -l").splitlines()
        # Remove "List of devices attached"
        assert resp.pop(0).startswith("List of devices attached")

        devices = []
        for l in resp:
            serial, product, model, device = p_devices.findall(l)[0]
            model = " ".join(model.split("_"))

            devices.append(f"{Color.BOLD}{Color.RED}[{serial}]{Color.END} {Color.DARKCYAN}{model}{Color.END}")

        # 2. DISPLAY devices
        print("Connected devices:\n")
        print("\n".join(devices))

        options = OptionWizard("", ["Refresh devices", "Back"])
        resp = options.run()

        if resp == 1:
            continue
        else:
            return "back"
