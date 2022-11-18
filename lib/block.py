# from typing import List

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

# from .node import Node


class Block:
    # nodes:List[Node]

    def __init__(self, origin, width, height):
        # self.nodes:List[Node] = []
        self.x, self.y = origin
        self.width = width
        self.height = height


    def plot(self):
        block = Rectangle((self.x, self.y), self.width, self.height, color="#BBB")
        
        plt.axes().add_patch(block)

