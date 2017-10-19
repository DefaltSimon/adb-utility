# coding=utf-8
import re

from adb.utilities import shell_output, OptionWizard, Meta
from adb.colors import Color


##########
# Adb devices
##########

def get_raw_devices() -> list:
    # 1. FIND all devices
    resp = shell_output("adb devices -l").splitlines()
    # Remove "List of devices attached"
    assert resp.pop(0).startswith("List of devices attached")

    return resp


def get_devices() -> list:
    resp = get_raw_devices()
    if not resp:
        return []

    devices = []
    for l in resp:
        serial, product, model, device = p_devices.findall(l)[0]
        model = " ".join(model.split("_"))

        devices.append(f"{Color.BOLD}{Color.RED}[{serial}]{Color.END} {Color.DARKCYAN}{model}{Color.END}")

    return devices


class DeviceMeta(Meta):
    def __init__(self):
        super().__init__()
        self.ayy = 0

    @property
    def title(self):
        return "devices"

    @property
    def description(self):
        return f"Lists all devices [{Color.CYAN}{len(get_raw_devices())} connected{Color.END}]"


meta = DeviceMeta()

p_devices = re.compile("([A-Z0-9]+)\s+device\s?(?:product:(\w+))?\s?(?:model:(\w+))?\s?(?:device:(\w+))?")


def run(**kwargs):
    intro = "Adb Devices"
    print(f"{'-' * 11}\n{intro}\n{'-' * 11}")

    running = True

    while running:
        devices = get_devices()

        if not devices:
            print(f"{Color.RED}No devices connected!{Color.END}\n")
            return "back"

        # 2. DISPLAY devices
        print("Connected devices:\n")
        print("\n".join(devices))

        options = OptionWizard("", ["Refresh devices", "Back"])
        resp = options.run()

        if resp == 1:
            continue
        else:
            return "back"
