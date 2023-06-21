import numpy as np
import supervision as sv
from crop_bbox_extremes.bbox_extremes import *
from crop_bbox_extremes.utils import *
import albumentations as A
import cv2

"""
functions for splitting images based on bbox extremes and min pixel values
"""


# we go from dataset to image to split. image to dict to dataset
def split_images_via_bbox_extremes_and_interval(dataset,
                                                min_boxes=1,
                                                interval=1280,
                                                min_pixel_value=1280):
    """
    takes in an dataset splits the images vertically using the points provided
    by the intervals. intervals are obtained by getting the bbox extremes and the min pixel params
    :param image_folder: location of images
    :param interval: interval for the split
    :param save_folder: save folder for the cropped images
    :param ann_folder: if theres a different folder for annotations..
    :param save: save the images
    :param min_boxes: check so that all images have an instance present
    :return:
    """
    filenames = list(dataset.images.keys())
    output = {}
    for filename in filenames:
        #info from our dataset
        img = dataset.images[filename]
        h,w,_ =img.shape
        ann = dataset.annotations[filename]
        class_ids = ann.class_id
        bboxes = ann.xyxy

        # instead of loading in the text file we can just load in bbox extremes here
        xmin, ymin, xmax, ymax = get_bbox_extreme_with_min_pixel_value(bboxes, min_pixel_value)
        if ymin < 0:
            ymin = 0

        # getting the coords for our vertical split for each image
        split_intervals = get_split_intervals(xmin, w, interval)
        split_image = vertical_split_img_with_intervals(img=img,
                                                        bboxes=bboxes,
                                                        class_ids=class_ids,
                                                        intervals=split_intervals,
                                                        ymin=ymin,
                                                        ymax=ymax,
                                                        min_boxes=min_boxes,
                                                        filename=filename)
        # formatting our data for a detection dataset
        for data in split_image:
            # casting data as numpy
            class_id = np.array(data['class_id'])
            anns = np.array(data['anns'])

            output[data['filename']] = {
                'image': data['image'],
                #casting as Detectionms to in order to make sv.Dataset
                'anns': sv.Detections(xyxy=anns, class_id=class_id),
            }

    return output


def vertical_split_img_with_intervals(img, intervals, bboxes, class_ids, filename, min_boxes, ymin, ymax):
    """
    splits the image using the albumentations library the x values are gotten from intervals. the y values can be given
    their default is 0, hieght of the image
    :param img: path or arr, if path we add a filename to our dict
    :param intervals: the poitns where we will crop
    :param bboxes: the bboxes, default is yolo format, just coords we will add the class label onto the 5th index.
    :param class_labels: list of the class ids, ints
    :return: a list of dictionaries containing the split image info
    """

    # getting the "ValueError: Your 'label_fields' are not valid - them must have same names as params in dict" so getting rid
    # adding the label on to the end of the box
    bboxes = [np.append(box, class_ids[i]) for i, box in enumerate(bboxes)]
    out_images = []

    for i in range(len(intervals) - 1):
        xmin = intervals[i]
        xmax = intervals[i + 1]
        split_coords = [xmin, ymin, xmax, ymax]

        split_image = get_split_image(img=img,
                                      split_coords=split_coords,
                                      bboxes=bboxes,
                                      min_boxes=min_boxes,
                                      class_ids=class_ids,
                                      )

        # maybe here just build the dicts
        if split_image:
            # adding filename
            file_no = f'_{i}'
            # where i is the number of crops per image
            crop_filename = insert_string_before_extension(filename, file_no)
            out = {
                'filename': crop_filename,
                'anns': split_image['bboxes'],
                'image': split_image['image'],
                'class_id': split_image['class_id']
            }
            out_images.append(out)
    # list of lists where each idx is a dict which reperesents an imagethat is split
    return out_images


def get_split_image(img, split_coords, bboxes, class_ids, min_boxes):
    """
    split our image and build a dictionary to return
    :param img: img as array
    :param xmin: min val dimensions for our split
    :param xmax: max val
    :param bboxes: bboxes from the image
    :param class_labels: class_labels as strs
    :return: a dict containing , image, bboxes, category_ids
    """
    xmin, ymin, xmax, ymax = split_coords
    aug = A.Compose([
        A.Crop(x_min=xmin, x_max=xmax, y_min=ymin, y_max=ymax),
    ], bbox_params=A.BboxParams(format='pascal_voc', min_visibility=0.3))

    vertical_split_image = aug(image=img, bboxes=bboxes, category_ids=class_ids)
    if len(vertical_split_image['bboxes']) > min_boxes:
        # gets rid of ourclass id at the end
        vertical_split_image['class_id'] = [box[4] for box in vertical_split_image['bboxes']]
        vertical_split_image['bboxes'] = [box[:4] for box in vertical_split_image['bboxes']]
        # gets our class id
        vertical_split_image['image'] = cv2.cvtColor(vertical_split_image['image'], cv2.COLOR_BGR2RGB)
        return vertical_split_image
    return None