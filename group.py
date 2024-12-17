import os
import shutil
import re
from collections import defaultdict

def get_base_pattern(filename):
    # Remove file extension and get base name
    base_name = os.path.splitext(filename)[0]
    
    # Try different pattern matching strategies
    patterns = [
        # Remove trailing numbers
        re.sub(r'\d+$', '', base_name),
        # Get first part before numbers
        re.match(r'^([A-Za-z]+|\d+[A-Za-z]+)', base_name),
        # Get everything before last number sequence
        re.sub(r'\d+([^\d]*?)$', r'\1', base_name),
        # Get common prefix
        re.sub(r'[0-9_-]+.*$', '', base_name)
    ]
    
    for pattern in patterns:
        if pattern and isinstance(pattern, str) and pattern != base_name:
            return pattern
        elif pattern and hasattr(pattern, 'group'):
            return pattern.group(1)
    return base_name

def collect_all_files(source_dir):
    """Collect all files from source directory and its subdirectories."""
    all_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.dgn', '.drv', '.dri')):
                full_path = os.path.join(root, file)
                all_files.append(full_path)
    return all_files

def create_destination_structure(dest_dir):
    """Create the basic directory structure."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    singles_dir = os.path.join(dest_dir, "single_files")
    if not os.path.exists(singles_dir):
        os.makedirs(singles_dir)

def organize_files(source_dir, dest_dir, max_depth=3):
    print(f"Starting file organization from: {source_dir}")
    print(f"Destination directory: {dest_dir}")
    
    # Create destination structure
    create_destination_structure(dest_dir)
    
    # Collect all files
    all_files = collect_all_files(source_dir)
    print(f"\nFound {len(all_files)} files to organize")
    
    # Group files by pattern
    pattern_groups = defaultdict(list)
    for file_path in all_files:
        filename = os.path.basename(file_path)
        base_pattern = get_base_pattern(filename)
        pattern_groups[base_pattern].append(file_path)
        
    # Process groups
    for pattern, group_files in pattern_groups.items():
        if len(group_files) > 1:
            # Create pattern directory
            pattern_dir = os.path.join(dest_dir, pattern)
            if not os.path.exists(pattern_dir):
                os.makedirs(pattern_dir)
            
            # Move files to pattern directory
            for file_path in group_files:
                filename = os.path.basename(file_path)
                dest_path = os.path.join(pattern_dir, filename)
                try:
                    shutil.copy2(file_path, dest_path)
                    print(f"Copied: {filename} -> {pattern}/")
                except Exception as e:
                    print(f"Error copying {filename}: {str(e)}")
        else:
            # Move single files to singles directory
            singles_dir = os.path.join(dest_dir, "single_files")
            for file_path in group_files:
                filename = os.path.basename(file_path)
                dest_path = os.path.join(singles_dir, filename)
                try:
                    shutil.copy2(file_path, dest_path)
                    print(f"Copied single file: {filename} -> single_files/")
                except Exception as e:
                    print(f"Error copying {filename}: {str(e)}")
    
    print("\nFile Organization Summary:")
    print("-------------------------")
    
    # Display final structure
    for root, dirs, files in os.walk(dest_dir):
        if files:
            rel_path = os.path.relpath(root, dest_dir)
            try:
                print(f"\n{rel_path}:")
                for file in sorted(files):
                    print(f"  - {file}")
            except UnicodeEncodeError:
                print(f"\n{rel_path}: (Contains files with special characters)")

if __name__ == "__main__":
    # Example usage
    source_directory = input("Enter source directory path: ")
    destination_directory = input("Enter destination directory path: ")
    
    if os.path.exists(source_directory):
        organize_files(source_directory, destination_directory)
    else:
        print("Source directory does not exist!")