import sys
import threading
import keyboard
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer, QRect, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QColor

crouch = 'ctrl'
width = 70
height = 10
background_color = QColor(255, 0, 0)
foreground_color = QColor(0, 255, 0)


class SignalHandler(QObject):
    trigger_refresh = pyqtSignal()


class RefreshSquare(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Refresh Square")

        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - width) // 2
        y = 3 * (screen.height() - height) // 4
        self.setGeometry(x, y, width, height)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.progress = 1.0
        self.refreshing = False
        self.duration = 2000
        self.update_interval = 50
        self.elapsed = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)

        # Signal bridge between threads
        self.signals = SignalHandler()
        self.signals.trigger_refresh.connect(self.start_refresh)

        # Start key listening thread
        threading.Thread(target=self.listen_for_ctrl, daemon=True).start()

    def listen_for_ctrl(self):
        # Use keyboard hook instead of blocking wait
        keyboard.on_press_key(crouch, lambda _: self.signals.trigger_refresh.emit())
        keyboard.wait()  # Keeps the listener running

    def start_refresh(self):
        if self.refreshing:
            return
        self.progress = 0.0
        self.elapsed = 0
        self.refreshing = True
        self.timer.start(self.update_interval)

    def update_progress(self):
        self.elapsed += self.update_interval
        self.progress = min(self.elapsed / self.duration, 1.0)
        self.update()

        if self.progress >= 1.0:
            self.timer.stop()
            self.refreshing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(background_color)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, self.width(), self.height())

        fill_width = int(self.width() * self.progress)
        green_rect = QRect(0, 0, fill_width, self.height())
        painter.setBrush(foreground_color)
        painter.drawRect(green_rect)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    square = RefreshSquare()
    square.show()
    sys.exit(app.exec_())
