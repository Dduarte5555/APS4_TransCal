# from matplotlib import pyplot as plt


class Force():
    def __new__(self, x: float, y: float):
        self.x = x
        self.y = y

    # def plot(self, x0: float, y0: float):
    #     norm = np.linalg.norm((self.x, self.y))
    #     dx = self.x / norm
    #     dy = self.y / norm
    #     mx = x0 + dx / 2
    #     my = y0 + dy / 2
    #     angle = np.arctan2(dy, dx) - np.pi
    #     alpha = np.degrees(angle)

    #     plt.arrow(
    #         x0,
    #         y0,
    #         dx,  # type: ignore
    #         dy,  # type: ignore
    #         head_width=0.1,
    #         width=0.05,
    #     )

    #     if alpha < 0:
    #         alpha += 180

    #     plt.text(
    #         mx,  # type: ignore
    #         my,  # type: ignore
    #         f"{norm:.2f}",
    #         horizontalalignment="center",
    #         verticalalignment="center",
    #         rotation=alpha,
    #     )
