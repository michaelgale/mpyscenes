from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


class BuildOutAction(SceneAction):
    def __init__(self, **kwargs):
        if "obj" in kwargs:
            kwargs["buildout"] = True
        super().__init__(**kwargs)


class FadeBuildOutAction(BuildOutAction):
    def __init__(self, **kwargs):
        self.duration = 1
        super().__init__(**kwargs)

    def setup_animators(self, start_time=0, **kwargs):
        a = self.choose_animator(start_time, to_value=0)
        self.animators["opacity"] = a


class FlyBuildOutAction(BuildOutAction):
    def __init__(self, **kwargs):
        self.duration = 1
        self.start_from = 0.5
        self.end_at = "left"
        self.loc = 0.5
        self.degree = 2
        super().__init__(**kwargs)

    def setup_animators(self, start_time=0, **kwargs):
        if self.end_at == "left" or self.end_at == "top":
            p0, p1 = self.start_from, -0.5
        elif self.end_at == "right" or self.end_at == "bottom":
            p0, p1 = self.start_from, 1.5
        aref = "x" if self.end_at in ["left", "right"] else "y"
        self.animators[aref] = EaseOutAnimator(
            start_time,
            p0,
            start_time + self.duration,
            p1,
            degree=self.degree,
            fps=self.fps,
        )
