import numpy as np
from PIL import Image, ImageDraw
from imageio import imread, imsave
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from moviepy.editor import *

from toolbox import *
from mpyscenes import *
from ..helpers import *


class LineSceneObject(SceneObject):
    def __init__(self, coords=None, **kwargs):
        self.stroke_width = 2
        self.aspect_correct = False
        super().__init__(**kwargs)
        self.coords = [coords]
        self.draw_anim = None
        self.draw_length = 0
        self.poly_lines = copy.deepcopy(coords)

    def pix_coords(self, coords=None):
        pc = []
        if coords is None:
            coords = self.poly_lines[0]
        for c in coords:
            r = self.pixsize[0] / self.pixsize[1] if self.aspect_correct else 1.0
            pc.append(self.pix_dim((c[0], r * c[1])))
        return pc

    @property
    def total_points(self):
        count = 0
        for poly_line in self.coords:
            count += len(poly_line)
        return count

    def translated_polylines(self, lines):
        return [translate_points(line, self.pos) for line in lines]

    def poly_line_lengths(self, lines):
        return [polyline_length(line) for line in lines]

    def poly_line_total_length(self, lines):
        return sum(self.poly_line_lengths(lines))

    def poly_line_vertex_count(self, lines):
        return sum([len(line) for line in lines])

    def update_poly_points(self, frame):
        if self.draw_anim is not None:
            self.draw_length = self.draw_anim[frame]
            tlines = self.translated_polylines(self.coords)
            all_points = max(self.draw_anim.frame_len, self.total_points)
            all_lines = []
            for line in tlines:
                pts = discretize_polyline(line, all_points)
                all_lines.append(pts)
            vtx_count = self.poly_line_vertex_count(all_lines)
            draw_count = int(math.ceil(self.draw_length * vtx_count))
            self.poly_lines = []
            count = 0
            for line in all_lines:
                pline = []
                for vtx in line:
                    if count < draw_count:
                        pline.append(vtx)
                        count += 1
                    else:
                        break
                self.poly_lines.append(pline)
                if count >= draw_count:
                    break
        else:
            self.poly_lines = [p for p in self.coords]

    def update_frame_pos(self, frame):
        if self.x_anim is not None:
            self.pos[0] = self.x_anim[frame]
        if self.y_anim is not None:
            self.pos[1] = self.y_anim[frame]

    def update_frame(self, frame):
        self.update_frame_pos(frame)
        self.update_frame_color(frame)
        self.update_frame_opacity(frame)
        self.update_frame_blur(frame)
        self.update_frame_scale(frame)
        self.update_frame_angle(frame)
        self.update_poly_points(frame)

    def get_clip_obj(self):
        pix = Image.new("RGBA", self.pix_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(pix)
        for line in self.poly_lines:
            draw.line(
                self.pix_coords(line),
                fill=(*self.color, 255),
                width=self.stroke_width,
                joint=["curve"],
            )
        pix = np.asarray(pix)
        self.clip_obj = ImageClip(pix, transparent=True, ismask=False)
        return self.clip_obj

    def get_clip_frame(self, frame, t0, t1):
        self.update_frame(frame)
        if not self.opacity > 0:
            return None
        clip = (
            self.get_clip_obj()
            .set_opacity(self.opacity)
            .set_start(t0)
            .set_end(t1)
            .set_layer(self.layer)
        )
        return clip


class TextLineSceneObject(LineSceneObject):
    def __init__(self, text=None, **kwargs):
        self.aspect_correct = True
        self.font_family = "DIN"
        self.font_size = 0.1
        super().__init__(**kwargs)

        prop = FontProperties(family=self.font_family)
        path = TextPath((0, 0), text, size=self.font_size, prop=prop)
        path = path.cleaned()
        self.coords = []
        line = []
        for p, c in zip(path.vertices, path.codes):
            if c == path.MOVETO:
                line = [(p[0], -p[1])]
            elif c == path.LINETO:
                line.append((p[0], -p[1]))
            elif c == path.CLOSEPOLY:
                line.append(line[0])
                self.coords.append(line)
