from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=30, filename="flyinout_movie")
    t0 = TextSceneObject(text="Hello", horz_align="center", color="#E05010", layer=1)
    t0.fontsize = 100
    s0 = FlyInOutScene(obj=t0, fade_in=True, fade_out=False)
    ms.add_scene(s0, start_time=0.25)

    ms.add_scene(
        FlyInOutScene(
            obj=TextSceneObject(
                text="Goodbye", horz_align="center", color="#FFFFFF", layer=1
            ),
            start_from="top",
            duration=3.5,
            loc=0.8,
            fade_in=False,
            fade_out=True,
        ),
        start_time=0.5,
    )

    ms.render_clips(0, 5)
    ms.render_video(prores_alpha=True)


if __name__ == "__main__":
    main()
