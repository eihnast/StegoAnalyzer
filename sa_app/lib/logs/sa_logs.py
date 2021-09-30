from .log import Log
from sa_app._app_config import *


def write_sa_logs(logs):
    if logs is None:
        return

    if logs.keys().__contains__("chi_sqr"):
        _write_chi_sqr_log(logs["chi_sqr"])

    if logs.keys().__contains__("rs"):
        _write_rs_log(logs["rs"])

    if logs.keys().__contains__("kza"):
        _write_kza_log(logs["kza"])


def _write_chi_sqr_log(data):
    log = Log(LOG_M_CHI_SQR + LOGS_EXT)
    log.write(data)


def _write_rs_log(data):
    log = Log(LOG_M_RS + LOGS_EXT)
    log.write(data)


def _write_kza_log(data):
    log = Log(LOG_M_KZA + LOGS_EXT)
    log.write(data)
