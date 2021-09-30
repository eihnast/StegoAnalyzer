import time

from sa_app.lib.logs import AppLog


class Timer:
    def __init__(self):
        self.__start_time = None
        self.__time_count = None

    def start(self):
        if self.__start_time is not None:
            AppLog().write("[Error] Таймер уже запущен")

        self.__start_time = time.perf_counter()

    def stop(self):
        if self.__start_time is None:
            AppLog().write("[Error] Таймер не был запущен")

        elapsed_time = time.perf_counter() - self.__start_time
        self.__start_time = None

        self.__time_count = elapsed_time

    def get_time_count(self):
        return self.__time_count
