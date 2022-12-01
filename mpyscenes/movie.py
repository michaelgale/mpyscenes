import subprocess as sp

from moviepy.editor import *

from toolbox import *
from mpyscenes import *
from .helpers import *


class Movie:
    """Top level class for managing objects and scenes for rendering into a movie."""

    def __init__(self, size=None, **kwargs):
        size = size_preset_tuple(size)
        if size is not None:
            self.size = size
        else:
            self.size = (1920, 1080)
        self.fps = 30
        self.bg_color = None
        self.filename = ""
        self.tempdir = "~/tmp/imagecache"
        self.codec = "libx264"
        self.clips = []
        self.objects = []
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v

    @property
    def width(self):
        return self.size[0]

    @width.setter
    def width(self, value):
        self.size[0] = value

    @property
    def height(self):
        return self.size[1]

    @height.setter
    def height(self, value):
        self.size[1] = value

    def add_object(self, obj):
        if isinstance(obj, list):
            objects = obj
        else:
            objects = [obj]
        for object in objects:
            self.objects.append(object)
            object.pixsize = self.size

    def add_scene(self, scene, start_time=0):
        scene.fps = self.fps
        scene.setup_scene(start_time=start_time)
        self.add_object(scene.obj)

    def _frame_filename(self, filename):
        if "." in filename:
            filename = filename.split(".")[0]
        filename = "%s_frame%%05d.png" % (filename)
        if self.tempdir is not None:
            filename = full_path(self.tempdir + os.sep + filename)
        return filename

    def render_video_frames(self, filename=None):
        """Generate individual PNG image files for each frame."""
        fn = filename if filename is not None else self.filename
        toolboxprint(
            "Rendering video frames %d x %d @ %d fps to %s"
            % (self.width, self.height, self.fps, fn),
            green_words=fn,
        )
        fn = self._frame_filename(fn)
        v = CompositeVideoClip(self.clips)
        v.write_images_sequence(fn, fps=self.fps, withmask=True, logger="bar")

    def render_video(self, filename=None, prores_alpha=False):
        """Renders final video file in either transparent ProRes4444 or mp4."""
        fn = filename if filename is not None else self.filename
        if prores_alpha:
            self.render_video_frames(filename=filename)
            fni = self._frame_filename(fn)
            fno = "%s.mov" % (fn)
            cmd = [
                "ffmpeg",
                "-y",
                "-r",
                "%d" % (self.fps),
                "-i",
                "%s" % (fni),
                "-c:v",
                "prores_ks",
                "-profile:v",
                "4",
                "-vendor",
                "apl0",
                "%s" % (fno),
            ]
            r = sp.run(cmd)
            if self.tempdir is not None:
                tmpdir = full_path(self.tempdir + os.sep)
                rmcmd = "rm %s*_frame*.png" % (tmpdir)
            else:
                rmcmd = "rm *_frame*.png"
            r = sp.run(rmcmd, shell=True)
            toolboxprint(
                "Video %d x %d @ %d fps encoded to ProRes4444 with alpha to %s"
                % (self.width, self.height, self.fps, fno),
                green_words=["ProRes4444", fno],
            )

        else:
            toolboxprint(
                "Rendering video %d x %d @ %d fps to %s"
                % (self.width, self.height, self.fps, fn),
                green_words=[fn],
            )
            if not fn.endswith(".mp4") and "libx264" in self.codec:
                fn = fn + ".mp4"
            v = CompositeVideoClip(self.clips)
            v.write_videofile(fn, fps=self.fps, codec=self.codec)

    def render_clips(self, tstart=0, tstop=0):
        """Generate clips for each frame within the specified time range."""
        self.clips = []

        # make a background fill for all clips if specified
        if self.bg_color is not None:
            bg = (
                ColorClip(
                    size=self.size, color=SceneObject.color_to_tuple(self.bg_color)
                )
                .set_start(tstart)
                .set_end(tstop)
            )
            self.clips.append(bg)
        fstart, fstop = int(tstart * self.fps), int(tstop * self.fps)

        # generate clips as required for each frame
        for i, frame in enumerate(range(fstart, fstop)):
            t0, t1 = frame / self.fps, (frame + 1) / self.fps
            toolboxprint(
                "Rendering frame %3d / %3d at frame %3d | time %.3f sec"
                % (i + 1, (fstop - fstart), frame, t0)
            )
            clip_count = 0
            for obj in self.objects:
                if not obj.is_mask:
                    clip = obj.get_clip_frame(frame, t0, t1)
                    if clip is not None:
                        self.clips.append(clip)
                        clip_count += 1
            if clip_count == 0:
                # dummy blank frame if no active clips in frame
                bg = ColorClip(size=self.size).set_start(t0).set_end(t1)
                bgm = ColorClip(size=self.size, ismask=True)
                bg = bg.set_mask(bgm).set_opacity(0)
                self.clips.append(bg)
