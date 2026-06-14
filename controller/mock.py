# Tên file: mocks.py

class FakeSignal:
    def __init__(self):
        self._slots = []
        
    def connect(self, func):
        self._slots.append(func)
        
    def emit(self, *args, **kwargs):
        for func in self._slots:
            func(*args, **kwargs)

class MockBoardWidget:
    def __init__(self):
        self.clicked_signal = FakeSignal()
        
    def update(self): 
        print("[UI] 🎨 Đã quét và vẽ lại toàn bộ bàn cờ!")
        
    def draw_dead_marks(self, coords): 
        print(f"[UI] ❌ Đã vẽ dấu X đỏ tại: {coords}")

class MockPanelWidget:
    def __init__(self):
        self.pass_signal = FakeSignal()
        self.resign_signal = FakeSignal()
        
    def update_turn_display(self, color): 
        print(f"[UI] 🏷️ Chữ trên màn hình đổi thành: Lượt của {color}")

class MockMainWindow:
    def __init__(self):
        self.board_widget = MockBoardWidget()
        self.panel_widget = MockPanelWidget()
        
    def show_error(self, msg): 
        print(f"\n[UI POPUP ⚠️] LỖI: {msg}")
        
    def show_message(self, msg): 
        print(f"\n[UI POPUP ℹ️] THÔNG BÁO: {msg}")