import os

# directories
# dataset_dir = '/Volumes/mydrive/localdrive/datasets/dyson_weight_estimation/'

dataset_dir="/" # Where to save the rgb and depth images

# raw_depth_dir = dataset_dir + 'raw_depth'
# opencv_depth_dir = dataset_dir + 'opencv_depth'
# pyrs_depth_dir = dataset_dir + 'pyrs_depth'
# rgb_image_dir = dataset_dir + 'rgb_image'
# point_cloud_dir = dataset_dir + 'point_cloud'
# bg_removed_dir = dataset_dir + 'bg_removed'

raw_depth_dir = '_rdepth'
opencv_depth_dir = '_odepth'
pyrs_depth_dir = '_pdepth'
rgb_image_dir = '_rgb'
point_cloud_dir = '_pc'
bg_removed_dir = '_bgremoved'

# file name
file_name_prefix = 'strawberry_'
sample_number = ''
sample_market = 'dyson_'
sample_type = 'lincoln_'
sample_subtype = 'tbd_'
sample_weight = ''
file_name = '/' + file_name_prefix + sample_market + sample_type + sample_subtype

# for post process
# file_name = '/strawberry_20cm__aldi__egypt__fortuna__21_01_2021_15_29_10_25.4_1'

if not os.path.isdir(dataset_dir):
    os.mkdir(dataset_dir)
    # os.mkdir(raw_depth_dir)
    # os.mkdir(opencv_depth_dir)
    # os.mkdir(pyrs_depth_dir)
    # os.mkdir(point_cloud_dir)
    # os.mkdir(rgb_image_dir)
    # os.mkdir(bg_removed_dir)
