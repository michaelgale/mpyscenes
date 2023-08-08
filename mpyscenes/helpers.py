from PIL import Image, ImageDraw, ImageOps
import numpy as np
import scipy
from moviepy.editor import *
from toolbox import *


def listify(items):
    if not isinstance(items, list):
        return [items]
    return items


def size_preset_tuple(sizestr):
    size = None
    if sizestr is not None:
        if isinstance(sizestr, str):
            sizestr = sizestr.lower()
            if "1080p" in sizestr:
                size = (1920, 1080)
            elif "720p" in sizestr:
                size = (1280, 720)
            elif "480p" in sizestr:
                size = (720, 480)
            elif "4k" in sizestr:
                size = (3840, 2160)
            elif "xga" in sizestr:
                size = (1024, 768)
            elif "wxga" in sizestr:
                size = (1280, 720)
            elif "svga" in sizestr:
                size = (800, 600)
            elif "vga" in sizestr:
                size = (640, 480)
        if isinstance(sizestr, (list, tuple)):
            if len(sizestr) == 2:
                size = tuple(sizestr)
    return size


def fill_array(a, color):
    if isinstance(color, (list, tuple)):
        c = color
    else:
        c = colour_from_name(color)
    r = np.ones_like(a)
    r[:, :, 0] = r[:, :, 0] * c[0]
    r[:, :, 1] = r[:, :, 1] * c[1]
    r[:, :, 2] = r[:, :, 2] * c[2]
    return r


def blur_image(a, sigma):
    if len(a.shape) == 3:
        rx = scipy.ndimage.gaussian_filter(a[:, :, 0], sigma, mode="nearest")
        gx = scipy.ndimage.gaussian_filter(a[:, :, 1], sigma, mode="nearest")
        bx = scipy.ndimage.gaussian_filter(a[:, :, 2], sigma, mode="nearest")
        r = np.zeros_like(a)
        r[:, :, 0] = rx
        r[:, :, 1] = gx
        r[:, :, 2] = bx
    else:
        r = scipy.ndimage.gaussian_filter(a, sigma, mode="nearest")
    return r


def crop_clip(clip, size):
    xc, yc = clip.size[0] / 2, clip.size[1] / 2
    w, h = size[0], size[1]
    x1, x2 = int(xc - w / 2), int(xc + w / 2)
    y1, y2 = int(yc - h / 2), int(yc + h / 2)
    clip.img = clip.img[y1:y2, x1:x2]
    clip.size = size
    clip.mask.img = clip.mask.img[y1:y2, x1:x2]
    clip.mask.size = size
    return clip


def add_margin(img, margin):
    width, height = img.size
    new_width = width + 2 * margin
    new_height = height + 2 * margin
    result = Image.new(img.mode, (new_width, new_height))
    result.paste(img, (margin, margin))
    return result


def new_image_copy_into(img, like_img):
    """Copies img into a new image with the same size as like_img"""
    x = np.zeros_like(like_img)
    x[:, :, 0] = img[:, :, 0]
    x[:, :, 1] = img[:, :, 1]
    x[:, :, 2] = img[:, :, 2]
    m = (x[:, :, 0] + x[:, :, 1] + x[:, :, 2]) / 3
    x[:, :, 3] = np.minimum(1, m) * 255
    return Image.fromarray(x)


def color_name(v):
    if isinstance(v, (tuple, list)):
        return colour_name_from_tuple(v)
    elif isinstance(v, str):
        if v[0] == "#":
            return colour_name_from_hex(v)
    return v


def color_to_tuple(v):
    c = (0, 0, 0)
    if isinstance(v, str):
        if v[0] == "#":
            c = rgb_from_hex(v, as_uint8=True)
        else:
            c = colour_from_name(v)
    elif isinstance(v, (list, tuple)):
        c = tuple(v)
        if c[0] <= 1.0 and c[1] <= 1.0 and c[2] <= 1.0:
            c = (int(c[x] * 255) for x in range(3))
    return c
