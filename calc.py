import math
from pytest import approx


def rotate(x, y, angle_rad):
    s = math.sin(angle_rad)
    c = math.cos(angle_rad)
    nx = x * c - y * s
    ny = x * s + y * c
    return nx, ny


def normalize_angle(angle):
    # result is (-PI, PI]
    while angle <= -math.pi:
        angle += 2 * math.pi
    while angle > math.pi:
        angle -= 2 * math.pi
    return angle


def heading_to_math(angle_rad):
    return normalize_angle(math.radians(90) - angle_rad)


def math_to_heading(angle_rad):
    return normalize_angle(math.radians(90) - angle_rad)


def wall_point(
    robot_x,
    robot_y,
    angle_rad,
    distance_mm,
    axis_deg=75.0,
    sensor_x=475.0,
    sensor_y=675.0,
):
    angle = angle_rad - math.radians(90)
    sensor_angle = math.radians(90 - axis_deg)
    lwx = sensor_x + distance_mm * math.cos(sensor_angle)
    lwy = sensor_y + distance_mm * math.sin(sensor_angle)
    rwx, rwy = rotate(lwx, lwy, angle);
    return (robot_x + rwx, robot_y + rwy)
