# system modules
import copy

# my modules
from mpyscenes import *


def test_scene_init():
    s1 = Scene(fps=30)
    assert s1.fps == 30
    assert len(s1.actions) == 0
    assert s1.obj is None


def test_flyinout_scene():
    s1 = FlyInOutScene(duration=3, start_from="top", fade_in=True)
    assert s1.fps == 60
    assert s1.duration == 3
    assert s1.intro == 1
    assert s1.outro == 1
    assert s1.drift == True
    assert s1.dwell_at == 0.5
    assert s1.start_from == "top"
    assert s1.bidir == False
    assert s1.loc == 0.5
    assert s1.fade_in == True
    assert s1.fade_out == False
    s1.setup_actions()
    assert len(s1.buildin) == 2
    assert len(s1.buildout) == 1
    assert len(s1.actions) == 1
    o1 = SceneObject()
    s1.obj = o1
    assert s1.obj.y_anim is None
    s1.setup_scene(start_time=10)
    assert s1.obj.y_anim.start_frame == 600
    assert s1.obj.y_anim.start_value == -0.5
    assert s1.obj.y_anim.stop_frame == 780
    assert s1.obj.y_anim.stop_value == 1.5
