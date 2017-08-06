#!/usr/bin/env python3
import numpy
import random
import matplotlib.pyplot as plt

def cubic_spline(p_0, p_1, p_2, p_3):
    t = numpy.arange(0.0, 1.0, 0.01)
    x = (1 - t)**3 * p_0[0] + 3*(1 - t)**2 * t * p_1[0] + \
        3 * (1 - t) * t**2 * p_2[0] + t**3 * p_3[0]
    y = (1 - t)**3 * p_0[1] + 3*(1 - t)**2 * t * p_1[1] + \
        3 * (1 - t) * t**2 * p_2[1] + t**3 * p_3[1]
    return x, y

def get_control_points(point_center, angle_min, angle_max, r_min, r_max):
    angle = random.uniform(angle_min, angle_max)
    r_a = random.uniform(r_min, r_max)
    r_b = random.uniform(r_min, r_max)
    control_point_a = (point_center[0] - r_a*numpy.cos(angle),
                       point_center[1] - r_a*numpy.sin(angle))
    control_point_b = (point_center[0] + r_b*numpy.cos(angle),
                       point_center[1] + r_b*numpy.sin(angle))
    return control_point_a, control_point_b

def puzzle_edge():
    # start and end points
    point_start = (0.0, 0.0)
    point_end = (1, 0)

    # define control points for approaching start and approaching end
    point_start_b = (0.3, 0.0)
    point_end_a = (0.7, 0)

    # define points what the curve will pass through
    point_0 = (random.uniform(0.3, 0.4), random.uniform(0.05, 0.15))
    point_1 = (random.uniform(0.2, 0.3), random.uniform(0.2, 0.3))
    point_2 = (random.uniform(0.7, 0.8), random.uniform(0.2, 0.3))
    point_3 = (random.uniform(0.6, 0.7), random.uniform(0.05, 0.15))

    # define control points before and after each passthrough point
    point_0_a, point_0_b = get_control_points(
        point_0,
        numpy.pi/4 - 0.1, numpy.pi/4 + 0.1,
        0.05, 0.15
    )
    point_1_a, point_1_b = get_control_points(
        point_1,
        numpy.pi/4 - 0.1, numpy.pi/4 + 0.1,
        0.05, 0.15
    )
    point_2_a, point_2_b = get_control_points(
        point_2,
        -numpy.pi/4 - 0.1, -numpy.pi/4 + 0.1,
        0.05, 0.15
    )
    point_3_a, point_3_b = get_control_points(
        point_3,
        -numpy.pi/4 - 0.1, -numpy.pi/4 + 0.1,
        0.05, 0.15
    )

    # initialize parallel x and y arrays
    x, y = numpy.array([]), numpy.array([])

    # generate the 5 segments and append them
    spline_0_x, spline_0_y = cubic_spline(
        point_start, point_start_b, point_0_a, point_0)
    spline_1_x, spline_1_y = cubic_spline(
        point_0, point_0_b, point_1_a, point_1)
    spline_2_x, spline_2_y = cubic_spline(
        point_1, point_1_b, point_2_a, point_2)
    spline_3_x, spline_3_y = cubic_spline(
        point_2, point_2_b, point_3_a, point_3)
    spline_4_x, spline_4_y = cubic_spline(
        point_3, point_3_b, point_end_a, point_end)
    x, y = numpy.append(x, spline_0_x), numpy.append(y, spline_0_y)
    x, y = numpy.append(x, spline_1_x), numpy.append(y, spline_1_y)
    x, y = numpy.append(x, spline_2_x), numpy.append(y, spline_2_y)
    x, y = numpy.append(x, spline_3_x), numpy.append(y, spline_3_y)
    x, y = numpy.append(x, spline_4_x), numpy.append(y, spline_4_y)

    return x, y

def puzzle_piece():
    edge_0_x, edge_0_y = puzzle_edge()
    edge_1_x, edge_1_y = puzzle_edge()
    edge_2_x, edge_2_y = puzzle_edge()
    edge_3_x, edge_3_y = puzzle_edge()

    x, y = numpy.array([]), numpy.array([])

    x, y = numpy.append(x, edge_0_x), numpy.append(y, edge_0_y + 1)
    x, y = numpy.append(x, 1 + edge_1_y), numpy.append(y, -edge_1_x + 1)
    x, y = numpy.append(x, edge_2_x[::-1]), numpy.append(y, -edge_2_y[::-1])
    x, y = numpy.append(x, -edge_3_y), numpy.append(y, edge_3_x)

    return x, y

if __name__ == "__main__":
    x, y = puzzle_piece()
    plt.plot(x,y)
    plt.show()
