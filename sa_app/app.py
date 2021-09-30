from argparse import ArgumentParser
from sys import argv, exc_info

from sa_core import AnalyzerParams, SaMethodsHandler

from sa_app.lib.logs import AppLog, clear_all_logs
from sa_app.gui import AppGui


class App:
    def __create_parser(self):
        parser = ArgumentParser()
        parser.add_argument('-g', '--gui', dest="gui", action='store_true',
                            help="start app in GUI mode and ignore another parameters")
        parser.add_argument('-m', '--method', dest="method",
                            help="choose method for analyze: chi2, rs, kza or all (-m all do the same as -am)")
        parser.add_argument('-am', '--allmethods', dest="allmethods", action="store_true",
                            help="use all available methods for analyze and ignore -m")
        parser.add_argument('-e', '--extract', dest="extract", action="store_true",
                            help="try to extract hidden data by analyze Koch-Zao method")
        parser.add_argument('-i', '--image', dest='image',
                            help="name or path to image file that will be analyzed")
        parser.add_argument('-sh', '--short', dest='short', action="store_true",
                            help="short output")
        return parser

    def __handler(self):
        arg_parser = self.__create_parser()
        args = arg_parser.parse_args(argv[1:])

        if args.gui or len(argv) <= 1:
            self.__start_gui()
            return

        if not args.image:
            print("You need to specify image name for analyze with \"-i img_name\"")
            return

        params = AnalyzerParams(args.image, args.method == 'chi2', args.method == 'rs', args.method == 'kza',
                                False, args.extract)

        m_handler = SaMethodsHandler(img=params.img)
        m_handler.set_params(do_chisqr=params.do_chisqr, do_rs=params.do_rs, do_kza=params.do_kza,
                             chisqr_visualize=params.chisqr_visualize, kza_extract=params.kza_extract)
        results = m_handler.exec()

        imgname = args.image
        pos = max(0, imgname.rfind("\\"), imgname.rfind("/"))
        imgname = imgname[pos + 1:]

        out = "{0}: ".format(imgname)
        if results.ChiSqrResult is not None:
            if args.short:
                out += "{0:.2%} ".format(results.ChiSqrResult.fullness)
            else:
                out += "By chi2: {0:.2%}. ".format(results.ChiSqrResult.fullness)
        if results.RsResult is not None:
            if args.short:
                out += "{0:.2%} ".format(results.RsResult.volume)
            else:
                out += "By RS: {0:.2%}. ".format(results.RsResult.volume)
        if results.KzaResult is not None:
            if args.short:
                out += "{0} bit ".format(results.KzaResult.volume)
            else:
                out += "By Koch-Zao analyze: {0} bit.".format(results.KzaResult.volume)

            ex_data = results.KzaResult.data
            if args.extract and ex_data is not None and len(ex_data) > 0 and not args.short:
                data = ""
                for line in ex_data:
                    data += line + '\n'
                out += " Extracted data:\n{0}".format(data[:-1])

        print(out)
        return

    def start(self, onlygui=False):
        clear_all_logs()
        AppLog().write("Выполнен запуск приложения", prefix=AppLog.Prefixes.Msg)

        if not onlygui:
            self.__handler()
        else:
            self.__start_gui()

    def __start_gui(self):
        AppLog().write("Выполняется запуск графического интерфейса", prefix=AppLog.Prefixes.Msg)

        try:
            app_gui = AppGui()
            app_gui.start()
        except Exception as ex:
            AppLog().write_with_error(ex, prefix=AppLog.Prefixes.GuiError,
                                      data="Возникла критическая ошибка интерфейса, будет осуществлён перезапуск GUI")
            self.__start_gui()
