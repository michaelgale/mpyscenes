from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


class BuildInAction(SceneAction):
    def __init__(self, **kwargs):
        if "obj" in kwargs:
            kwargs["buildin"] = True
        super().__init__(**kwargs)


class FadeBuildInAction(FadeAction):
    def __init__(self, **kwargs):
        self.duration = 1
        super().__init__(**kwargs)

    def setup_animators(self, start_time=0, **kwargs):
        opacity = 1
        if "opacity" in kwargs:
            opacity = kwargs["opacity"]
        self.animators["opacity"] = LinearAnimator(
            start_time, 0, start_time + self.duration, opacity, fps=self.fps
        )


class DropBuildInAction(BuildInAction):
    def __init__(self, **kwargs):
        self.duration = 1
        self.start_from = "top"
        self.loc = 0.5
        self.end_at = 0.5
        self.degree = 2
        super().__init__(**kwargs)

    def setup_animators(self, start_time=0, **kwargs):
        if self.start_from == "left" or self.start_from == "top":
            p0 = -0.5
        elif self.start_from == "right" or self.start_from == "bottom":
            p0 = 1.5
        aref = "x" if self.start_from in ["left", "right"] else "y"
        self.animators[aref] = EaseInAnimator(
            start_time,
            p0,
            start_time + self.duration,
            self.end_at,
            degree=self.degree,
            fps=self.fps,
        )


class BounceBuildInAction(BuildInAction):
    def __init__(self, **kwargs):
        self.duration = 2
        self.start_from = "top"
        self.loc = 0.5
        self.end_at = 0.5
        self.degree = 2
        self.bounces = 4
        self.damping = 0.333
        self.gravity = 10.0
        self.squash = None
        super().__init__(**kwargs)

    def setup_animators(self, start_time=0, **kwargs):
        if self.start_from == "left" or self.start_from == "top":
            p0 = -0.5
        elif self.start_from == "right" or self.start_from == "bottom":
            p0 = 1.5
        aref = "x" if self.start_from in ["left", "right"] else "y"
        href = "height" if self.start_from in ["top", "bottom"] else "width"
        wref = "width" if self.start_from in ["top", "bottom"] else "height"
        height = (
            self.obj.height if self.start_from in ["top", "bottom"] else self.obj.width
        )
        width = (
            self.obj.width if self.start_from in ["top", "bottom"] else self.obj.height
        )
        t0 = start_time
        p1 = self.end_at
        self.animators[aref] = []
        kw = {"degree": self.degree, "fps": self.fps}
        hmax = abs(p1 - p0)
        vmax = math.sqrt(2 * hmax * self.gravity)
        td = sqrt(2 * hmax / self.gravity)
        squash = 0
        if self.squash is not None:
            self.animators[href] = []
            self.animators[wref] = []
            squash = self.squash
            squash = min(0.9, squash)
            squash = max(0.1, squash)

        ts = (squash * height) / vmax
        for _ in range(self.bounces):
            self.animators[aref].append(EaseInAnimator(t0, p0, t0 + td, p1, **kw))
            if self.squash is not None:
                hs = (1.0 - squash) * height
                self.animators[href].append(
                    LinearAnimator(t0 + td, height, t0 + td + ts, hs, fps=self.fps)
                )
                As = width * (height - hs)
                ws = 0.5 * As / hs if hs > 0 and As > 0 else 0
                ws += width
                self.animators[wref].append(
                    LinearAnimator(t0 + td, width, t0 + td + ts, ws, fps=self.fps)
                )
            t0 += td
            p0 = p1
            vmax *= self.damping
            hmax = 0.5 * vmax * vmax / self.gravity
            td = sqrt(2 * hmax / self.gravity)
            hmax = -hmax if self.start_from in ["left", "top"] else hmax
            p1 = self.end_at + hmax
            self.animators[aref].append(EaseOutAnimator(t0, p0, t0 + td, p1, **kw))
            if self.squash is not None:
                self.animators[href].append(
                    LinearAnimator(t0, hs, t0 + td, height, fps=self.fps)
                )
                self.animators[wref].append(
                    LinearAnimator(t0, ws, t0 + td, width, fps=self.fps)
                )
                squash *= self.damping
            t0 += td
            p0 = p1
            p1 = self.end_at
        self.animators[aref].append(EaseInAnimator(t0, p0, t0 + td, self.end_at, **kw))


class FlyBuildInAction(BuildInAction):
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
        aref = "x" if self.start_from in ["left", "right"] else "y"
        self.animators[aref] = EaseOutAnimator(
            start_time,
            p0,
            start_time + self.duration,
            p1,
            degree=self.degree,
            fps=self.fps,
        )
