from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


class Scene:
    def __init__(self, obj, **kwargs):
        self.obj = obj
        self.fps = obj.fps
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v


class FlyInOutScene(Scene):
    def __init__(self, obj, **kwargs):
        self.duration = 4
        self.intro = 1
        self.outro = 1
        self.drift = True
        self.shear = 0
        self.dwell_at = 0.5
        self.start_from = "left"
        self.bidir = False
        self.loc = 0.5
        self.degree = 2
        self.fade_in = False
        self.fade_out = False
        super().__init__(obj, **kwargs)
        self.setup_actions()

    def setup_actions(self):
        START_END_MAP = {
            "left": "right",
            "top": "bottom",
            "right": "left",
            "left": "right",
        }
        mid_duration = self.duration - (self.intro + self.outro)
        mid0, mid1 = 0.4, 0.6
        if self.start_from in ["right", "bottom"]:
            mid0, mid1 = 0.6, 0.4

        if not self.drift:
            mid0, mid1 = self.dwell_at, self.dwell_at
        if not self.bidir:
            end_at = START_END_MAP[self.start_from]
        else:
            end_at = self.start_from

        # Build in action
        a = FlyBuildInAction(
            duration=self.intro,
            start_from=self.start_from,
            end_at=mid0,
            loc=self.loc,
            degree=self.degree,
            fps=self.fps,
        )
        self.obj.add_buildin(a)
        if self.fade_in:
            self.obj.add_buildin(FadeBuildInAction(duration=self.intro, fps=self.fps))
        if self.shear:
            if self.start_from in ["left", "right"]:
                shear = -self.shear if self.start_from == "right" else self.shear
                a = ShearXAction(duration=0, shear=shear)
                self.obj.add_buildin(a)
                a = ShearXAction(
                    duration=self.intro, ease_in=False, ease_out=True, degree=3, shear=0
                )
                self.obj.add_buildin(a)
            else:
                shear = -self.shear if self.start_from == "top" else self.shear
                a = ShearYAction(duration=0, shear=shear)
                self.obj.add_buildin(a)
                a = ShearYAction(
                    duration=self.intro, ease_in=False, ease_out=True, degree=3, shear=0
                )
                self.obj.add_buildin(a)

        # In frame actions
        if self.start_from in ["left", "right"]:
            start_pos = [mid0, self.loc]
            end_pos = [mid1, self.loc]
        else:
            start_pos = [self.loc, mid0]
            end_pos = [self.loc, mid1]
        self.obj.set_pos(start_pos)

        if self.drift:
            a = LinearMoveAction(
                duration=mid_duration,
                start_pos=start_pos,
                end_pos=end_pos,
                fps=self.fps,
            )
            self.obj.add_action(a)

        # Build out actions
        a = FlyBuildOutAction(
            duration=self.outro,
            start_from=mid1,
            end_at=end_at,
            loc=self.loc,
            degree=self.degree,
            fps=self.fps,
        )
        self.obj.add_buildout(a)
        if self.shear:
            if self.start_from in ["left", "right"]:
                shear = -self.shear if self.start_from == "right" else self.shear
                a = ShearXAction(
                    duration=self.outro,
                    ease_in=False,
                    ease_out=True,
                    degree=3,
                    shear=shear,
                )
            else:
                shear = -self.shear if self.start_from == "top" else self.shear
                a = ShearYAction(
                    duration=self.outro,
                    ease_in=False,
                    ease_out=True,
                    degree=3,
                    shear=shear,
                )
            self.obj.add_buildout(a)
        if self.fade_out:
            self.obj.add_buildout(FadeBuildOutAction(duration=self.outro, fps=self.fps))
