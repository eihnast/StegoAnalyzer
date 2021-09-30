import sa_core.sa_lib as salib

from sa_app._app_config import *


def bits_array_to_str(bits_array):
    return salib.bits_array_to_str(bits_array)


def write_bits_array(bits_array, path):
    return salib.write_bits_array(bits_array, path)


def str_to_bits_array(s):
    return salib.str_to_bits_array(s)


def read_bits_array(path):
    return salib.read_bits_array(path)


def write_extracted_data(ex_data, filename, write_time=True):
    return salib.write_extracted_data(ex_data, filename, ex_path=STEGO_EXTRACTED_PATH, write_time=write_time)
