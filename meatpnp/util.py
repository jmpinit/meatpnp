import numpy as np
from matplotlib import pyplot as plt


# https://stackoverflow.com/a/20555267
def solve_affine(p1, p2, p3, p4, s1, s2, s3, s4):
    primary = np.array([p1, p2, p3, p4])
    secondary = np.array([s1, s2, s3, s4])

    # n = primary.shape[0]
    def pad(x):
        return np.hstack([x, np.ones((x.shape[0], 1))])

    def unpad(x):
        return x[:, :-1]

    x = pad(primary)
    y = pad(secondary)

    # Solve the least squares problem X * A = Y
    # to find our transformation matrix A
    a, res, rank, s = np.linalg.lstsq(x, y, rcond=None)

    return lambda x: unpad(np.dot(pad(np.array([x])), a))[0]


def plot_parts(part_pos):
    x = part_pos['PosX'].to_numpy()
    y = part_pos['PosY'].to_numpy()

    plt.xlim([-40, 40])
    plt.ylim([-40, 40])
    plt.scatter(x, y)

    labels = part_pos['Ref'].to_numpy()

    for i, label in enumerate(labels):
        plt.annotate(label, (x[i], y[i]))

    plt.show()
