from PySide6 import QtCore, QtWidgets


class CollapsibleBox(QtWidgets.QWidget):
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)

        # 1) Header button: make it expand horizontally
        self.toggle_button = QtWidgets.QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.ArrowType.RightArrow)

        # <-- Add this line to stretch the button to full width -->
        self.toggle_button.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,     # horizontal: expanding
            QtWidgets.QSizePolicy.Policy.Fixed         # vertical: fixed height
        )
        # ----------------------------------------------------------------

        # 2) Content area
        self.content_area = QtWidgets.QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.content_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        # 3) Layout
        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        # 4) Animation
        self._animation = QtCore.QPropertyAnimation(self.content_area, b"maximumHeight")
        self._animation.setDuration(200)
        self._animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        # 5) Wire toggle → animation
        self.toggle_button.toggled.connect(self._start_animation)

        # 6) Inner widget
        self.inner = QtWidgets.QWidget()
        self.inner.setLayout(QtWidgets.QVBoxLayout())
        self.content_area.setWidget(self.inner)
        self.content_area.setWidgetResizable(True)

    def _start_animation(self, checked: bool):
        self.toggle_button.setArrowType(QtCore.Qt.ArrowType.DownArrow if checked else QtCore.Qt.ArrowType.RightArrow)
        content_height = self.inner.sizeHint().height()
        start = 0 if checked else content_height
        end = content_height if checked else 0

        self._animation.stop()
        self._animation.setStartValue(start)
        self._animation.setEndValue(end)
        self._animation.start()

    def add_widget(self, widget: QtWidgets.QWidget):
        self.inner.layout().addWidget(widget)
