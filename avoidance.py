import unittest
import os
import time
import cv2
import numpy as np
from absl import app, flags, logging
# import pigpio as gpio
# from part import Part
# from rplidar import RPLidar
# from servo_motor import ServoMotor
# from motor import DCMotor
import matplotlib.pyplot as plt
import cubic_spline_planner

show_animation = True

MIN_DISTANCE = 0.425  # m
BOX_WIDTH = 0.4
BOX_LENGTH = 0.4
BOX_OBJ_COORD = np.asarray([[MIN_DISTANCE, MIN_DISTANCE + BOX_LENGTH, MIN_DISTANCE + BOX_LENGTH, MIN_DISTANCE, MIN_DISTANCE],
                           [BOX_WIDTH, BOX_WIDTH, -BOX_WIDTH, -BOX_WIDTH, BOX_WIDTH]])

# dcMotor1 = DCMotor(ena_pin=24, in1_pin=13, in2_pin=19)
# dcMotor2 = DCMotor(ena_pin=23, in1_pin=20, in2_pin=21)
# servoMotor = ServoMotor(steering_pin=18)


def get_robot_in_position():
    t_end = time.time() + 3
    lidar_reading_at_0_degrees = MIN_DISTANCE
    while lidar_reading_at_0_degrees < MIN_DISTANCE:
        print("moving_backwards")
        # dcMotor1.move_backwards(100)
        # dcMotor2.move_backwards(100)
    # dcMotor1.stop_motor()
    # dcMotor2.stop_motor()
    print("stopping motors")


def calculate_trajectory():
    # x, y = get_box_position()
    # if x < MIN_DISTANCE:
    #     get_robot_in_position()

    trajectory_points = np.asarray([[0., 0.165, MIN_DISTANCE, MIN_DISTANCE + 0.4],
                                    [0., 0.165, BOX_OBJ_COORD[1, 0] + 0.2, BOX_OBJ_COORD[1, 0] + 0.2]])
    trajectory = np.polyfit(x=trajectory_points[0, :], y=trajectory_points[1, :], deg=3)
    print(trajectory)

    trajectory_x = np.linspace(0, MIN_DISTANCE + 0.4, 82)
    trajectory_y = np.polyval(trajectory, trajectory_x)

    return trajectory_x, trajectory_y


def path_planner():
    trajectory_x, trajectory_y = calculate_trajectory()

    yaw_angle = 0.0
    steering_angle = 0.0

    steering_angles = [yaw_angle]
    yaw_angles = [steering_angle]

    for i in range(1, len(trajectory_x)):
        yaw_angle = np.arctan2(trajectory_y[i] - trajectory_y[i - 1],
                               trajectory_x[i] - trajectory_x[i - 1])
        yaw_angles.append(yaw_angle)
        steering_angle = yaw_angles[i] - yaw_angles[i - 1]
        if np.deg2rad(-40.) <= steering_angle <= np.deg2rad(40.):
            steering_angles.append(steering_angle)
        elif steering_angle > 0:
            steering_angles.append(np.deg2rad(40.))
        else:
            steering_angles.append(np.deg2rad(-40.))

    return steering_angles, yaw_angles


def convert_steering_angle_to_motor_rotation_angle(steering_angle_value):
    return ((np.pi / 3) * steering_angle_value) / np.deg2rad(40)


def main(_argv):
    steering_angles, yaw_angles = path_planner()
    trajectory_x, trajectory_y = calculate_trajectory()

    for i in range(len(trajectory_x)):
        plt.cla()
        plt.plot(trajectory_x[i], trajectory_y[i], 'ro', ms=15.)
        plt.plot(BOX_OBJ_COORD[0, :], BOX_OBJ_COORD[1, :], label="box")
        plt.plot(trajectory_x, trajectory_y, 'g', label="trajectory")
        plt.axis("equal")
        plt.grid(True)
        plt.title("Yaw angle: " + str(round(yaw_angles[i], 3))
                  + "\n" + "Steering angle: " + str(round(steering_angles[i], 3)))
        plt.pause(0.001)

    # for i in range(len(trajectory_x)):
    #     dcMotor1.moveforward(75)
    #     dcMotor2.moveforward(75)
    #     servoMotor.rotate(convert_steering_angle_to_motor_rotation_angle(steering_angles[i]))
    #     time.sleep(0.001)


if __name__ == '__main__':
    app.run(main)
