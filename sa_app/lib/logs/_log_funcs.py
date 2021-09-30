import os.path

from sa_app._app_config import LOGS_PATH


def open_log_file(name="log_file"):
    try:
        if not os.path.isdir(LOGS_PATH):
            os.mkdir(LOGS_PATH)

        log = open(LOGS_PATH + "/" + name, 'a', encoding="utf-8")
    except Exception as ex:
        print("[Log Error] Can`t start log file " + name)
        print("[Log Error] Error is {0}".format(type(ex).__name__))
        log = None

    return log


def writelog(logfile=None, data=""):
    if logfile is not None:
        try:
            logfile.write(data + "\n")
            logfile.flush()
        except Exception as ex:
            template = "[Error] |{0}| {1!r}"
            msg = template.format(type(ex).__name__, ex.args)
            print(msg)


def clear_all_logs():
    if not os.path.isdir(LOGS_PATH):
        return

    for file in os.listdir(LOGS_PATH):
        open(os.path.join(LOGS_PATH, file), 'w')
