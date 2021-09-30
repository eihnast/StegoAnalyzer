from tkinter import *

from sa_app.lib.logs import AppLog
from sa_app.lib.gui_lib import *

from .._gui_configs import *


class GuiSchemeAbout:
    def __init__(self, window, about_window):
        self.__window = window
        self.__about = about_window

        self.__icon()
        self.__about_window()
        self.__about_maintext()

    def __icon(self):
        try:
            self.__about.iconbitmap(ICON_PATH)
        except TclError:
            msg = "Не удалось загрузить файл иконки по пути: {0}".format(ICON_PATH)
            AppLog().write(msg, prefix=AppLog.Prefixes.GuiError)
        except Exception as ex:
            AppLog().write_error(ex, err_type=AppLog.Prefixes.GuiError)

    def __about_window(self):
        # About window
        about_width, about_height = ABOUT_WINDOW_SIZES
        coord_w, coord_h = get_window_coords(self.__window, width=about_width, height=about_height)
        self.__about.geometry('{}x{}+{}+{}'.format(about_width, about_height, coord_w, coord_h))
        self.__about.resizable(False, False)
        self.__about.title(ABOUT_WINDOW_TITLE)
        self.__about["bg"] = C['gray']

    def __about_maintext(self):
        self.text_frame = Text(self.__about, bd=0, cursor="arrow", exportselection=0, padx=0, pady=0, relief="flat",
                               bg=C['gray'], font=ABOUT_MAINTEXT_FONT, wrap=WORD)
        self.text_frame.tag_configure("center", justify='center')
        self.text_frame.place(x=15, y=15,
                              width=self.__about.winfo_width() - 30, height=self.__about.winfo_height() - 30)
        self.text_frame.insert(1.0, ABOUT_TEXT)
        self.text_frame.tag_add("center", "1.0", "end")
        self.text_frame.config(state="disabled")
