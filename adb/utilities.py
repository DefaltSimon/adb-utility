# coding=utf-8
from subprocess import getoutput
from typing import Union
from json import loads


def is_invalid_argument(text: str) -> bool:
    return "'" in text or '"' in text


def quote(text: str) -> str:
    if " " in text:
        return f'"{text}"'
    else:
        return text


def shell(command: str) -> str:
    return getoutput(command)


def get_json(file: str) -> dict:
    with open(file) as j:
        return loads(j.read())


class OptionWizard:
    def __init__(self, title: str, options: list, custom_returns: list = None, **kwargs):
        self.title = title

        self.options = options
        self.custom_returns = custom_returns or list(range(1, len(options)+1))

        self.option_nums = list(range(1, len(self.options)+1))

        self.printer = kwargs.get("printer")
        self.input_text = kwargs.get("input_text", "> ")

    def generate_options(self) -> str:
        options = []
        for c, o in enumerate(self.options):
            options.append("[{}] {}".format(c+1, o))

        return "\n".join(options)

    def _print(self, text):
        if self.printer:
            self.printer(text)
        else:
            print(text)

    def __str__(self):
        return "{}\n{}".format(self.title, self.generate_options())

    def __repr__(self):
        return "<{} {},{}>".format(self.__class__.__name__, self.title, self.options)

    # Blocking method
    def run(self) -> str:
        self._print(self.__str__())

        valid = False
        resp = None

        while not valid:
            # Wait for input
            resp = input(self.input_text)

            if not resp.isdigit():
                self._print("Please specify a number")
                continue
            else:
                resp = int(resp)

            if resp not in self.option_nums:
                self._print("No such option")
                continue

            # Everything is okay
            valid = True

        return self.custom_returns[resp-1]


class ItemList:
    def __init__(self, items: list, **kwargs):
        self.items = items
        self.printer = kwargs.get("printer")

    def _print(self, text):
        if self.printer:
            self.printer(text)
        else:
            print(text)

    def print_items(self):
        opt = ["- {}".format(o) for o in self.items]

        self._print("\n".join(opt))
