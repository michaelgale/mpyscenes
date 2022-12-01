# system modules
import copy

# my modules
from mpyscenes import *


def test_scene_object():
    s1 = SceneObject(pixsize="720p")
    assert s1.pixsize == (1280, 720)
    s2 = SceneObject(pixsize=(800, 400))
    assert s2.pixsize == (800, 400)

    s2.set_pos((10, 20))
    assert s2.pos.x == 10
    assert s2.pos.y == 20

    s2.set_pos([50, 60])
    assert s2.pos.x == 50
    assert s2.pos.y == 60

    s2.set_pos(Point(0.1, 0.5))
    assert s2.pos.x == 0.1
    assert s2.pos.y == 0.5

    s2.set_pos(0.3, 1.5)
    assert s2.pos.x == 0.3
    assert s2.pos.y == 1.5
