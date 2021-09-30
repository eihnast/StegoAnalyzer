from tkinter import *
from sa_core.stego_module import StegoMethod

from sa_app.lib.logs import AppLog
from sa_app.lib.gui_lib import *

from .._gui_configs import *


class GuiSchemeStego:
    def __init__(self, window, stego_window):
        self.__window = window
        self.__stego = stego_window
        self.__active_btn = None

        self.__icon()
        self.__stego_window()
        self.__main_background()
        self.__frame_img_load()
        self.__frame_settings()
        self.__frame_lsb()
        self.__frame_lsb_params()
        self.__frame_kz()
        self.__frame_kz_params()
        self.__decrypt_btn()

        self.__method_buttons = [self.lsb_btn, self.lsb_direct_btn, self.lsb_rnd_btn,
                                 self.kz_btn, self.kz_direct_btn, self.kz_rnd_btn]

    def __icon(self):
        try:
            self.__stego.iconbitmap(ICON_PATH)
        except TclError:
            msg = "Не удалось загрузить файл иконки по пути: {0}".format(ICON_PATH)
            AppLog().write(msg, prefix=AppLog.Prefixes.GuiError)
        except Exception as ex:
            AppLog().write_error(ex, err_type=AppLog.Prefixes.GuiError)

    def __stego_window(self):
        # Stego window
        stego_width, stego_height = STEGO_WINDOW_SIZES
        coord_w, coord_h = get_window_coords(self.__window, width=stego_width, height=stego_height)
        self.__stego.geometry('{}x{}+{}+{}'.format(stego_width, stego_height, coord_w, coord_h))
        self.__stego.resizable(False, False)
        self.__stego.title(STEGO_WINDOW_TITLE)
        self.__stego["bg"] = C['gray']

    def __main_background(self):
        # Main frame in border
        cx, cy = 5, 5
        self.mainframe = Frame(self.__stego, bg=C['gray'],
                               highlightthickness=5, highlightbackground=C['black'], highlightcolor=C['black'])
        self.mainframe.place(x=cx, y=cy, width=STEGO_WINDOW_WIDTH - cx * 2, height=STEGO_WINDOW_HEIGHT - cy * 2)

    def __frame_img_load(self):
        # Choosing img frame
        imgch_width, imgch_height = STEGO_IMG_CHOOSING_SIZES
        x, y = STEGO_IMG_CHOOSING_COORDS

        self.imgch_frame = Frame(self.mainframe, bg=C['white_m'],
                                 highlightthickness=2, highlightbackground=C['black'])
        self.imgch_frame.place(x=x, y=y, width=imgch_width, height=imgch_height)

        # Choosing img title
        text = StringVar()
        text.set(STEGO_IMG_CHOOSING_TITLE)
        self.imgch_title = Label(self.imgch_frame, textvariable=text, font=STEGO_IMG_CHOOSING_FONT,
                                 bg=self.imgch_frame["bg"])
        self.imgch_title.place(x=0, y=0, width=imgch_width - 4, height=imgch_height // 2 - 4)

        # Img name entry
        self.img_name = StringVar()
        self.img_name.set("")
        self.imgch_name = Entry(self.imgch_frame, state="disabled", justify="center",
                                textvariable=self.img_name, font=STEGO_IMG_CHOOSING_NAME_FONT)
        self.imgch_name.place(x=10, y=imgch_height // 2,
                              width=imgch_width // 2 - 13 - 2, height=imgch_height // 3)

        # Choosing img button
        self.imgch_btn = Button(self.imgch_frame, text=STEGO_IMG_CHOOSING_BTN_TEXT, font=STEGO_IMG_CHOOSING_BTN_FONT,
                                bg=C['black'], fg=C['gray'], activebackground=C['gray'], activeforeground=C['black'])
        self.imgch_btn.place(x=10 + imgch_width // 2 - 13 + 6, y=imgch_height // 2,
                             width=imgch_width // 2 - 13 - 2, height=imgch_height // 3)

    def __frame_settings(self):
        fset_width, fset_height = FRAME_DEC_SETTINGS_SIZES
        x, y = FRAME_DEC_SETTINGS_COORDS

        self.settings_frame = Frame(self.mainframe, bg=C['white_m'],
                                    highlightthickness=2, highlightbackground=C['black'])
        self.settings_frame.place(x=x, y=y, width=fset_width, height=fset_height)

    def __frame_lsb(self):
        flsb_width, flsb_height = FRAME_LSB_SIZES
        x, y = FRAME_LSB_COORDS

        self.lsb_frame = Frame(self.settings_frame, bg=C['white_m'],
                               highlightthickness=0, highlightbackground=C['black'])
        self.lsb_frame.place(x=x - 2, y=y, width=flsb_width, height=flsb_height - 4)

        # Buttons
        x, y = DEC_LSB_BTN_COORDS
        self.lsb_btn = Button(self.lsb_frame, text=DEC_LSB_BTN_TEXT, font=DEC_LSB_BTN_FONT, bd=2)
        self.lsb_btn.place(x=x, y=y, width=DEC_LSB_BTN_WIDTH, height=DEC_LSB_BTN_HEIGHT)

        x, y = DEC_LSB_DIRECT_BTN_COORDS
        self.lsb_direct_btn = Button(self.lsb_frame, text=DEC_LSB_DIRECT_BTN_TEXT, font=DEC_LSB_DIRECT_BTN_FONT, bd=2)
        self.lsb_direct_btn.place(x=x, y=y, width=DEC_LSB_DIRECT_BTN_WIDTH, height=DEC_LSB_DIRECT_BTN_HEIGHT)

        x, y = DEC_LSB_RND_BTN_COORDS
        self.lsb_rnd_btn = Button(self.lsb_frame, text=DEC_LSB_RND_BTN_TEXT, font=DEC_LSB_RND_BTN_FONT, bd=2)
        self.lsb_rnd_btn.place(x=x, y=y, width=DEC_LSB_RND_BTN_WIDTH, height=DEC_LSB_RND_BTN_HEIGHT)

    def __frame_lsb_params(self):
        x, y = DEC_LSB_RND_BTN_COORDS
        xleft = DEC_LSB_DIRECT_BTN_COORDS[0]

        lsbps_width, lsbps_height = STEGO_LSB_PARAMS_ENTRY_SIZES
        self.lsb_seed = StringVar()
        self.lsb_seed.set("")
        y += DEC_LSB_RND_BTN_HEIGHT + 10
        self.lsbp_seed_entry = Entry(self.lsb_frame, state="normal", justify="center",
                                     textvariable=self.lsb_seed, font=STEGO_LSB_PARAMS_ENTRY_FONT)
        self.lsbp_seed_entry.place(x=x, y=y, width=lsbps_width, height=lsbps_height)

        text_seed = StringVar()
        text_seed.set(STEGO_LSB_PARAMS_SEED_TEXT)
        label_width, label_height = STEGO_LSB_PARAMS_TEXTS_SIZES
        self.lsbp_seed_title = Label(self.lsb_frame, textvariable=text_seed, font=STEGO_LSB_PARAMS_TEXT_FONT,
                                     bg=self.lsb_frame["bg"], justify="right")
        self.lsbp_seed_title.place(x=xleft, y=y, width=label_width, height=label_height)

        lsbpsi_width, lsbpsi_height = STEGO_LSB_PARAMS_ENTRY_SIZES
        self.lsb_startind = StringVar()
        self.lsb_startind.set("")
        y += lsbps_height + 10
        self.lsbp_startind_entry = Entry(self.lsb_frame, state="normal", justify="center",
                                         textvariable=self.lsb_startind, font=STEGO_LSB_PARAMS_ENTRY_FONT)
        self.lsbp_startind_entry.place(x=x, y=y, width=lsbpsi_width, height=lsbpsi_height)

        text_startind = StringVar()
        text_startind.set(STEGO_LSB_PARAMS_STARTIND_TEXT)
        label_width, label_height = STEGO_LSB_PARAMS_TEXTS_SIZES
        self.lsbp_starind_title = Label(self.lsb_frame, textvariable=text_startind, font=STEGO_LSB_PARAMS_TEXT_FONT,
                                        bg=self.lsb_frame["bg"], justify="right")
        self.lsbp_starind_title.place(x=xleft, y=y, width=label_width, height=label_height)

        lsbpl_width, lsbpl_height = STEGO_LSB_PARAMS_ENTRY_SIZES
        self.lsb_length = StringVar()
        self.lsb_length.set("")
        y += lsbpsi_height + 10
        self.lsbp_length_entry = Entry(self.lsb_frame, state="normal", justify="center",
                                       textvariable=self.lsb_length, font=STEGO_LSB_PARAMS_ENTRY_FONT)
        self.lsbp_length_entry.place(x=x, y=y, width=lsbpl_width, height=lsbpl_height)

        text_length = StringVar()
        text_length.set(STEGO_LSB_PARAMS_LENGTH_TEXT)
        label_width, label_height = STEGO_LSB_PARAMS_TEXTS_SIZES
        self.lsbp_length_title = Label(self.lsb_frame, textvariable=text_length, font=STEGO_LSB_PARAMS_TEXT_FONT,
                                       bg=self.lsb_frame["bg"], justify="right")
        self.lsbp_length_title.place(x=xleft, y=y, width=label_width, height=label_height)

    def __frame_kz(self):
        fkz_width, fkz_height = FRAME_KZ_SIZES
        x, y = FRAME_KZ_COORDS

        self.kz_frame = Frame(self.settings_frame, bg=C['white_m'],
                              highlightthickness=0, highlightbackground=C['black'])
        self.kz_frame.place(x=x - 2, y=y, width=fkz_width, height=fkz_height - 4)

        # Buttons
        x, y = DEC_KZ_BTN_COORDS
        self.kz_btn = Button(self.kz_frame, text=DEC_KZ_BTN_TEXT, font=DEC_KZ_BTN_FONT, bd=2)
        self.kz_btn.place(x=x, y=y, width=DEC_KZ_BTN_WIDTH, height=DEC_KZ_BTN_HEIGHT)

        x, y = DEC_KZ_DIRECT_BTN_COORDS
        self.kz_direct_btn = Button(self.kz_frame, text=DEC_KZ_DIRECT_BTN_TEXT, font=DEC_KZ_DIRECT_BTN_FONT, bd=2)
        self.kz_direct_btn.place(x=x, y=y, width=DEC_KZ_DIRECT_BTN_WIDTH, height=DEC_KZ_DIRECT_BTN_HEIGHT)

        x, y = DEC_KZ_RND_BTN_COORDS
        self.kz_rnd_btn = Button(self.kz_frame, text=DEC_KZ_RND_BTN_TEXT, font=DEC_KZ_RND_BTN_FONT, bd=2)
        self.kz_rnd_btn.place(x=x, y=y, width=DEC_KZ_RND_BTN_WIDTH, height=DEC_KZ_RND_BTN_HEIGHT)

    def __frame_kz_params(self):
        x, y = DEC_KZ_RND_BTN_COORDS
        xleft = DEC_KZ_DIRECT_BTN_COORDS[0]

        kzps_width, kzps_height = STEGO_KZ_PARAMS_ENTRY_SIZES
        self.kz_seed = StringVar()
        self.kz_seed.set("")
        y += DEC_KZ_RND_BTN_HEIGHT + 10
        self.kzp_seed_entry = Entry(self.kz_frame, state="normal", justify="center",
                                    textvariable=self.kz_seed, font=STEGO_KZ_PARAMS_ENTRY_FONT)
        self.kzp_seed_entry.place(x=x, y=y, width=kzps_width, height=kzps_height)

        text_seed = StringVar()
        text_seed.set(STEGO_KZ_PARAMS_SEED_TEXT)
        label_width, label_height = STEGO_KZ_PARAMS_TEXTS_SIZES
        self.kzp_seed_title = Label(self.kz_frame, textvariable=text_seed, font=STEGO_KZ_PARAMS_TEXT_FONT,
                                    bg=self.kz_frame["bg"], justify="right")
        self.kzp_seed_title.place(x=xleft, y=y, width=label_width, height=label_height)

        kzpcrd_width, kzpcrd_height = STEGO_KZ_PARAMS_ENTRY_SIZES
        y += kzps_height + 10
        self.kz_coord_first = StringVar()
        self.kz_coord_first.set("")
        self.kzp_crdf_entry = Entry(self.kz_frame, state="normal", justify="center",
                                    textvariable=self.kz_coord_first, font=STEGO_KZ_PARAMS_ENTRY_FONT)
        self.kzp_crdf_entry.place(x=x, y=y, width=kzpcrd_width // 2 - 1, height=kzpcrd_height)

        self.kz_coord_second = StringVar()
        self.kz_coord_second.set("")
        self.kzp_crds_entry = Entry(self.kz_frame, state="normal", justify="center",
                                    textvariable=self.kz_coord_second, font=STEGO_KZ_PARAMS_ENTRY_FONT)
        self.kzp_crds_entry.place(x=x + kzpcrd_width // 2 + 2, y=y, width=kzpcrd_width // 2 - 1, height=kzpcrd_height)

        text_coords = StringVar()
        text_coords.set(STEGO_KZ_PARAMS_COORDS_TEXT)
        label_width, label_height = STEGO_KZ_PARAMS_TEXTS_SIZES
        self.kzp_coords_title = Label(self.kz_frame, textvariable=text_coords, font=STEGO_KZ_PARAMS_TEXT_FONT,
                                      bg=self.kz_frame["bg"], justify="right")
        self.kzp_coords_title.place(x=xleft, y=y, width=label_width, height=label_height)

        kzpthr_width, kzpthr_height = STEGO_KZ_PARAMS_ENTRY_SIZES
        self.kz_threshold = StringVar()
        self.kz_threshold.set("")
        y += kzpcrd_height + 10
        self.kzp_threshold_entry = Entry(self.kz_frame, state="normal", justify="center",
                                         textvariable=self.kz_threshold, font=STEGO_KZ_PARAMS_ENTRY_FONT)
        self.kzp_threshold_entry.place(x=x, y=y, width=kzpthr_width, height=kzpthr_height)

        text_threshold = StringVar()
        text_threshold.set(STEGO_KZ_PARAMS_THRESHOLD_TEXT)
        label_width, label_height = STEGO_KZ_PARAMS_TEXTS_SIZES
        self.kzp_threshold_title = Label(self.kz_frame, textvariable=text_threshold, font=STEGO_KZ_PARAMS_TEXT_FONT,
                                         bg=self.kz_frame["bg"], justify="right")
        self.kzp_threshold_title.place(x=xleft, y=y, width=label_width, height=label_height)

    def __decrypt_btn(self):
        btndec_width, btndec_height = BTN_DECRYPT_SIZES
        x, y = BTN_DECRYPT_COORDS

        self.dec_btn = Button(self.mainframe, text=BTN_DECRYPT_TEXT, font=BTN_DECRYPT_FONT, bd=2,
                              bg=C['black'], fg=C['gray'], activebackground=C['gray'], activeforeground=C['black'])
        self.dec_btn.place(x=x, y=y, width=btndec_width, height=btndec_height)

    def __btn_turn(self, button, activated=True):
        if activated:
            button.config(bg=C['black'], fg=C['gray'], activebackground=C['gray'], activeforeground=C['black'])
        else:
            button.config(bg=C['gray'], fg=C['black'], activebackground=C['black'], activeforeground=C['gray'])

    def set_buttons(self, active_btn):
        if active_btn == self.lsb_btn:
            self.set_buttons(self.lsb_direct_btn)
            return
        elif active_btn == self.kz_btn:
            self.set_buttons(self.kz_direct_btn)
            return

        for btn in self.__method_buttons:
            if btn != active_btn:
                self.__btn_turn(btn, False)

        self.__btn_turn(active_btn, True)
        self.__active_btn = active_btn
        self.__btn_conn_check()

    def __btn_conn_check(self):
        if self.__active_btn == self.lsb_direct_btn or self.__active_btn == self.lsb_rnd_btn:
            self.__btn_turn(self.lsb_btn, True)
        elif self.__active_btn == self.kz_direct_btn or self.__active_btn == self.kz_rnd_btn:
            self.__btn_turn(self.kz_btn, True)

    # Maybe Errors! Need to check
    def get_active_method(self):
        for i in range(len(self.__method_buttons)):
            if self.__method_buttons[i] == self.__active_btn:
                return StegoMethod(i)

    def __waiting_frame(self):
        # Waiting frame
        wt_width, wt_height = WAITING_MINI_FRAME_SIZES
        x, y = WAITING_MINI_FRAME_COORDS
        self.wt_frame = Frame(self.__stego, bg=C['white_m'], highlightthickness=5, highlightbackground=C['black'])
        self.wt_frame.place(x=x, y=y, width=wt_width, height=wt_height)

        # Waiting text
        wt_text = StringVar()
        wt_text.set(WAITING_MINI_TEXT)
        self.wt_title = Label(self.wt_frame, textvariable=wt_text, font=WAITING_MINI_FONT, fg=C['gray'], bg=C['black'])
        self.wt_title.place(x=5, y=5, width=wt_width - 20, height=wt_height - 20)

        # Waiting gif
        try:
            gif_width, gif_height = WAITING_MINI_GIF_SIZES
            gif_x, gif_y = WAITING_MINI_GIF_COORDS
            wt_icon = AnimatedGif(self.wt_frame, LOADING_GIF_PATH)
            wt_icon.place(x=gif_x, y=gif_y, width=gif_width, height=gif_height)
        except TclError:
            msg = "[GUI Error] Can`t load icon file by this path: {0}".format(LOADING_GIF_PATH)
            AppLog().write(msg, True)
        except Exception as ex:
            AppLog().write_error(ex, True, err_type="GUI Error")

    def enable_waiting(self):
        self.__waiting_frame()

    def disable_waiting(self):
        self.wt_frame.destroy()
