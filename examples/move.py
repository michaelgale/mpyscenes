from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=30, filename="move_movie")
    rect = RectSceneObject(size=(0.2, 0.2), pos=(0.6, 0.6), color="#10C040")
    rect.add_buildin(FadeInAction(duration=0.25))
    moves = [
        MoveUpAction(duration=0.5, ease_in=False, offset=0.2),
        MoveLeftAction(duration=2.5, offset=0.5, oscillate=True, rate=6),
        MoveDownAction(duration=1, offset=0.3),
        MoveRightAction(0.5, 0.5),
    ]
    rect.add_action(moves)
    rect.add_action(ScaleAction(2, 1.25, delay=0.5))
    rect.add_buildout(FadeOutAction(duration=0.25))
    ms.add_sceneobject(rect, start_time=0.25)

    ms.render_video(0, 5)


if __name__ == "__main__":
    main()
