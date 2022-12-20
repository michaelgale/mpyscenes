from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=60, filename="./movies/fade_movie")
    r0 = RectSceneObject(size=(0.4, 0.2), pos=(0.6, 0.6), color="#C01040")
    FadeBuildInAction(obj=r0, duration=0.5)
    r0.add_action(NoAction(duration=0.75))
    FadeBuildOutAction(obj=r0, duration=0.25)
    ms.add_sceneobject(r0, start_time=0.25)

    ms.render_video(0, 2)


if __name__ == "__main__":
    main()
