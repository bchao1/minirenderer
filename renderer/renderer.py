import numpy as np 

from canvas import WireframeCanvas
from parser import WireframeParser
import geometry
import colors

class WireframeRenderer:
    def __init__(self,
        imsize=1000,
        fg_color=colors.WHITE,
        bg_color=colors.WHITE,
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

    def render(self, filename):
        self.parser.readfile(filename)
        self.scale = self.get_scale(self.parser.x_range, self.parser.y_range)
        self.imsize = self.parser.get_imsize(self.scale)
        self.canvas = WireframeCanvas(self.imsize, self.fg_color, self.bg_color)
        
        light_dir = np.array([0, 0, 1]) # light direction
        for f in self.parser.faces:
            f_canvas = []  # face coordinates to draw on canvas
            n = f.normal  # compute normal vector of face
            I = np.dot(n, light_dir)  # compute color intensity of polygons
            for vid in f.vids:
                x, y = self.parser.vertices[vid].coor2D  # world coordinates
                x_canvas = self.rescale(x, self.parser.x_range)  # transform to canvas coordinates
                y_canvas = self.rescale(y, self.parser.y_range)
                f_canvas.append((x_canvas, y_canvas))
            self.canvas.drawpoly(f_canvas, fill=colors.color_grad(colors.WHITE, I))
        self.canvas.verticalFlip()
        self.canvas.save('../images/bunny.png')
        self.canvas.show()
        print(self.canvas.size)
        self.canvas.close()


if __name__ == '__main__':
    path = '../examples/bunny.obj'
    wf = WireframeRenderer()
    wf.render(path)



