'''
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
'''
from PySide2 import QtWidgets, QtGui, QtCore

from opencmiss.zinc.material import Material
from opencmiss.zincwidgets.ui.ui_materialeditorwidget import Ui_MaterialEditor
from opencmiss.utils.zinc.general import ChangeManager

class MaterialEditorWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        '''
        Call the super class init functions
        '''
        QtWidgets.QWidget.__init__(self, parent)
        self._ui = Ui_MaterialEditor()
        self._ui.setupUi(self)
        self._nullObjectName = None
        self._materialmodule = None
        self._materialmodulenotifier = None
        self._currentMaterial = None

        self._makeConnections()
        self._buildMaterialList()

    def _makeConnections(self):
        self._ui.apply_button.clicked.connect(self._materialApplyClicked)
        self._ui.revert_button.clicked.connect(self._materialRevertClicked)
        self._ui.create_button.clicked.connect(self._materialCreateClicked)
        self._ui.delete_button.clicked.connect(self._materialDeleteClicked)
        self._ui.ambientSelectColour_button.clicked.connect(self._selectColourClicked)
        self._ui.diffuseSelectColour_button.clicked.connect(self._selectColourClicked)
        self._ui.emittedSelectColour_button.clicked.connect(self._selectColourClicked)
        self._ui.specularSelectColour_button.clicked.connect(self._selectColourClicked)
        self._ui.materials_listView.clicked[QtCore.QModelIndex].connect(self._materialListItemClicked)

    def _selectColourClicked(self, event):
        color = QtWidgets.QColorDialog.getColor()
        print(color)
        if color.isValid():
            print("before", color)
            self.sender().setStyleSheet("background-color: {}".format(color.name()))
            print("after", color)
            diffuseColour = [color.redF(), color.greenF(), color.blueF()]
            print(diffuseColour)

    def _buildMaterialList(self):
        '''
        Rebuilds the list of items in the Listview from the material module
        '''
        self._materialItems = QtGui.QStandardItemModel(self._ui.materials_listView)
        selectedIndex = None
        if self._materialmodule:
            if self._nullObjectName:
                self._ui.material_listView.addItem(self._nullObjectName)
            materialiter = self._materialmodule.createMaterialiterator()
            material = materialiter.next()
            if not self._currentMaterial:
                self._currentMaterial = material
            while material.isValid():
                name = None
                name = material.getName()
                item = QtGui.QStandardItem(name)
                item.setData(material)
                item.setEditable(True)
                self._materialItems.appendRow(item)     
                if material.getName() == self._currentMaterial.getName():
                    print(material.getName() , " ", self._currentMaterial.getName())
                    selectedIndex = self._materialItems.indexFromItem(item)
                    print(material.getName() , " ", selectedIndex)
                material = materialiter.next()
            self._ui.materials_listView.setModel(self._materialItems)
            if selectedIndex:
                self._ui.materials_listView.setCurrentIndex(selectedIndex)
        self._ui.materials_listView.show()
        self._displayMaterial()

    def _displayMaterial(self):
        '''
        Display the currently chosen material
        '''
        if self._currentMaterial:
            ambientColour, diffuseColour, emissionColour, specularColour = self._getCurrentMaterialColour()
        else:
            print("No Current Material")
            ambientColour, diffuseColour, emissionColour, specularColour = QtGui.QColor(0,0,0),QtGui.QColor(0,0,0),QtGui.QColor(0,0,0),QtGui.QColor(0,0,0)
        self._ui.ambientSelectColour_button.setStyleSheet("background-color: {}".format(ambientColour.name()))
        self._ui.diffuseSelectColour_button.setStyleSheet("background-color: {}".format(diffuseColour.name()))
        self._ui.emittedSelectColour_button.setStyleSheet("background-color: {}".format(emissionColour.name()))
        self._ui.specularSelectColour_button.setStyleSheet("background-color: {}".format(specularColour.name()))

    def _getCurrentMaterialColour(self):
        result, ambientColour = self._currentMaterial.getAttributeReal3(Material.ATTRIBUTE_AMBIENT)
        result, diffuseColour = self._currentMaterial.getAttributeReal3(Material.ATTRIBUTE_DIFFUSE)
        result, emissionColour = self._currentMaterial.getAttributeReal3(Material.ATTRIBUTE_EMISSION)
        result, specularColour = self._currentMaterial.getAttributeReal3(Material.ATTRIBUTE_SPECULAR)
        intAmbientColour = QtGui.QColor(int(ambientColour[0]*255), int(ambientColour[1]*255), int(ambientColour[1]*255))
        intDiffuseColour = QtGui.QColor(int(diffuseColour[0]*255), int(diffuseColour[1]*255), int(diffuseColour[1]*255))
        intEmissionColour = QtGui.QColor(int(emissionColour[0]*255), int(emissionColour[1]*255), int(emissionColour[1]*255))
        intSpecularColour = QtGui.QColor(int(specularColour[0]*255), int(specularColour[1]*255), int(specularColour[1]*255))
        return intAmbientColour, intDiffuseColour, intEmissionColour, intSpecularColour

    def _materialCreateClicked(self):
        """
        Create a new material.
        """
        with ChangeManager(self._materialmodule):
            material = self._materialmodule.createMaterial()
            material.setName("bob")
            material.setManaged(True)
            # plus any number of other changes to the material module or materials it manages
        self._buildMaterialList()

    def _materialDeleteClicked(self):
        """
        Delete the currently selected step, except for initial config.
        Select next step after, or before if none.
        """
        self.removeMaterialByName(self._currentMaterial.getName())
        self._currentMaterial = None
        self._buildMaterialList()

    def _materialApplyClicked(self):
        """
        Apply material.
        """
        self._setMaterialColour(Material.ATTRIBUTE_AMBIENT, self._ui.ambientSelectColour_button)
        self._setMaterialColour(Material.ATTRIBUTE_DIFFUSE, self._ui.diffuseSelectColour_button)
        self._setMaterialColour(Material.ATTRIBUTE_EMISSION,self._ui.emittedSelectColour_button)
        self._setMaterialColour(Material.ATTRIBUTE_SPECULAR,self._ui.specularSelectColour_button)
    
    def _setMaterialColour(self, materialAttribute, attributeButton):
        buttonColour = attributeButton.palette().button().color()
        colourF = [buttonColour.redF(), buttonColour.greenF(), buttonColour.blueF()]
        self._currentMaterial.setAttributeReal3(materialAttribute, colourF)

    def _materialRevertClicked(self):
        """
        Delete the currently selected step, except for initial config.
        Select next step after, or before if none.
        """
        self._displayMaterial()

    def _materialListItemClicked(self, modelIndex):
        """
        Changes current step and possibly changes checked/run status.
        """
        model = modelIndex.model()
        item = model.itemFromIndex(modelIndex)
        material = item.data()
        if material != self._currentMaterial:
           self._currentMaterial = material
           self._displayMaterial()

    def setNullObjectName(self, nullObjectName):
        '''
        Enable a null object option with the supplied name e.g. '-' or '<select>'
        Default is None
        '''
        self._nullObjectName = nullObjectName

    def setMaterialmodule(self, materialmodule):
        '''
        Sets the region that this widget chooses materials from
        '''
        self._materialmodule = materialmodule

    def getMaterial(self):
        '''
        Must call this from currentIndexChanged() slot to get/update current material
        '''
        materialName = self.currentText()
        if self._nullObjectName and (materialName == self._nullObjectName):
            self._currentMaterial = None
        else:
            self._currentMaterial = self._materialmodule.findMaterialByName(materialName)
        return self._material

    def setMaterial(self, material):
        '''
        Set the currently selected material
        '''
        if not material or not material.isValid():
            self._currentMaterial = None
        else:
            self._currentMaterial = material
        self._displayMaterial()

    def setContext(self, zincContext):
        """
        Sets the Argon material object which supplies the zinc context and has utilities for
        managing materials.
        :param materials: ArgonSpectrums object
        """
        # self._spectrums = spectrums
        # self._currentSpectrumName = None
        self._zincContext = zincContext
        self._ui.sceneviewerWidgetPreview.setContext(self._zincContext)
        self._previewZincRegion = self._zincContext.createRegion()
        self._previewZincRegion.setName("Spectrum editor preview region")
        self._previewZincScene = self._previewZincRegion.getScene()
        sceneviewer = self._ui.sceneviewerWidgetPreview.getSceneviewer()
        if sceneviewer:
            sceneviewer.setScene(self._previewZincScene)
        # spectrummodule = self._zincContext.getSpectrummodule()
        # self._spectrummodulenotifier = spectrummodule.createSpectrummodulenotifier()
        # self._spectrummodulenotifier.setCallback(self._spectrummoduleCallback)
        # self._buildSpectrumList()
        self.setMaterialmodule(self._zincContext.getMaterialmodule())
        self._buildMaterialList()

    def renameMaterial(self, material, name):
        """
        Renames material and its glyph
        :return True on success, otherwise False (means name not set)
        """
        colourBar = self.findOrCreateSpectrumGlyphColourBar(material)
        result = material.setName(name)
        if result == ZINC_OK:
            glyphName = SPECTRUM_GLYPH_NAME_FORMAT.format(name)
            tmpName = glyphName
            i = 1
            while (colourBar.setName(tmpName) != ZINC_OK):
                tmpName = glyphName + str(i)
                i += 1
            return True
        return False

    def removeMaterialByName(self, name):
        """
        Unmanages material and its colour bar. Note material is only removed if neither are in use.
        :return True if material and colour bar removed, false if failed i.e. either are in use.
        """
        self._currentMaterial = None
        self._displayMaterial()
        material = self._materialmodule.findMaterialByName(name)
        item = self._materialItems.findItems(name)
        item[0].setData(None)
        del item
        self._materialItems.clear()
        # material.setName(None)
        material.setManaged(False)
        del material
        material = self._materialmodule.findMaterialByName(name)
        if material.isValid():
            # material is in use so can't remove
            material.setManaged(True)
            return False
        return True

    def _materialmoduleCallback(self, materialmoduleevent):
        '''
        Callback for change in materials; may need to rebuild material list
        '''
        changeSummary = materialmoduleevent.getSummaryMaterialChangeFlags()
        #print("_materialmoduleCallback changeSummary " + str(changeSummary))
        # Can't do this as may be received after new material module is set!
        # if changeSummary == Material.CHANGE_FLAG_FINAL:
        #    self.setMaterialmodule(None)
        if 0 != (changeSummary & (Material.CHANGE_FLAG_IDENTIFIER | Material.CHANGE_FLAG_ADD | Material.CHANGE_FLAG_REMOVE)):
            self._buildMaterialList()

