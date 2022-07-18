## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#####################################################
##              Align Depth to Color               ##
#####################################################

# First import the library
import pyrealsense2.pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
from pyntcloud import PyntCloud
import os
import sys

from file_var import *
# from python_tkinter import key, myClick, callback, get_point, callback_rect, rs_call

# Create a pipeline
pipeline = rs.pipeline()

# Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# point cloud
pc = rs.pointcloud()

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: ", depth_scale)
# exit()

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

image_id = 1
group_id = 0
canvas_directory = ''

# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
clipping_distance_in_meters = 0.20  # 1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

# Streaming loop
try:
    while True:

        while group_id == 0:
            group_id = input('group_id: ')
            print('group_id: ', group_id)
            canvas_directory = dataset_dir + '/' + group_id
            if os.path.isdir(canvas_directory):
                print('Folder with group_id exists: ', group_id)
                group_id = 0
            else:
                os.mkdir(canvas_directory)

        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        pc.map_to(color_frame)
        pointcloud_3 = pc.calculate(aligned_depth_frame)




        # if image_id == 3:
        #     clipping_distance_in_meters = 0.25  # 1 meter
        #     clipping_distance = clipping_distance_in_meters / depth_scale

        # Remove background - Set pixels further than clipping_distance to grey
        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

        # coloriser
        colourised_depth = np.asarray(rs.colorizer().colorize(aligned_depth_frame).get_data())
        # print(colourised_depth.shape)

        # Render images
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        # images = np.hstack((bg_removed, colourised_depth, color_image))
        images = np.hstack((bg_removed, colourised_depth))
        # cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Align Example', images)
        key = cv2.waitKey(1)

        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

        elif key == 115:

            full_file_name = file_name + '_' + str(group_id) + '_' + str(image_id)
            cv2.imwrite(dataset_dir + '/' + str(group_id) + '/' + full_file_name + rgb_image_dir + '.png', color_image)
            cv2.imwrite(dataset_dir + '/' + str(group_id) + '/' + full_file_name + bg_removed_dir + '.png', bg_removed)
            cv2.imwrite(dataset_dir + '/' + str(group_id) + '/' + full_file_name + opencv_depth_dir + '.png', depth_colormap)
            cv2.imwrite(dataset_dir + '/' + str(group_id) + '/' + full_file_name + pyrs_depth_dir + '.png', colourised_depth)
            np.save(dataset_dir + '/' + str(group_id) + '/' + full_file_name + raw_depth_dir, depth_image)
            pointcloud_3.export_to_ply(dataset_dir + '/' + str(group_id) + '/' + full_file_name + point_cloud_dir + '.ply', color_frame)
            print(" Data Saved ", full_file_name)
            # image_id += 1

        elif key == 50:
            print('2 pressed')
            clipping_distance_in_meters = 0.25  # 1 meter
            clipping_distance = clipping_distance_in_meters / depth_scale
            image_id = 2

        elif key == 49:
            print('1 pressed')
            clipping_distance_in_meters = 0.20  # 1 meter
            clipping_distance = clipping_distance_in_meters / depth_scale
            image_id = 1

        elif key == 51:
            print('3 pressed')
            clipping_distance_in_meters = 0.20  # 1 meter
            clipping_distance = clipping_distance_in_meters / depth_scale
            image_id = 3

        # print('image_id: ', image_id)


except KeyboardInterrupt:
    pipeline.stop()

finally:
    cv2.destroyAllWindows()
    pipeline.stop()

sys.path.append(os.getcwd())
os.system('python ./python_tkinter.py ' + canvas_directory)
