# coding=utf-8


def is_invalid_argument(text: str) -> bool:
    return "'" in text or '"' in text


class OptionBuilder:
    def __init__(self, title: str, options: list, printer_callback=None, **kwargs):
        self.title = title
        self.options = options

        self.option_nums = list(range(1, len(self.options)+1))

        self.printer = printer_callback
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

    # Blocking method
    def run(self) -> int:
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

        return resp


# a = OptionBuilder("ayy", ["memes", "more memes", "even more"])
# print(a.option_nums)
# a.run()
