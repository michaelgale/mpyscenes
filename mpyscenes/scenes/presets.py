from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


class FlyInOutScene(Scene):
    def __init__(self, **kwargs):
        self.duration = 4
        self.intro = 1
        self.outro = 1
        self.drift = True
        self.dwell_at = 0.5
        self.start_from = "left"
        self.bidir = False
        self.loc = 0.5
        self.degree = 2
        self.fade_in = False
        self.fade_out = False
        super().__init__(**kwargs)

    def setup_actions(self):
        mid_duration = self.duration - (self.intro + self.outro)
        mid0, mid1 = 0.4, 0.6
        if not self.drift:
            mid0, mid1 = self.dwell_at, self.dwell_at
        if not self.bidir:
            end_at = START_END_MAP[self.start_from]
        else:
            end_at = self.start_from

        # Build in action
        a = FlyInBuildAction(
            duration=self.intro,
            start_from=self.start_from,
            end_at=mid0,
            loc=self.loc,
            degree=self.degree,
            fps=self.fps,
        )
        self.buildin.append(a)
        if self.fade_in:
            self.buildin.append(FadeInAction(duration=self.intro, fps=self.fps))

        # In frame actions
        if self.start_from in ["left", "right"]:
            start_pos = [mid0, self.loc]
            end_pos = [mid1, self.loc]
        else:
            start_pos = [self.loc, mid0]
            end_pos = [self.loc, mid1]
        if self.drift:
            a = LinearMoveAction(
                duration=mid_duration,
                start_pos=start_pos,
                end_pos=end_pos,
                fps=self.fps,
            )
            self.actions.append(a)

        # Build out actions
        a = FlyOutBuildAction(
            duration=self.outro,
            start_from=mid1,
            end_at=end_at,
            loc=self.loc,
            degree=self.degree,
            fps=self.fps,
        )
        self.buildout.append(a)
        if self.fade_out:
            self.buildout.append(FadeOutAction(duration=self.outro, fps=self.fps))
