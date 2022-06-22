from PySide2 import QtWidgets, QtCore


class FieldPropertiesWidget(QtWidgets.QWidget):

    requirementChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super(FieldPropertiesWidget, self).__init__(parent)
        self._field = None
        self._vertical_layout = QtWidgets.QVBoxLayout(self)

    def set_field(self, field):
        self._clear_ui()
        self._field = field
        if self._field.field_is_valid():
            self._setup_ui()

    def _clear_ui(self):
        for i in reversed(range(self._vertical_layout.count())):
            widget_to_remove = self._vertical_layout.itemAt(i).widget()
            # remove it from the layout list
            self._vertical_layout.removeWidget(widget_to_remove)
            # remove it from the GUI
            widget_to_remove.setParent(None)

    def clear_field(self):
        self._field = None
        self._clear_ui()

    def _setup_ui(self):
        # Every field has a title and global properties.
        self._setup_title()
        self._setup_properties()
        # Setup field specific widgets.
        for index, req in enumerate(self._field.requirements()):
            self._setup_requirement(req)
            self._field.populate_requirement(index, req)
        self.show()

    def _setup_title(self):
        self._title_groupbox = QtWidgets.QGroupBox(self)
        self._title_groupbox.setTitle(u"Field type")
        self._title_layout = QtWidgets.QVBoxLayout(self._title_groupbox)
        self._title_label = QtWidgets.QLabel(self._field.get_field_type())
        self._title_layout.addWidget(self._title_label)
        self._vertical_layout.addWidget(self._title_groupbox)

    def _setup_properties(self):
        is_managed = self._field.is_managed()
        is_type_coordinate = self._field.is_type_coordinate()

        self._properties_groupbox = QtWidgets.QGroupBox(self)
        self._properties_groupbox.setTitle(u"Properties")
        # self._properties_groupbox.setObjectName(u"_properties_groupbox")
        # self._properties_groupbox.setEnabled(self._field.properties_enabled())
        # self._properties_groupbox.setCheckable(False)
        self._properties_layout = QtWidgets.QVBoxLayout(self._properties_groupbox)
        # self._properties_layout.setObjectName(u"_properties_layout")
        self._type_coordinate_checkbox = QtWidgets.QCheckBox(self._properties_groupbox)
        self._type_coordinate_checkbox.setCheckState(QtCore.Qt.Checked if is_type_coordinate else QtCore.Qt.Unchecked)
        self._type_coordinate_checkbox.stateChanged.connect(self._type_coordinate_clicked)
        # self._type_coordinate_checkbox.setObjectName(u"_type_coordinate_checkbox")
        self._type_coordinate_checkbox.setText(u"Is Coordinate")
        self._managed_checkbox = QtWidgets.QCheckBox(self._properties_groupbox)
        self._managed_checkbox.setEnabled(not self._field.defining_field())
        self._managed_checkbox.setCheckState(QtCore.Qt.Checked if is_managed else QtCore.Qt.Unchecked)
        self._managed_checkbox.stateChanged.connect(self._managed_clicked)
        # self._managed_checkbox.setObjectName(u"_managed_checkbox")
        self._managed_checkbox.setText(u"Managed")

        self._properties_layout.addWidget(self._managed_checkbox)
        self._properties_layout.addWidget(self._type_coordinate_checkbox)

        self._vertical_layout.addWidget(self._properties_groupbox)

    def _managed_clicked(self, state):
        self._field.set_managed(state == QtCore.Qt.Checked)

    def _type_coordinate_clicked(self, state):
        self._field.set_type_coordinate(state == QtCore.Qt.Checked)

    def _setup_requirement(self, req):
        req.set_callback(self._requirement_changed)
        widget = req.widget()
        if widget is not None:
            self._vertical_layout.addWidget(widget)

    def _requirement_changed(self):
        self.requirementChanged.emit()
