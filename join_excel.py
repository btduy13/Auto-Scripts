import os
import pandas as pd
from pathlib import Path

def join_excel_files(folder_path):
    # Danh sách để lưu các DataFrame
    all_dfs = []
    
    # Duyệt qua tất cả các file trong thư mục
    for file in os.listdir(folder_path):
        # Kiểm tra nếu file có đuôi .xlsx hoặc .xls
        if file.lower().endswith(('.xlsx', '.xls')):
            file_path = os.path.join(folder_path, file)
            try:
                # Đọc file Excel
                df = pd.read_excel(file_path)
                # Thêm tên file gốc vào DataFrame
                df['Tên File Gốc'] = Path(file).stem
                all_dfs.append(df)
                print(f"Đã đọc file: {file}")
            except Exception as e:
                print(f"Lỗi khi đọc file {file}: {str(e)}")
    
    if all_dfs:
        # Gộp tất cả DataFrame
        merged_df = pd.concat(all_dfs, ignore_index=True)
        
        # Tạo tên file Excel kết quả
        output_path = os.path.join(folder_path, 'file_gop.xlsx')
        
        # Xuất ra file Excel
        merged_df.to_excel(output_path, index=False)
        print(f"\nĐã gộp thành công! File kết quả: {output_path}")
        print(f"Tổng số dòng: {len(merged_df)}")
    else:
        print("Không tìm thấy file Excel nào trong thư mục!")

if __name__ == "__main__":
    # Nhập đường dẫn thư mục chứa các file Excel
    folder_path = r"C:\Users\USER\Downloads\BSR-MACRO\BSR-MACRO\DQT_KLOC\DQT_KLOC"
    
    # Kiểm tra thư mục có tồn tại không
    if os.path.exists(folder_path):
        join_excel_files(folder_path)
    else:
        print("Thư mục không tồn tại!") 