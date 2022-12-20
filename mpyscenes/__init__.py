"""mpyscenes - Helper utilities to build complex scenes for moviepy."""

import os

# fmt: off
__project__ = 'mpyscenes'
__version__ = '0.2.0'
# fmt: on

VERSION = __project__ + "-" + __version__

script_dir = os.path.dirname(__file__)

from .movie import Movie

# from .scenes.scene import *
from .sceneobject.sceneobject import SceneObject
from .sceneobject.rectsceneobject import RectSceneObject, ImageSceneObject
from .sceneobject.textsceneobject import TextSceneObject
from .sceneobject.linesceneobject import LineSceneObject, TextLineSceneObject
from .sceneaction.action import *
from .sceneaction.buildin import *
from .sceneaction.buildout import *
from .sceneaction.presets import *
from .helpers import size_preset_tuple
