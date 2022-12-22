import numpy as np
from PIL import Image, ImageDraw, ImageOps
from imageio import imread, imsave

from moviepy.editor import *

from toolbox import *
from mpyscenes import *
from ..helpers import *


class TextSceneObject(SceneObject):
    def __init__(self, text="", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font = "DIN-Bold"
        self.fontsize = 64
        self.kerning = 0
        self.stroke_width = 0
        self.stroke_color = None
        self.text_width = 0
        self.text_height = 0
        self.horz_align = "center"
        self.vert_align = "center"
        for k, v in kwargs.items():
            if k in self.__dict__:
                if "color" in k:
                    if isinstance(v, str):
                        if "#" in v:
                            self.__dict__[k] = rgb_from_hex(v, as_uint8=True)
                        else:
                            self.__dict__[k] = colour_from_name(v)
                    else:
                        self.__dict__[k] = v
                elif "pos" in k:
                    self.set_pos(kwargs["pos"])
                else:
                    self.__dict__[k] = v

    @property
    def width(self):
        return self.text_width

    @property
    def height(self):
        return self.text_height

    def new_clip_obj(self):
        def _get_text_clip(size=None):
            r = TextClip(
                self.text,
                color=self.color_name(self.color),
                size=size,
                font=self.font,
                fontsize=self.fontsize,
                kerning=self.kerning,
                stroke_width=self.stroke_width,
                stroke_color=self.stroke_color,
                align="center",
                transparent=True,
                bg_color="transparent",
            )
            return r

        r = _get_text_clip()
        self.text_width, self.text_height = r.size[0], r.size[1]
        r = _get_text_clip(size=self.pixsize)
        return r

    def align_pos(self):
        spos = list(self.pix_pos)
        if self.horz_align == "left":
            spos[0] += self.text_width / 2
        elif self.horz_align == "right":
            spos[0] -= self.text_width / 2
        if self.vert_align == "top":
            spos[1] += self.text_width / 2
        elif self.vert_align == "bottom":
            spos[1] -= self.text_width / 2
        spos[0] += (1.0 - self.scale) * self.pixsize[0] / 2
        spos[1] += (1.0 - self.scale) * self.pixsize[1] / 2
        return spos

    def update_frame_pos(self, frame):
        if self.x_anim is not None:
            self.pos[0] = self.x_anim[frame]
        if self.y_anim is not None:
            self.pos[1] = self.y_anim[frame]

    def update_frame(self, frame):
        self.update_frame_angle(frame)
        self.update_frame_pos(frame)
        self.update_frame_color(frame)
        self.update_frame_opacity(frame)
        self.update_frame_scale(frame)
        self.update_frame_blur(frame)
        self.update_frame_shearx(frame)
        self.update_frame_sheary(frame)

    def get_frame_mask(self, frame, t0, t1):
        self.mask_obj.scenesize = self.pixsize
        self.mask_obj.update_frame(frame)
        mask = self.mask_obj.get_clip_obj().set_start(t0).set_end(t1)
        return mask

    def get_clip_frame(self, frame, t0, t1):
        self.update_frame(frame)
        if self.clip_obj is None or not self.color == self.prev_color:
            self.clip_obj = self.new_clip_obj()
        if not self.opacity > 0:
            return None
        clipx = self.clip_obj.set_duration(t1 - t0)
        if (
            self.angle_anim is not None
            or abs(self.angle) > 0
            or self.shearx_anim is not None
            or self.sheary_anim is not None
        ):
            pix = Image.new("RGBA", (self.pixsize[0], self.pixsize[1]), (0, 0, 0, 0))
            x = np.zeros_like(pix)
            x[:, :, 0] = self.clip_obj.img[:, :, 0]
            x[:, :, 1] = self.clip_obj.img[:, :, 1]
            x[:, :, 2] = self.clip_obj.img[:, :, 2]
            m = (x[:, :, 0] + x[:, :, 1] + x[:, :, 2]) / 3
            x[:, :, 3] = np.minimum(1, m) * 255
            ximg = Image.fromarray(x)
            ximg = ximg.rotate(self.angle, resample=Image.BILINEAR)
            r = Rect(self.width / self.pixsize[0], self.height / self.pixsize[1])
            r.move_to(self.pos.as_tuple())
            ximg, x0, y0 = self.transform_img(ximg, r)
            r = Rect(self.width, self.height)
            pix.paste(ximg, box=(-int(r.width / 2), -int(r.height / 2)))
            pix = np.asarray(pix)
            clipx.mask = ImageClip(1.0 * pix[:, :, 3] / 255, ismask=True)
            clipx = ImageClip(pix, transparent=True, ismask=False)
        if self.blur_anim is not None:
            fl = lambda pic: fill_array(pic, self.color)
            clipx = clipx.fl_image(fl)
            bl = lambda pic: blur_image(pic, self.blur)
            clipx.mask = clipx.mask.fl_image(bl)
        if self.scale_anim is not None:
            clipx = clipx.resize(self.scale).set_duration(t1 - t0)
            if self.scale > 1.0:
                clipx = crop_clip(clipx, self.pixsize)
        clipx = (
            clipx.set_position(self.align_pos())
            .set_opacity(self.opacity)
            .set_duration(t1 - t0)
        )
        clipx = crop_clip(clipx, self.pixsize)
        clip = (
            CompositeVideoClip([clipx], size=self.pixsize, bg_color=None)
            .set_start(t0)
            .set_end(t1)
            .set_layer(self.layer)
        )
        if self.mask_obj is not None:
            mask = self.get_frame_mask(frame, t0, t1)
            fl = lambda pic: np.minimum(pic, mask.img)
            clip.mask = clip.mask.fl_image(fl)
        return clip
