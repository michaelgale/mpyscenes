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
        self.fps = 60
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


class NoAction(SceneAction):
    def __init__(self, **kwargs):
        self.duration = 0
        super().__init__(**kwargs)


class MoveAction(SceneAction):
    def __init__(self, **kwargs):
        self.duration = 4
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
