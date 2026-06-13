# Chứa hàm export_to_sgf và import từ file .sgf
def coord_to_sgf(x: int, y: int, y_offset: int = 0) -> str:
    # Áp dụng offset nếu trục y của bạn không bắt đầu từ 0
    adjusted_y = y + y_offset
    
    # Kiểm tra giới hạn để đảm bảo không vượt quá bảng chữ cái 'a'-'z' (bàn cờ tối đa 26x26)
    if not (0 <= x <= 25 and 0 <= adjusted_y <= 25):
        raise ValueError(f"Tọa độ ({x}, {y}) sau khi bù trừ nằm ngoài giới hạn hợp lệ của SGF (0-25).")

    # Sử dụng bảng mã ASCII để tính toán ký tự
    col_char = chr(ord('a') + x)
    row_char = chr(ord('a') + adjusted_y)

    return f"{col_char}{row_char}"


def sgf_to_coord(sgf_str: str, y_offset: int = 0) -> tuple:
    if not isinstance(sgf_str, str) or len(sgf_str) != 2:
        raise ValueError("Chuỗi SGF không hợp lệ. Phải là một chuỗi gồm đúng 2 ký tự.")
    
    sgf_str = sgf_str.lower()
    
    # Chuyển ký tự về số nguyên bằng cách trừ đi giá trị ASCII của 'a'
    x = ord(sgf_str[0]) - ord('a')
    y = ord(sgf_str[1]) - ord('a') + y_offset
    
    if not (0 <= x <= 25 and 0 <= (y - y_offset) <= 25):
        raise ValueError(f"Ký tự '{sgf_str}' nằm ngoài giới hạn hợp lệ của SGF ('a'-'z').")

    return (x, y)
