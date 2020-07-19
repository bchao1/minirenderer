import numpy as np 

from .canvas import WireframeCanvas
from .parser import WireframeParser
from . import geometry
from . import colors

class WireframeRenderer:
    def __init__(self,
        imsize=1000,
        fg_color=colors.WHITE,
        bg_color=colors.WHITE
    ):
        self.parser = WireframeParser()

        self.imsize = imsize
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.canvas = None
    
    def rescale(self, c, c_range):
        cmin, cmax = c_range
        return 1.0 * self.scale * (c - cmin)
    
    def get_scale(self, x_range, y_range):
        dx = geometry.dist(x_range)
        dy = geometry.dist(y_range)
        sz = max(dx, dy)
        scale = 1.0 * self.imsize / sz
        return scale

    def readfile(self, infile):
        self.parser.readfile(infile)

    def adjust_camera(self, camera, center, up):
        self.parser.adjust_camera(camera, center, up)

    def render(self, mode, camera, center, up):
        # compute camera coordinates

        self.adjust_camera(camera, center, up)
        self.scale = self.get_scale(self.parser.x_range, self.parser.y_range)
        self.canvas_size = self.parser.get_canvas_size(self.scale)
        self.canvas = WireframeCanvas(self.canvas_size, self.fg_color, self.bg_color)
        
        light_dir = np.array([0, 0, 1]) # light direction, into the frame
        for f in self.parser.faces:
            f_canvas = []  # face coordinates to draw on canvas
            n = f.normal  # compute normal vector of face
            I = np.dot(n, light_dir)  # compute color intensity of polygons
            for vid in f.vids:
                x, y = self.parser.vertices[vid].coor2D  # world coordinates
                x_canvas = self.rescale(x, self.parser.x_range)  # transform to canvas coordinates
                y_canvas = self.rescale(y, self.parser.y_range)
                f_canvas.append((x_canvas, y_canvas))
            if mode == 'wireframe':
                self.canvas.drawpoly(f_canvas, outline=colors.BLACK)
            elif mode == 'triangle':
                self.canvas.drawpoly(f_canvas, fill=colors.color_grad(colors.WHITE, I))
        
        self.canvas.postprocess()
        return self.canvas