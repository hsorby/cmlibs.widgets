from copy import copy

from PySide2 import QtWidgets
from opencmiss.zinc.field import FieldFindMeshLocation, FieldEdgeDiscontinuity

from opencmiss.zincwidgets.fieldchooserwidget import FieldChooserWidget
from opencmiss.zincwidgets.fields.lists import MESH_NAMES, SEARCH_MODES, MEASURE_TYPES
from opencmiss.zincwidgets.fields.parsers import display_as_vector, parse_to_vector, display_as_integer_vector, parse_to_integer_vector, display_as_integer, parse_to_integer


class FieldRequirementBase(object):

    def __init__(self):
        super().__init__()
        self._widget = QtWidgets.QFrame()
        self._callback = None
        self._finalised = False

    @staticmethod
    def fulfilled():
        return False

    def set_callback(self, callback):
        self._callback = callback

    def widget(self):
        return self._widget

    def set_finalised(self):
        self._finalised = True


class FieldRequirementNeverMet(FieldRequirementBase):
    pass


class FieldRequirementAlwaysMet(FieldRequirementBase):

    @staticmethod
    def fulfilled():
        return True


class FieldRequirementComboBoxBase(FieldRequirementBase):

    def __init__(self, label, items):
        super().__init__()
        self._widget = QtWidgets.QFrame()
        layout = QtWidgets.QHBoxLayout(self._widget)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QtWidgets.QLabel(label)
        self._combobox = QtWidgets.QComboBox(self._widget)
        self._combobox.addItems(items)
        layout.addWidget(label)
        layout.addWidget(self._combobox)

    def value(self):
        return self._combobox.currentIndex()

    def set_value(self, value):
        self._combobox.setCurrentIndex(value)

    def fulfilled(self):
        return True

    def set_finalised(self):
        self._combobox.setEnabled(False)


class FieldRequirementMeasure(FieldRequirementComboBoxBase):

    def __init__(self):
        super().__init__("Measure:", MEASURE_TYPES)

    def value(self):
        return self._combobox.currentIndex() + FieldEdgeDiscontinuity.MEASURE_C1

    def set_value(self, value):
        self._combobox.setCurrentIndex(value - FieldEdgeDiscontinuity.MEASURE_C1)


class FieldRequirementMeshName(FieldRequirementComboBoxBase):

    def __init__(self):
        super().__init__("Mesh:", MESH_NAMES)


class FieldRequirementSearchMode(FieldRequirementComboBoxBase):

    def __init__(self):
        super().__init__("Search mode:", SEARCH_MODES)

    def value(self):
        return self._combobox.currentIndex() + FieldFindMeshLocation.SEARCH_MODE_EXACT

    def set_value(self, value):
        self._combobox.setCurrentIndex(value - FieldFindMeshLocation.SEARCH_MODE_EXACT)


class FieldRequirementSearchMesh(FieldRequirementComboBoxBase):

    def __init__(self, region):
        search_mesh_names = copy(MESH_NAMES)
        field_module = region.getFieldmodule()
        field_iterator = field_module.createFielditerator()
        field = field_iterator.next()
        while field.isValid():
            if field.castElementGroup().isValid():
                search_mesh_names.append(field.getName())
            field = field_iterator.next()
        super().__init__("Search mesh:", search_mesh_names)


class FieldRequirementSourceFieldBase(FieldRequirementBase):

    def __init__(self, region, label, conditional_constraint):
        super().__init__()
        self._widget = QtWidgets.QFrame()
        layout = QtWidgets.QHBoxLayout(self._widget)
        layout.setContentsMargins(0, 0, 0, 0)
        label_widget = QtWidgets.QLabel(label)
        self._source_field_chooser = FieldChooserWidget(self._widget)
        self._source_field_chooser.setObjectName("field_requirements_source_field_base_chooser")
        self._source_field_chooser.set_listen_for_field_notifications(False)
        self._source_field_chooser.allowUnmanagedField(True)
        self._source_field_chooser.setNullObjectName("-")
        self._source_field_chooser.setRegion(region)
        if conditional_constraint is not None:
            self._source_field_chooser.setConditional(conditional_constraint)
        layout.addWidget(label_widget)
        layout.addWidget(self._source_field_chooser)
        self._source_field_chooser.currentTextChanged.connect(self._field_changed)

    def _field_changed(self):
        self._callback()

    def value(self):
        return self._source_field_chooser.getField()

    def set_value(self, value):
        self._source_field_chooser.setField(value)

    def fulfilled(self):
        region = self._source_field_chooser.getRegion()
        if region is None:
            return False

        field = self._source_field_chooser.getField()
        return True if field and field.isValid() else False

    def set_finalised(self):
        self._source_field_chooser.setEnabled(False)


class FieldRequirementSourceField(FieldRequirementSourceFieldBase):

    def __init__(self, region, label, conditional_constraint=None):
        super().__init__(region, label, conditional_constraint)


class FieldRequirementOptionalSourceField(FieldRequirementSourceFieldBase):

    def __init__(self, region, label, conditional_constraint=None):
        super().__init__(region, label, conditional_constraint)

    def fulfilled(self):
        return True


class FieldRequirementLineEditBase(FieldRequirementBase):

    def __init__(self, label):
        super().__init__()
        self._widget = QtWidgets.QFrame()
        layout = QtWidgets.QHBoxLayout(self._widget)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QtWidgets.QLabel(label)
        self._line_edit = QtWidgets.QLineEdit()
        layout.addWidget(label)
        layout.addWidget(self._line_edit)
        self._line_edit.textEdited.connect(self._text_changed)

    def _text_changed(self):
        self._callback()

    def set_finalised(self):
        self._line_edit.setEnabled(False)


class FieldRequirementStringValue(FieldRequirementLineEditBase):

    def __init__(self):
        super().__init__("String:")

    def value(self):
        return self._line_edit.text()

    def set_value(self, value):
        self._line_edit.setText(value)

    def fulfilled(self):
        return len(self.value()) > 0


class FieldRequirementNaturalNumberValue(FieldRequirementLineEditBase):

    def __init__(self, label):
        super().__init__(label)

    def value(self):
        return parse_to_integer(self._line_edit.text())

    def set_value(self, value):
        self._line_edit.setText(display_as_integer(value))

    def fulfilled(self):
        value = self.value()
        return False if value is None else value > 0


class FieldRequirementNumberOfRows(FieldRequirementNaturalNumberValue):

    def __init__(self):
        super(FieldRequirementNumberOfRows, self).__init__("Number of Rows:")


class FieldRequirementComponentIndexes(FieldRequirementLineEditBase):

    def __init__(self):
        super().__init__("Component Indices:")

    def value(self):
        return parse_to_integer_vector(self._line_edit.text())

    def set_value(self, value):
        self._line_edit.setText(display_as_integer_vector(value))

    def fulfilled(self):
        values = self.value()
        return False if len(values) == 0 else all([v > 0 for v in values])


class FieldRequirementRealListValues(FieldRequirementLineEditBase):

    def __init__(self):
        super().__init__("Values:")

    def value(self):
        return parse_to_vector(self._line_edit.text())

    def set_value(self, value):
        self._line_edit.setText(display_as_vector(value))

    def fulfilled(self):
        return len(self.value()) > 0
