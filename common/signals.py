from PyQt5.QtCore import QObject, pyqtSignal


class Signals(QObject):
    # crouch
    ctrl_pressed = pyqtSignal()
    v_pressed = pyqtSignal()

    # jump
    space_pressed = pyqtSignal()
    wheel_down = pyqtSignal()
