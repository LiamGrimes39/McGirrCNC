import os
import re
import shutil

def clean_title(title):
    """Remove invalid characters for Windows filenames."""
    return re.sub(r'[<>:"/\\|?*()]', '', title)

def extract_title_from_file(filepath):
    """Extract and clean the title from the second line of the file."""
    try:
        with open(filepath, 'r') as file:
            file.readline()  # Skip the first line
            second_line = file.readline().strip()  # Read the second line
            if second_line.startswith('O'):
                title = second_line[5:].replace(')', '').strip()
                return clean_title(title)
            else:
                print(f"File {filepath} doesn't match the expected pattern.")
                return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def rename_files_in_directory(directory):
    """Rename files in the given directory based on their extracted titles."""
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            title = extract_title_from_file(filepath)
            if title:
                name_part, extension = os.path.splitext(filename)
                new_filename = f"{name_part} {title}{extension}"
                new_filepath = os.path.join(directory, new_filename)
                
                try:
                    print(f"Attempting to rename: {filepath} to {new_filepath}")
                    os.rename(filepath, new_filepath)
                    print(f"Renamed '{filename}' to '{new_filename}'")
                except Exception as e:
                    print(f"Error renaming file {filename} to {new_filename}: {e}")

def scan_existing_directories(base_path):
    """Scan for existing directories and extract their ranges."""
    ranges = []
    for dirpath, dirnames, _ in os.walk(base_path):
        for dirname in dirnames:
            match = re.match(r"(\d{4})-(\d{4})", dirname)
            if match:
                start_range, end_range = int(match.group(1)), int(match.group(2))
                ranges.append((start_range, end_range, os.path.join(dirpath, dirname)))
    return ranges

def get_directory_for_file(ranges, four_digits):
    """Get the appropriate directory for a file based on its four-digit prefix."""
    for start, end, path in ranges:
        if start <= four_digits <= end:
            return path
    return None

def move_files(source_path, base_path):
    """Move files from the source path to the appropriate directories in the base path."""
    ranges = scan_existing_directories(base_path)
    
    for filename in os.listdir(source_path):
        file_path = os.path.join(source_path, filename)
        if os.path.isfile(file_path) and filename[:4].isdigit():
            four_digits = int(filename[:4])
            target_directory = get_directory_for_file(ranges, four_digits)
            
            if target_directory:
                sub_ranges = scan_existing_directories(target_directory)
                final_directory = get_directory_for_file(sub_ranges, four_digits) or target_directory

                os.makedirs(final_directory, exist_ok=True)
                
                dst = os.path.join(final_directory, filename)
                if os.path.exists(dst):
                    os.remove(dst)
                shutil.move(file_path, dst)
                print(f"Moved {filename} to {final_directory}")
            else:
                print(f"No target directory found for {filename}")
        else:
            print(f"Skipping {filename}: not a file or doesn't start with digits")


source_path = r"C:\Users\liamg\OneDrive\Desktop\In here dad"
base_path = r"C:\Users\liamg\OneDrive\Desktop\Machine Programs"

# First, rename the files in the source directory
rename_files_in_directory(source_path)

# Then, move the renamed files to the appropriate directories
move_files(source_path, base_path)

#Liam Grimes 28/06/24