import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


class RectSceneObject(SceneObject):
    def __init__(self, size=(0, 0), **kwargs):
        self.rect = Rect(*size)
        super().__init__(**kwargs)
        self.color = (255, 255, 255)
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

    def set_pos(self, pos, y=None):
        super().set_pos(pos, y)
        self.rect.move_to(self.pos.as_tuple())

    def set_size(self, size):
        self.rect.set_size(size)

    def update_frame(self, frame):
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

    def get_rect_clip_pix(self, x0, y0, x1, y1, color=None):
        if self.is_mask:
            rect = np.array([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)])
            img = Image.new("L", (self.pixsize[0], self.pixsize[1]), 0)
            draw = ImageDraw.Draw(img)
            draw.polygon([tuple(p) for p in rect], fill=255)
            pix = np.asarray(img).reshape(self.pixsize[1], self.pixsize[0], 1)
            return ImageClip(pix, transparent=True, ismask=True)
        else:
            color = color if color is not None else (0, 0, 0)
            rect = np.array([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)])
            img = Image.new("RGBA", (self.pixsize[0], self.pixsize[1]), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.polygon([tuple(p) for p in rect], fill=color)
            pix = np.asarray(img)
            return ImageClip(pix, transparent=True, ismask=False)

    def get_rect_clip(self, x0, y0, x1, y1, color=None):
        xp0 = int(x0 * self.pixsize[0])
        xp1 = int(x1 * self.pixsize[0])
        yp0 = int(y0 * self.pixsize[1])
        yp1 = int(y1 * self.pixsize[1])
        return self.get_rect_clip_pix(xp0, yp0, xp1, yp1, color)

    def get_clip_obj(self):
        self.clip_obj = self.get_rect_clip(
            self.rect.left,
            self.rect.top,
            self.rect.right,
            self.rect.bottom,
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
        return clip
