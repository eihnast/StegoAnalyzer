from tkinter import *

from ..schemes.scheme_about import GuiSchemeAbout


class AboutWindow:
    def __init__(self, window):
        self.__window = window
        self.__about = Toplevel(self.__window)

        GuiSchemeAbout(self.__window, self.__about)

    def give_control(self):
        self.__about.grab_set()
        self.__about.focus_set()
        self.__about.wait_window()
