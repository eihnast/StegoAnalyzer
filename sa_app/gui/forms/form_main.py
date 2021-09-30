from tkinter import *
from tkinter import filedialog
from threading import Thread

from sa_core.image_handler import *

from ..schemes.scheme_main import GuiSchemeMain
from .._gui_configs import *
from .form_about import AboutWindow
from .form_extractor import StegoWindow
from sa_app.lib.gui_lib import get_tkimg_bypath
from sa_app._app_config import *


class MainWindow:
    def __init__(self, analyzer_method=None):
        self.__about = None
        self.__analyzer_method = None
        self.__loaded_img = None
        self.__preview_img = None

        self.__window = Tk()

        self.__schema = GuiSchemeMain(self.__window)
        self.__configure_actions()

        if analyzer_method is not None:
            self.__analyzer_method = analyzer_method

    def __configure_actions(self):
        self.__schema.menu.add_command(label=MENU_BTN_ABOUT_TEXT, command=self.__start_about)
        self.__schema.menu.add_command(label=MENU_BTN_STEGO_TEXT, command=self.__start_stego)

        self.__schema.imgch_btn.config(command=self.__load_img)
        self.__schema.an_chi2_check.config(command=self.__checks_handler_chi2)
        self.__schema.an_kza_check.config(command=self.__cheks_handler_kza)
        self.__schema.analyze_btn.config(command=self.__analyze_img)

    def start(self):
        self.__window.mainloop()

    def get_schema(self):
        return self.__schema

    def get_loaded_img(self):
        return self.__loaded_img

    def __start_about(self):
        AboutWindow(self.__window).give_control()

    def __start_stego(self):
        StegoWindow(self.__window).give_control()

    def __checks_handler_chi2(self):
        if not self.__schema.analyze_chi2.get():
            self.__schema.chi2_vis.set(False)
            self.__schema.an_chi2_vis.config(state="disabled")
        else:
            self.__schema.an_chi2_vis.config(state="normal")

    def __cheks_handler_kza(self):
        if not self.__schema.analyze_kza.get():
            self.__schema.kza_extract.set(False)
            self.__schema.an_kza_ex.config(state="disabled")
        else:
            self.__schema.an_kza_ex.config(state="normal")

    def upd_preview(self, img, size=None):
        self.__preview_img = img
        self.__schema.ip_img.config(image=self.__preview_img)
        if size is None:
            size = img.width(), img.height()
        self.__schema.ip_info_text.set("Ширина: {0}. Высота: {1}.".format(size[0], size[1]))

    def __load_img(self):
        img = filedialog.askopenfilename(filetypes=FILETYPES)
        if img is not None and len(img) > 0:
            self.__loaded_img = img
            self.__schema.img_name.set(img[img.rfind("/") + 1:])

            prev = get_tkimg_bypath(img, width=self.__schema.ip_img.winfo_width())
            self.upd_preview(prev, ImageHandler().load(img).get_size())

    def __clear_results_area(self):
        self.__schema.results_chi2_res.set("")
        self.__schema.results_kza_res.set("")
        self.__schema.results_rs_res.set("")
        self.replace_text(self.__schema.anres_kza_ex_data, "")

    def replace_text(self, text_widget, new_text):
        text_widget.config(state="normal")
        if len(text_widget.get(1.0)) > 0:
            text_widget.delete(1.0, END)
        text_widget.insert(1.0, new_text)
        text_widget.config(state="disabled")

    def __analyze_img(self):
        if self.__loaded_img is not None:
            self.__clear_results_area()
            self.__waiting(True)
            self.__window.update()

            analyze_thread = Thread(target=self.__analyzer_method)
            analyze_thread.start()
            while analyze_thread.is_alive():
                self.__window.update()

            self.__waiting(False)

    def __active_controls(self):
        s = self.__schema
        r = [s.imgch_btn, s.analyze_btn, s.an_chi2_check, s.an_rs_check, s.an_kza_check, s.an_chi2_vis, s.an_kza_ex]
        return r

    def __switch_controls(self, enabled):
        controls = self.__active_controls()
        for control in controls:
            control.config(state="normal" if enabled else "disabled")

    def __waiting(self, enabled):
        if enabled:
            self.__switch_controls(False)
            self.__schema.enable_waiting()
        else:
            self.__switch_controls(True)
            self.__schema.disable_waiting()
