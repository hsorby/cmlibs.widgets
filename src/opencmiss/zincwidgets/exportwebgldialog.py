"""
   Copyright 2016 University of Auckland

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from PySide2 import QtWidgets, QtGui, QtCore

from opencmiss.zincwidgets.fieldconditions import *
from opencmiss.zinc.field import Field
from opencmiss.zinc.status import OK as ZINC_OK
from opencmiss.zincwidgets.ui.ui_exportwebglwidget import Ui_ExportWebGLWidget
from opencmiss.utils.zinc.general import ChangeManager

def QLineEdit_parseRealNonNegative(lineedit):
    """
    Return non-negative real value from line edit text, or negative if failed.
    """
    try:
        value = float(lineedit.text())
        if value >= 0.0:
            return value
    except:
        pass
    return -1.0

class ExportWebGLDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        """
        Call the super class init functions
        """
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_ExportWebGLWidget()
        self._ui.setupUi(self)
        self._argonModel = None

        self._makeConnections()


    def _makeConnections(self):
        self._ui.export_button.clicked.connect(self._exportWebGLClicked)
        self._ui.prefix_lineEdit.editingFinished.connect(self._prefixEntered)
        self._ui.timeSteps_lineEdit.editingFinished.connect(self._timeStepsEntered)
        self._ui.initialTime_lineEdit.editingFinished.connect(self._initialTimeEntered)
        self._ui.finishTime_lineEdit.editingFinished.connect(self._finishTimeEntered)

    def _displayExportWebGL(self):
        """
        Display the currently chosen exportWebGL
        """
        self._ui.prefix_lineEdit.setText(self._argonModel._prefix)
        self._ui.timeSteps_lineEdit.setText(str(self._argonModel._numberOfTimeSteps))
        self._ui.initialTime_lineEdit.setText(str(self._argonModel._initialTime))
        self._ui.finishTime_lineEdit.setText(str(self._argonModel._finishTime))

    def _prefixEntered(self):
        value = self._ui.prefix_lineEdit.text()
        self._argonModel._prefix = value

    def _timeStepsEntered(self):
        value = self._ui.timeSteps_lineEdit.text()
        self._argonModel._numberOfTimeSteps = float(value)

    def _initialTimeEntered(self):
        value = self._ui.initialTime_lineEdit.text()
        self._argonModel._initialTime = float(value)

    def _finishTimeEntered(self):
        value = self._ui.finishTime_lineEdit.text()
        self._argonModel._finishTime = float(value)
    
    def _exportWebGLClicked(self):
        """
        Export a new WebGL.
        """
        self.accept()

    def setArgonModel(self, argonModel):
        """
        Sets the region that this widget chooses exportWebGLs from
        """
        self._argonModel = argonModel
        self._displayExportWebGL()
