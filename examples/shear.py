from moviepy.editor import *
from toolbox import *
from mpyscenes import *


def main():
    ms = Movie(size="720p", fps=30, filename="./movies/shear_movie")
    r0 = RectSceneObject(size=(0.4, 0.2), pos=(0.6, 0.6), color="#C01040")
    # r0 = TextSceneObject(text="hello", fontsize=100, pos=(0.6, 0.6))
    FlyInOutScene(obj=r0, start_from="left", fade_in=True, fade_out=False, shear=0.3)
    ms.add_sceneobject(r0, start_time=0.25)

    obj = ImageSceneObject(
        filename="LogoColour512px.png", size=(0.2, 0.2), pos=(0.3, 0.3)
    )
    obj.add_action(ShearXAction(duration=1.75, shear=0.2))
    ms.add_sceneobject(obj, start_time=0.1)

    obj2 = TextSceneObject(text="hello", fontsize=100, pos=(0.75, 0.75))
    obj2.add_action(ShearXAction(duration=1.75, shear=0.2))
    ms.add_sceneobject(obj2, start_time=0.1)

    ms.render_video(0, 4.5, prores_alpha=False)


if __name__ == "__main__":
    main()
