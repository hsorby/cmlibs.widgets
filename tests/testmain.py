import os
from PySide6 import QtWidgets
from cmlibs.zincwidgets.materialeditorwidget import MaterialEditorWidget
from cmlibs.argon.argondocument import ArgonDocument

if __name__ == '__main__':
    import sys
    filename = r"c:/users/ywan787/mapclient_workflows/argon_viewer\..\..\neondata\neonheart\heart.argon"
    # filename = r"c:/users/ywan787/mapclient_workflows/argon_viewer\..\..\neondata\neoncube\colourcube.argon"
    # with open(filename, 'r') as f:
    #     state = f.read()
    #     document = ArgonDocument()
    #     document.initialiseVisualisationContents()
    #     # set current directory to path from file, to support scripts and fieldml with external resources
    #     path = os.path.dirname(filename)
    #     os.chdir(path)
    #     document.deserialize(state)

    # zincContext = document.getZincContext()
    app = QtWidgets.QApplication(sys.argv)
    # w = ExportWebGLDialog()
    w = GraphicsEditorWidget()
    # w.setZincContext(zincContext)
    w.show()
    sys.exit(app.exec_())

    model_changed = False
