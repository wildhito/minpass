import tkinter
from minpass.debug import debug


class Clipboard(object):
    """ Manage clipboard content
    """
    def __init__(self):
        self.__tk = tkinter.Tk()
        self.__tk.withdraw()

    def __del__(self):
        """ Clear clipboard while destroying Clipboard object
        """
        self.__tk.clipboard_clear()
        self.__tk.clipboard_append("")
        self.__tk.update()
        self.__tk.destroy()
        debug("Cleared clipboard")

    def copy(self, content):
        """ Copy a content to clipboard

        Args:
            content: string to copy
        """
        self.__tk.clipboard_clear()
        self.__tk.clipboard_append(content)
        debug("New clipboard content: %s" % self.__tk.clipboard_get())

