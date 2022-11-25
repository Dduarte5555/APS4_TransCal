import numpy as np
from matplotlib import pyplot as plt

from .node import Node
from .tag import Tag


class Beam:
    id:int = None

    def __init__(self, node1: Node, node2: Node):
        self.node1 = node1
        self.node2 = node2

    @property
    def length(self):
        return self.node1.get_distance_from(self.node2)

    @property
    def angle(self):
        return self.node1.get_angle_from(self.node2)

    @property
    def sin_cos(self):
        dx = self.node2.x - self.node1.x
        dy = self.node2.y - self.node1.y
        l = np.sqrt(dx**2 + dy**2)

        return dy / l, dx / l

    @property
    def deformation(self):
        s, c = self.sin_cos
        vec = [-c, -s, c, s]
        pos = [self.node1.x, self.node1.y, self.node2.x, self.node2.y]

        return np.dot(vec, pos) / self.length

    @property
    def tension(self):
        return self.elasticity * self.deformation

    @property
    def rigidity(self):
        rigidity = self.elasticity * self.area / self.length
        s, c = self.sin_cos
        a = np.array([ [c, s, 0, 0],
                       [0, 0, c, s], ])
        b = np.array([ [1.0, -1.0],
                       [-1.0, 1.0], ])

        salkdjsad = np.matmul(a.T * rigidity,  b)

        return np.matmul(salkdjsad, a)

    def define_material(self, elasticity:float, area:float):
        self.elasticity = elasticity
        self.area = area

    def get_tag(self):
        return Tag(
            "elem",
            eid=self._id,
            shape="line2",
            nodes=f"{self.node1._id} {self.node2._id}",
            truss="true",
        )

    def plot(self, *args, **kwargs):
        mx = (self.node1.x + self.node2.x) / 2
        my = (self.node1.y + self.node2.y) / 2
        alpha = np.degrees(self.angle)

        if alpha < 0:
            alpha += 180

        plt.plot(
            [self.node1.x, self.node2.x], [self.node1.y, self.node2.y], *args, **kwargs
        )
        plt.text(
            mx,
            my,
            f"{self.length:.2f}",
            horizontalalignment="center",
            verticalalignment="center",
            rotation=alpha,
        )
