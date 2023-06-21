## crop util functions
def get_bbox_extreme_with_min_pixel_value(bboxes, min_pixel_value):
    bbox_extremes = get_bbox_extremes(bboxes)
    bbox_extremes_with_min_pixel_value = check_bbox_extremes_for_min_pixel_value(bbox_extremes, min_pixel_value)
    return bbox_extremes_with_min_pixel_value


def check_bbox_extremes_for_min_pixel_value(bbox, min_pixel_value):
    # Calculate the width and height of the cropped image
    min_x, min_y, max_x, max_y = bbox
    width = max_x - min_x
    height = max_y - min_y

    # Check if the width and height of the cropped image meet the minimum pixel value
    if width < min_pixel_value:
        min_x -= (min_pixel_value - width) // 2
        max_x += (min_pixel_value - width + 1) // 2
    if height < min_pixel_value:
        min_y -= round(min_pixel_value - height) // 2
        max_y += round(min_pixel_value - height + 1) // 2
    out = [int(min_x), int(min_y), int(max_x), int(max_y)]
    for i, x in enumerate(out):
        if x < 0:
            out[i] = 0
    return out


def get_bbox_extremes(bboxes):
    """
    Given a list of bounding boxes (xmin, ymin, xmax, ymax), return the lowest xmin and ymin and highest xmax and ymax
    across all the bounding boxes.

    Args:
    - bboxes: list of tuples representing bounding boxes in the format (xmin, ymin, xmax, ymax)

    Returns:
    - Tuple containing (lowest xmin, lowest ymin, highest xmax, highest ymax)
    """
    min_x = min([bbox[0] for bbox in bboxes])
    min_y = min([bbox[1] for bbox in bboxes])
    max_x = max([bbox[2] for bbox in bboxes])
    max_y = max([bbox[3] for bbox in bboxes])
    box = (min_x, min_y, max_x, max_y)

    return box



def get_split_intervals(start, end, interval, image_width):
    """
    getting split points for an image, usually start will be equal to 0 and end
    will be the images width.

    In our case we are starting where the bboxes start(bbox extreme xmin) and endning where they end(bbox extreme xmax).
    """
    # start is the minimum value
    # end is the width of the image gotten from our bbox extreme

    # if theres a remainder we subtract the last line
    new_width = end-start
    num_lines = (new_width // interval) - 1 if (new_width // interval) > 0 else 0
    # for the first value of start for our splits

    if new_width < interval:
      diff_width_interval = interval-new_width
      start_diff =  start - diff_width_interval
      end_diff = end+diff_width_interval
      if start_diff > 0:
        start=start_diff
      elif end_diff < image_width:
        end=end_diff

    intervals = [start]
    # Draw vertical lines at every n number of pixels until step > end
    if num_lines > 0:
        x = interval + start
        for i in range(num_lines):
            intervals.append(x)
            x += interval
            if x + interval > end:
              continue


    # appending image with for the last split
    intervals.append(end)
    return intervals