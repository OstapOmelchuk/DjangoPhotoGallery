import os
import shutil
import cv2
import urllib.request
from colorthief import ColorThief


def download_img(url, dest, filename):
    if not (filename.lower().endswith(('.png', '.jpg', '.jpeg'))):
        filename += ".jpg"

    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')
        ]

        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, filename)
        src_path = os.path.abspath(os.curdir) + "/" + filename
        dst_path = dest + filename
        loc = shutil.move(src_path, dst_path)
        return loc
    except Exception as e:
        return {"result": "error", "message": f"Error downloading photo to local storage {filename}"}


def get_image_size(path_to_img):
    im = cv2.imread(path_to_img)
    return im.shape[0:2]


def get_image_color(path_to_img):
    color_thief = ColorThief(path_to_img)
    rgb = color_thief.get_color(quality=1)
    return ('{:X}{:X}{:X}').format(rgb[0], rgb[1], rgb[2])

