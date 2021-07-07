from PySide2 import QtWidgets, QtGui, QtCore
from opencmiss.zincwidgets.materialeditorwidget import MaterialEditorWidget
from opencmiss.zinc.material import Materialmodule
from opencmiss.argon.core.argondocument import ArgonDocument

if __name__ == '__main__':
    import sys
    filename = r"C:\Users\ywan787\neondata\argondata\heart.argon"
    try:
        with open(filename, 'r') as f:
            state = f.read()
            document = ArgonDocument()
            document.initialiseVisualisationContents()
            # set current directory to path from file, to support scripts and fieldml with external resources
            path = os.path.dirname(filename)
            os.chdir(path)
            document.deserialize(state)
    except:
        print("error")
    zincContext = document.getZincContext()
    app = QtWidgets.QApplication(sys.argv)
    w = MaterialEditorWidget()
    w.setContext(zincContext)
    w.show()
    sys.exit(app.exec_())

    model_changed = False