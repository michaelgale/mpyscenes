from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=30, filename="move_movie")
    s0 = Scene(obj=RectSceneObject(size=(0.2, 0.2), pos=(0.6, 0.6), color="#10C040"))
    # s0.buildin.append(FadeInAction(duration=0.5))
    s0.actions.append(MoveUpAction(duration=0.5, ease_in=False, offset=0.2))
    s0.actions.append(MoveLeftAction(duration=1, delay=1, offset=0.5))
    s0.actions.append(MoveDownAction(duration=1, delay=2, offset=0.3))
    s0.actions.append(MoveRightAction(duration=0.5, delay=2, offset=0.5))
    s0.buildout.append(FadeOutAction(duration=0.25))
    ms.add_scene(s0, start_time=0.25)

    ms.render_video(0, 5)


if __name__ == "__main__":
    main()
