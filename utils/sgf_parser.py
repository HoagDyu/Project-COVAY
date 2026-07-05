# Chứa hàm export_to_sgf và import từ file .sgf
def coord_to_sgf(x: int, y: int, y_offset: int = 0) -> str:
    
    adjusted_y = y + y_offset
    
    if not (0 <= x <= 25 and 0 <= adjusted_y <= 25):
        raise ValueError(f"Coordinates ({x}, {y}) after offset are out of valid SGF bounds (0-25).")

    col_char = chr(ord('a') + x)
    row_char = chr(ord('a') + adjusted_y)

    return f"{col_char}{row_char}"


def sgf_to_coord(sgf_str: str, y_offset: int = 0) -> tuple:
    
    if not isinstance(sgf_str, str) or len(sgf_str) != 2:
        raise ValueError("Invalid SGF string. It must be a string of exactly 2 characters.")
    
    sgf_str = sgf_str.lower()
    
    x = ord(sgf_str[0]) - ord('a')
    y = ord(sgf_str[1]) - ord('a') + y_offset
    
    if not (0 <= x <= 25 and 0 <= (y - y_offset) <= 25):
        raise ValueError(f"The SGF string '{sgf_str}' is out of valid SGF bounds ('a'-'z').")

    return (x, y)