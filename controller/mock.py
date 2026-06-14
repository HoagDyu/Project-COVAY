# =====================================================================
# TÊN FILE: mocks.py
# CHỨC NĂNG: Mô phỏng toàn bộ Giao diện (UI) của Game Cờ Vây
# =====================================================================

class FakeSignal:
    """Mô phỏng cơ chế pyqtSignal của PyQt6"""
    def __init__(self):
        self._slots = []
        
    def connect(self, func):
        self._slots.append(func)
        
    def emit(self, *args, **kwargs):
        for func in self._slots:
            func(*args, **kwargs)

# ---------------------------------------------------------------------
# 1. MOCK MENU VIEW (Màn hình sảnh chờ)
# ---------------------------------------------------------------------
class MockMenuView:
    def __init__(self):
        self.pvp_start_signal = FakeSignal() # Nút: Bắt đầu PvP
        self.pve_start_signal = FakeSignal() # Nút: Bắt đầu PvE (Đánh với máy)

# ---------------------------------------------------------------------
# 2. MOCK BOARD WIDGET (Khu vực bàn cờ)
# ---------------------------------------------------------------------
class MockBoardWidget:
    def __init__(self):
        self.clicked_signal = FakeSignal() # Tương đương: Nút đặt cờ (Click lên lưới)
        
    def update(self): 
        print("[UI BÀN CỜ] 🎨 Đã quét và vẽ lại toàn bộ quân cờ trên bàn!")
        
    def draw_dead_marks(self, coords): 
        print(f"[UI BÀN CỜ] ❌ Đã vẽ dấu X đỏ tại các tọa độ: {coords}")

# ---------------------------------------------------------------------
# 3. MOCK PANEL WIDGET (Bảng điều khiển trong trận đấu)
# ---------------------------------------------------------------------
class MockPanelWidget:
    def __init__(self):
        self.pass_signal = FakeSignal()    # Nút: Bỏ lượt (Pass)
        self.resign_signal = FakeSignal()  # Nút: Đầu hàng (Resign)
        self.pause_signal = FakeSignal()   # Nút: Tạm dừng (Pause)
        self.undo_signal = FakeSignal()
        self.forward_signal = FakeSignal()     # Nút: Quay lại nước trước (Undo)
        
    def update_turn_display(self, color): 
        print(f"[UI PANEL] 🏷️ Màn hình hiển thị: Đến lượt của quân {color}")

# ---------------------------------------------------------------------
# 4. MOCK MAIN WINDOW (Khung cửa sổ tổng của ứng dụng)
# ---------------------------------------------------------------------
class MockMainWindow:
    def __init__(self):
        # Chứa tất cả các màn hình và widget con bên trong
        self.menu_view = MockMenuView()
        self.board_widget = MockBoardWidget()
        self.panel_widget = MockPanelWidget()
        
    def show_error(self, msg): 
        print(f"\n[UI POPUP ⚠️ LỖI] {msg}")
        
    def show_message(self, msg): 
        print(f"\n[UI POPUP ℹ️ THÔNG BÁO] {msg}")

    def switch_to_match_screen(self):
        """Giả lập việc UI chuyển từ màn hình Menu sang màn hình Bàn cờ"""
        print("\n[UI HỆ THỐNG] 🔄 Đã chuyển giao diện: MENU ---> BÀN CỜ")

    def switch_to_menu_screen(self):
        """Giả lập việc UI trở về sảnh chờ"""
        print("\n[UI HỆ THỐNG] 🔄 Đã chuyển giao diện: BÀN CỜ ---> MENU")