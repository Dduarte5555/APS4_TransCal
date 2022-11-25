from typing import List

import numpy as np
from matplotlib import pyplot as plt

from .force import Force
from .displacement import Displacement
from .tag import Tag


class Node:
    id:int
    x:float
    y:float
    forces:List[Force]
    displacement:Displacement

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.forces = []
        self.displacement = Displacement()

    def get_distance_from(self, node):
        return np.hypot(self.x - node.x, self.y - node.y)

    def get_angle_from(self, node):
        dx = self.x - node.x
        dy = self.y - node.y

        return np.arctan2(dy, dx) - np.pi

    def rotate_by(self, theta: float, origin):
        x = self.x - origin.x
        y = self.y - origin.y

        self.x = origin.x + x * np.cos(theta) - y * np.sin(theta)
        self.y = origin.y + x * np.sin(theta) + y * np.cos(theta)

        return self

    def add_force(self, force:Force):
        if force not in self.forces:
            self.forces.append(force)

    def apply_force(self, x:float, y:float):
        force = Force(x, y)

        self.add_force(force)

        return force

    def get_resultant_force(self):
        Rx = 0
        Ry = 0

        for force in self.forces:
            Rx += force.x
            Ry += force.y

        return Force(Rx, Ry)

    def get_tag(self):
        tag = Tag("node", nid=self.id, x=self.x, y=self.y, z=0)

        return tag

    def get_selection_tag(self):
        return

    def plot(self):
        plt.scatter([self.x], [self.y])

        # for force in self.forces:
        #     force.plot(self.x, self.y)

#   <nodeselection name="Unnamed(6)">
#     <node nid="16" />
#   </nodeselection>