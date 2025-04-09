import keyboard, mouse

from common.signals import Signals


def keyboard_listener(key: str, signals: Signals):
    keyboard.on_press_key(key, lambda _: signals.space_pressed.emit())
    keyboard.wait()


def mouse_listener(event: callable):
    mouse.hook(event)
    mouse.wait()


def handle_mouse_wheel_down_event(event, signals: Signals):
    if isinstance(event, mouse.WheelEvent) and event.delta < 0:
        signals.wheel_down.emit()
