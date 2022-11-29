import numpy as np

from .truss import Truss
from .method import Method


class Solver:
    mask:np.ndarray
    mask_:np.ndarray
    rigidity:np.ndarray
    forces:np.ndarray
    displacement:np.ndarray
    internal_deformation:np.ndarray
    internal_tension:np.ndarray
    internal_forces:np.ndarray

    def __init__(self, truss:Truss):
        self.truss = truss
    
    def execute(self, method:Method, tol:float):
        self._execute_rigidity()
        self._execute_mask()
        self._execute_forces()
        self._execute_displacement(method, tol)
        self._execute_reactions()
        self._execute_internal_deformation()
        self._execute_internal_tension()
        self._execute_internal_force()

    def get_reactions(self):
        return self.forces[self.mask]

    def _execute_mask(self):
        self.mask = np.array([node.displacement.get_axis() for node in self.truss.nodes]).flatten()
        self.mask_ = np.bitwise_not(self.mask)

    def _execute_rigidity(self):
        size = len(self.truss.nodes)
        K = np.zeros((size * 2, size * 2))

        for beam in self.truss.beams:
            Ke = beam.rigidity
            i1 = (beam.node1.id - 1) * 2
            i2 = (beam.node2.id - 1) * 2

            K[i1:i1+2, i1:i1+2] += Ke[0:2, 0:2]
            K[i1:i1+2, i2:i2+2] += Ke[0:2, 2:4]
            K[i2:i2+2, i1:i1+2] += Ke[2:4, 0:2]
            K[i2:i2+2, i2:i2+2] += Ke[2:4, 2:4]

        self.rigidity = K

    def _get_masked_rigidity(self, mask):
        return self.rigidity[mask][:, mask]

    def _execute_forces(self):
        F = []

        for node in self.truss.nodes:
            r = node.get_resultant_force()

            F.append(r.x)
            F.append(r.y)

        self.forces = np.array(F)

    def _execute_displacement(self, method, tol:float):
        u = np.zeros(self.rigidity.shape[1])

        u[self.mask_] = method.solve(
            k = self._get_masked_rigidity(self.mask_),
            y = self.forces[self.mask_],
            tol = tol
        )

        self.displacement = u

    def _execute_reactions(self):
        self.forces[self.mask] = np.matmul(self.rigidity, self.displacement)[self.mask]

    def _execute_internal_deformation(self):
        deformations = []

        for beam in self.truss.beams:
            i1 = (beam.node1.id - 1) * 2
            i2 = (beam.node2.id - 1) * 2
            u1 = self.displacement[i1:i1+2]
            u2 = self.displacement[i2:i2+2]
            deformation = beam.get_deformation(u1, u2)

            deformations.append(deformation)

        self.internal_deformation = np.array(deformations)

    def _execute_internal_tension(self):
        tensions = []

        for deformation, beam in zip(self.internal_deformation, self.truss.beams):
            tension = deformation * beam.material.elasticity

            tensions.append(tension)

        self.internal_tension = np.array(tensions)

    def _execute_internal_force(self):
        forces = []

        for tension, beam in zip(self.internal_tension, self.truss.beams):
            force = tension * beam.material.area

            forces.append(force)

        self.internal_forces = np.array(forces)
