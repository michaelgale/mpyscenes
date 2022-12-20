from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=30, filename="line_movie")
    coords = [
        (0.25, 0.25),
        (0.75, 0.25),
        (0.75, 0.75),
        (0.25, 0.25),
    ]
    line = LineSceneObject(
        coords=coords, color="#1990FF", stroke_width=5, pos=(0.2, -0.1), opacity=0
    )
    line.add_action(FadeInAction(duration=1))
    line.add_action([DrawAction(duration=1.0), DrawAction(duration=1.0, length=0.25)])
    line.add_buildout(FadeOutAction(duration=0.5))
    ms.add_sceneobject(line, start_time=0.25)
    text = TextLineSceneObject(
        text="Hello", pos=(0.5, 0.5), stroke_width=3, color="#E06010"
    )
    text.add_action([DrawAction(duration=2)])
    ms.add_sceneobject(text, start_time=0)

    ms.render_video(0, 3, prores_alpha=True)


if __name__ == "__main__":
    main()
