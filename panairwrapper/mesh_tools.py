"""Turns a surface description into a panair network"""
import numpy as np
import sys
from math import sin, cos, sqrt
import panairwrapper.filehandling as fh


def axisymmetric_surf(data_x, data_r, N_theta):

    theta_start = np.pi  # radians
    theta_end = np.pi/2.  # radians

    data_t = np.linspace(theta_start, theta_end, N_theta)

    surf_coords = np.zeros([len(data_t), len(data_x), 3])

    for i, t in enumerate(data_t):
        for j, x in enumerate(data_x):
            surf_coords[i, j, 0] = x
            surf_coords[i, j, 1] = data_r[j]*sin(t)
            surf_coords[i, j, 2] = data_r[j]*cos(t)

    num_points = len(data_x)

    max_axial = 200
    num_network = int(num_points/max_axial)
    if not (num_points % max_axial) == 0:
        num_network += 1
    nn = int(num_points/num_network)

    network_list = []
    if num_network > 1:
        for i in range(num_network):
            if i == num_network-1:
                network_list.append(surf_coords[:, i*nn:])
            else:
                network_list.append(surf_coords[:, i*nn:(i+1)*nn+1])

    else:
        network_list.append(surf_coords)

    return network_list


def _distance_point_to_line(P1, P2, PQ):
    x0, y0 = PQ
    x1, y1 = P1
    x2, y2 = P2
    dy = y2-y1
    dx = x2-x1

    return abs(dy*x0-dx*y0+x2*y1-y2*x1)/sqrt(dy*dy+dx*dx)


def _calc_error(point_list):
    # calculates error if all points between endpoints of point_list
    # were removed.
    error = 0.
    front = point_list[0]
    back = point_list[-1]
    for i in range(1, len(point_list)-1):
        error += _distance_point_to_line(front, back, point_list[i])

    return error


def _calc_length(point_list):
    # calculates error if all points between endpoints of point_list
    # were removed.
    x_f, y_f = point_list[0]
    x_b, y_b = point_list[-1]

    length = sqrt((x_b-x_f)**2+(y_b-y_f)**2)

    return length


def coarsen_axi(data_x, data_r, tol, max_length):
    # move x and r data into a list of "points"
    point_list = []
    for i in range(len(data_x)):
        point_list.append(np.array([data_x[i], data_r[i]]))

    # ITERATIVE ALGORITHM
    # Indices for the start and end points of the algorithm
    Pstart = 0
    Pend = len(point_list)-1
    # Indices for 2 pointers that define current range being examined
    P1 = Pstart
    P2 = Pstart+2

    new_point_list = [point_list[Pstart]]

    while P2 <= Pend:
        error = _calc_error(point_list[P1:P2+1])

        if error > tol:
            new_point_list.extend(point_list[P1+1:P2+1])
            P1 = P2
            P2 = P1 + 2
        else:
            while error < tol and P2 <= Pend:
                P2 += 1
                error = _calc_error(point_list[P1:P2+1])
                cell_length = _calc_length(point_list[P1:P2+1])
                # print(cell_length)
                if cell_length > max_length:
                    error += tol*10.
            P2 -= 1
            new_point_list.append(point_list[P2])
            P1 = P2
            P2 = P1 + 2

    print("size of new list", len(new_point_list))
    sys.stdout.flush()
    new_x = np.zeros(len(new_point_list))
    new_r = np.zeros(len(new_point_list))
    for i in range(1, len(new_point_list)):
        new_x[i] = new_point_list[i][0]
        new_r[i] = new_point_list[i][1]

    return new_x, new_r
