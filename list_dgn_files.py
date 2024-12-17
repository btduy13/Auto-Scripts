import os
import pandas as pd
from datetime import datetime

def collect_dgn_files(source_dir):
    """Collect all .dgn files from source directory and its subdirectories."""
    dgn_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.dgn'):
                full_path = os.path.join(root, file)
                file_info = {
                    'File Name': file.upper(),
                    'Full Path': full_path,
                    'Size (KB)': round(os.path.getsize(full_path) / 1024, 2),
                    'Last Modified': datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d %H:%M:%S')
                }
                dgn_files.append(file_info)
    return dgn_files

def export_to_excel(file_list, output_path):
    """Export the file list to Excel."""
    if file_list:
        df = pd.DataFrame(file_list)
        df.to_excel(output_path, index=False)
        print(f"\nExcel file created successfully at: {output_path}")
        print(f"Total .dgn files found: {len(file_list)}")
    else:
        print("No .dgn files found in the specified directory.")

if __name__ == "__main__":
    # Get input from user
    source_directory = input("Enter source directory path: ")
    
    if os.path.exists(source_directory):
        # Create output filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(os.path.dirname(source_directory), f'dgn_files_list_{timestamp}.xlsx')
        
        # Collect and export files
        dgn_files = collect_dgn_files(source_directory)
        export_to_excel(dgn_files, output_file)
    else:
        print("Source directory does not exist!") 