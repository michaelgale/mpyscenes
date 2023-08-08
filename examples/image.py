from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=30, filename="./movies/image_movie")
    obj = ImageSceneObject(
        filename="LogoColour512px.png", size=(0.2, 0.2), pos=(0.3, 0.6)
    )
    DropBuildInAction(obj=obj, end_at=0.75, duration=0.75)
    MoveUpAction(obj=obj, duration=0.5, ease_in=False, offset=0.3)
    ScaleAction(obj=obj, duration=0.5, delay=0.5, scale=0.5)
    ScaleAction(obj=obj, duration=0.5, delay=1, scale=1.5)
    BlurAction(obj=obj, duration=0.5, delay=1.5, blur=20)
    FadeBuildOutAction(obj=obj, duration=0.25)

    ms.add_sceneobject(obj, start_time=0.25)
    ms.render_video(0, 4, prores_alpha=True)


if __name__ == "__main__":
    main()
