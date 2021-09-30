from .log import Log


class AppLog:
    __instance = None

    __logname = "_app_log.txt"

    class Prefixes:
        Error = "Error"
        Msg = "Message"
        GuiError = "GUI Error"

    def __init__(self):
        self.__log = Log(self.__logname)

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super(AppLog, cls).__new__(cls)
        return cls.__instance

    def write(self, data, prefix=None, console_out=False):
        if prefix is not None:
            prefix = "[{0}] ".format(prefix)
        else:
            prefix = ""
        self.__log.write(prefix + data, console_out)

    def write_error(self, ex, console_out=False, err_type=Prefixes.Error):
        self.__log.write_error(ex, console_out, err_type)

    def write_with_error(self, ex, data, console_out=False, prefix=Prefixes.Error):
        self.write(data, prefix=prefix, console_out=console_out)
        self.write_error(ex, err_type=prefix, console_out=console_out)
