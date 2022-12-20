from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=30, filename="./movies/flyinout_movie")
    t0 = TextSceneObject(text="Hello", horz_align="center", color="#E05010", layer=1)
    t0.fontsize = 100
    FlyInOutScene(obj=t0, fade_in=True, fade_out=False)
    t0.add_action(
        ChangeColorAction(duration=2.0, color=(20, 20, 225), oscillate=True, rate=6)
    )
    ms.add_sceneobject(t0, start_time=0.25)

    t1 = TextSceneObject(text="Goodbye", horz_align="center", color="#FFFFFF", layer=1)
    FlyInOutScene(
        obj=t1,
        start_from="top",
        duration=3.5,
        loc=0.8,
        fade_in=False,
        fade_out=True,
    )
    ms.add_sceneobject(t1, start_time=0.5)

    ms.render_video(0, 5, prores_alpha=False)


if __name__ == "__main__":
    main()
