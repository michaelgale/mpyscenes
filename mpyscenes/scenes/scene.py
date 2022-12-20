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
    elif key == "color_r":
        return obj.color[0]
    elif key == "color_g":
        return obj.color[1]
    elif key == "color_b":
        return obj.color[2]
    elif key == "draw":
        return obj.draw_length
    return None


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

    def _listify(self, items):
        if not isinstance(items, list):
            return [items]
        return items

    def add_action(self, actions):
        actions = self._listify(actions)
        t0 = actions[0].delay
        for action in actions:
            action.delay = t0
            self.actions.append(action)
            t0 += action.duration

    def add_buildin(self, actions):
        actions = self._listify(actions)
        t0 = actions[0].delay
        for action in actions:
            action.delay = t0
            self.buildin.append(action)
            t0 += action.duration

    def add_buildout(self, actions):
        actions = self._listify(actions)
        t0 = actions[0].delay
        for action in actions:
            action.delay = t0
            self.buildout.append(action)
            t0 += action.duration

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
        self.obj.assign_animator_from_key(key, a)
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
        t0 += self._setup_action_animators(self.buildin, start_time=t0, **kwargs)
        t0 += self._setup_action_animators(self.actions, start_time=t0, **kwargs)
        t0 += self._setup_action_animators(self.buildout, start_time=t0, **kwargs)
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
