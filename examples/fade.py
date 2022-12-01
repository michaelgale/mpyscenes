from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=60, filename="fade_movie")
    s0 = Scene(obj=RectSceneObject(size=(0.4, 0.2), pos=(0.6, 0.6), color="#C01040"))
    s0.buildin.append(FadeInAction(duration=0.5))
    s0.actions.append(NoAction(duration=0.75))
    s0.buildout.append(FadeOutAction(duration=0.25))
    ms.add_scene(s0, start_time=0.25)

    ms.render_video(0, 2)


if __name__ == "__main__":
    main()
