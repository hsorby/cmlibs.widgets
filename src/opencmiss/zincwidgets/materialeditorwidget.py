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
from opencmiss.zinc.material import Material
from opencmiss.zinc.glyph import Glyph
from opencmiss.zinc.status import OK as ZINC_OK
from opencmiss.zincwidgets.ui.ui_materialeditorwidget import Ui_MaterialEditor
from opencmiss.utils.zinc.general import ChangeManager


class MaterialEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        """
        Call the super class init functions
        """
        QtWidgets.QWidget.__init__(self, parent)
        self._ui = Ui_MaterialEditor()
        self._ui.setupUi(self)

        self._zincContext = None
        self._previewZincRegion = None
        self._nullObjectName = None
        self._materials = None
        self._materialmodulenotifier = None
        self._currentMaterial = None
        self._previewZincScene = None

        self._materialItems = QtGui.QStandardItemModel(self._ui.materials_listView)
        self._makeConnections()

    def _makeConnections(self):
        self._ui.create_button.clicked.connect(self._materialCreateClicked)
        self._ui.delete_button.clicked.connect(self._materialDeleteClicked)
        self._ui.materials_listView.clicked[QtCore.QModelIndex].connect(self._materialListItemClicked)
        self._ui.ambientSelectColour_button.clicked.connect(self._selectColourClicked)
        self._ui.diffuseSelectColour_button.clicked.connect(self._selectColourClicked)
        self._ui.emittedSelectColour_button.clicked.connect(self._selectColourClicked)
        self._ui.specularSelectColour_button.clicked.connect(self._selectColourClicked)
        self._ui.alpha_lineEdit.editingFinished.connect(self._alphaEntered)
        self._ui.alpha_slider.valueChanged.connect(self._alphaSliderValueChanged)
        self._ui.shininess_lineEdit.editingFinished.connect(self._shininessEntered)
        self._ui.shininess_slider.valueChanged.connect(self._shininessSliderValueChanged)
        self._ui.sceneviewerWidgetPreview.graphicsInitialized.connect(self._previewGraphicsInitialised)
        self._ui.texture_comboBox.currentIndexChanged.connect(self._textureChanged)
        self._ui.region_comboBox.currentIndexChanged.connect(self._regionChanged)
        self._ui.imageField_comboBox.currentIndexChanged.connect(self._imageFieldChanged)

    def setMaterials(self, materials):
        """
        Sets the Argon materials object which supplies the zinc context and has utilities for
        managing materials.
        :param materials: ArgonMaterials object
        """
        self._materials = materials
        self._zincContext = materials.getZincContext()
        self._ui.sceneviewerWidgetPreview.setContext(self._zincContext)
        self._previewZincRegion = self._zincContext.createRegion()
        self._previewZincRegion.setName("Material editor preview region")
        self._previewZincScene = self._previewZincRegion.getScene()
        self._buildMaterialList()
        sceneviewer = self._ui.sceneviewerWidgetPreview.getSceneviewer()
        if sceneviewer:
            self._setupPreviewScene(sceneviewer)
        # material_module = self._zincContext.getMaterialmodule()
        # self._materialmodulenotifier = material_module.createMaterialmodulenotifier()
        # self._materialmodulenotifier.setCallback(self._materialmoduleCallback)
        self._buildMaterialList()

    def _materialmoduleCallback(self, materialModuleEvent):
        changeSummary = materialModuleEvent.getSummarySpectrumChangeFlags()
        # print("Material Editor: _materialmoduleCallback changeSummary " + str(changeSummary))
        if 0 != (changeSummary & (Material.CHANGE_FLAG_IDENTIFIER | Material.CHANGE_FLAG_ADD | Material.CHANGE_FLAG_REMOVE)):
            self._buildSpectrumList()

    def _materialCreateClicked(self):
        """
        Create a new material.
        """
        name = 'temp'
        mm = self._zincContext.getMaterialmodule()
        with ChangeManager(mm):
            material = mm.createMaterial()
            material.setName(name)
            material.setManaged(True)
        self._addMaterialToModelList(material)

    def _addMaterialToModelList(self, material, row=0):
        item = QtGui.QStandardItem(material.getName())
        item.setData(material)
        item.setEditable(True)
        self._materialItems.insertRow(row, item)
        index = self._materialItems.indexFromItem(item)
        self._ui.materials_listView.setCurrentIndex(index)
        self._updateCurrentMaterial(material)

    def _renameMaterial(self, material, name):
        """
        Renames material
        :return True on success, otherwise False (means name not set)
        """
        result = material.setName(name)
        if result == ZINC_OK:
            return True
        return False

    def _materialDeleteClicked(self):
        """
        Delete the currently selected material.
        """
        self._clearPreview()
        self._removeMaterialByName(self._currentMaterial.getName())

    def _removeMaterialByName(self, name):
        """
        Unmanages material. Note material is only removed if not in use.
        :return True if material removed, false if failed.
        """
        self._currentMaterial = None
        sm = self._zincContext.getMaterialmodule()
        items = self._materialItems.findItems(name)
        item = items[0]
        row = item.row()
        self._materialItems.removeRow(row)
        del item
        material = sm.findMaterialByName(name)
        material.setManaged(False)
        del material
        material = sm.findMaterialByName(name)
        if material.isValid():
            # I'm still in use.
            material.setManaged(True)
            successfully_removed = False
            self._addMaterialToModelList(material, row)
            QtWidgets.QMessageBox.information(self, "Info", "This material is still in use and can't be deleted.")
        else:
            successfully_removed = True
            if row < self._materialItems.rowCount():
                index = self._materialItems.index(row,0)
            else:
                index = self._materialItems.index(row - 1,0)
            self._ui.materials_listView.setCurrentIndex(index)
            item = self._materialItems.itemFromIndex(index)
            self._updateCurrentMaterial(item.data())
        return successfully_removed

    def _buildMaterialList(self):
        """
        Rebuilds the list of items in the Listview from the material module
        """
        selectedIndex = None
        mm = self._zincContext.getMaterialmodule()

        if self._nullObjectName:
            self._ui.material_listView.addItem(self._nullObjectName)
        material_iter = mm.createMaterialiterator()
        material = material_iter.next()
        if not self._currentMaterial:
            self._updateCurrentMaterial(material)
        while material.isValid():
            name = material.getName()
            item = QtGui.QStandardItem(name)
            item.setData(material)
            item.setEditable(True)
            self._materialItems.appendRow(item)
            if material.getName() == self._currentMaterial.getName():
                selectedIndex = self._materialItems.indexFromItem(item)
            material = material_iter.next()
        self._ui.materials_listView.setModel(self._materialItems)
        if selectedIndex:
            self._ui.materials_listView.setCurrentIndex(selectedIndex)
        self._materialItems.itemChanged.connect(self._onMaterialItemChanged)
        itemDelegate = QtWidgets.QItemDelegate(self._ui.materials_listView)
        self._ui.materials_listView.setItemDelegate(itemDelegate)
        self._ui.materials_listView.show()

    def _onMaterialItemChanged(self, item):
        """
        For QStandardItemModel ItemChanged Signal, catch the item text edit event.
        Update the material name.
        """ 
        newName = item.text()
        if self._renameMaterial(item.data(), newName):
            return
        item.setText(item.data().getName())
        QtWidgets.QMessageBox.information(self, "Info", "Can't change this material's name to %s."%newName)

    def _materialListItemClicked(self, modelIndex):
        item = modelIndex.model().itemFromIndex(modelIndex)
        if item.data() != self._currentMaterial:
           self._updateCurrentMaterial(item.data())

    def _updateCurrentMaterial(self, material):
        self._currentMaterial = material
        self._displayMaterial()

    def _displayMaterial(self):
        """
        Display the currently chosen material
        """
        self._updateButtonColour()
        self._updateAlpha()
        self._updateShininess()
        self._buildTextureComboBox()
        self._buildRegionComboBox()
        self._previewMaterial()

    def _updateButtonColour(self):
        ambientColour, diffuseColour, emissionColour, specularColour = self._getCurrentMaterialColour()
        self._ui.ambientSelectColour_button.setStyleSheet("background-color: {}".format(ambientColour.name()))
        self._ui.diffuseSelectColour_button.setStyleSheet("background-color: {}".format(diffuseColour.name()))
        self._ui.emittedSelectColour_button.setStyleSheet("background-color: {}".format(emissionColour.name()))
        self._ui.specularSelectColour_button.setStyleSheet("background-color: {}".format(specularColour.name()))

    def _getCurrentMaterialColour(self):
        result, ambientColour = self._currentMaterial.getAttributeReal3(Material.ATTRIBUTE_AMBIENT)
        result, diffuseColour = self._currentMaterial.getAttributeReal3(Material.ATTRIBUTE_DIFFUSE)
        result, emissionColour = self._currentMaterial.getAttributeReal3(Material.ATTRIBUTE_EMISSION)
        result, specularColour = self._currentMaterial.getAttributeReal3(Material.ATTRIBUTE_SPECULAR)
        intAmbientColour = QtGui.QColor(int(ambientColour[0]*255), int(ambientColour[1]*255), int(ambientColour[2]*255))
        intDiffuseColour = QtGui.QColor(int(diffuseColour[0]*255), int(diffuseColour[1]*255), int(diffuseColour[2]*255))
        intEmissionColour = QtGui.QColor(int(emissionColour[0]*255), int(emissionColour[1]*255), int(emissionColour[2]*255))
        intSpecularColour = QtGui.QColor(int(specularColour[0]*255), int(specularColour[1]*255), int(specularColour[2]*255))
        return intAmbientColour, intDiffuseColour, intEmissionColour, intSpecularColour

    def _selectColourClicked(self, event):
        sender = self.sender()
        colorDialog = QtWidgets.QColorDialog(sender)
        colorDialog.setCurrentColor(sender.palette().button().color())
        color = colorDialog.getColor(initial = sender.palette().button().color())
        if color.isValid():
            self.sender().setStyleSheet("background-color: {}".format(color.name()))
            self._setMaterialColour(sender)
    
    def _setMaterialColour(self, attributeButton):
        if attributeButton == self._ui.ambientSelectColour_button:
            materialAttribute = Material.ATTRIBUTE_AMBIENT
        elif attributeButton == self._ui.diffuseSelectColour_button:
            materialAttribute = Material.ATTRIBUTE_DIFFUSE
        elif attributeButton == self._ui.emittedSelectColour_button:
            materialAttribute = Material.ATTRIBUTE_EMISSION
        elif attributeButton == self._ui.specularSelectColour_button:
            materialAttribute = Material.ATTRIBUTE_SPECULAR
        buttonColour = attributeButton.palette().button().color()
        colourF = [buttonColour.redF(), buttonColour.greenF(), buttonColour.blueF()]
        self._currentMaterial.setAttributeReal3(materialAttribute, colourF)

    def _alphaEntered(self):
        value = self._ui.alpha_lineEdit.text()
        self._currentMaterial.setAttributeReal(Material.ATTRIBUTE_ALPHA, float(value))
        self._updateAlpha()

    def _alphaSliderValueChanged(self):
        value = self._ui.alpha_slider.value()/100
        self._currentMaterial.setAttributeReal(Material.ATTRIBUTE_ALPHA, value)
        self._updateAlpha()

    def _updateAlpha(self):
        alpha = self._currentMaterial.getAttributeReal(Material.ATTRIBUTE_ALPHA)
        self._ui.alpha_slider.setValue(alpha*100)
        self._ui.alpha_lineEdit.setText(str(alpha))

    def _shininessEntered(self):
        value = self._ui.shininess_lineEdit.text()
        self._currentMaterial.setAttributeReal(Material.ATTRIBUTE_SHININESS, float(value))
        self._updateShininess()

    def _shininessSliderValueChanged(self):
        value = self._ui.shininess_slider.value()/100
        self._currentMaterial.setAttributeReal(Material.ATTRIBUTE_SHININESS, value)
        self._updateShininess()

    def _updateShininess(self):
        shininess = self._currentMaterial.getAttributeReal(Material.ATTRIBUTE_SHININESS)
        self._ui.shininess_slider.setValue(shininess*100)
        self._ui.shininess_lineEdit.setText(str(shininess))

    def _buildTextureComboBox(self):
        self._ui.texture_comboBox.clear()
        for i in range(4):
            self._ui.texture_comboBox.addItem("%d"%(i + 1))

    def _buildRegionComboBox(self):
        self._ui.region_comboBox.setRootRegion(self._zincContext.getDefaultRegion())
    
    def _buildImageFieldComboBox(self, region):
        self._ui.imageField_comboBox.clear()
        self._ui.imageField_comboBox.setConditional(is_field_image)
        self._ui.imageField_comboBox.setRegion(region)

    def _textureChanged(self, index):
        texture = self._currentMaterial.getTextureField(index)

    def _regionChanged(self, index):
        self._buildImageFieldComboBox(self._ui.region_comboBox.getRegion())
    
    def _imageFieldChanged(self, index):
        texture = self._ui.texture_comboBox.currentIndex() + 1
        imageField = self._ui.region_comboBox.getRegion().getFieldmodule().findFieldByName(self._ui.imageField_comboBox.currentText())
        self._currentMaterial.setTextureField(texture, imageField)

    def _clearPreview(self):
        self._previewZincScene.removeAllGraphics()
    
    def _previewMaterial(self):
        if self._previewZincScene is None:
            return
        if (self._currentMaterial is None) or (not self._currentMaterial.isValid()):
            self._previewZincScene.removeAllGraphics()
            return
        points = self._previewZincScene.getFirstGraphics()
        self._previewZincScene.beginChange()
        if not points.isValid():
            points = self._previewZincScene.createGraphicsPoints()
            pointsattr = points.getGraphicspointattributes()
            pointsattr.setBaseSize(1.0)
            tessellationModule = self._previewZincScene.getTessellationmodule()
            tessellation = tessellationModule.findTessellationByName("material_preview")
            if not tessellation.isValid():
                tessellation = tessellationModule.createTessellation()
                tessellation.setName("material_preview")
                tessellation.setManaged(False)
                tessellation.setCircleDivisions(48)
            points.setTessellation(tessellation)
        else:
            pointsattr = points.getGraphicspointattributes()
        pointsattr.setGlyphShapeType(Glyph.SHAPE_TYPE_SPHERE)
        points.setMaterial(self._currentMaterial)
        self._previewZincScene.endChange()

    def _setupPreviewScene(self, sceneviewer):
        with ChangeManager(sceneviewer):
            sceneviewer.setScene(self._previewZincScene)
            sceneviewer.setZoomRate(0)
            sceneviewer.setTumbleRate(0)
            sceneviewer.setTranslationRate(0)
            sceneviewer.setLookatParametersNonSkew([3.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
            sceneviewer.setViewAngle(0.679673818908244)
            sceneviewer.setNearClippingPlane(2.4)
            sceneviewer.setFarClippingPlane(3.0)

    def _previewGraphicsInitialised(self):
        sceneviewer = self._ui.sceneviewerWidgetPreview.getSceneviewer()
        if sceneviewer:
            self._setupPreviewScene(sceneviewer)
