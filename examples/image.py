from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=30, filename="image_movie")
    s0 = Scene(
        obj=ImageSceneObject(
            filename="LogoColour512px.png", size=(0.2, 0.2), pos=(0.3, 0.6)
        )
    )
    s0.actions.append(MoveUpAction(duration=0.5, ease_in=False, offset=0.3))
    s0.actions.append(ScaleAction(duration=0.5, delay=0.5, scale=0.5))
    s0.actions.append(ScaleAction(duration=0.5, delay=1, scale=1.5))
    s0.actions.append(BlurAction(duration=0.5, delay=1.5, blur=20))
    s0.buildout.append(FadeOutAction(duration=0.25))
    ms.add_scene(s0, start_time=0.25)

    ms.render_video(0, 4, prores_alpha=True)


if __name__ == "__main__":
    main()
