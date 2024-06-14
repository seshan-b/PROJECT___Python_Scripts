import os
import re

def clean_name(name, mode):
    """
    Function to clean the name by removing or replacing special characters.
    """
    # Define a set of special characters to remove (except space and &)
    special_characters = set('<>:"/\\|?*^.()%[]')
    
    # Initialize cleaned_name as an empty string
    cleaned_name = ""
    
    # For each character in name:
    for i, char in enumerate(name):
        # If character is a space, use an underscore
        if char == ' ':
            cleaned_name += '_'
        # If character is &, replace with _and_
        elif char == '&':
            if i > 0 and name[i-1] != '_':
                cleaned_name += '_'
            cleaned_name += 'and'
            if i < len(name) - 1 and name[i+1] != '_':
                cleaned_name += '_'
        # If character is not in special characters set, append it to cleaned_name
        elif char not in special_characters:
            cleaned_name += char

    # Remove leading or trailing underscores or hyphens
    cleaned_name = cleaned_name.strip('_-')
    
    return cleaned_name

def renumber_files(files, path, mode):
    """
    Function to renumber files in sequence.
    """
    file_counter = 1
    for item in sorted(files):
        item_path = os.path.join(path, item)
        file_name, file_extension = os.path.splitext(item)
        
        # Clean the file name
        cleaned_file_name = clean_name(file_name, mode)
        
        if mode == 'clean_full':
            # Remove any existing sequence numbers
            cleaned_file_name = re.sub(r'-\d{4}$', '', cleaned_file_name)
            # Append new sequence number
            cleaned_file_name += f'-{file_counter:04}'
            file_counter += 1
        
        # Combine cleaned_file_name and extension
        cleaned_item = cleaned_file_name + file_extension
        
        # Rename the file if the cleaned name is different from the original
        if cleaned_item != item:
            new_item_path = os.path.join(path, cleaned_item)
            os.rename(item_path, new_item_path)
            print(f"Renamed file: {item_path} -> {new_item_path}")

def process_directory(path, mode):
    """
    Function to process a directory: clean and rename files and folders.
    """
    # Collect all files and directories
    files = []
    directories = []
    
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            files.append(item)
        elif os.path.isdir(item_path):
            directories.append(item)
    
    # Renumber files to ensure consistency
    renumber_files(files, path, mode)
    
    # Process subdirectories
    for item in directories:
        item_path = os.path.join(path, item)
        
        # Clean the directory name
        cleaned_item = clean_name(item, mode)
        
        # Rename the directory if cleaned_item is different from item
        if cleaned_item != item:
            new_item_path = os.path.join(path, cleaned_item)
            os.rename(item_path, new_item_path)
            print(f"Renamed directory: {item_path} -> {new_item_path}")
            item_path = new_item_path  # Update item_path to the new name
        
        # Recursively call process_directory on the new directory path
        process_directory(item_path, mode)

def main():
    # Prompt the user to enter the directory path
    directory_path = input("Please enter the directory path: ")
    
    # Check if the provided path exists and is a directory
    if not os.path.isdir(directory_path):
        print("The provided path is not a valid directory.")
        return
    
    # Prompt the user to choose the mode: 'clean' or 'clean_full'
    mode = input("Enter mode ('clean' or 'clean_full'): ").strip().lower()
    if mode not in ['clean', 'clean_full']:
        print("Invalid mode selected.")
        return
    
    # Call process_directory with the provided directory path and mode
    process_directory(directory_path, mode)

if __name__ == "__main__":
    main()
