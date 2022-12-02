from moviepy.editor import *
from toolbox import *
from mpyscenes import *
from ..helpers import *


def object_value_from_key(obj, key):
    if key == "x":
        return obj.pos.x
    elif key == "y":
        return obj.pos.y
    elif key == "left":
        return obj.rect.left
    elif key == "right":
        return obj.rect.right
    elif key == "width":
        return obj.rect.width
    elif key == "height":
        return obj.rect.height
    elif key == "top":
        return obj.rect.top
    elif key == "bottom":
        return obj.rect.bottom
    elif key == "opacity":
        return obj.opacity
    elif key == "blur":
        return obj.blur
    elif key == "scale":
        return obj.scale
    elif key == "angle":
        return obj.angle
    return None


def assign_object_animator_from_key(obj, key, animator):
    if key == "x":
        obj.x_anim = animator
    elif key == "y":
        obj.y_anim = animator
    elif key == "left":
        obj.left_anim = animator
    elif key == "right":
        obj.right_anim = animator
    elif key == "width":
        obj.width_anim = animator
    elif key == "height":
        obj.height_anim = animator
    elif key == "top":
        obj.top_anim = animator
    elif key == "bottom":
        obj.bottom_anim = animator
    elif key == "opacity":
        obj.op_anim = animator
    elif key == "blur":
        obj.blur_anim = animator
    elif key == "scale":
        obj.scale_anim = animator
    elif key == "angle":
        obj.angle_anim = animator


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
                t0 = start_time + action.delay
                td = action.duration + action.delay
                action.setup_animators(start_time=t0, fps=self.fps, **kwargs)
                if td > max_duration:
                    max_duration = td
        return max_duration

    def _initialize_first_animator(self, key, animators):
        a = animators[0]
        if a.link_to_previous:
            a.link_to_previous = False
            v = object_value_from_key(self.obj, key)
            if v is not None:
                a.start_value = v
                if a.value_from_previous is not None:
                    a.stop_value = a.value_from_previous
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
        assign_object_animator_from_key(self.obj, key, a)
        if key == "x":
            if "loc" in self.__dict__:
                self.obj.pos = Point(0, self.loc)
        elif key == "y":
            if "loc" in self.__dict__:
                self.obj.pos = Point(self.loc, 0)

    def setup_scene(self, start_time=0, **kwargs):
        for action in [*self.buildin, *self.actions, *self.buildout]:
            action.fps = self.fps
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
