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
    def c(self):
        return self._c 
    
    @property
    def id(self):
        return self._id
    
    @property
    def coor2D(self):
        return (self._x, self._y)
    
    @property
    def coor3D(self):
        return (self._x, self._y, self._z)
    
    def perspective2D(self, c):
        """ 
            c is the camera z position (in pixels).
            Default use coor2D where c = inf.
        """
        return (self.x/(1-self.z/c), self.y/(1-self.z/c))
    
    def __sub__(self, v):
        return np.subtract(self.coor3D, v.coor3D)


class Face:
    _vertices = None

    def __init__(self, vids):
        self._vids = vids
    
    @property
    def vids(self):
        return self._vids
    
    @property
    def zmean(self):
        """ Simple wrap-around for painter's algorithm """
        return np.mean([self._vertices[vid].z for vid in self._vids])
    
    @property
    def normal(self):
        v0 = self._vertices[self._vids[0]]
        v1 = self._vertices[self._vids[1]]
        v2 = self._vertices[self._vids[2]]

        l0 = v1 - v0
        l1 = v2 - v0
        n = np.cross(l0, l1)
        norm = np.sqrt(np.sum(n ** 2)) + 1e-20 # guard
        return n / norm


def dist(t):
    return t[1] - t[0]

def normalize(v):
    norm = np.sqrt(np.sum(v ** 2)) + 1e-20
    return v / norm

def lookAt(camera, center, up):
    camera = np.array(camera)
    center = np.array(center)
    up = np.array(up)

    z = normalize(camera - center)
    x = normalize(np.cross(up, z))
    y = normalize(np.cross(z, x))

    m_inv = np.eye(4)
    tr = np.eye(4)
    for i in range(3):
        m_inv[0][i] = x[i]
        m_inv[1][i] = y[i]
        m_inv[2][i] = z[i]
        tr[i][3] = -center[i]
    return np.matmul(m_inv, tr)


if __name__ == '__main__':
    v = Vertex(0, 0, 0, 0)
    