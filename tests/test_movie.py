# system modules
import copy

# my modules
from mpyscenes import *


def test_movie_init():
    m1 = Movie(size="720p")
    assert m1.size == (1280, 720)
    m2 = Movie(size=(800, 480))
    assert m2.size == (800, 480)
