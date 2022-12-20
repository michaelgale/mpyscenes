from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=30, filename="./movies/text_movie")
    t0 = TextSceneObject(text="Hello", horz_align="center", color="#E05010", layer=1)
    t0.fontsize = 100
    t0.set_pos(0.35, 0.5)
    ms.add_object(t0)
    ms.render_video(0, 1, prores_alpha=False)


if __name__ == "__main__":
    main()
