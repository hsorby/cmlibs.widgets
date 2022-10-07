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
from PySide2 import QtWidgets

from opencmiss.zincwidgets.ui.ui_consoleeditorwidget import Ui_ConsoleEditorWidget


class ConsoleEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self._ui = Ui_ConsoleEditorWidget()
        self._ui.setupUi(self)

    def setZincContext(self, zinc_context):
        self._ui.interactiveConsoleWidget.set_context(zinc_context)

    def setDocument(self, document):
        self._ui.interactiveConsoleWidget.set_document(document)