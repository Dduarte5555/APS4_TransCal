from .profe import importa
from .truss import Truss


class Loads:
    @staticmethod
    def execute(filename):
        nodes, beams, forces, restrictions = Loads._load(filename)
        solid = Truss()

        Loads._make_nodes(solid, nodes)
        Loads._make_beams(solid, beams)
        Loads._make_forces(solid, forces)
        Loads._make_restrictions(solid, restrictions)

        return solid

    @staticmethod
    def _load(filename):
        _, nodes, _, beams, _, forces, _, restrictions = importa(filename)

        return nodes, beams, forces, restrictions

    @staticmethod
    def _make_nodes(solid, nodes):
        for x, y in nodes.T:
            solid.make_node(x, y)

    @staticmethod
    def _make_beams(solid, beams):
        for node1_i, node2_i, elasticity, area in beams:
            node1 = solid.nodes[int(node1_i - 1)]
            node2 = solid.nodes[int(node2_i - 1)]

            beam = solid.make_beam(node1, node2)
            beam.define_material(elasticity, area)

    @staticmethod
    def _make_forces(solid, forces):
        forces = forces.T[0]

        for node_i, (fx, fy) in enumerate(zip(forces.T[::2], forces.T[1::2])):
            solid.nodes[node_i].apply_force(fx, fy)

    @staticmethod
    def _make_restrictions(solid, restrictions):
        for node_i, direction in enumerate(restrictions):
            node = solid.nodes[node_i]

            if direction in (1, 3):
                node.add_displacement_x()
            if direction in (2, 3):
                node.add_displacement_y()
