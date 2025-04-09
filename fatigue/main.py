import threading

from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget

from common.listeners import keyboard_listener, mouse_listener, handle_mouse_wheel_down_event
from common.signals import Signals

title = 'Fatigue Cooldown'
jump = 'space'
width = 70
height = 10
foreground_color = QColor(255, 244, 104)
cooldown_time_ms = 2000
fps = 500


class FatigueCooldownBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)

        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - width) // 2
        y = 3 * (screen.height() - height) // 4 + 20
        self.setGeometry(x, y, width, height)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.progress = 0
        self.refreshing = False
        self.cooldown = cooldown_time_ms
        self.update_interval = int(1000 / fps)
        self.elapsed = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)

        self.signals = Signals()
        self.signals.space_pressed.connect(self.refresh)
        self.signals.wheel_down.connect(self.refresh)
        self.start_listeners()

    def refresh(self):
        self.progress = 1
        self.elapsed = 0
        self.refreshing = True
        self.timer.start(self.update_interval)
        self.update()

    def update_progress(self):
        self.elapsed += self.update_interval
        self.progress = max(1 - (self.elapsed / self.cooldown), 0)
        self.update()

        if self.progress <= 0:
            self.timer.stop()
            self.refreshing = False

    def start_listeners(self):
        threading.Thread(target=keyboard_listener, args=(jump, self.signals.space_pressed), daemon=True).start()

        def handle_mwheeldown_event(event):
            handle_mouse_wheel_down_event(event, self.signals)

        threading.Thread(target=mouse_listener, args=(handle_mwheeldown_event,), daemon=True).start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)

        fill_width = int(self.width() * self.progress)
        if fill_width > 0:
            painter.setBrush(foreground_color)
            painter.drawRect(QRect(0, 0, fill_width, self.height()))
