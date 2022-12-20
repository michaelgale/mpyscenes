from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=30, filename="./movies/scale_movie")
    obj = RectSceneObject(size=(0.2, 0.2), pos=(0.3, 0.6), color="#1050C0")
    obj.add_action(MoveUpAction(duration=0.5, ease_in=False, offset=0.2))
    obj.add_action(ScaleAction(duration=0.5, delay=0.5, scale=0.5))
    obj.add_action(ScaleAction(duration=0.5, delay=1, scale=1.5))
    obj.add_action(BlurAction(duration=0.75, delay=1.5, blur=25))
    obj.add_action(BlurAction(duration=0.75, delay=2.25, blur=0))
    obj.add_buildout(FadeBuildOutAction(duration=0.25))
    ms.add_sceneobject(obj, start_time=0.25)

    ms.render_video(0, 5.5)


if __name__ == "__main__":
    main()
