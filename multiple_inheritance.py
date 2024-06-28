import sys

from PySide6 import QtOpenGLWidgets, QtWidgets

from cmlibs.widgets.viewwidget import ViewWidget


class A:

    def __init__(self):
        pass


class B(QtOpenGLWidgets.QOpenGLWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent


class D(QtOpenGLWidgets.QOpenGLWidget, A):

    def __init__(self, parent=None):
        QtOpenGLWidgets.QOpenGLWidget.__init__(self, parent)
        A.__init__(self)


def main():
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    d = D(w)
    print(d)

    vw = ViewWidget([{}], None, w)
    print(vw)


if __name__ == "__main__":
    main()
