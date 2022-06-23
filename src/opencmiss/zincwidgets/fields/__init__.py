from copy import copy

from PySide2 import QtWidgets
from opencmiss.zinc.field import FieldEdgeDiscontinuity, FieldFindMeshLocation

from opencmiss.zincwidgets.fieldchooserwidget import FieldChooserWidget
from opencmiss.zincwidgets.fieldconditions import FieldIsRealValued, FieldIsDeterminantEligible, FieldIsSquareMatrix, FieldIsScalar
from opencmiss.zincwidgets.fields.parsers import parse_to_vector, display_as_vector, parse_to_integer, display_as_integer, parse_to_integer_vector, display_as_integer_vector

MEASURE_TYPES = ["C1", "G1", "Surface Normal"]
MESH_NAMES = ["mesh3d", "mesh2d", "mesh1d"]
SEARCH_MODES = ["Exact", "Nearest"]

NONE_FIELD_TYPE_NAME = "<unknown>"
FIELD_TYPES = [
    'FieldAbs', 'FieldAcos', 'FieldAdd', 'FieldAlias', 'FieldAnd', 'FieldApply', 'FieldArgumentReal', 'FieldAsin',
    'FieldAtan', 'FieldAtan2', 'FieldComponent', 'FieldConcatenate', 'FieldConstant',
    'FieldCoordinateTransformation', 'FieldCos', 'FieldCrossProduct', 'FieldCurl',
    'FieldDerivative', 'FieldDeterminant', 'FieldDivergence', 'FieldDivide',
    'FieldDotProduct', 'FieldEdgeDiscontinuity', 'FieldEigenvalues',
    'FieldEigenvectors', 'FieldEmbedded', 'FieldEqualTo', 'FieldExp',
    'FieldFibreAxes', 'FieldFindMeshLocation', 'FieldFiniteElement', 'FieldGradient',
    'FieldGreaterThan', 'FieldIdentity', 'FieldIf', 'FieldIsDefined', 'FieldIsExterior',
    'FieldIsOnFace', 'FieldLessThan', 'FieldLog', 'FieldMagnitude', 'FieldMatrixInvert',
    'FieldMatrixMultiply', 'FieldMultiply', 'FieldNodeValue', 'FieldNormalise', 'FieldNot',
    'FieldOr', 'FieldPower', 'FieldProjection', 'FieldSin', 'FieldSqrt',
    'FieldStoredMeshLocation', 'FieldStoredString', 'FieldStringConstant', 'FieldSubtract',
    'FieldSumComponents', 'FieldTan', 'FieldTimeLookup', 'FieldTimeValue', 'FieldTranspose',
    'FieldVectorCoordinateTransformation', 'FieldXor'
]

FIELDS_REQUIRING_REAL_LIST_VALUES = ['FieldConstant']
FIELDS_REQUIRING_STRING_VALUE = ['FieldStringConstant']
FIELDS_REQUIRING_NO_ARGUMENTS = ['FieldStoredString', 'FieldIsExterior']
FIELDS_REQUIRING_ONE_SOURCE_FIELD = ['FieldAlias']
FIELDS_REQUIRING_ONE_REAL_SOURCE_FIELD = [
    'FieldAbs', 'FieldLog', 'FieldSqrt', 'FieldExp', 'FieldIdentity',
    'FieldConcatenate', 'FieldCrossProduct', 'FieldNot', 'FieldSin',
    'FieldCos', 'FieldTan', 'FieldAsin', 'FieldAcos', 'FieldAtan',
    'FieldMagnitude', 'FieldNormalise', 'FieldSumComponents',
    'FieldCoordinateTransformation',
]
FIELDS_REQUIRING_TWO_SOURCE_FIELDS = [
    'FieldVectorCoordinateTransformation', 'FieldCurl',
    'FieldDivergence', 'FieldEmbedded', 'FieldGradient',
    'FieldFibreAxes', 'FieldProjection', 'FieldTimeLookup',
    'FieldEqualTo',
]
FIELDS_REQUIRING_TWO_REAL_SOURCE_FIELDS = [
    'FieldAdd', 'FieldPower', 'FieldMultiply', 'FieldDivide',
    'FieldSubtract', 'FieldAnd', 'FieldGreaterThan',
    'FieldLessThan', 'FieldOr', 'FieldXor', 'FieldAtan2',
    'FieldDotProduct',
]
FIELDS_REQUIRING_ONE_DETERMINANT_SOURCE_FIELD = ['FieldDeterminant']
FIELDS_REQUIRING_ONE_SQUARE_MATRIX_SOURCE_FIELD = ['FieldEigenvalues', 'FieldMatrixInvert']
FIELDS_REQUIRING_THREE_SOURCE_FIELDS = ['FieldIf']


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


