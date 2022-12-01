from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


class FadeOutAction(SceneAction):
    def __init__(self, **kwargs):
        self.duration = 1
        super().__init__(**kwargs)

    def setup_animators(self, start_time=0, **kwargs):
        self.animators["opacity"] = LinearAnimator(
            start_time, 1, start_time + self.duration, 0, fps=self.fps
        )


class FlyOutBuildAction(SceneAction):
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
        if self.end_at in ["left", "right"]:
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
