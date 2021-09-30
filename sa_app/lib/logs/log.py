from ._log_funcs import open_log_file, writelog


class Log:
    def __init__(self, logname):
        self.__logname = logname
        self.__logfile = open_log_file(self.__logname)

    def write(self, data, console_out=False):
        writelog(self.__logfile, data)

        if console_out:
            print(data)

    def write_error(self, ex, console_out=False, err_type="Error"):
        template = "[{0}] {1}\n[{0}] {2!r}"
        msg = template.format(err_type, type(ex).__name__, ex.args)
        self.write(msg, console_out)
