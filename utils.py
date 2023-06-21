import os

def insert_string_before_extension(file_basename, string_to_insert):
    # Get the file extension
    file_extension = os.path.splitext(file_basename)[1]
    # Get the file name without extension
    file_name = os.path.splitext(file_basename)[0]
    # Create new file name with string inserted before extension
    new_file_name = os.path.basename(file_name + string_to_insert + file_extension)
    # Rename the file
    return new_file_name