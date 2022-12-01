from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=60, filename="fade_movie")
    r0 = RectSceneObject(size=(0.4, 0.2), color="#C01040")
    r0.set_pos(0.6, 0.6)
    s0 = Scene(obj=r0, fps=ms.fps)
    s0.buildin.append(FadeInAction(duration=0.5, fps=ms.fps))
    s0.actions.append(SceneAction(duration=0.75, fps=ms.fps))
    s0.buildout.append(FadeOutAction(duration=0.25, fps=ms.fps))
    ms.add_scene(s0, start_time=0.25)

    ms.render_clips(0, 2)
    ms.render_video(prores_alpha=True)


if __name__ == "__main__":
    main()
