# keypoint annotation for strawberry db 1 dataset
# Some basic setup:
import pathlib
import re
from tqdm import tqdm
from matplotlib import pyplot as plt

import detectron2

# Setup detectron2 logger
from detectron2.utils.logger import setup_logger
from skimage import measure
from shapely.geometry import Polygon, MultiPolygon

setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# if your dataset is in COCO format, this cell can be replaced by the following three lines:
# from detectron2.data.datasets import register_coco_instances
# register_coco_instances("my_dataset_train", {}, "json_annotation_train.json", "path/to/image/dir")
# register_coco_instances("my_dataset_val", {}, "json_annotation_val.json", "path/to/image/dir")

from detectron2.structures import BoxMode

points = []


def draw_circle(event, x, y, flags, param):

    # points.clear()
    if event == cv2.EVENT_LBUTTONDBLCLK:
        # print('callback: ', x, y)
        points.append((x, y))
        # cv2.circle(img,(x,y),100,(255,0,0),-1)
        # v = int(input('labelled: '))
        # if v == 0:
        #     x, y = 0, 0
        # print('x, y, v: ', x, y, v)
        # correct = input('correct: ')
        # if correct == 'y':
        #     points.append((x, y, v))


def label_it(win_name, img, b_box):

    category_id = None
    keypoints = []

    cv2.destroyAllWindows()
    cv2.namedWindow(win_name)
    cv2.setMouseCallback(win_name, draw_circle)
    x, y, max_x, max_y = b_box
    cv2.rectangle(
        img,
        (int(x), int(y)),
        (int(0 + max_x), int(0 + max_y)),
        thickness=1,
        color=(255, 0, 0),
    )
    cv2.imshow(win_name, img)

    while True:
        key = cv2.waitKey(0)

        # space: save as ripe
        if key == ord("q"):
            category_id = 0
            points.clear()
            cv2.destroyWindow(win_name)
            break

        # q: save as unripe
        elif key == ord("w"):
            category_id = 1
            points.clear()
            cv2.destroyWindow(win_name)
            break

        # w: means not bbox not valid
        elif key == ord("e"):
            category_id = 2
            points.clear()
            cv2.destroyWindow(win_name)
            break

        #  clear current keypoints
        elif key == ord("d"):
            keypoints.clear()
            points.clear()
            category_id = None

        # no point clicked: continue
        elif len(points) == 0:
            points.clear()
            continue

        else:

            # visible and labelled
            if key == ord("z"):
                keypoints.append((*points[-1], 2))

            # invisible with other and labelled
            elif key == ord("x"):
                keypoints.append((*points[-1], 1))

            # invisible by self and labelled
            elif key == ord("c"):
                keypoints.append((*points[-1], -1))
                category_id = 1

            # marked but not labelled
            elif key == ord("v"):
                keypoints.append((*points[-1], 0))
                category_id = 1
            points.clear()

        print("keypoints: ", keypoints)

        if len(keypoints) != 0:
            for keypoint in keypoints:
                cv2.circle(img, keypoint[:2], radius=5, color=(0, 0, 255), thickness=-1)
            cv2.imshow(win_name, img)

    return category_id, keypoints


def get_strawberry_dicts(img_dir, dump_dir):

    for idx, image_file in tqdm(enumerate(pathlib.Path(img_dir).rglob("*.png"))):
        print("image file: ", image_file.absolute())
        dump_file_name = re.sub(".png", ".json", image_file.name)
        dump_file_path = dump_dir + dump_file_name
        if os.path.isfile(dump_file_path):
            print("json exists: ", dump_file_path)
            continue

        record = {}

        label = cv2.imread(re.sub("img", "label", str(image_file)))
        img = cv2.imread(str(image_file))
        height, width = img.shape[:2]
        print(height, width)

        # cv2.imshow('original_file', img)
        # key = cv2.waitKey(0)
        # if key == ord('q'):
        #     break
        record["file_name"] = image_file.as_posix()
        record["image_id"] = idx
        record["height"] = height
        record["width"] = width

        objs = []
        for instance in np.unique(label)[1:]:

            print("instance: ", instance)
            bin_img = np.asarray(np.where(label != instance, 0, 255), dtype=np.float32)
            # print('bin img shape: ', bin_img.shape)
            bin_img = cv2.cvtColor(bin_img, cv2.COLOR_RGB2GRAY)
            _, bin_img = cv2.threshold(bin_img, 250, 255, cv2.THRESH_BINARY)
            print("bin_img.shape ", bin_img.shape)
            contours = measure.find_contours(bin_img, positive_orientation="low")

            segmentations = []
            polygons = []
            for idx, contour in enumerate(contours):

                for i in range(len(contour)):
                    row, col = contour[i]
                    contour[i] = (col - 1, row - 1)

                # Make a polygon and simplify it
                if contour.shape[0] < 3:
                    continue
                poly = Polygon(contour)
                # print('poly: ', poly)
                # poly = poly.simplify(1.0, preserve_topology=False)
                polygons.append(poly)
                segmentation = np.array(poly.exterior.coords).ravel().tolist()
                print(segmentation)
                segmentations.append(segmentation)

            # Combine the polygons to calculate the bounding box and area
            multi_poly = MultiPolygon(polygons)
            bbox = multi_poly.bounds
            print("bbox: ", bbox)

            category_id, keypoints = label_it(image_file.name, img, bbox)
            if category_id == 2:
                continue

            print("returned category id, keypoint: ", category_id, keypoints)

            assert (category_id == 0) or (category_id == 1)
            assert len(keypoints) == 5

            print(len(segmentation), segmentation)

            obj = {
                "bbox": bbox,
                "bbox_mode": BoxMode.XYXY_ABS,
                "segmentation": segmentations,
                "category_id": category_id,
                "keypoints": keypoints,
            }
            objs.append(obj)
        record["annotations"] = objs
        with open(dump_file_path, "w") as f:
            json.dump(record, f)


def main():
    data_dir = "/home/adeayo/Documents/DataCollectionAndAnnotation/Annotation/train/img" # Image directory
    dump_dir = "/home/adeayo/Documents/DataCollectionAndAnnotation/Annotation/dump/img" #dump directory

    get_strawberry_dicts(img_dir=data_dir, dump_dir=dump_dir)


if __name__ == "__main__":
    main()
