from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


class FadeInAction(SceneAction):
    def __init__(self, **kwargs):
        self.duration = 1
        super().__init__(**kwargs)

    def setup_animators(self, start_time=0, **kwargs):
        self.animators["opacity"] = LinearAnimator(
            start_time, 0, start_time + self.duration, 1, fps=self.fps
        )


class DropInBuildAction(SceneAction):
    def __init__(self, **kwargs):
        self.duration = 2
        self.start_from = "left"
        self.loc = 0.5
        self.end_at = 0.5
        self.degree = 2
        super().__init__(**kwargs)

    def setup_animators(self, start_time=0, **kwargs):
        if self.start_from == "left" or self.start_from == "top":
            p0 = -0.5
        elif self.start_from == "right" or self.start_from == "bottom":
            p0 = 1.5
        if self.start_from in ["left", "right"]:
            aref = "x"
        else:
            aref = "y"
        self.animators[aref] = EaseInAnimator(
            start_time,
            p0,
            start_time + self.duration,
            self.end_at,
            degree=self.degree,
            fps=self.fps,
        )


class FlyInBuildAction(SceneAction):
    def __init__(self, **kwargs):
        self.duration = 1
        self.end_at = 0.5
        self.start_from = "left"
        self.loc = 0.5
        self.degree = 2
        super().__init__(**kwargs)

    def setup_animators(self, start_time=0, **kwargs):
        if self.start_from == "left" or self.start_from == "top":
            p0, p1 = -0.5, self.end_at
        elif self.start_from == "right" or self.start_from == "bottom":
            p0, p1 = 1.5, self.end_at
        if self.start_from in ["left", "right"]:
            aref = "x"
        else:
            aref = "y"
        self.animators[aref] = EaseOutAnimator(
            start_time,
            p0,
            start_time + self.duration,
            p1,
            degree=self.degree,
            fps=self.fps,
        )
