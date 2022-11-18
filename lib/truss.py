from typing import List

import numpy as np

from .node import Node
from .beam import Beam
from .tag import Tag


class Truss:
    nodes:List[Node]
    beams:List[Beam]

    def __init__(self):
        self.nodes = []
        self.beams = []

    @property
    def rigidity(self):
        size = len(self.nodes)
        K = np.zeros((size * 2, size * 2))

        for beam in self.beams:
            Ke = beam.rigidity
            i1 = beam.node1.id - 1
            i2 = beam.node2.id - 1

            K[i1:i1+2, i1:i1+2] += Ke[0:2, 0:2]
            K[i1:i1+2, i2:i2+2] += Ke[0:2, 2:4]
            K[i2:i2+2, i1:i1+2] += Ke[2:4, 0:2]
            K[i2:i2+2, i2:i2+2] += Ke[2:4, 2:4]

        return K

    def add_node(self, node:Node):
        last_id = self.nodes[-1].id if len(self.nodes) > 0 else 0

        if node not in self.nodes:
            node.id = last_id + 1

            self.nodes.append(node)

    def add_beam(self, beam:Beam):
        if beam not in self.beams:
            self.add_node(beam.node1)
            self.add_node(beam.node2)
            self.beams.append(beam)

    def add_truss(self, truss):
        for node in truss.nodes:
            self.add_node(node)

        for beam in truss.beams:
            self.add_beam(beam)

    def make_node(self, x:float, y:float):
        node = Node(x, y)

        self.add_node(node)

        return node

    def make_beam(self, node1:Node, node2:Node):
        beam = Beam(node1, node2)

        self.add_beam(beam)

        return beam

    def solve(self):
        pass

    def plot(self):
        for beam in self.beams:
            beam.plot(c="#888")

        for node in self.nodes:
            node.plot()

    def to_string(self):
        self.update()

        return Tag("liml8").append_tree([
            Tag("analysis", type="S20"),

            *(
                node.get_tag() for node in self.nodes
            ),

            Tag("elset", name="Default", color="-6710887", material="Material").append_tree([
                beam.get_tag() for beam in self.beams
            ]),

            Tag("mat", mid=1, name="Material").append_tree([
                Tag("geometric", type="RectBar", recta=self.beam_width, rectb=self.beam_thickness),
                Tag("mechanical", type="Isotropic"),
            ]),
        ]).to_string()
