import os, sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from slide.main import SlideCooldownBar
from fatigue.main import FatigueCooldownBar

app = QApplication(sys.argv)

icon_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
icon = QIcon(os.path.join(icon_path, "boringx.ico"))
app.setWindowIcon(icon)

slide_bar = SlideCooldownBar()
slide_bar.setWindowIcon(icon)
slide_bar.show()

fatigue_bar = FatigueCooldownBar()
fatigue_bar.setWindowIcon(icon)
fatigue_bar.show()

sys.exit(app.exec_())
