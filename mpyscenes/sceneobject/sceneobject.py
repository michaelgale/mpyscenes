from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


class SceneObject:
    """Base class which defines the properties of an object in a movie scene.
    SceneObjects can be added directly to a Movie if they are more or less
    persistent in a movie.  For animated or special behaviors in a movie, a
    SceneObject can have one or more SceneActions applied to it."""

    def __init__(self, **kwargs):
        self.pos = Point(0, 0)
        self.color = (255, 255, 255)
        self.opacity = 1
        self.scale = 1.0
        self.angle = 0.0
        self.blur = 0
        self.layer = 0
        self.shearx = 0
        self.sheary = 0
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
        self.shearx_anim = None
        self.sheary_anim = None
        self.clip_obj = None
        self.mask_obj = None
        self.is_mask = False
        for k, v in kwargs.items():
            if k in self.__dict__:
                if "color" in k:
                    self.__dict__[k] = color_to_tuple(v)
                else:
                    self.__dict__[k] = v
        if "pixsize" in kwargs:
            self.pixsize = size_preset_tuple(kwargs["pixsize"])
        else:
            self.pixsize = (0, 0)
        if "pos" in kwargs:
            self.set_pos(kwargs["pos"])

        self.prev_color = (255, 255, 255)
        self.fps = 60
        self.buildin = []
        self.buildout = []
        self.actions = []
        self.animators = {}

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

    @property
    def animator_count(self):
        all_animators = [
            self.x_anim,
            self.y_anim,
            self.op_anim,
            self.scale_anim,
            self.blur_anim,
            self.enable_anim,
            self.angle_anim,
            self.color_r_anim,
            self.color_g_anim,
            self.color_b_anim,
            self.shearx_anim,
            self.sheary_anim,
        ]
        ac = 0
        for a in all_animators:
            if a is not None:
                if a.is_active:
                    ac += 1
        return ac

    @property
    def pix_size(self):
        return (self.pixsize[0], self.pixsize[1])

    def pix_dim(self, p):
        return int(p[0] * self.pixsize[0]), int(p[1] * self.pixsize[1])

    def rect_pix_dim(self, rect):
        return int(rect.width * self.pixsize[0]), int(rect.height * self.pixsize[1])

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

    def update_frame_shearx(self, frame):
        if self.shearx_anim is not None:
            self.shearx = self.shearx_anim[frame]

    def update_frame_sheary(self, frame):
        if self.sheary_anim is not None:
            self.sheary = self.sheary_anim[frame]

    def update_frame_color(self, frame):
        color = list(self.color)
        if self.color_r_anim is not None:
            color[0] = int(self.color_r_anim[frame])
        if self.color_g_anim is not None:
            color[1] = int(self.color_g_anim[frame])
        if self.color_b_anim is not None:
            color[2] = int(self.color_b_anim[frame])
        self.prev_color = self.color
        self.color = tuple(color)

    def shear_angles(self):
        angx, angy = 0, 0
        if self.shearx:
            angx = math.degrees(math.atan2(self.shearx, 1))
        if self.sheary:
            angy = math.degrees(math.atan2(self.sheary, 1))
        return angx, angy

    def transform_img(self, img, rect, scale=1.0, no_rotate=False):
        rw, rh = self.pix_dim((rect.width, rect.height))
        xc, yc = self.pix_dim(rect.get_centre())
        angx, angy = self.shear_angles()
        if abs(1.0 - scale) > 0:
            img = ImageOps.scale(img, scale)
        img = add_margin(img, int(max(rw / 2, rh / 2)))
        img = img.rotate(self.angle, expand=True)
        x0, y0 = int(xc - img.size[0] / 2), int(yc - img.size[1] / 2)
        x0 += int(2 * rh * math.sin(math.radians(angx)))
        y0 += int(2 * rw * math.sin(math.radians(angy)))
        ps = (self.pixsize[0], self.pixsize[1])
        if self.shearx:
            img = img.transform(ps, Image.AFFINE, (1.0, self.shearx, 0, 0, 1, 0))
        if self.sheary:
            img = img.transform(ps, Image.AFFINE, (1.0, 0, 0, self.sheary, 1, 0))
        return img, x0, y0

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
        elif key == "shearx":
            self.shearx_anim = animator
        elif key == "sheary":
            self.sheary_anim = animator

    def object_value_from_key(self, key):
        if key == "x":
            return self.pos.x
        elif key == "y":
            return self.pos.y
        elif key == "left":
            return self.rect.left
        elif key == "right":
            return self.rect.right
        elif key == "width":
            return self.rect.width
        elif key == "height":
            return self.rect.height
        elif key == "top":
            return self.rect.top
        elif key == "bottom":
            return self.rect.bottom
        elif key == "opacity":
            return self.opacity
        elif key == "blur":
            return self.blur
        elif key == "scale":
            return self.scale
        elif key == "angle":
            return self.angle
        elif key == "color_r":
            return self.color[0]
        elif key == "color_g":
            return self.color[1]
        elif key == "color_b":
            return self.color[2]
        elif key == "draw":
            return self.draw_length
        elif key == "shearx":
            return self.shearx
        elif key == "sheary":
            return self.sheary
        return None

    def add_action(self, actions):
        actions = listify(actions)
        t0 = actions[0].delay
        for action in actions:
            action.delay = t0
            self.actions.append(action)
            t0 += action.duration

    def add_buildin(self, actions):
        actions = listify(actions)
        t0 = actions[0].delay
        for action in actions:
            action.delay = t0
            self.buildin.append(action)
            t0 += action.duration

    def add_buildout(self, actions):
        actions = listify(actions)
        t0 = actions[0].delay
        for action in actions:
            action.delay = t0
            self.buildout.append(action)
            t0 += action.duration

    def _setup_action_animators(self, actions, start_time=0, **kwargs):
        max_duration = 0
        if len(actions) > 0:
            for action in actions:
                t0 = start_time + action.delay
                td = action.duration + action.delay
                action.setup_animators(start_time=t0, fps=self.fps, **kwargs)
                if "loc" in action.__dict__:
                    self.loc = action.loc
                if td > max_duration:
                    max_duration = td
        return max_duration

    def _initialize_first_animator(self, key, animators):
        a = animators[0]
        if a.link_to_previous:
            a.link_to_previous = False
            v = self.object_value_from_key(key)
            if v is not None:
                a.start_value = v
                if a.previous_to_value is not None:
                    a.stop_value = a.previous_to_value
                else:
                    a.stop_value = a.start_value + a.offset_from_previous

    def _assign_animators(self, key, animators):
        self._initialize_first_animator(key, animators)
        a = AnimatorGroup(animators[0].start_frame, [animators[0]])
        a.fps = self.fps
        if len(animators) > 1:
            for animator in animators[1:]:
                delay = animator.start_frame - a.stop_frame
                a.add_animator(animator, with_delay=delay)
        self.assign_animator_from_key(key, a)
        if key == "x":
            if "loc" in self.__dict__:
                self.pos = Point(0, self.loc)
        elif key == "y":
            if "loc" in self.__dict__:
                self.pos = Point(self.loc, 0)

    def setup_scene(self, start_time=0, **kwargs):
        for action in [*self.buildin, *self.actions, *self.buildout]:
            action.fps = self.fps
        # self.setup_actions()
        t0 = start_time
        t0 += self._setup_action_animators(self.buildin, start_time=t0, **kwargs)
        t0 += self._setup_action_animators(self.actions, start_time=t0, **kwargs)
        t0 += self._setup_action_animators(self.buildout, start_time=t0, **kwargs)
        self.animators = {}
        for action in [*self.buildin, *self.actions, *self.buildout]:
            for k, v in action.animators.items():
                if v is None:
                    continue
                if k not in self.animators:
                    if isinstance(v, list):
                        self.animators[k] = v
                    else:
                        self.animators[k] = [v]
                else:
                    if isinstance(v, list):
                        self.animators[k].extend(v)
                    else:
                        self.animators[k].append(v)
        for k, v in self.animators.items():
            self._assign_animators(k, v)
