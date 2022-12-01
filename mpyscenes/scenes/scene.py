from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


class Scene:
    """A base class for associating a scene object with actions.
    Scene objects can include text objects, rectangles, etc.
    Actions are catergorized by time as build in to the frame, actions
    within the frame and finally build out of the frame.  Actions are
    processed into animators which modulate properties of an object such
    as position, opacity, size, etc."""

    def __init__(self, obj=None, **kwargs):
        self.obj = obj
        self.fps = 60
        self.buildin = []
        self.buildout = []
        self.actions = []
        self.animators = {}
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __str__(self):
        s = []
        s.append("Scene: %s" % (type(self)))
        for k, v in self.__dict__.items():
            if isinstance(v, dict):
                s.append("  %s:" % (k))
                for ak, av in v.items():
                    s.append("    %s: %s" % (ak, av))
            else:
                s.append("  %s: %s" % (k, v))
        return "\n".join(s)

    def setup_actions(self):
        # usually implemented by a derived class
        pass

    def _setup_action_animators(self, actions, start_time=0, **kwargs):
        max_duration = 0
        if len(actions) > 0:
            for action in actions:
                action.setup_animators(start_time=start_time, fps=self.fps, **kwargs)
                if action.duration > max_duration:
                    max_duration = action.duration
        return max_duration

    def _assign_animators(self, key, animators):
        a = AnimatorGroup(animators[0].start_frame, [animators[0]])
        a.fps = self.fps
        if len(animators) > 1:
            for animator in animators[1:]:
                delay = animator.start_frame - a.stop_frame
                a.add_animator(animator, with_delay=delay)
        if key == "x":
            self.obj.x_anim = a
            self.obj.pos = Point(0, self.loc)
        elif key == "y":
            self.obj.y_anim = a
            self.obj.pos = Point(self.loc, 0)
        elif key == "opacity":
            self.obj.op_anim = a

    def setup_scene(self, start_time=0, **kwargs):
        self.setup_actions()
        t0 = start_time
        td = self._setup_action_animators(self.buildin, start_time=t0, **kwargs)
        t0 += td
        td = self._setup_action_animators(self.actions, start_time=t0, **kwargs)
        t0 += td
        td = self._setup_action_animators(self.buildout, start_time=t0, **kwargs)
        self.animators = {}
        for action in [*self.buildin, *self.actions, *self.buildout]:
            for k, v in action.animators.items():
                if v is None:
                    continue
                if k not in self.animators:
                    self.animators[k] = [v]
                else:
                    self.animators[k].append(v)
        for k, v in self.animators.items():
            self._assign_animators(k, v)
