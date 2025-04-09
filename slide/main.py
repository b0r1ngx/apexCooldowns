import threading

from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget

from common.listeners import keyboard_listener
from common.signals import Signals

title = 'Slide Cooldown'
keys = ('ctrl', 'v')
width = 70
height = 10
background_color = QColor(255, 61, 0)
foreground_color = QColor(0, 255, 118)
cooldown_time_ms = 2000
fps = 500


class SlideCooldownBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)

        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - width) // 2
        y = 3 * (screen.height() - height) // 4
        self.setGeometry(x, y, width, height)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.progress = 1
        self.refreshing = False
        self.cooldown = cooldown_time_ms
        self.update_interval = int(1000 / fps)
        self.elapsed = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)

        self.signals = Signals()
        self.signals.ctrl_pressed.connect(self.refresh)
        self.signals.v_pressed.connect(self.refresh)
        self.start_listeners()

    def refresh(self):
        # use this, if you don't need to refresh when it is in refreshing state
        # if self.refreshing:
        #     return
        self.progress = 0
        self.elapsed = 0
        self.refreshing = True
        self.timer.start(self.update_interval)

    def update_progress(self):
        self.elapsed += self.update_interval
        self.progress = min(self.elapsed / self.cooldown, 1)
        self.update()

        if self.progress >= 1:
            self.timer.stop()
            self.refreshing = False

    def start_listeners(self):
        for key in keys:
            if key == 'ctrl':
                signal = self.signals.ctrl_pressed
            else:
                signal = self.signals.v_pressed
            threading.Thread(target=keyboard_listener, args=(key, signal), daemon=True).start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(background_color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, self.width(), self.height())

        fill_width = int(self.width() * self.progress)
        green_rect = QRect(0, 0, fill_width, self.height())
        painter.setBrush(foreground_color)
        painter.drawRect(green_rect)
