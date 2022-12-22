import numpy as np
from PIL import Image, ImageDraw, ImageOps
from imageio import imread, imsave
from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


class RectSceneObject(SceneObject):
    def __init__(self, size=(0, 0), **kwargs):
        self.rect = Rect(*size)
        super().__init__(**kwargs)
        self.top_anim = None
        self.bottom_anim = None
        self.left_anim = None
        self.right_anim = None
        self.width_anim = None
        self.height_anim = None
        self.x_anim = None
        self.y_anim = None

        for k, v in kwargs.items():
            if k in self.__dict__:
                if "color" in k:
                    self.__dict__[k] = SceneObject.color_to_tuple(v)
                elif "pos" in k:
                    self.set_pos(kwargs["pos"])
                else:
                    self.__dict__[k] = v

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    def scale_rect(self, rect):
        rect = self.rect.copy()
        if self.scale_anim is not None or abs(self.scale - 1.0) > 1e3:
            w, h = self.rect.width * self.scale, self.rect.height * self.scale
            rect.set_size_anchored(w, h)
        return rect

    def set_pos(self, pos, y=None):
        super().set_pos(pos, y)
        self.rect.move_to(self.pos.as_tuple())

    def set_size(self, size):
        self.rect.set_size(size)

    def update_frame(self, frame):
        self.update_frame_color(frame)
        self.update_frame_opacity(frame)
        if self.top_anim is not None:
            self.rect.top = self.top_anim[frame]
            self.rect.get_size()
        if self.bottom_anim is not None:
            self.rect.bottom = self.bottom_anim[frame]
            self.rect.get_size()
        if self.left_anim is not None:
            self.rect.left = self.left_anim[frame]
            self.rect.get_size()
        if self.right_anim is not None:
            self.rect.right = self.right_anim[frame]
            self.rect.get_size()
        if self.x_anim is not None:
            self.pos[0] = self.x_anim[frame]
            self.set_pos(self.pos)
        if self.y_anim is not None:
            self.pos[1] = self.y_anim[frame]
            self.set_pos(self.pos)
        if self.width_anim is not None:
            self.rect.set_size_anchored(self.width_anim[frame], self.rect.height)
        if self.height_anim is not None:
            self.rect.set_size_anchored(self.rect.width, self.height_anim[frame])
        self.update_frame_blur(frame)
        self.update_frame_scale(frame)
        self.update_frame_angle(frame)
        self.update_frame_shearx(frame)
        self.update_frame_sheary(frame)

    def get_rect_clip_pix(self, x0, y0, x1, y1, color=None):
        r = self.scale_rect(self.rect)
        if self.is_mask:
            rect = np.array([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)])
            img = Image.new("L", (self.pixsize[0], self.pixsize[1]), 0)
            draw = ImageDraw.Draw(img)
            draw.polygon([tuple(p) for p in rect], fill=255)
            pix = np.asarray(img).reshape(self.pixsize[1], self.pixsize[0], 1)
            return ImageClip(pix, transparent=True, ismask=True)
        else:
            color = color if color is not None else (0, 0, 0)
            ps = (self.pixsize[0], self.pixsize[1])
            pix = Image.new("RGBA", ps, (0, 0, 0, 0))
            rw, rh = int(r.width * self.pixsize[0]), int(r.height * self.pixsize[1])
            img = Image.new("RGBA", (rw, rh), (*color, 255))
            img, x0, y0 = self.transform_img(img, r)
            pix.paste(img, box=(x0, y0))
            pix = np.asarray(pix)
            self.mask = ImageClip(1.0 * pix[:, :, 3] / 255, ismask=True)
            return ImageClip(pix, transparent=True, ismask=False)

    def get_rect_clip(self, x0, y0, x1, y1, color=None):
        xp0 = int(x0 * self.pixsize[0])
        xp1 = int(x1 * self.pixsize[0])
        yp0 = int(y0 * self.pixsize[1])
        yp1 = int(y1 * self.pixsize[1])
        return self.get_rect_clip_pix(xp0, yp0, xp1, yp1, color)

    def get_clip_obj(self):
        r = self.rect.copy()
        if self.scale_anim is not None or abs(self.scale - 1.0) > 1e3:
            w, h = self.rect.width * self.scale, self.rect.height * self.scale
            r.set_size_anchored(w, h)
        self.clip_obj = self.get_rect_clip(
            r.left,
            r.top,
            r.right,
            r.bottom,
            self.color,
        )
        return self.clip_obj

    def get_clip_frame(self, frame, t0, t1):
        self.update_frame(frame)
        if not self.opacity > 0:
            return None
        clip = (
            self.get_clip_obj()
            .set_opacity(self.opacity)
            .set_start(t0)
            .set_end(t1)
            .set_layer(self.layer)
        )
        if self.blur_anim is not None:
            fl = lambda pic: fill_array(pic, self.color)
            clip = clip.fl_image(fl)
            bl = lambda pic: blur_image(pic, self.blur)
            clip.mask = clip.mask.fl_image(bl)
        return clip


class ImageSceneObject(RectSceneObject):
    def __init__(self, size=(0, 0), filename=None, **kwargs):
        self.rect = Rect(*size)
        super().__init__(size=size, **kwargs)
        self.filename = filename

    def get_clip_obj(self):
        r = self.scale_rect(self.rect)
        if self.filename is not None:
            ps = (self.pixsize[0], self.pixsize[1])
            pix = Image.new("RGBA", ps, (0, 0, 0, 0))
            img = imread(self.filename)
            scale = r.width * self.pixsize[0] / img.shape[0]
            img = Image.fromarray(img, mode="RGBA")
            img, x0, y0 = self.transform_img(img, r, scale=scale)
            pix.paste(img, box=(x0, y0))
            pix = np.asarray(pix)
            self.mask = ImageClip(1.0 * pix[:, :, 3] / 255, ismask=True)
            self.clip_obj = ImageClip(pix, transparent=True, ismask=False)
        return self.clip_obj

    def get_clip_frame(self, frame, t0, t1):
        self.update_frame(frame)
        if not self.opacity > 0:
            return None
        clip = (
            self.get_clip_obj()
            .set_opacity(self.opacity)
            .set_start(t0)
            .set_end(t1)
            .set_layer(self.layer)
        )
        if self.blur_anim is not None:
            bl = lambda pic: blur_image(pic, self.blur)
            clip = clip.fl_image(bl)
        return clip
