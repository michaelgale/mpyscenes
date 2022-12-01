# system modules
import copy

# my modules
from mpyscenes import *


def test_actions():
    f1 = FadeInAction()
    assert f1.duration is not None


def test_dropinaction():
    f1 = DropInBuildAction(
        duration=3, start_from="right", loc=0.1, end_at=0.3, degree=3
    )
    assert f1.duration == 3
    assert f1.start_from == "right"
    assert f1.loc == 0.1
    assert f1.end_at == 0.3
    assert f1.degree == 3


def test_dropin_action():
    f1 = FlyInBuildAction(duration=3, start_from="right", loc=0.1, end_at=0.3, degree=3)
    assert f1.duration == 3
    assert f1.start_from == "right"
    assert f1.loc == 0.1
    assert f1.end_at == 0.3
    assert f1.degree == 3
    assert f1.fps == 60


def test_fadeout_action():
    f1 = FadeOutAction(fps=30, duration=3)
    assert f1.duration == 3
    assert f1.fps == 30


def test_flyout_action():
    f1 = FlyOutBuildAction(duration=3, start_from=0.1, loc=0.2, end_at="top", degree=3)
    assert f1.duration == 3
    assert f1.start_from == 0.1
    assert f1.loc == 0.2
    assert f1.end_at == "top"
    assert f1.degree == 3


def test_move_action():
    f1 = MoveAction(duration=3, start_pos=(1, 2), end_pos=(3, 4))
    assert f1.duration == 3
    assert f1.start_pos.x == 1
    assert f1.start_pos.y == 2
    assert f1.end_pos.x == 3
    assert f1.end_pos.y == 4


def test_move_action():
    f1 = MoveAction(duration=3, start_pos=(1, 2), end_pos=(3, 5))
    assert f1.duration == 3
    assert f1.start_pos.x == 1
    assert f1.start_pos.y == 2
    assert f1.end_pos.x == 3
    assert f1.end_pos.y == 5
    assert f1.x_distance == 2
    assert f1.y_distance == 3
    assert f1.x_start == 1
    assert f1.y_start == 2

    f2 = LinearMoveAction(duration=3, start_pos=(5, 7), end_pos=(8, 1))
    assert f2.duration == 3
    assert f2.start_pos.x == 5
    assert f2.start_pos.y == 7
    assert f2.end_pos.x == 8
    assert f2.end_pos.y == 1
    assert f2.x_distance == 3
    assert f2.y_distance == 6
    assert f2.x_start == 5
    assert f2.y_start == 7
    f2.setup_animators(start_time=5)
    assert f2.animators["x"] is not None
    assert f2.animators["x"].start_frame == 300
    assert f2.animators["x"].start_value == 5
    assert f2.animators["x"].stop_frame == 480
    assert f2.animators["x"].stop_value == 8
    assert f2.animators["x"].frame_len == 180
    assert f2.animators["x"].value_range == 3
    assert f2.animators["y"] is not None
    assert f2.animators["y"].start_frame == 300
    assert f2.animators["y"].start_value == 7
    assert f2.animators["y"].stop_frame == 480
    assert f2.animators["y"].stop_value == 1
    assert f2.animators["y"].frame_len == 180
    assert f2.animators["y"].value_range == 6

    f3 = EaseInOutMoveAction(
        fps=30, duration=3, start_pos=(5, 7), end_pos=(5, 1), degree=3
    )
    assert f3.duration == 3
    assert f3.start_pos.x == 5
    assert f3.start_pos.y == 7
    assert f3.end_pos.x == 5
    assert f3.end_pos.y == 1
    assert f3.x_distance == 0
    assert f3.y_distance == 6
    assert f3.x_start == 5
    assert f3.y_start == 7
    assert f3.degree == 3
    assert f3.fps == 30
    f3.setup_animators(start_time=1)
    assert f3.animators["x"] is None
    assert f3.animators["y"] is not None
    assert f3.animators["y"].start_frame == 30
    assert f3.animators["y"].start_value == 7
    assert f3.animators["y"].stop_frame == 120
    assert f3.animators["y"].stop_value == 1
    assert f3.animators["y"].frame_len == 90
    assert f3.animators["y"].value_range == 6
