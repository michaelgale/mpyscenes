from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=60, filename="./movies/bounce_movie")
    t0 = TextSceneObject(text="Hello", horz_align="center", color="#E05010", layer=1)
    t0.fontsize = 100
    # DropBuildInAction(obj=t0, duration=0.5, end_at=0.8)
    BounceBuildInAction(
        obj=t0, duration=4, damping=0.4, loc=0.8, start_from="right", end_at=0.2
    )
    r0 = RectSceneObject(size=(0.2, 0.05), color="#1020C0")
    r1 = RectSceneObject(size=(0.1, 0.1), color="#E020C0")
    r2 = RectSceneObject(size=(0.1, 0.35), color="#30D020")

    BounceBuildInAction(
        obj=r0, damping=0.5, loc=0.4, squash=0.4, start_from="left", end_at=0.8
    )
    BounceBuildInAction(obj=r1, loc=0.6, start_from="bottom", end_at=0.5)
    BounceBuildInAction(
        obj=r2,
        damping=0.6,
        bounces=5,
        squash=0.333,
        loc=0.3,
        end_at=0.8 - r2.height / 2,
    )
    ms.add_sceneobject(r2)
    ms.add_sceneobject(r1, start_time=0.5)
    ms.add_sceneobject(r0, start_time=0.75)
    # FlyInOutScene(obj=t0, fade_in=True, fade_out=False)
    # t0.add_action(
    #     ChangeColorAction(duration=2.0, color=(20, 20, 225), oscillate=True, rate=6)
    # )
    ms.add_sceneobject(t0, start_time=0.25)

    ms.render_video(0, 3, prores_alpha=False)


if __name__ == "__main__":
    main()
