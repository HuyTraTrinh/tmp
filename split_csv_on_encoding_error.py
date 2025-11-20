import os

def split_csv_on_encoding_error(input_file, output_file1, output_file2):
    """
    Đọc file CSV và tách thành 2 file khi gặp lỗi encoding:
    - File 1: Từ đầu đến trước dòng bị lỗi (bao gồm header)
    - File 2: Từ dòng bị lỗi đến hết file (bao gồm header)
    """
    
    print(f"🔄 Đang đọc file và tìm vị trí lỗi encoding...")
    
    # Đọc file ở chế độ binary để tìm vị trí lỗi chính xác
    error_line_number = None
    error_byte_position = None
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            line_number = 0
            for line in f:
                line_number += 1
    except UnicodeDecodeError as e:
        error_byte_position = e.start
        print(f"⚠️ Gặp lỗi encoding tại byte position {error_byte_position}: {e}")
    
    # Đếm số dòng đến vị trí lỗi bằng cách đọc binary
    if error_byte_position is not None:
        with open(input_file, 'rb') as f:
            content_before_error = f.read(error_byte_position)
            error_line_number = content_before_error.count(b'\n') + 1
            print(f"   Lỗi xảy ra tại dòng {error_line_number}")
    
    # Đếm tổng số dòng (đọc binary để không bị lỗi)
    with open(input_file, 'rb') as f:
        total_lines = sum(1 for _ in f)
    
    print(f"\n📊 THÔNG TIN:")
    print(f"   - Tổng số dòng trong file: {total_lines}")
    
    if error_line_number is None:
        print(f"\n✓ Không gặp lỗi encoding. File đọc hoàn chỉnh!")
        return
    
    print(f"   - Dòng bị lỗi: {error_line_number}")
    print(f"   - File 1 sẽ có: {error_line_number - 1} dòng")
    print(f"   - File 2 sẽ có: {total_lines - error_line_number + 2} dòng (bao gồm header)")
    
    # Đọc file ở chế độ binary và tách
    with open(input_file, 'rb') as f_in:
        # Đọc header (dòng đầu tiên)
        header = f_in.readline()
        
        # Ghi File 1: Từ đầu đến trước dòng lỗi
        print(f"\n🔄 Đang ghi File 1...")
        with open(output_file1, 'wb') as f1:
            f1.write(header)  # Ghi header
            
            current_line = 1
            for line in f_in:
                current_line += 1
                if current_line < error_line_number:
                    f1.write(line)
                    if current_line % 100000 == 0:
                        print(f"   Đã ghi {current_line} dòng...")
                elif current_line >= error_line_number:
                    # Đặt lại vị trí file để đọc từ dòng lỗi
                    break
        
        print(f"✓ Đã ghi File 1 ({output_file1}): {error_line_number - 1} dòng")
    
    # Ghi File 2: Từ dòng lỗi đến hết
    print(f"\n🔄 Đang ghi File 2...")
    with open(input_file, 'rb') as f_in:
        # Ghi header
        header = f_in.readline()
        
        with open(output_file2, 'wb') as f2:
            f2.write(header)  # Ghi header
            
            # Bỏ qua các dòng trước dòng lỗi
            current_line = 1
            for line in f_in:
                current_line += 1
                if current_line < error_line_number:
                    continue
                else:
                    # Ghi từ dòng lỗi đến hết
                    f2.write(line)
                    if current_line % 100000 == 0:
                        print(f"   Đã ghi {current_line - error_line_number + 2} dòng...")
            
            # Ghi các dòng còn lại
            for line in f_in:
                f2.write(line)
                current_line += 1
                if current_line % 100000 == 0:
                    print(f"   Đã ghi {current_line - error_line_number + 2} dòng...")
    
    file2_lines = total_lines - error_line_number + 2
    print(f"✓ Đã ghi File 2 ({output_file2}): {file2_lines} dòng")
    
    print(f"\n✅ HOÀN THÀNH!")
    print(f"\nLưu ý: File 2 chứa dòng bị lỗi encoding. Bạn cần:")
    print(f"   1. Mở file trong hex editor để xem byte lỗi")
    print(f"   2. Sửa hoặc xóa dòng lỗi")
    print(f"   3. Hoặc đọc file với encoding khác (latin-1, cp1252, ...)")


# Sử dụng
if __name__ == "__main__":
    input_csv = "/home/dev01/face_search/ver3/emb_process4/ninhbinh.csv"  # File CSV đầu vào
    output_csv1 = "ninhbinh_before_error.csv"       # File từ đầu đến trước dòng lỗi
    output_csv2 = "ninhbinh_from_error.csv"         # File từ dòng lỗi đến hết
    
    split_csv_on_encoding_error(input_csv, output_csv1, output_csv2)
