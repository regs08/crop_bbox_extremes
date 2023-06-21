import os

def get_split_intervals(start, end, interval):
    """
    getting split points for an image, usually start will be equal to 0 and end
    will be the images width.

    In our case we are starting where the bboxes start and endning where they end.
    """
    # start is the minimum value
    # end is the width of the image gotten from our bbox extreme

    # if theres a remainder we subtract the last line
    num_lines = (end // interval) - 1 if (end // interval) > 0 else 0
    # for the first value of start for our splits
    intervals = [start]

    # Draw vertical lines at every n number of pixels until step > end
    if num_lines > 0:
        x = interval + start
        for i in range(num_lines):
            intervals.append(x)
            x += interval
            if x + interval > end:
                break
    # appending image with for the last split
    intervals.append(end)
    return intervals


def insert_string_before_extension(file_basename, string_to_insert):
    # Get the file extension
    file_extension = os.path.splitext(file_basename)[1]
    # Get the file name without extension
    file_name = os.path.splitext(file_basename)[0]
    # Create new file name with string inserted before extension
    new_file_name = os.path.basename(file_name + string_to_insert + file_extension)
    # Rename the file
    return new_file_name