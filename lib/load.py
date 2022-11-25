from .profe import importa
from .truss import Truss
from .material import Material


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
            node1_i = int(node1_i - 1)
            node2_i = int(node2_i - 1)

            Loads._make_beam(solid, node1_i, node2_i, elasticity, area)

    @staticmethod
    def _make_beam(solid, node1_i, node2_i, elasticity, area):
        node1 = solid.nodes[node1_i]
        node2 = solid.nodes[node2_i]

        beam = solid.make_beam(node1, node2)
        material = Material(elasticity, area, str(beam.id))
        beam.set_material(material)

    @staticmethod
    def _make_forces(solid, forces):
        for node, fx, fy in Loads._get_forces(solid, forces):
            node.apply_force(fx, fy)

    @staticmethod
    def _get_forces(solid, forces):
        forces_ = forces.T[0]
        zip_xy = zip(forces_.T[::2], forces_.T[1::2])

        return ((solid.nodes[node_i], fx, fy) for node_i, (fx, fy) in enumerate(zip_xy))

    @staticmethod
    def _make_restrictions(solid, restrictions):
        for restriction in Loads._get_restrictions(restrictions):
            node_i = restriction // 2
            node = solid.nodes[node_i]

            if restriction % 2 == 0:
                node.displacement.set_x()
            else:
                node.displacement.set_y()

    @staticmethod
    def _get_restrictions(restrictions):
        return (int(restriction) for restriction in restrictions.T[0])
