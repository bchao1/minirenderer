import math
from geometry import Vertex, Face

class WireframeParser:
    def __init__(self):
        pass
        
    def readfile(self, filename):
        self._vertices = {}
        self._faces = []
        self._min_x, self._min_y = math.inf, math.inf
        self._max_x, self._max_y = -math.inf, -math.inf

        with open(filename, 'r') as file:
            for line in file:
                if not line.strip():
                    continue
                line = line.strip().split(' ')
                line = [s for s in line if len(s) > 0]
                if line[0] == 'v':
                    coors = [float(c) for c in line[1:]]
                    vid = len(self._vertices) + 1
                    v = Vertex(*coors, vid)
                    self._vertices[vid] = v
                    self._min_x, self._max_x = min(self._min_x, v.x), max(self._max_x, v.x)
                    self._min_y, self._max_y = min(self._min_y, v.y), max(self._max_y, v.y)
                elif line[0] == 'f':
                    Face._vertices = self._vertices
                    vs = [int(v.split('/')[0]) for v in line[1:]]
                    f = Face(vs)
                    self._faces.append(f)
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
    
    def get_imsize(self, scale):
        def d(t):
            return t[1] - t[0]
        return (int(scale * d(self.x_range)), int(scale * d(self.y_range)))


def test():
    wf = WireframeParser()
    wf.readfile('../examples/airboat.obj')
    print(wf.y_range)

if __name__ == '__main__':
    test()