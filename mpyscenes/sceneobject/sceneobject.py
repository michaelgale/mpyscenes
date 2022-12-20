from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


class SceneObject:
    """Base class which defines the properties of an object in a movie scene.
    SceneObjects can be added directly to a Movie if they are more or less
    persistent in a movie.  For animated or special behaviors in a movie, a
    SceneObject can be attached to a Scene and have one or more SceneActions
    applied to it."""

    def __init__(self, **kwargs):
        self.pos = Point(0, 0)
        self.opacity = 1
        self.scale = 1.0
        self.angle = 0.0
        self.blur = 0
        self.layer = 0
        self.x_anim = None
        self.y_anim = None
        self.op_anim = None
        self.scale_anim = None
        self.blur_anim = None
        self.enable_anim = None
        self.angle_anim = None
        self.color_r_anim = None
        self.color_g_anim = None
        self.color_b_anim = None
        self.clip_obj = None
        self.mask_obj = None
        self.is_mask = False
        for k, v in kwargs.items():
            if k in self.__dict__:
                if "color" in k:
                    self.__dict__[k] = SceneObject.color_to_tuple(v)
                else:
                    self.__dict__[k] = v
        if "pixsize" in kwargs:
            self.pixsize = size_preset_tuple(kwargs["pixsize"])
        else:
            self.pixsize = (0, 0)
        if "pos" in kwargs:
            self.set_pos(kwargs["pos"])
        self.scene = Scene(obj=self)

    def __str__(self):
        s = []
        s.append("SceneObject: %s" % (type(self)))
        for k, v in self.__dict__.items():
            if isinstance(v, dict):
                s.append("  %s:" % (k))
                for ak, av in v.items():
                    s.append("    %s: %s" % (ak, av))
            else:
                s.append("  %s: %s" % (k, v))
        return "\n".join(s)

    @property
    def pix_pos(self):
        x = (self.pos[0] - 0.5) * self.pixsize[0]
        y = (self.pos[1] - 0.5) * self.pixsize[1]
        return x, y

    def set_pos(self, pos, y=None):
        self.pos = Point(pos, y)

    def update_frame_opacity(self, frame):
        if self.op_anim is not None:
            self.opacity = self.op_anim[frame]

    def update_frame_scale(self, frame):
        if self.scale_anim is not None:
            self.scale = self.scale_anim[frame]

    def update_frame_angle(self, frame):
        if self.angle_anim is not None:
            self.angle = self.angle_anim[frame]

    def update_frame_blur(self, frame):
        if self.blur_anim is not None:
            self.blur = self.blur_anim[frame]

    def update_frame_color(self, frame):
        color = list(self.color)
        if self.color_r_anim is not None:
            color[0] = int(self.color_r_anim[frame])
        if self.color_g_anim is not None:
            color[1] = int(self.color_g_anim[frame])
        if self.color_b_anim is not None:
            color[2] = int(self.color_b_anim[frame])
        self.color = tuple(color)

    def assign_animator_from_key(self, key, animator):
        if key == "x":
            self.x_anim = animator
        elif key == "y":
            self.y_anim = animator
        elif key == "left":
            self.left_anim = animator
        elif key == "right":
            self.right_anim = animator
        elif key == "width":
            self.width_anim = animator
        elif key == "height":
            self.height_anim = animator
        elif key == "top":
            self.top_anim = animator
        elif key == "bottom":
            self.bottom_anim = animator
        elif key == "opacity":
            self.op_anim = animator
        elif key == "blur":
            self.blur_anim = animator
        elif key == "scale":
            self.scale_anim = animator
        elif key == "angle":
            self.angle_anim = animator
        elif key == "color_r":
            self.color_r_anim = animator
        elif key == "color_g":
            self.color_g_anim = animator
        elif key == "color_b":
            self.color_b_anim = animator
        elif key == "draw":
            self.draw_anim = animator

    def add_action(self, action):
        self.scene.add_action(action)

    def add_buildin(self, action):
        self.scene.add_buildin(action)

    def add_buildout(self, action):
        self.scene.add_buildout(action)

    def color_name(self, v):
        if isinstance(v, (tuple, list)):
            return colour_name_from_tuple(v)
        elif isinstance(v, str):
            if v[0] == "#":
                return colour_name_from_hex(v)
        return v

    @staticmethod
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
