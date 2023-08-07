"""
This module contains global functions that can be injected into Python's builtins.
"""

def SET_GLOBALS():
    """
    Inject custom functions into Python's builtins.
    This allows the functions to be used globally without needing to import them.
    """
    import builtins

    builtins.FLY = FlyDebugGlobals

class FlyDebugGlobals:

    @staticmethod
    def pdb():
        """
        A global function to quickly enter Python's debugger (pdb).
        Can be called anywhere in the code after SET_GLOBALS() has been run.

        :return: pdb
        """
        import pdb

        return pdb

    @staticmethod
    def printer(*args, title="DEBUG"):
        """
        A global print function that prints a debug header and footer around the arguments.
        Can be called anywhere in the code after SET_GLOBALS() has been run.

        :param args: The values to print.
        :param title: An optional title for the debug section.
        :param color: An optional color for the debug header and footer (default is cyan).
        """
        import colorama

        line = "-" * 60
        colored_line = colorama.Fore.CYAN + line
        colored_title = colorama.Fore.CYAN + colorama.Style.BRIGHT + title

        print("")
        print(colored_line)
        print(colored_title)
        print(colored_line)
        for i, arg in enumerate(args):
            print(colorama.Fore.WHITE + colorama.Style.NORMAL + arg)
            if i < len(args) - 1:
                print("")
        print(colored_line)
        print("")
        print(colorama.Fore.WHITE + colorama.Style.RESET_ALL)
        
