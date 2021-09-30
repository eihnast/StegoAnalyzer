import os.path

from sa_core import AnalyzerParams, SaMethodsHandler

from .forms.form_main import MainWindow
from sa_app.lib.gui_lib import get_tkimg_byarr
from sa_app.lib.logs import write_sa_logs, AppLog


class AppGui:
    def __init__(self):
        self.__main_window = MainWindow(self.__analyzer)

    def start(self):
        self.__main_window.start()

    def __get_data_for_analyzer(self):
        schema = self.__main_window.get_schema()

        img = self.__main_window.get_loaded_img()
        do_chisqr = schema.analyze_chi2.get()
        do_rs = schema.analyze_rs.get()
        do_kza = schema.analyze_kza.get()
        chisqr_visualize = schema.chi2_vis.get()
        kza_extract = schema.kza_extract.get()

        return AnalyzerParams(img, do_chisqr, do_rs, do_kza, chisqr_visualize, kza_extract)

    def __analyzer(self):
        params = self.__get_data_for_analyzer()
        schema = self.__main_window.get_schema()

        if params.img is not None:
            handler = SaMethodsHandler(img_path=params.img)
            handler.set_params(do_chisqr=params.do_chisqr, do_rs=params.do_rs, do_kza=params.do_kza,
                               chisqr_visualize=params.chisqr_visualize, kza_extract=params.kza_extract)
            try:
                results = handler.exec()
            except Exception as ex:
                AppLog().write_with_error(ex, "Ошибка при выполении операций стегоанализа")
                return

            if results.ChiSqrResult is not None:
                schema.results_chi2_res.set("{0:.2%}".format(results.ChiSqrResult.fullness))

                chisqr_imar = results.ChiSqrResult.visualized
                if chisqr_imar is not None:
                    prev = get_tkimg_byarr(chisqr_imar, width=schema.ip_img.winfo_width())
                    size = chisqr_imar.shape[1], chisqr_imar.shape[0]
                    self.__main_window.upd_preview(prev, size)

            if results.RsResult is not None:
                schema.results_rs_res.set("{0:.2%}".format(results.RsResult.volume))

            if results.KzaResult is not None:
                schema.results_kza_res.set("{0} бит".format(results.KzaResult.volume))

                if results.KzaResult.data is not None:
                    self.__main_window.replace_text(schema.anres_kza_ex_data, results.KzaResult.data)

            # Writing all methods logs
            logs = handler.get_all_logs()
            write_sa_logs(logs)

            duration = handler.get_duration()
            AppLog().write("Операции стегоанализа для {0} были завершены за {1:.3f} с"
                           .format(os.path.split(params.img)[1], duration), prefix=AppLog.Prefixes.Msg)
