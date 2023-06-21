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

def replace_first_element_in_folder(folder_path):
    # Get a list of files in the folder
    files = os.listdir(folder_path)

    # Iterate over each file in the folder
    for file_name in files:
        # Check if the file is a text file
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)

            # Read the contents of the file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Modify the lines by replacing the first element with 0
            modified_lines = []
            for line in lines:
                elements = line.split()
                if len(elements) > 0:
                    elements[0] = '0'
                modified_line = ' '.join(elements) + '\n'
                modified_lines.append(modified_line)

            # Save the changes back to the file
            with open(file_path, 'w') as file:
                file.writelines(modified_lines)

            print(f"Modified and saved changes to '{file_path}' successfully!")

    print("Modification of all files in the folder is complete.")