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
