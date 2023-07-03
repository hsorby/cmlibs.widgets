"""
   Copyright 2023 University of Auckland

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
from PySide6 import QtCore, QtWidgets

from cmlibs.widgets.ui.ui_groupmanagerwidget import Ui_GroupManagerWidget
from cmlibs.utils.zinc.group import group_add_group_elements, group_remove_group_elements, \
    group_add_not_group_elements, group_remove_not_group_elements


NULL_PLACEHOLDER = "---"

OPERATION_MAP = {
    "Add": {"operation": group_add_group_elements, "NOT-operation": group_add_not_group_elements,
            "tooltip": "Add all nodes/elements in this group to the selected group"},
    "Remove": {"operation": group_remove_group_elements, "NOT-operation": group_remove_not_group_elements,
               "tooltip": "Remove all nodes/elements in this group from the selected group"},
}


class GroupManagerWidget(QtWidgets.QWidget):
    """
    This widget takes a list of Zinc groups as an input and provides a GUI allowing the user to redefine a specific group based on the
    nodes/elements contained in each of the other groups in the list. Calls to the GroupManagerWidget constructor must ensure that the
    group arguments are valid and non-empty.

    This widget emits a group_updated signal when the group operations are applied.

    :param current_group: The FieldGroup to add elements to.
    :param group_list: A list of FieldGroups to use for redefining the current group.
    """
    group_updated = QtCore.Signal()

    def __init__(self, parent=None, current_group=None, group_list=None):
        QtWidgets.QWidget.__init__(self, parent)
        self._ui = Ui_GroupManagerWidget()
        self._ui.setupUi(self)

        self._current_group = current_group
        self._group_map = {group.getName(): group for group in group_list}

        self._setup_widget()
        self._make_connections()

    def _setup_widget(self):
        current_group_name = self._current_group.getName()
        if current_group_name in self._group_map:
            del self._group_map[current_group_name]

        # Set the current group label text.
        self._ui.currentGroupLabel.setText(self._ui.currentGroupLabel.text() + current_group_name)

        # Setup table.
        horizontal_header = self._ui.groupTableWidget.horizontalHeader()
        horizontal_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self._create_row(0)

        self._setup_whats_this()

    def _create_row(self, i):
        self._ui.groupTableWidget.insertRow(i)

        group_combo_box = QtWidgets.QComboBox()
        group_combo_box.addItems([NULL_PLACEHOLDER] + list(self._group_map.keys()))
        group_combo_box.currentTextChanged.connect(self._group_selection_changed)

        operation_combo_box = QtWidgets.QComboBox()
        operation_combo_box.addItem(NULL_PLACEHOLDER)
        for j in range(len(OPERATION_MAP)):
            key, value = list(OPERATION_MAP.items())[j]
            operation_combo_box.addItem(key)
            operation_combo_box.setItemData(j + 1, value["tooltip"], QtCore.Qt.ToolTipRole)

        not_combo_box = QtWidgets.QComboBox()
        not_combo_box.addItems([NULL_PLACEHOLDER, "Not"])

        self._ui.groupTableWidget.setCellWidget(i, 0, group_combo_box)
        self._ui.groupTableWidget.setCellWidget(i, 1, operation_combo_box)
        self._ui.groupTableWidget.setCellWidget(i, 2, not_combo_box)

    def _setup_whats_this(self):
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowContextHelpButtonHint)
        self.setWhatsThis(
            f"""
            <html>
            The Group Manager Widget provides the ability to redefine the selected group (<i>{self._current_group.getName()}</i>) based on
            elements of other groups defined over the same model. For each line in the widget:
            
            <ul>
            <li>The <b>Group</b> combo-box defines the group of elements to be used for the operation.</li>
            <li>The <b>Operation</b> combo-box defines whether to <i>Add</i> or <i>Remove</i> elements to/from
            <i>{self._current_group.getName()}</i>.</li>
            <li>The <b>Complement</b> combo-box defines whether we should use all elements in the group or all elements <i>Not</i> in the
            group for the operation.</li>
            </ul>
            
            Group operations will be performed in the order that they are listed in the widget.
            </html>
            """
        )

    def _make_connections(self):
        self._ui.clearPushButton.clicked.connect(self._clear_table)
        self._ui.applyPushButton.clicked.connect(self._apply_group_operations)

    def get_current_group(self):
        return self._current_group

    def set_current_group(self, current_group):
        self._current_group = current_group
        self.reset()

    def get_group_list(self):
        return list(self._group_map.values())
    
    def set_group_list(self, group_list):
        self._group_map = {group.getName(): group for group in group_list}
        self.reset()

    def _clear_table(self):
        for _ in range(self._ui.groupTableWidget.rowCount()):
            self._ui.groupTableWidget.removeRow(0)
        self._create_row(0)

    def reset(self):
        self._clear_table()
        self._setup_widget()

    def _group_selection_changed(self, current_text):
        count = self._ui.groupTableWidget.rowCount()
        current_row = self._ui.groupTableWidget.currentRow()
        if current_text in self._group_map.keys():
            if current_row == count - 1:
                self._create_row(count)
        elif count > 1:
            self._ui.groupTableWidget.removeRow(current_row)

    def _apply_group_operations(self):
        for i in range(self._ui.groupTableWidget.rowCount()):
            text = self._ui.groupTableWidget.cellWidget(i, 1).currentText()
            if text in OPERATION_MAP.keys():
                group = self._group_map[self._ui.groupTableWidget.cellWidget(i, 0).currentText()]
                if self._ui.groupTableWidget.cellWidget(i, 2).currentText() == NULL_PLACEHOLDER:
                    OPERATION_MAP[text]["operation"](self._current_group, group)
                else:
                    OPERATION_MAP[text]["NOT-operation"](self._current_group, group)
        self.group_updated.emit()
