from PySide2 import QtWidgets

from opencmiss.zincwidgets.fields.parsers import parse_to_vector, display_vector

NONE_FIELD_TYPE_NAME = "<unknown>"
FIELD_TYPES = ['FieldAbs', 'FieldAcos', 'FieldAdd', 'FieldAlias', 'FieldAnd', 'FieldApply', 'FieldArgumentReal', 'FieldAsin', \
               'FieldAtan', 'FieldAtan2', 'FieldComponent', 'FieldConcatenate', 'FieldConstant', \
               'FieldCoordinateTransformation', 'FieldCos', 'FieldCrossProduct', 'FieldCurl', \
               'FieldDerivative', 'FieldDeterminant', 'FieldDivergence', 'FieldDivide', \
               'FieldDotProduct', 'FieldEdgeDiscontinuity', 'FieldEigenvalues', \
               'FieldEigenvectors', 'FieldEmbedded', 'FieldEqualTo', 'FieldExp', \
               'FieldFibreAxes', 'FieldFindMeshLocation', 'FieldFiniteElement', 'FieldGradient', \
               'FieldGreaterThan', 'FieldIdentity', 'FieldIf', 'FieldIsDefined', 'FieldIsExterior', \
               'FieldIsOnFace', 'FieldLessThan', 'FieldLog', 'FieldMagnitude', 'FieldMatrixInvert', \
               'FieldMatrixMultiply', 'FieldMultiply', 'FieldNodeValue', 'FieldNormalise', 'FieldNot', \
               'FieldOr', 'FieldPower', 'FieldProjection', 'FieldSin', 'FieldSqrt', \
               'FieldStoredMeshLocation', 'FieldStoredString', 'FieldStringConstant', 'FieldSubtract', \
               'FieldSumComponents', 'FieldTan', 'FieldTimeLookup', 'FieldTimeValue', 'FieldTranspose', \
               'FieldVectorCoordinateTransformation', 'FieldXor']

FIELDS_REQUIRING_REAL_LIST_VALUES = ['FieldConstant']
FIELDS_REQUIRING_STRING_VALUE = ['FieldStringConstant']
FIELDS_REQUIRING_NO_ARGUMENTS = ['FieldStoredString', 'FieldIsExterior']


class FieldRequirementBase(object):

    def __init__(self):
        super().__init__()
        self._widget = None
        self._callback = None

    @staticmethod
    def fulfilled():
        return False

    def set_callback(self, callback):
        self._callback = callback

    def widget(self):
        return self._widget


class FieldRequirementNeverMet(FieldRequirementBase):
    pass


class FieldRequirementAlwaysMet(FieldRequirementBase):

    @staticmethod
    def fulfilled():
        return True


class FieldRequirementLineEditBase(FieldRequirementBase):

    def __init__(self, label):
        super().__init__()
        self._groupbox = QtWidgets.QGroupBox()
        self._groupbox.setTitle("Parameters")
        layout = QtWidgets.QHBoxLayout(self._groupbox)
        label = QtWidgets.QLabel(label)
        self._line_edit = QtWidgets.QLineEdit()
        layout.addWidget(label)
        layout.addWidget(self._line_edit)
        self._line_edit.textEdited.connect(self._text_changed)

    def _text_changed(self):
        self._callback()

    def widget(self):
        return self._groupbox


class FieldRequirementStringValue(FieldRequirementLineEditBase):

    def __init__(self):
        super().__init__("String:")

    def value(self):
        return self._line_edit.text()

    def set_value(self, value):
        self._line_edit.setText(value)

    def fulfilled(self):
        return len(self.value()) > 0


class FieldRequirementRealListValues(FieldRequirementLineEditBase):

    def __init__(self):
        super().__init__("Values:")

    def value(self):
        return parse_to_vector(self._line_edit.text())

    def set_value(self, value):
        self._line_edit.setText(display_vector(value))

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
            elif field_type == "FieldStringConstant":
                if index != 0:
                    return
                text = self._field.evaluateString(field_cache)
                requirement.set_value(text)


class FieldTypeBase(object):

    def __init__(self):
        super().__init__()
        self._field_type = None
        self._requirements = None
        self._field = None
        self._managed = False
        self._type_coordinate = False

    def _pre_set_managed(self, state):
        self._managed = state

    def _pre_is_managed(self):
        return self._managed

    def _pre_set_type_coordinate(self, state):
        self._type_coordinate = state

    def _pre_is_type_coordinate(self):
        return self._type_coordinate

    def set_field_type(self, field_type):
        self._field_type = NONE_FIELD_TYPE_NAME
        if field_type in FIELD_TYPES:
            self._field_type = field_type

    def get_field_type(self):
        return self._field_type

    def has_requirements_met(self):
        if self._requirements is None:
            return False

        return all([r.fulfilled() for r in self._requirements])

    def requirements(self):
        if self._requirements is not None:
            return self._requirements

        self._requirements = []
        if self._field_type in FIELDS_REQUIRING_REAL_LIST_VALUES:
            self._requirements.append(FieldRequirementRealListValues())
        elif self._field_type in FIELDS_REQUIRING_STRING_VALUE:
            self._requirements.append(FieldRequirementStringValue())
        elif self._field_type in FIELDS_REQUIRING_NO_ARGUMENTS:
            self._requirements.append(FieldRequirementAlwaysMet())
        else:
            self._requirements.append(FieldRequirementNeverMet())

        return self._requirements

    def define_new_field(self, field_module, field_name):
        new_field = None
        if self._field_type == "FieldConstant":
            args = self._requirements[0].value()
            new_field = field_module.createFieldConstant(args)
        elif self._field_type == "FieldStringConstant":
            args = self._requirements[0].value()
            new_field = field_module.createFieldStringConstant(args)
        elif self._field_type in FIELDS_REQUIRING_NO_ARGUMENTS:
            methodToCall = getattr(field_module, "create" + self._field_type)
            new_field = methodToCall()

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
