from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=30, filename="color_movie")
    s0 = Scene(obj=RectSceneObject(size=(0.2, 0.2), pos=(0.3, 0.6), color="#1050C0"))
    s0.actions.append(
        ChangeColorAction(
            duration=3.0, delay=0.1, color=(255, 20, 20), oscillate=True, rate=6
        )
    )
    s0.actions.append(MoveUpAction(duration=0.5, ease_in=False, offset=0.2))
    s0.actions.append(ScaleAction(duration=0.5, delay=0.5, scale=0.5))
    s0.actions.append(ScaleAction(duration=0.5, delay=1, scale=1.5))
    s0.actions.append(BlurAction(duration=0.75, delay=1.5, blur=25))
    s0.actions.append(BlurAction(duration=0.75, delay=2.25, blur=0))
    s0.buildout.append(FadeOutAction(duration=0.25))
    ms.add_scene(s0, start_time=0.25)

    ms.render_video(0, 5.5)


if __name__ == "__main__":
    main()
