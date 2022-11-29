from typing import List

import numpy as np

from .node import Node
from .beam import Beam
from .material import Material
from .tag import Tag


class Truss:
    nodes:List[Node]
    beams:List[Beam]
    material:Material

    def __init__(self):
        self.nodes = []
        self.beams = []
        self.material = None

    def add_node(self, node:Node):
        last_id = self.nodes[-1].id if len(self.nodes) > 0 else 0

        if node not in self.nodes:
            node.id = last_id + 1

            self.nodes.append(node)

    def add_beam(self, beam:Beam):
        last_id = self.beams[-1].id if len(self.beams) > 0 else 0

        if beam not in self.beams:
            beam.id = last_id + 1

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

    def set_material(self, material:Material):
        material.id = 1
        self.material = material

    def plot(self):
        for beam in self.beams:
            beam.plot(c="#888")

        for node in self.nodes:
            node.plot()

    def get_tag(self):
        tag = Tag("liml8")

        tag.append_tree([
            Tag("analysis", type="S20")
        ])
        tag.append_tree([
            node.get_tag()
            for node in self.nodes
        ])

        if self.material != None:
            material = self.material.get_set_tag()
            material.append_tree([
                beam.get_tag()
                for beam in self.beams
                if beam.material == None
            ])

            tag.append_child(material)
            tag.append_child(material.get_tag())
        
        for beam in self.beams:
            if beam.material != None:
                if self.material != None:
                    beam.material.id += 1

                tag.append_child(beam.get_tag())
                tag.append_child(beam.material.get_tag())

        return tag

    def to_string(self):
        return self.get_tag().to_string()