class FieldBase(object):

    def __init__(self):
        super().__init__()
        self._field = None

    def set_field(self, field):
        self._field = None
        if field and field.isValid():
            self._field = field

    def get_field(self):
        return self._field

    def _is_defined(self):
        return bool(self._field and self._field.isValid())

    def _set_type_coordinate(self, state):
        self._field.setTypeCoordinate(state)

    def _is_type_coordinate(self):
        return self._field.isTypeCoordinate()

    def _set_managed(self, state):
        self._field.setManaged(state)

    def _is_managed(self):
        return self._field.isManaged()

    def populate_requirement(self, index, requirement):
        if self._field and self._field.isValid():
            field_type = self.get_field_type()
            field_module = self._field.getFieldmodule()
            field_cache = field_module.createFieldcache()
            if field_type == "FieldConstant":
                if index != 0:
                    return
                numberOfComponents = self._field.getNumberOfComponents()
                returnedValues = self._field.evaluateReal(field_cache, numberOfComponents)
                requirement.set_value(returnedValues[1])
            elif field_type == "FieldComponent":
                if index == 0:
                    number_of_components = self._field.getNumberOfComponents()
                    component_field = self._field.castComponent()
                    values = []
                    for i in range(1, number_of_components + 1):
                        values.append(component_field.getSourceComponentIndex(i))

                    requirement.set_value(values)
                elif index == 1:
                    requirement.set_value(self._field.getSourceField(1))
            elif field_type == "FieldStringConstant":
                if index != 0:
                    return
                text = self._field.evaluateString(field_cache)
                requirement.set_value(text)
            elif field_type == "FieldTranspose":
                if index == 0:
                    requirement.set_value("")
                elif index == 1:
                    requirement.set_value(self._field.getSourceField(1))
            elif field_type in FIELDS_REQUIRING_ONE_REAL_SOURCE_FIELD or \
                    field_type in FIELDS_REQUIRING_ONE_DETERMINANT_SOURCE_FIELD or \
                    field_type in FIELDS_REQUIRING_ONE_SQUARE_MATRIX_SOURCE_FIELD or \
                    field_type in FIELDS_REQUIRING_ONE_SOURCE_FIELD or \
                    field_type in FIELDS_REQUIRING_TWO_REAL_SOURCE_FIELDS or \
                    field_type in FIELDS_REQUIRING_TWO_SOURCE_FIELDS or \
                    field_type in FIELDS_REQUIRING_THREE_SOURCE_FIELDS:
                requirement.set_value(self._field.getSourceField(index + 1))
            elif field_type == "FieldEdgeDiscontinuity":
                if index == 0:
                    requirement.set_value(self._field.getSourceField(1))
                elif index == 1:
                    index = self._field.castEdgeDiscontinuity().getMeasure()
                    requirement.set_value(index)
                elif index == 2:
                    field = self._field.castEdgeDiscontinuity().getConditionalField()
                    if field and field.isValid():
                        requirement.set_value(field)
            elif field_type == "FieldFindMeshLocation":
                if index == 0:
                    requirement.set_value(self._field.getSourceField(1))
                elif index == 1:
                    requirement.set_value(self._field.getSourceField(2))
                elif index == 2:
                    mesh_name = self._field.castFindMeshLocation().getMesh().getName()
                    requirement.set_value(mesh_name)
                elif index == 3:
                    index = self._field.castFindMeshLocation().getSearchMode()
                    requirement.set_value(index)
                elif index == 4:
                    search_mesh_name = self._field.castFindMeshLocation().getSearchMesh().getName()
                    requirement.set_value(search_mesh_name)


