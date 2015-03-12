import asyncio
import code
import sys


class Repl(code.InteractiveConsole):
    def __init__(self, loop=None, *args, **kwargs):
        super(Repl, self).__init__(*args, **kwargs)
        if loop is None:
            loop = asyncio.get_event_loop()
        loop.add_reader(sys.stdin, self.on_stdin)

    def interact(self, banner=None):
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        cprt = 'Type "help", "copyright", "credits" or "license" for more information.'
        if banner is None:
            self.write("Python %s on %s\n%s\n(%s)\n" %
                       (sys.version, sys.platform, cprt,
                        self.__class__.__name__))
        elif banner:
            self.write("%s\n" % str(banner))

        self.prompt(False)

    def prompt(self, more):
        if more:
            prompt = sys.ps2
        else:
            prompt = sys.ps1
        print(prompt, end="", flush=True)

    def on_stdin(self):
        line = sys.stdin.readline()
        more = self.push(line)
        self.prompt(more)


if __name__ == "__main__":
    from . import main

    r = Repl()
    r.interact()

    main()
