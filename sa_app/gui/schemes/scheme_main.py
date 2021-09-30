from tkinter import *

from sa_app.lib.logs import AppLog
from sa_app.lib.gui_lib import *

from .._gui_configs import *


class GuiSchemeMain:
    def __init__(self, window):
        self.__window = window

        self.__icon()
        self.__main_window()
        self.__main_background()
        self.__main_title()
        self.__menu()
        self.__frame_img_load()
        self.__frame_analysis()
        self.__analysis_button()
        self.__frame_results()
        self.__frame_preview()

    def __icon(self):
        try:
            self.__window.iconbitmap(ICON_PATH)
        except TclError:
            msg = "Не удалось загрузить файл иконки по пути: {0}".format(ICON_PATH)
            AppLog().write(msg, prefix=AppLog.Prefixes.GuiError)
        except Exception as ex:
            AppLog().write_error(ex, err_type=AppLog.Prefixes.GuiError)

    def __main_window(self):
        # Main program window
        main_width, main_height = MAIN_WINDOW_SIZES
        coord_w, coord_h = get_window_coords(self.__window, main_width, main_height)
        self.__window.geometry('{}x{}+{}+{}'.format(main_width, main_height, coord_w, coord_h))
        self.__window.resizable(False, False)
        self.__window.title(MAIN_WINDOW_TITLE)
        self.__window["bg"] = C['gray']

    def __main_background(self):
        # Main frame in border
        cx, cy = 15, 15
        self.mainframe = Frame(self.__window, bg=C['gray'],
                               highlightthickness=10, highlightbackground=C['black'], highlightcolor=C['black'])
        self.mainframe.place(x=cx, y=cy, width=MAIN_WINDOW_WIDTH - cx * 2, height=MAIN_WINDOW_HEIGHT - cy * 2 - 20)

    def __main_title(self):
        # Program title
        title_width, title_height = MAIN_TITLE_SIZES
        cx, cy = MAIN_WINDOW_WIDTH // 2 - title_width // 2, 2
        title_text = StringVar()
        title_text.set(MAIN_TITLE_TEXT)

        self.title_back = Label(self.__window, bg=C['gray'])
        self.title_back.place(x=cx, y=cy, width=title_width, height=title_height)

        self.title = Label(self.__window, textvariable=title_text, font=MAIN_TITLE_FONT, fg=C['gray'], bg=C['black'])
        self.title.place(x=cx + 2, y=cy + 2, width=title_width - 4, height=title_height - 4)

    def __menu(self):
        # Program menu
        self.menu = Menu(self.__window)
        self.__window.config(menu=self.menu)

    def __frame_img_load(self):
        # Choosing img frame
        imgch_width, imgch_height = IMG_CHOOSING_SIZES
        x, y = IMG_CHOOSING_COORDS

        self.imgch_frame = Frame(self.mainframe, bg=C['white_m'],
                                 highlightthickness=2, highlightbackground=C['black'])
        self.imgch_frame.place(x=x, y=y, width=imgch_width, height=imgch_height)

        # Choosing img title
        text = StringVar()
        text.set(IMG_CHOOSING_TITLE)
        self.imgch_title = Label(self.imgch_frame, textvariable=text, font=IMG_CHOOSING_FONT,
                                 bg=self.imgch_frame["bg"])
        self.imgch_title.place(x=0, y=0, width=imgch_width - 4, height=imgch_height // 2 - 4)

        # Img name entry
        self.img_name = StringVar()
        self.img_name.set("")
        self.imgch_name = Entry(self.imgch_frame, state="disabled", justify="center",
                                textvariable=self.img_name, font=IMG_CHOOSING_NAME_FONT)
        self.imgch_name.place(x=10, y=imgch_height // 3, width=imgch_width - 24, height=imgch_height // 5)

        # Choosing img button
        self.imgch_btn = Button(self.imgch_frame, text=IMG_CHOOSING_BTN_TEXT, font=IMG_CHOOSING_BTN_FONT,
                                bg=C['black'], fg=C['gray'], activebackground=C['gray'], activeforeground=C['black'])
        self.imgch_btn.place(x=10, y=imgch_height // 3 * 2 - 4, width=imgch_width - 24, height=imgch_height // 4)

    def __frame_analysis(self):
        # Analysis frame
        an_width, an_height = FRAME_ANALYSIS_SIZES
        x, y = FRAME_ANALYSIS_COORDS

        self.an_frame = Frame(self.mainframe, bg=C['white_m'],
                              highlightthickness=2, highlightbackground=C['black'])
        self.an_frame.place(x=x, y=y, width=an_width, height=an_height)

        # ChiSqr check
        self.analyze_chi2 = BooleanVar()
        self.an_chi2_check = Checkbutton(self.an_frame, text=ANALYSIS_CHOOSING_CHISQR_TEXT, onvalue=True,
                                         offvalue=False, variable=self.analyze_chi2, bg=self.an_frame["bg"])
        self.an_chi2_check.select()
        self.an_chi2_check.place(x=10, y=8, height=(an_height - 20) // 5)

        # RS check
        self.analyze_rs = BooleanVar()
        self.an_rs_check = Checkbutton(self.an_frame, text=ANALYSIS_CHOOSING_RS_TEXT, onvalue=True,
                                       offvalue=False, variable=self.analyze_rs, bg=self.an_frame["bg"])
        self.an_rs_check.select()
        self.an_rs_check.place(x=10, y=28, height=(an_height - 20) // 5)

        # Koch-Zao analysis check
        self.analyze_kza = BooleanVar()
        self.an_kza_check = Checkbutton(self.an_frame, text=ANALYSIS_CHOOSING_KZAA_TEXT, onvalue=True,
                                        offvalue=False, variable=self.analyze_kza, bg=self.an_frame["bg"])
        self.an_kza_check.select()
        self.an_kza_check.place(x=10, y=48, height=(an_height - 20) // 5)

        # Koch-Zhao analysis try extract
        self.kza_extract = BooleanVar()
        self.an_kza_ex = Checkbutton(self.an_frame, text=ANALYSIS_CHOOSING_KZA_EXTRACT_TEXT, onvalue=True,
                                     offvalue=False, variable=self.kza_extract, bg=self.an_frame["bg"])
        self.an_kza_ex.select()
        self.an_kza_ex.place(x=10, y=68, height=(an_height - 20) // 5)

        # ChiSqr visualize
        self.chi2_vis = BooleanVar()
        self.an_chi2_vis = Checkbutton(self.an_frame, text=ANALYSIS_CHOOSING_CHISQR_VISUALIZE_TEXT, onvalue=True,
                                       offvalue=False, variable=self.chi2_vis, bg=self.an_frame["bg"])
        self.an_chi2_vis.select()
        self.an_chi2_vis.place(x=10, y=88, height=(an_height - 20) // 5)

        # Load button
        self.__analysis_button()

    def __analysis_button(self):
        # Analyze button
        x, y = FRAME_ANALYSIS_COORDS
        y += FRAME_ANALYSIS_HEIGHT

        self.analyze_btn = Button(self.mainframe, text=ANALYSIS_BTN_TEXT, font=FRAME_ANALYSIS_BTN_FONT, bd=2,
                                  bg=C['black'], fg=C['gray'], activebackground=C['gray'], activeforeground=C['black'])
        self.analyze_btn.place(x=x, y=y, width=300, height=30)

    def __frame_results(self):
        # Analysis results frame
        anres_width, anres_height = FRAME_RESULTS_SIZES
        x, y = FRAME_RESULTS_COORDS

        self.anres_frame = Frame(self.mainframe, bg=C['white_m'],
                                 highlightthickness=2, highlightbackground=C['black'])
        self.anres_frame.place(x=x, y=y, width=anres_width, height=anres_height)

        # Analysis results title
        text = StringVar()
        text.set(RESULTS_TITLE_TEXT)
        self.anres_title = Label(self.anres_frame, textvariable=text,
                                 font=FRAME_RESULTS_TITLE_FONT, justify="center", bg=self.anres_frame["bg"])
        self.anres_title.place(x=0, y=5, width=anres_width - 4, height=20)

        # ChiSqr fullness
        self.results_chi2_res = StringVar()
        self.anres_chi2 = Label(self.anres_frame, text=FRAME_RESULTS_CHISQR_TITLE,
                                font=FRAME_RESULTS_MAIN_FONT, bg=self.anres_frame["bg"])
        self.anres_chi2.place(x=5, y=40, width=anres_width - 14, height=15)
        self.anres_chi2_res = Label(self.anres_frame, textvariable=self.results_chi2_res,
                                    font=FRAME_RESULTS_MAIN_FONT, bg=self.anres_frame["bg"])
        self.anres_chi2_res.place(x=5, y=55, width=anres_width - 14, height=15)

        # RS fullness
        self.results_rs_res = StringVar()
        self.anres_rs = Label(self.anres_frame, text=FRAME_RESULTS_RS_TITLE,
                              font=FRAME_RESULTS_MAIN_FONT, bg=self.anres_frame["bg"])
        self.anres_rs.place(x=5, y=75, width=anres_width - 14, height=15)
        self.anres_rs_res = Label(self.anres_frame, textvariable=self.results_rs_res,
                                  font=FRAME_RESULTS_MAIN_FONT, bg=self.anres_frame["bg"])
        self.anres_rs_res.place(x=5, y=90, width=anres_width - 14, height=15)

        # KZA fullness
        self.results_kza_res = StringVar()
        self.anres_kza = Label(self.anres_frame, text=FRAME_RESULTS_KZA_TITLE,
                               font=FRAME_RESULTS_MAIN_FONT, bg=self.anres_frame["bg"])
        self.anres_kza.place(x=5, y=110, width=anres_width - 14, height=15)
        self.anres_kza_res = Label(self.anres_frame, textvariable=self.results_kza_res,
                                   font=FRAME_RESULTS_MAIN_FONT, bg=self.anres_frame["bg"])
        self.anres_kza_res.place(x=5, y=125, width=anres_width - 14, height=15)

        # KZA extract
        self.anres_kza_ex = Label(self.anres_frame, text=FRAME_RESULTS_KZA_EXTRACT_TITLE,
                                  font=FRAME_RESULTS_MAIN_FONT, bg=self.anres_frame["bg"])
        self.anres_kza_ex.place(x=5, y=145, width=anres_width - 14, height=15)
        self.anres_kza_ex_data = Text(self.anres_frame, font=FRAME_RESULTS_EXTRACTED_FONT,
                                      bg=self.anres_frame["bg"], state="disabled", wrap=WORD)
        self.anres_kza_ex_data.place(x=5, y=165, width=anres_width - 14 - 14, height=120)

        # Scrollbar for extracted data
        scroll = Scrollbar(self.anres_frame, command=self.anres_kza_ex_data.yview)
        scroll.place(x=anres_width - 14 - 14 + 5, y=165, width=14, height=120)
        self.anres_kza_ex_data.config(yscrollcommand=scroll.set)

    def __frame_preview(self):
        # Img preview frame
        ip_width, ip_height = IMG_PREVIEW_SIZES
        x, y = IMG_PREVIEW_COORDS
        y_info = y - 28

        self.ip_frame = Frame(self.mainframe, bg=C['white_m'], highlightthickness=2, highlightbackground=C['black'])
        self.ip_frame.place(x=x, y=y, width=ip_width, height=ip_height)

        # Img preview info label
        self.ip_info_text = StringVar()
        self.ip_info = Label(self.mainframe, bg=C['white_m'], font=IMG_PREVIEW_INFO_FONT,
                             bd=2, relief="solid", textvariable=self.ip_info_text)
        self.ip_info.place(x=x, y=y_info, width=ip_width, height=30)

        # Img preview picture
        self.ip_img = Label(self.ip_frame, bg=C['white_m'])
        self.ip_img.place(x=0, y=0, width=ip_width - 4, height=ip_height - 4)

    def __waiting_frame(self):
        # Waiting frame
        wt_width, wt_height = WAITING_FRAME_SIZES
        x, y = WAITING_FRAME_COORDS
        self.wt_frame = Frame(self.__window, bg=C['white_m'], highlightthickness=5, highlightbackground=C['black'])
        self.wt_frame.place(x=x, y=y, width=wt_width, height=wt_height)

        # Waiting text
        wt_text = StringVar()
        wt_text.set(WAITING_TEXT)
        self.wt_title = Label(self.wt_frame, textvariable=wt_text, font=WAITING_FONT, fg=C['gray'], bg=C['black'])
        self.wt_title.place(x=5, y=5, width=wt_width - 20, height=wt_height - 20)

        # Waiting gif
        try:
            gif_width, gif_height = WAITING_GIF_SIZES
            gif_x, gif_y = WAITING_GIF_COORDS
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
