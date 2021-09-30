import os.path
from tkinter import *
from tkinter import filedialog
from threading import Thread

from sa_core.stego_module import StegoMethod, ExtractorHandler

from ..schemes.scheme_extractor import GuiSchemeStego
from .._gui_configs import *
from sa_app.lib import write_extracted_data
from sa_app._app_config import *


class StegoWindow:
    def __init__(self, window):
        self.__window = window
        self.__stego = Toplevel(self.__window)
        self.__loaded_img = None
        self.__dec_method = None

        self.__schema = GuiSchemeStego(self.__window, self.__stego)
        self.__switch_method_btn(self.__schema.lsb_direct_btn)

        self.__configure_actions()

    def __configure_actions(self):
        self.__schema.imgch_btn.config(command=self.__load_img)
        self.__schema.dec_btn.config(command=self.__decrypt)

        self.__schema.lsb_btn.config(command=lambda: self.__switch_method_btn(self.__schema.lsb_btn))
        self.__schema.lsb_direct_btn.config(command=lambda: self.__switch_method_btn(self.__schema.lsb_direct_btn))
        self.__schema.lsb_rnd_btn.config(command=lambda: self.__switch_method_btn(self.__schema.lsb_rnd_btn))
        self.__schema.kz_btn.config(command=lambda: self.__switch_method_btn(self.__schema.kz_btn))
        self.__schema.kz_direct_btn.config(command=lambda: self.__switch_method_btn(self.__schema.kz_direct_btn))
        self.__schema.kz_rnd_btn.config(command=lambda: self.__switch_method_btn(self.__schema.kz_rnd_btn))

    def give_control(self):
        self.__stego.grab_set()
        self.__stego.focus_set()
        self.__stego.wait_window()

    def __load_img(self):
        img = filedialog.askopenfilename(filetypes=FILETYPES)
        if img is not None and len(img) > 0:
            self.__loaded_img = img
            self.__schema.img_name.set(img[img.rfind("/") + 1:])

    def __parse_lsb_params(self):
        raw_seed = self.__schema.lsb_seed.get()
        raw_startind = self.__schema.lsb_startind.get()
        raw_length = self.__schema.lsb_length.get()
        seed = startind = length = None

        try:
            raw_seed = int(raw_seed)
        except ValueError:
            pass

        try:
            raw_startind = int(raw_startind)
        except ValueError:
            pass

        try:
            raw_length = int(raw_length)
        except ValueError:
            pass

        if isinstance(raw_seed, int) and raw_seed > 0:
            seed = raw_seed
        if isinstance(raw_startind, int) and raw_startind >= 0:
            startind = raw_startind
        if isinstance(raw_length, int) and raw_length > 0:
            length = raw_length

        return seed, startind, length

    def __parse_kz_params(self):
        raw_seed = self.__schema.kz_seed.get()
        raw_threshold = self.__schema.kz_threshold.get()
        raw_coord_first = self.__schema.kz_coord_first.get()
        raw_coord_second = self.__schema.kz_coord_second.get()
        seed = threshold = coords = None

        try:
            raw_seed = int(raw_seed)
        except ValueError:
            pass

        try:
            raw_threshold = int(raw_threshold)
        except ValueError:
            pass

        try:
            raw_coord_first = int(raw_coord_first)
        except ValueError:
            pass

        try:
            raw_coord_second = int(raw_coord_second)
        except ValueError:
            pass

        if isinstance(raw_seed, int) and raw_seed > 0:
            seed = raw_seed
        if isinstance(raw_threshold, int) and raw_threshold >= 0:
            threshold = raw_threshold
        if isinstance(raw_coord_first, int) and raw_coord_first >= 0:
            coords = (raw_coord_first, )
            if isinstance(raw_coord_second, int) and raw_coord_second > 0:
                coords = (raw_coord_first, raw_coord_second)

        return seed, threshold, coords

    def __decrypt_func(self):
        params = None
        if self.__dec_method == StegoMethod.LSB_LINEAR or self.__dec_method == StegoMethod.LSB_RANDOM:
            params = self.__parse_lsb_params()
        elif self.__dec_method == StegoMethod.KZ_LINEAR or self.__dec_method == StegoMethod.KZ_RANDOM:
            params = self.__parse_kz_params()

        extractor = ExtractorHandler(self.__dec_method, self.__loaded_img, params)
        ex = extractor.exec()

        write_extracted_data(ex, os.path.split(self.__loaded_img)[1])

    def __decrypt(self):
        if self.__loaded_img is None or self.__loaded_img == "":
            return

        self.__waiting(True)
        self.__stego.update()

        dec_thread = Thread(target=self.__decrypt_func)
        dec_thread.start()
        while dec_thread.is_alive():
            self.__stego.update()

        self.__waiting(False)

    def __switch_method_btn(self, btn):
        self.__schema.set_buttons(btn)
        self.__dec_method = self.__schema.get_active_method()
        self.__change_params_availability()

    def __get_dec_params_entries(self):
        schema = self.__schema
        lsbarams = [schema.lsbp_seed_entry, schema.lsbp_length_entry, schema.lsbp_startind_entry]
        kzparams = [schema.kzp_seed_entry, schema.kzp_crdf_entry,
                    schema.kzp_crds_entry, schema.kzp_threshold_entry]
        return lsbarams, kzparams

    def __change_params_availability(self):
        if self.__dec_method == StegoMethod.LSB_LINEAR or self.__dec_method == StegoMethod.LSB_RANDOM:
            lsbcheck = True
        elif self.__dec_method == StegoMethod.KZ_LINEAR or self.__dec_method == StegoMethod.KZ_RANDOM:
            lsbcheck = False
        else:
            return

        lsbarams, kzparams = self.__get_dec_params_entries()
        for param in lsbarams:
            param.config(state="normal" if lsbcheck else "disabled")
        for param in kzparams:
            param.config(state="disabled" if lsbcheck else "normal")

    def __active_controls(self):
        s = self.__schema
        r = [s.imgch_btn, s.kz_btn, s.lsb_btn, s.lsb_rnd_btn,
             s.lsb_direct_btn, s.kz_rnd_btn, s.kz_direct_btn, s.dec_btn,
             s.lsbp_seed_entry, s.lsbp_startind_entry, s.lsbp_length_entry,
             s.kzp_seed_entry, s.kzp_crdf_entry, s.kzp_crdf_entry, s.kzp_threshold_entry]
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
