from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=30, filename="rect_movie")
    ms.add_object(RectSceneObject(size=(0.4, 0.2), pos=(0.6, 0.2), color="#801080"))
    ms.render_clips(0, 1)
    ms.render_video(prores_alpha=True)


if __name__ == "__main__":
    main()
