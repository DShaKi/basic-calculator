from PyQt5.QtWidgets import QPushButton, QGraphicsColorizeEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QEvent, QSize
from PyQt5.QtGui import QIcon

class Button(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.color_effect = QGraphicsColorizeEffect(self)
        self.button_palette = self.palette()
        self.color_effect.setColor(self.button_palette.color(self.backgroundRole()))
        self.color_effect.setStrength(0)
        self.setGraphicsEffect(self.color_effect)

        self.anim = QPropertyAnimation(self.color_effect, b"strength")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.color_effect.strength())
        self.anim.setEndValue(0.25)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.color_effect.strength())
        self.anim.setEndValue(0)
        self.anim.start()
        super().leaveEvent(event)

class IconButton(Button):
    def __init__(self, icon_paths: dict, mode: bool, parent=None):
        """
        icon_paths: dict with keys:
            'light_normal', 'light_hover', 'dark_normal', 'dark_hover'
            each value is a file path string to the icon image
        """
        super().__init__(parent) 

        self.icons = {
            key: QIcon(path) for key, path in icon_paths.items()
        }

        if mode:
            self.mode = "dark"
        else:
            self.mode = "light"
        
        self.setIcon(self.icons[f"{self.mode}_normal"])
        self.setIconSize(QSize(24, 24))

        self.setMouseTracking(True)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            self.setIcon(self.icons[f"{self.mode}_hover"])
        elif event.type() == QEvent.Leave:
            self.setIcon(self.icons[f"{self.mode}_normal"])
        return super().eventFilter(obj, event)

    def toggle_mode(self, mode):
        self.mode = mode
        self.setIcon(self.icons[f"{mode}_normal"])