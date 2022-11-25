import numpy as np


class Solver:
    @staticmethod
    def _get_err(x, xi):
        return np.abs((xi - x) / xi)


class GaussSeidel_Solver(Solver):
    @staticmethod
    def solve(k:np.ndarray, y:np.ndarray, tol:float=1e-10):
        x = np.zeros_like(y, dtype=np.float64)
        conv = [False] * y.shape[0]

        i = -1
        try:
            while not all(conv):
                i = (i + 1) % x.shape[0]

                if conv[i]:
                    continue

                xi = GaussSeidel_Solver._xi(k, x, y, i)

                if Solver._get_err(x[i], xi) < tol:
                    conv[i] = True

                x[i] = xi
        except KeyboardInterrupt:
            pass

        return x

    @staticmethod
    def _xi (k, x, y, i):
        return (y[i] - (k[i, :].dot(x) - k[i, i] * x[i])) / k[i, i]


if __name__ == "__main__":
    a = np.array([
        [ 1.59, -0.40, -0.54],
        [-0.40,  1.70,  0.40],
        [-0.54,  0.40,  0.54]
    ]) * 1e8

    b = np.array([
        0, 150, -100
    ])

    u = GaussSeidel_Solver.solve(a, b)

    print(u.round(8))
