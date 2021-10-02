import numpy as _np
from PIL import Image as _Image, ImageTk as _ImageTk

from sa_app.lib.logs import AppLog as _AppLog


def get_tkimg_bypath(img_path, widget_sizes=None):
    try:
        img = _Image.open(img_path)
        if widget_sizes is not None:
            img = img.resize(fit_img_size((img.width, img.height), widget_sizes))
        result = _ImageTk.PhotoImage(img)
    except Exception as ex:
        _AppLog().write_with_error(ex, prefix="GUI Error",
                                   data="Возникла ошибка при загрузке превью изображения по пути {0}".format(img_path))
        return None

    return result


def get_tkimg_byarr(img_array, widget_sizes=None):
    try:
        img = _Image.fromarray(img_array.astype(_np.uint8))
        if widget_sizes is not None:
            img = img.resize(fit_img_size((img.width, img.height), widget_sizes))
        result = _ImageTk.PhotoImage(img)
    except Exception as ex:
        _AppLog().write_with_error(ex, prefix="GUI Error",
                                   data="Возникла ошибка при загрузке превью изображения из массива пикселей")
        return None

    return result


def fit_img_size(sizes, new_sizes=None):
    if new_sizes is not None:
        w, h = sizes
        w_new, h_new = new_sizes
        if w >= h:
            h_new = h * (w_new / w)
        else:
            w_new = w * (h_new / h)
        return int(w_new), int(h_new)
    return sizes


def get_window_coords(window, width=None, height=None):  # get_window_coords
    if window is not None:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        if width is None:
            width = window.winfo_width()
        if height is None:
            height = window.winfo_height()
        coords = screen_width // 2 - width // 2, screen_height // 2 - height // 2
        return coords
    return None
