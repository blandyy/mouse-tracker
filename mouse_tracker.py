import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtCore import Qt, QTimer, QPoint
from pynput import keyboard, mouse


class MouseTracker(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("屏幕坐标捕获器")
        self.setGeometry(100, 100, 300, 50)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # 用于显示鼠标当前坐标的标签
        self.coord_label = QLabel("当前坐标: (0, 0)", self)
        self.coord_label.setAlignment(Qt.AlignCenter)

        # 用于显示固定坐标的提示标签
        self.fixed_remark_label = QLabel("按Ctrl+右键点击固定坐标", self)
        self.fixed_remark_label.setAlignment(Qt.AlignCenter)

        # 用于显示固定坐标的标签
        self.fixed_coord_label = QLabel("固定坐标: ", self)
        self.fixed_coord_label.setAlignment(Qt.AlignCenter)

        # 布局设置
        layout = QVBoxLayout()
        layout.addWidget(self.coord_label)
        layout.addWidget(self.fixed_remark_label)
        layout.addWidget(self.fixed_coord_label)
        self.setLayout(layout)

        # 初始化变量
        self.fixed_point = None  # 记录的固定坐标
        self.ctrl_pressed = False  # ctrl是否被按下

        # 定时器用于实时更新鼠标位置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_coordinates)
        self.timer.start(100)

        # 全局键盘监听器
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press, on_release=self.on_key_release
        )
        self.keyboard_listener.start()

        # 全局鼠标监听器
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.mouse_listener.start()

    def update_coordinates(self):
        """实时更新当前鼠标的坐标位置"""
        pos = QCursor.pos()
        # 获取屏幕缩放比例
        screen = QGuiApplication.screenAt(pos)
        dpi_scale = screen.devicePixelRatio()
        scaled_pos = pos * dpi_scale  # 考虑DPI缩放比例
        self.coord_label.setText(f"当前坐标: ({scaled_pos.x()}, {scaled_pos.y()})")

    def on_mouse_click(self, x, y, button, pressed):
        if pressed and button == mouse.Button.right and self.ctrl_pressed:
            self.fixed_point = QPoint(x, y)
            self.fixed_coord_label.setText(
                f"固定坐标: ({self.fixed_point.x()}, {self.fixed_point.y()})"
            )

    def on_key_press(self, key):
        if key == keyboard.Key.esc:
            self.fixed_point = None
            self.fixed_coord_label.setText("固定坐标: ")
        elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            self.ctrl_pressed = True  # 设置标志变量为true，代表ctrl一直被按下

    def on_key_release(self, key):
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            self.ctrl_pressed = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MouseTracker()
    window.show()
    sys.exit(app.exec())
