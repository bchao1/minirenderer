import numpy as np

class Vertex:
    def __init__(self, x, y, z, id):
        self._x = x
        self._y = y
        self._z = z
        self._id = id
    
    @property
    def x(self):
        return self._x 
    
    @property
    def y(self):
        return self._y 
    
    @property
    def z(self):
        return self._z

    @property
    def id(self):
        return self._id
    
    @property
    def coor2D(self):
        return (self._x, self._y)
    
    @property
    def coor3D(self):
        return (self._x, self._y, self._z)
    
    def __sub__(self, v):
        return np.subtract(self.coor3D, v.coor3D)
    

class Vector3D:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

class Face:
    def __init__(self, vids):
        self._vids = vids
    
    @property
    def vids(self):
        return self._vids
    
    def normal(self, vertices):
        v0 = vertices[self._vids[0]]
        v1 = vertices[self._vids[1]]
        v2 = vertices[self._vids[2]]

        l0 = v1 - v0
        l1 = v2 - v0
        n = np.cross(l0, l1)
        norm = np.sqrt(np.sum(n ** 2)) + 1e-20 # guard
        return n / norm


def dist(t):
    return t[1] - t[0]

if __name__ == '__main__':
    v = Vertex(0, 0, 0, 0)
    