from PyQt5.QtWidgets import QPushButton, QGraphicsColorizeEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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
