"""mpyscenes - Helper utilities to build complex scenes for moviepy."""

import os

# fmt: off
__project__ = 'mpyscenes'
__version__ = '0.1.0'
# fmt: on

VERSION = __project__ + "-" + __version__

script_dir = os.path.dirname(__file__)

from .movie import Movie
from .sceneobject.sceneobject import SceneObject
from .sceneobject.rectsceneobject import RectSceneObject, ImageSceneObject
from .sceneobject.textsceneobject import TextSceneObject
from .scenes.scene import *
from .scenes.action import *
from .scenes.buildin import *
from .scenes.buildout import *
from .scenes.presets import *
from .helpers import size_preset_tuple
