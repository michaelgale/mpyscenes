from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


class SceneAction:
    """Base class for specifying an individual action.  An action may
    generate one or more animators which are then applied to an object
    by the Scene class.
    """

    def __init__(self, **kwargs):
        self.duration = 0
        self.fps = 60
        self.delay = 0
        self.ease_in = True
        self.ease_out = True
        self.animators = {
            "x": None,
            "y": None,
            "left": None,
            "right": None,
            "width": None,
            "height": None,
            "top": None,
            "bottom": None,
            "opacity": None,
            "blur": None,
            "scale": None,
            "angle": None,
        }
        for k, v in kwargs.items():
            self.__dict__[k] = v
        if "duration" not in self.__dict__:
            self.duration = 0

    def __str__(self):
        s = []
        s.append("SceneAction: %s" % (type(self)))
        for k, v in self.__dict__.items():
            if k == "animators":
                s.append("  animators:")
                for ak, av in self.animators.items():
                    s.append("    %s: %s" % (ak, av))
            else:
                s.append("  %s: %s" % (k, v))
        return "\n".join(s)

    def setup_animators(self, start_time=0, **kwargs):
        pass

    def choose_animator(self, start_time, offset=None, to_value=None):
        t0, t1 = start_time, start_time + self.duration
        if self.ease_in:
            if self.ease_out:
                a = EaseInOutAnimator(
                    t0,
                    0,
                    t1,
                    0,
                    fps=self.fps,
                    offset_from_previous=offset,
                    value_from_previous=to_value,
                )
            else:
                a = EaseInAnimator(
                    t0,
                    0,
                    t1,
                    0,
                    fps=self.fps,
                    offset_from_previous=offset,
                    value_from_previous=to_value,
                )
        elif self.ease_out:
            a = EaseOutAnimator(
                t0,
                0,
                t1,
                0,
                fps=self.fps,
                offset_from_previous=offset,
                value_from_previous=to_value,
            )
        else:
            a = LinearAnimator(
                t0,
                0,
                t1,
                0,
                fps=self.fps,
                offset_from_previous=offset,
                value_from_previous=to_value,
            )
        return a


class NoAction(SceneAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MoveAction(SceneAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_pos = Point(0, 0)
        if "start_pos" in kwargs:
            self.start_pos = Point(kwargs["start_pos"])
        self.end_pos = Point(0, 0)
        if "end_pos" in kwargs:
            self.end_pos = Point(kwargs["end_pos"])

    @property
    def x_distance(self):
        return abs(self.end_pos[0] - self.start_pos[0])

    @property
    def y_distance(self):
        return abs(self.end_pos[1] - self.start_pos[1])

    @property
    def x_start(self):
        return self.start_pos[0]

    @property
    def x_end(self):
        return self.end_pos[0]

    @property
    def y_start(self):
        return self.start_pos[1]

    @property
    def y_end(self):
        return self.end_pos[1]


class MoveUpAction(MoveAction):
    def __init__(self, duration=1, offset=0, **kwargs):
        super().__init__(**kwargs)
        self.duration = duration
        self.offset = offset

    def setup_animators(self, start_time=0, **kwargs):
        a = self.choose_animator(start_time, offset=-self.offset)
        self.animators["y"] = a


class MoveDownAction(MoveAction):
    def __init__(self, duration=1, offset=0, **kwargs):
        super().__init__(**kwargs)
        self.duration = duration
        self.offset = offset

    def setup_animators(self, start_time=0, **kwargs):
        a = self.choose_animator(start_time, offset=self.offset)
        self.animators["y"] = a


class MoveLeftAction(MoveAction):
    def __init__(self, duration=1, offset=0, **kwargs):
        super().__init__(**kwargs)
        self.duration = duration
        self.offset = offset

    def setup_animators(self, start_time=0, **kwargs):
        a = self.choose_animator(start_time, offset=-self.offset)
        self.animators["x"] = a


class MoveRightAction(MoveAction):
    def __init__(self, duration=1, offset=0, **kwargs):
        super().__init__(**kwargs)
        self.duration = duration
        self.offset = offset

    def setup_animators(self, start_time=0, **kwargs):
        a = self.choose_animator(start_time, offset=self.offset)
        self.animators["x"] = a


class LinearMoveAction(MoveAction):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setup_animators(self, start_time=0, **kwargs):
        if self.x_distance > 0:
            self.animators["x"] = LinearAnimator(
                start_time,
                self.x_start,
                start_time + self.duration,
                self.x_end,
                fps=self.fps,
            )
        if self.y_distance > 0:
            self.animators["y"] = LinearAnimator(
                start_time,
                self.y_start,
                start_time + self.duration,
                self.y_end,
                fps=self.fps,
            )


class EaseInOutMoveAction(MoveAction):
    def __init__(self, **kwargs):
        self.degree = 2
        super().__init__(**kwargs)

    def setup_animators(self, start_time=0, **kwargs):
        if self.x_distance > 0:
            self.animators["x"] = EaseInOutAnimator(
                start_time,
                self.x_start,
                start_time + self.duration,
                self.x_end,
                degree=self.degree,
                fps=self.fps,
            )
        if self.y_distance > 0:
            self.animators["y"] = EaseInOutAnimator(
                start_time,
                self.y_start,
                start_time + self.duration,
                self.y_end,
                degree=self.degree,
                fps=self.fps,
            )


class ScaleAction(SceneAction):
    def __init__(self, duration=1, scale=1.0, **kwargs):
        super().__init__(**kwargs)
        self.duration = duration
        self.scale = scale

    def setup_animators(self, start_time=0, **kwargs):
        a = self.choose_animator(start_time, to_value=self.scale)
        self.animators["scale"] = a


class BlurAction(SceneAction):
    def __init__(self, duration=1, blur=1.0, **kwargs):
        super().__init__(**kwargs)
        self.duration = duration
        self.blur = blur

    def setup_animators(self, start_time=0, **kwargs):
        a = self.choose_animator(start_time, to_value=self.blur)
        self.animators["blur"] = a


class RotateAction(SceneAction):
    def __init__(self, duration=1, angle=0.0, **kwargs):
        super().__init__(**kwargs)
        self.duration = duration
        self.angle = angle

    def setup_animators(self, start_time=0, **kwargs):
        a = self.choose_animator(start_time, to_value=self.angle)
        self.animators["angle"] = a
