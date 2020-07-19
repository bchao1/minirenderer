import math
import numpy as np
import geometry

class WireframeParser:
    def __init__(self):
        pass
        
    def readfile(self, filename):
        self._vertices = {}
        self._faces = []
        self.coors = []

        with open(filename, 'r') as file:
            for line in file:
                if not line.strip():
                    continue
                line = line.strip().split(' ')
                line = [s for s in line if len(s) > 0]
                if line[0] == 'v':
                    coor = [float(c) for c in line[1:]] # x, y, z coordinates
                    coor.append(1) # dummy 4-th dimension
                    self.coors.append(coor)
                elif line[0] == 'f':
                    vs = [int(v.split('/')[0]) for v in line[1:]]
                    f = geometry.Face(vs)
                    self._faces.append(f)
        self.coors = np.stack(self.coors) # raw coordinates
    
    def adjust_camera(self, camera, center, up):
        view = geometry.lookAt(camera, center, up)
        print(view)
        self.camera_coors = np.transpose(np.matmul(view, np.transpose(self.coors)))
        print(self.camera_coors.shape)

        self._min_x, self._min_y = math.inf, math.inf
        self._max_x, self._max_y = -math.inf, -math.inf
        for i, coor in enumerate(self.camera_coors):
            vid = i + 1
            v = geometry.Vertex(*coor[:-1], vid)
            self._vertices[vid] = v
            self._min_x, self._max_x = min(self._min_x, v.x), max(self._max_x, v.x)
            self._min_y, self._max_y = min(self._min_y, v.y), max(self._max_y, v.y)
        geometry.Face._vertices = self._vertices
        self.faces.sort(key = lambda f: f.zmean)

    @property
    def vertices(self):
        return self._vertices
    
    @property
    def faces(self):
        return self._faces

    @property
    def x_range(self):
        return (self._min_x, self._max_x)
    
    @property
    def y_range(self):
        return (self._min_y, self._max_y)
    
    def get_canvas_size(self, scale):
        def d(t):
            return t[1] - t[0]
        return (int(scale * d(self.x_range)), int(scale * d(self.y_range)))


def test():
    wf = WireframeParser()
    wf.readfile('../examples/airboat.obj')
    print(wf.y_range)

if __name__ == '__main__':
    test()