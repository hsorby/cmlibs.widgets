"""
Zinc Enumeration Chooser Widget

Widget for choosing an enumeration item, derived from QComboBox

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from PySide2 import QtCore, QtWidgets

import re
from opencmiss.zinc.element import Element
from opencmiss.zinc.field import Field
from opencmiss.zinc.status import OK as ZINC_OK

class EnumerationChooserWidget(QtWidgets.QComboBox):

    def __init__(self, parent=None):
        '''
        Call the super class init functions
        '''
        QtWidgets.QComboBox.__init__(self, parent)
        self._item = None

    def setEnumsList(self, enumToString, stringToEnum):
        self._enumToString = enumToString
        self._stringToEnum = stringToEnum
        self._buildItemList()

    def _buildItemList(self):
        '''
        Rebuilds the list of items in the ComboBox from the item module
        '''
        self.blockSignals(True)
        self.clear()
        i = 1
        while True:
            name = self._getStringFromEnum(i)
            if name:
                self.addItem(name)
                i += 1
            else:
                break
        self.blockSignals(False)
        self._displayItem()

    def _getStringFromEnum(self, enum):
        if self._enumToString == Field.DomainTypeEnumToString:
            enumString = self._enumToString(2**(enum - 1))
        else:
            enumString = self._enumToString(enum)
        if not enumString:
            return None
        enumString = enumString.lower()
        if bool(re.search(r'_\d', enumString)):
            enumString = enumString.replace('_', ' = ')
        else:
            enumString = enumString.replace('_', ' ')
        return enumString

    def _getEnumFromString(self, enumString):
        enumString = enumString.upper()
        if bool(re.search(r' = ', enumString)):
            enumString = enumString.replace(' = ', '_')
        else:
            enumString = enumString.replace(' ', '_')
        return self._stringToEnum(enumString)

    def _displayItem(self):
        '''
        Display the currently chosen item in the ComboBox
        '''
        self.blockSignals(True)
        if self._item:
            itemName = self._getStringFromEnum(self._item)
            index = self.findText(itemName)
        else:
            index = 0
        self.setCurrentIndex(index)
        self.blockSignals(False)

    def getItem(self):
        '''
        Must call this from currentIndexChanged() slot to get/update current item
        '''
        itemName = str(self.currentText())
        self._item = self._getEnumFromString(itemName)
        return self._item

    def setItem(self, item):
        '''
        Set the currently selected item
        '''
        if not item or not self._getStringFromEnum(item):
            self._item = None
        else:
            self._item = item
        self._displayItem()
