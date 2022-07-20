from meatpnp.util import solve_affine


def test_affine():
    hole_to_hole = 54.09  # mm
    p1 = (0, 0, 0)
    p2 = (10, 0, 0)
    p3 = (0, 10, 0)
    p4 = (10, 10, 0)
    s1 = (0, 0, 0)
    s2 = (1, 0, 0)
    s3 = (0, 1, 0)
    s4 = (1, 1, 0)
    t = solve_affine(p1, p2, p3, p4, s1, s2, s3, s4)
    # print(t(np.array([(5, 5, 0)])))
    print(t((5, 5, 0)))


if __name__ == '__main__':
    test_affine()
