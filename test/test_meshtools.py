import panairwrapper.mesh_tools as mt
import pytest
import numpy as np
import matplotlib.pyplot as plt


def test_meshcurvilinear():
    # setup boundaries
    x_lower = np.full((3, 2), 0.1)
    x_lower[:, 1] = np.array([0.2, .55, .9])
    x_upper = np.full((3, 2), 1.)
    x_upper[:, 1] = np.array([0., 0.5, 1.])
    y_lower = np.full((3, 2), 0.)
    y_lower[0, 1] = 0.2
    y_lower[:, 0] = np.array([0.1, 0.4, 1.])
    y_upper = np.full((3, 2), 1.)
    y_upper[0, 1] = 0.9
    y_upper[:, 0] = np.array([0.1, 0.4, 1.])

    # run test
    grid = mt.mesh_curvilinear(x_lower, x_upper, y_lower, y_upper)
    testgrid = np.array([[[0.1, 0.2],
                          [0.1, 0.55],
                          [0.1, 0.9]],
                         [[0.4, 0.],
                          [0.55, 0.5],
                          [0.4, 1.]],
                         [[1., 0.],
                          [1., 0.5],
                          [1., 1.]]])

    assert np.array_equal(grid, testgrid)


def test_meshparameterspace_nolimits():
    n_width = 5
    mesh_x, mesh_y = mt.meshparameterspace(shape=(n_width, n_width))
    spacing = np.linspace(0., 1., n_width)
    testmesh_x, testmesh_y = np.meshgrid(spacing, spacing, indexing='ij')

    assert np.array_equal(mesh_x, testmesh_x)
    assert np.array_equal(mesh_y, testmesh_y)


def test_meshparameterspace_etalimit():
    n_width = 3
    # create array for lower eta bound
    eta_min = np.zeros((n_width, 2))
    eta_min[:, 0] = np.linspace(0., 1., n_width)
    eta_min[:, 1] = np.linspace(0.2, .4, n_width)

    mesh_x, mesh_y = mt.meshparameterspace(shape=(n_width, n_width),
                                           eta_limits=(eta_min, None))

    print('mesh_x', mesh_x)
    print('mesh_y', mesh_y)
    testmesh = np.array([[[0., 0.2],
                          [0., 0.6],
                          [0., 1.]],
                         [[0.5, 0.3],
                          [0.5, 0.65],
                          [0.5, 1.]],
                         [[1., 0.4],
                          [1., 0.7],
                          [1., 1.]]])

    testmesh_x = np.array([[0., 0., 0.],
                           [0.5, 0.5, 0.5],
                           [1., 1., 1.]])
    testmesh_y = np.array([[0.2, 0.6, 1.],
                           [0.3, 0.65, 1.],
                           [0.4, 0.7, 1.]])

    assert np.allclose(mesh_x, testmesh_x, rtol=0., atol=1.e-15)
    assert np.allclose(mesh_y, testmesh_y, rtol=0., atol=1.e-15)


def test_cosinespacing():
    points = mt.cosine_spacing(.2, 1., 10)
    test_points = np.array([0.2, 0.22412295, 0.29358222, 0.4, 0.53054073,
                            0.66945927, 0.8, 0.90641778,  0.97587705, 1.])

    assert np.allclose(points, test_points, rtol=0., atol=1.e-7)
