"""
    https://github.com/SkoltechRobotics/rplidar
    authors: Avesalon Razvan, Horju Rares
"""

import unittest
import os
import time
import cv2
import numpy as np
from absl import app, flags, logging
import pigpio as gpio
from part import Part
from rplidar import RPLidar
from keyboard_controll import convert_degrees_to_rad


def plot_measurement(measurement):
    ROWS = 480
    COLS = 480

    DX = 240
    DY = 240

    dm_px = 1
    mm_dm = 100

    rows_grid = np.linspace(start=0, stop=ROWS, num=20)
    cols_grid = np.linspace(start=0, stop=COLS, num=20)

    mat_img_3ch = np.zeros(shape=(ROWS, COLS, 3))

    for m in measurement.T:
        x = int(m[0] / mm_dm * dm_px) + DX
        y = int(m[1] / mm_dm * dm_px) + DY

        x = x - x % dm_px
        y = y - y % dm_px

        cv2.rectangle(mat_img_3ch, (x, y), (x + 2, y + 2), (0, 0, 255), -1)

        for i in range(20):
            cv2.line(mat_img_3ch, (int(rows_grid[i]), 0), (int(rows_grid[i]), ROWS - 1), (255, 255, 255), 1)
            cv2.line(mat_img_3ch, (0, int(cols_grid[i])), (COLS - 1, int(cols_grid[i])), (255, 255, 255), 1)

    cv2.circle(img=mat_img_3ch, center=(DX, DY), radius=5, color=(255, 0, 0), thickness=-1)
    cv2.namedWindow('newMat_3ch', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('newMat_3ch', mat_img_3ch)
    cv2.waitKey(0)


def tu_lidar(_argv):
    lidar = RPLidar('/dev/ttyUSB0')

    # check lidar state and health
    print(lidar.get_info())
    print(lidar.get_health())

    for i, scan in enumerate(lidar.iter_scans(max_buf_meas=800, min_len=5)):
        print(i, len(scan))

        valid_measurements = np.array([])
        for measurement in scan:
            quality, angle, distance = measurement
            if distance != 0:
                x = distance * np.cos(convert_degrees_to_rad(angle))
                y = distance * np.sin(convert_degrees_to_rad(angle))
                cartesian = np.array([x, y])
                measurement = np.vstack((measurement, cartesian))

            if measurement.shape[0]:
                plot_measurement(measurement)

        if i > 10:
            break

    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()


def tu_plot(_argv):
    x = np.array([1415, 4480, 6753, 7155, 9871, 12847, 14351, 16459, 17619, 18758])
    y = np.array([1473, 2746, 3251, 6240, 6635, 6674, 8192, 18669, 19294, 20589])
    m = np.vstack((x.T, y.T))
    plot_measurement(m)

if __name__ == '__main__':
    app.run(tu_plot)
