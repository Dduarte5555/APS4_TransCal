import numpy as np

from .tag import Tag


class Material:
    id:int
    elasticity:float
    area:float
    name:str

    def __init__(self, elasticity:float, area:float, name="Default"):
        self.elasticity = elasticity
        self.area = area
        self.name = name

    def get_rigidity(self, length:float):
        return self.elasticity * self.area / length

    def get_tag(self):
        side = np.sqrt(self.area)
        tag = Tag("mat", mid=self.id, name=self.name)
        
        tag.append_tree([
            Tag("geometric", type="RectBar", recta=side, rectb=side),
            Tag("mechanical", type="Isotropic", youngsmodulus=self.elasticity),
        ])

        return tag

    def get_set_tag(self):
        return Tag("elset", material=self.name,  color=-6710887, name="")
