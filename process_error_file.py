import csv
import os

def split_csv_on_error(input_file, output_file1, output_file2):
    """
    Đọc file CSV và tách thành 2 file khi gặp lỗi:
    - File 1: Từ đầu đến dòng trước dòng bị lỗi (ghi ngay khi đọc)
    - File 2: Từ dòng bị lỗi đến hết file (ghi ngay khi đọc)
    """
    error_row_number = None
    
    # Mở file output 1 để ghi liên tục
    f1 = open(output_file1, 'w', encoding='utf-8', newline='')
    writer1 = csv.writer(f1)
    
    # Đọc file cho đến khi gặp lỗi
    try:
        with open(input_file, 'r', encoding='utf-8', newline='') as f_in:
            reader = csv.reader(f_in)
            
            # Đọc header
            try:
                header = next(reader)
                writer1.writerow(header)  # Ghi header ngay
            except StopIteration:
                print("File CSV rỗng!")
                f1.close()
                return
            
            # Đọc và ghi từng dòng
            row_number = 1  # Bắt đầu từ 1 (sau header)
            for row in reader:
                row_number += 1
                writer1.writerow(row)  # Ghi ngay vào file 1
                
    except Exception as e:
        error_row_number = row_number
        print(f"⚠️ Gặp lỗi tại dòng {error_row_number}: {type(e).__name__}: {e}")
    finally:
        f1.close()
    
    # Đếm tổng số dòng trong file
    with open(input_file, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)
    
    total_records = total_lines - 1  # Trừ header
    
    # Hiển thị thông tin
    print(f"\n📊 THÔNG TIN FILE CSV:")
    print(f"   - Tổng số dòng: {total_lines} dòng (bao gồm header)")
    print(f"   - Tổng số bản ghi: {total_records} bản ghi")
    
    # Nếu không có lỗi
    if error_row_number is None:
        print(f"\n✓ Không gặp lỗi. File đã được đọc hoàn chỉnh!")
        # Xóa file 2 nếu không cần
        if os.path.exists(output_file2):
            os.remove(output_file2)
        return
    
    print(f"   - STT dòng bị lỗi: {error_row_number} (dòng thứ {error_row_number} tính từ đầu file, bản ghi thứ {error_row_number - 1})")
    print(f"   - Số bản ghi trước lỗi: {error_row_number - 2} bản ghi")
    print(f"   - Số bản ghi từ lỗi đến cuối: {total_records - error_row_number + 2} bản ghi")
    
    # Xóa dòng cuối cùng trong file 1 (dòng lỗi chưa hoàn thành)
    # Đọc lại file 1 và xóa dòng cuối
    with open(output_file1, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(output_file1, 'w', encoding='utf-8') as f:
        f.writelines(lines[:-1])  # Ghi lại không có dòng cuối
    
    print(f"\n✓ Đã ghi File 1 ({output_file1}): {len(lines)-1} dòng")
    
    # Ghi File 2: Từ dòng lỗi đến hết (đọc và ghi streaming)
    with open(input_file, 'r', encoding='utf-8') as f_in:
        with open(output_file2, 'w', encoding='utf-8') as f_out:
            # Ghi header
            header_line = f_in.readline()
            f_out.write(header_line)
            
            # Bỏ qua các dòng trước dòng lỗi
            for i in range(1, error_row_number):
                f_in.readline()
            
            # Ghi từ dòng lỗi đến hết
            line_count = 1  # Header
            for line in f_in:
                f_out.write(line)
                line_count += 1
    
    print(f"✓ Đã ghi File 2 ({output_file2}): {line_count} dòng")


# Sử dụng
if __name__ == "__main__":
    input_csv = "/data/face_v3/emb/angiang.csv"  # File CSV đầu vào
    output_csv1 = "part1_before_error.csv"  # File chứa dữ liệu từ đầu đến trước dòng lỗi
    output_csv2 = "part2_from_error.csv"    # File chứa dữ liệu từ dòng lỗi đến hết
    
    split_csv_on_error(input_csv, output_csv1, output_csv2)