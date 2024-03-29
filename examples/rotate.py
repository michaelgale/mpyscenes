from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=60, filename="./movies/rotate_movie")
    img = ImageSceneObject(
        filename="LogoColour512px.png", size=(0.2, 0.2), pos=(0.3, 0.6), angle=45
    )
    img.add_action(MoveUpAction(duration=0.5, ease_in=False, offset=0.3))
    img.add_action(ScaleAction(duration=0.5, delay=0.5, scale=0.5))
    img.add_buildout(FadeBuildOutAction(duration=0.25))
    ms.add_sceneobject(img, start_time=0.25)

    t0 = TextSceneObject(text="Hello", horz_align="center", color="#E05010", layer=1)
    t0.fontsize = 100
    t0.angle = 180
    t0.set_pos(0.65, 0.3)
    t0.add_action(ScaleAction(duration=0.5, scale=0.75))
    t0.add_action(MoveDownAction(duration=1.5, delay=0, offset=0.3))
    t0.add_action(RotateAction(duration=1, delay=0.5, angle=0))
    t0.add_buildout(FadeBuildOutAction(duration=0.25))
    ms.add_sceneobject(t0, start_time=0.15)

    r0 = RectSceneObject(size=(0.1, 0.2), pos=(0.5, 0.5), color="#801080")
    r0.add_action(RotateAction(duration=1, delay=0.25, angle=180))
    ms.add_sceneobject(r0, start_time=0)

    ms.render_video(0, 3, prores_alpha=False)


if __name__ == "__main__":
    main()
