# Project-COVAY

Ứng dụng Cờ Vây (Go) viết bằng Python và PyQt6, hỗ trợ chơi:

- Người vs Người (PVP)
- Người vs Máy (PVE) với bot heuristic cơ bản

Mục tiêu của dự án là mô phỏng đầy đủ một ván Cờ Vây trên giao diện desktop, gồm đặt quân, bắt quân, pass, resign, đồng hồ đếm thời gian và tính điểm cuối ván theo territory + prisoner + komi.

## Tính năng chính

- Menu chọn cấu hình trước trận:
  - Kích thước bàn: 9x9, 13x13, 19x19
  - Thời gian mỗi bên: 1, 3, 5, 15, 30 phút
  - Màu của bot trong chế độ PVE
- Luật cơ bản:
  - Kiểm tra nước đi hợp lệ
  - Không được đi vào ô đã có quân
  - Chặn nước tự sát
  - Bắt quân theo nhóm hết khí
  - Kết thúc ván khi hai bên pass liên tiếp
- Điều khiển trận đấu:
  - Pass, Resign, Pause/Resume
  - Chế độ cleaning và xác nhận kết thúc
  - Đồng hồ riêng cho Đen/Trắng, xử thua khi hết giờ
- AI bot:
  - Duyệt tất cả nước hợp lệ
  - Chấm điểm heuristic (trung tâm, hàng xóm đồng minh/đối thủ, khí, độ nguy hiểm)
  - Chọn ngẫu nhiên trong nhóm nước tốt nhất
- Tiện ích SGF:
  - Chuyển đổi tọa độ nội bộ <-> định dạng SGF (`aa`..`zz`) trong `utils/sgf_parser.py`

## Kiến trúc dự án

Dự án tổ chức theo hướng MVC:

- Model (`model/`):
  - `entities.py`: định nghĩa `Player`, `Cell`, `Move`, `CellGroup`
  - `board_logic.py`: logic bàn cờ, bắt quân, pass, tính territory, tính điểm
  - `rules.py`: kiểm tra luật (hợp lệ, ô trống, suicide, ko)
- View (`view/`):
  - `main_window.py`: cửa sổ chính và điều hướng màn hình
  - `menu_widget.py`: màn hình menu cấu hình trận
  - `match_screen.py`: layout trận đấu
  - `board_widget.py` + `cell_widget.py`: vẽ bàn cờ và ô
  - `panel_widget.py`: panel thao tác, prisoners, đồng hồ
- Controller (`controller/`):
  - `game_manager.py`: điều phối trận đấu, trạng thái game, tương tác giữa view và model
- AI (`ai/`):
  - `class_bot.py`: định nghĩa bot và worker chạy trên thread
  - `bot_algorithm.py`: thuật toán chọn nước đi heuristic

## Cấu trúc thư mục

```text
Project-COVAY/
|-- main.py
|-- requirements.txt
|-- ai/
|-- controller/
|-- core/
|-- model/
|-- utils/
|-- view/
|   |-- ui/
|-- assets/
|   |-- images/
|-- tests/
|-- output/
```

## Yêu cầu môi trường

- Python 3.10+ (khuyến nghị 3.11)
- Hệ điều hành: Windows/macOS/Linux

Thư viện chính:

- `PyQt6==6.11.0`
- `PyQt6-Qt6==6.11.1`
- `PyQt6_sip==13.11.1`
- `PyQt5Designer==5.14.1` (hỗ trợ thiết kế UI)

## Cài đặt và chạy

### 1. Tạo môi trường ảo

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Cài dependencies

```powershell
pip install -r requirements.txt
```

### 3. Chạy ứng dụng

```powershell
python main.py
```

## Cách chơi nhanh

1. Chọn chế độ `PVP` hoặc `PVE` ở menu.
2. Chọn kích thước bàn, thời gian, và màu bot (nếu PVE).
3. Trong trận đấu:
   - Click vào giao điểm để đặt quân.
   - Dùng `Pass` để bỏ lượt.
   - `Resign` để đầu hàng.
   - `Pause` để tạm dừng đồng hồ.
4. Ván kết thúc khi:
   - Hai bên pass liên tiếp, hoặc
   - Một bên resign, hoặc
   - Một bên hết giờ.
