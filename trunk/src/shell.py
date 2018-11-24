#-*- coding: utf-8 -*-

import sys


from code import interact, InteractiveConsole
class MyInteractive(InteractiveConsole):
    def interact(self, banner=None, call=None):
        """Closely emulate the interactive Python console.
    
        The optional banner argument specify the banner to print
        before the first interaction; by default it prints a banner
        similar to the one printed by the real Python interpreter,
        followed by the current class name in parentheses (so as not
        to confuse this with the real interpreter -- since it's so
        close!).
    
        """
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        cprt = 'Type "help", "copyright", "credits" or "license" for more information.'
        if banner:
            self.write("%s\nPython %s on %s\n%s\n(%s)\n" %
                       (banner,sys.version, sys.platform, cprt,
                        self.__class__.__name__))
        else:
            self.write("%s\n" % str(banner))
        more = 0
        if call:
            call()
        while 1:
            try:
                if more:
                    prompt = sys.ps2
                else:
                    prompt = sys.ps1
                try:
                    line = self.raw_input(prompt)
                    # Can be None if sys.stdin was redefined
                    encoding = getattr(sys.stdin, "encoding", None)
                    if encoding and not isinstance(line, unicode):
                        line = line.decode(encoding)
                except EOFError:
                    self.write("\n")
                    break
                else:
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.resetbuffer()
                more = 0
                
banner = "Mole Command Shell"


if __name__ == '__main__':
        namespace = {}#self.make_shell_env(global_options)
        from code import interact, InteractiveConsole
        Interpreter = MyInteractive(namespace)
        def call():
            from billing_server import main
            main()
            
        Interpreter.interact(banner, call=call)