class FieldTypeBase(object):

    def __init__(self):
        super().__init__()
        self._field_type = None
        self._properties = None
        self._managed = False
        self._type_coordinate = False
        self._region = None

    def _pre_set_managed(self, state):
        self._managed = state

    def _pre_is_managed(self):
        return self._managed

    def _pre_set_type_coordinate(self, state):
        self._type_coordinate = state

    def _pre_is_type_coordinate(self):
        return self._type_coordinate

    def _requirements(self, kind=None):
        def _filter(p):
            if kind is None:
                return True

            return p["group"] == kind

        return [r for p in self._properties if _filter(p) for r in p["requirements"]]

    def set_region(self, region):
        self._region = region

    def set_field_type(self, field_type):
        self._field_type = NONE_FIELD_TYPE_NAME
        if field_type in FIELD_TYPES:
            self._field_type = field_type

    def get_field_type(self):
        return self._field_type

    def has_requirements_met(self):
        if self._properties is None:
            return False

        return all([r.fulfilled() for r in self._requirements()])

    def properties(self):
        if self._properties is not None:
            return self._properties

        requirements = []
        if self._field_type in FIELDS_REQUIRING_REAL_LIST_VALUES:
            requirements.append(FieldRequirementRealListValues())
        elif self._field_type in FIELDS_REQUIRING_STRING_VALUE:
            requirements.append(FieldRequirementStringValue())
        elif self._field_type in FIELDS_REQUIRING_ONE_SOURCE_FIELD:
            requirements.append(FieldRequirementSourceField(self._region, "Source Field:"))
        elif self._field_type in FIELDS_REQUIRING_NO_ARGUMENTS:
            pass
        elif self._field_type == "FieldTranspose":
            requirements.append(FieldRequirementNumberOfRows())
            requirements.append(FieldRequirementSourceField(self._region, "Source Field:", FieldIsRealValued))
        elif self._field_type == "FieldComponent":
            requirements.append(FieldRequirementComponentIndexes())
            requirements.append(FieldRequirementSourceField(self._region, "Source Field:", FieldIsRealValued))
        elif self._field_type in FIELDS_REQUIRING_ONE_REAL_SOURCE_FIELD or \
                self._field_type == "FieldEdgeDiscontinuity":
            requirements.append(FieldRequirementSourceField(self._region, "Source Field:", FieldIsRealValued))
        elif self._field_type in FIELDS_REQUIRING_TWO_SOURCE_FIELDS:
            requirements.append(FieldRequirementSourceField(self._region, "Source Field 1:"))
            requirements.append(FieldRequirementSourceField(self._region, "Source Field 2:"))
        elif self._field_type in FIELDS_REQUIRING_TWO_REAL_SOURCE_FIELDS:
            requirements.append(FieldRequirementSourceField(self._region, "Source Field 1:", FieldIsRealValued))
            requirements.append(FieldRequirementSourceField(self._region, "Source Field 2:", FieldIsRealValued))
        elif self._field_type in FIELDS_REQUIRING_THREE_SOURCE_FIELDS:
            requirements.append(FieldRequirementSourceField(self._region, "Source Field 1:", FieldIsRealValued))
            requirements.append(FieldRequirementSourceField(self._region, "Source Field 2:", FieldIsRealValued))
            requirements.append(FieldRequirementSourceField(self._region, "Source Field 3:"))
        elif self._field_type in FIELDS_REQUIRING_ONE_DETERMINANT_SOURCE_FIELD:
            requirements.append(FieldRequirementSourceField(self._region, "Source Field:", FieldIsDeterminantEligible))
        elif self._field_type in FIELDS_REQUIRING_ONE_SQUARE_MATRIX_SOURCE_FIELD:
            requirements.append(FieldRequirementSourceField(self._region, "Source Field:", FieldIsSquareMatrix))
        elif self._field_type == "FieldFindMeshLocation":
            requirements.append(FieldRequirementSourceField(self._region, "Source Field:", FieldIsRealValued))
            requirements.append(FieldRequirementSourceField(self._region, "Mesh Field:", FieldIsRealValued))
            requirements.append(FieldRequirementMeshName())
        else:
            requirements.append(FieldRequirementNeverMet())

        self._properties = [{"group": "Parameters", "requirements": requirements}]

        additional_requirements = []
        if self._field_type == "FieldEdgeDiscontinuity":
            additional_requirements.append(FieldRequirementMeasure())
            additional_requirements.append(FieldRequirementOptionalSourceField(self._region, "Conditional Field:", FieldIsScalar))
        elif self._field_type == "FieldFindMeshLocation":
            additional_requirements.append(FieldRequirementSearchMode())
            additional_requirements.append(FieldRequirementSearchMesh(self._region))

        self._properties.append({"group": "Additional Properties", "requirements": additional_requirements})

        if self._is_defined():
            for r in self._requirements():
                r.set_finalised()

        return self._properties

    def define_new_field(self, field_module, field_name):
        requirements = self._requirements("Parameters")

        args = []
        for req in requirements:
            args.append(req.value())

        methodToCall = getattr(field_module, "create" + self._field_type)
        new_field = methodToCall(*args)

        if self._field_type == "FieldEdgeDiscontinuity":
            additional_requirements = self._requirements("Additional Properties")
            new_field.setMeasure(additional_requirements[0].value())
            conditional_field = additional_requirements[1].value()
            if conditional_field and conditional_field.isValid():
                new_field.setConditionalField(conditional_field)

        new_field.setName(field_name)
        new_field.setManaged(self._managed)
        new_field.setTypeCoordinate(self._type_coordinate)

        return new_field


class FieldInterface(FieldBase, FieldTypeBase):

    def __init__(self, field, field_type):
        super(FieldInterface, self).__init__()
        self.set_field(field)
        self.set_field_type(field_type)

    def defining_field(self):
        return self.get_field() is None and self.get_field_type() != NONE_FIELD_TYPE_NAME

    def field_is_valid(self):
        return self.get_field() is not None or self.get_field_type() != NONE_FIELD_TYPE_NAME

    def field_is_defineable(self):
        return self.defining_field() and self.has_requirements_met()

    def properties_enabled(self):
        return self.get_field() is not None

    def set_managed(self, state):
        if self.defining_field():
            self._pre_set_managed(state)
        else:
            self._set_managed(state)

    def set_type_coordinate(self, state):
        if self.defining_field():
            self._pre_set_type_coordinate(state)
        else:
            self._set_type_coordinate(state)

    def is_managed(self):
        if self.defining_field():
            return self._pre_is_managed()

        return self._is_managed()

    def is_type_coordinate(self):
        if self.defining_field():
            return self._pre_is_type_coordinate()

        return self._is_type_coordinate()
