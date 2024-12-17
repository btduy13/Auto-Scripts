import os
import pandas as pd
from pathlib import Path

def list_dgn_files(folder_path):
    # Danh sách để lưu tên các file
    dgn_files = []
    
    # Duyệt qua tất cả các file trong thư mục và thư mục con
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Kiểm tra nếu file có đuôi .dgn
            if file.lower().endswith('.dgn'):
                # Lấy tên thư mục cuối cùng thay vì tên file
                last_folder = os.path.basename(root)
                if last_folder not in dgn_files:  # Tránh trùng lặp
                    dgn_files.append(last_folder)
    
    # Tạo DataFrame từ danh sách file
    df = pd.DataFrame(dgn_files, columns=['Tên File'])
    
    # Tạo tên file Excel
    excel_path = os.path.join(folder_path, 'danh_sach_file_dgn.xlsx')
    
    # Xuất ra file Excel
    df.to_excel(excel_path, index=False)
    print(f"Đã xuất danh sách file ra: {excel_path}")

# Sử dụng script
if __name__ == "__main__":
    # Nhập đường dẫn thư mục cần quét
    folder_path = r"C:\Users\USER\Downloads\BSR-MACRO\BSR-MACRO\DQR_MOC\DQR_MOC"
    
    # Kiểm tra thư mục có tồn tại không
    if os.path.exists(folder_path):
        list_dgn_files(folder_path)
    else:
        print("Thư mục không tồn tại!")