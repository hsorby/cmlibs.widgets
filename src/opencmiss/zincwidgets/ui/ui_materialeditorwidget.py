# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'materialeditorwidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from opencmiss.zincwidgets.sceneviewerwidget import SceneviewerWidget


class Ui_MaterialEditor(object):
    def setupUi(self, MaterialEditor):
        if not MaterialEditor.objectName():
            MaterialEditor.setObjectName(u"MaterialEditor")
        MaterialEditor.resize(783, 1004)
        self.verticalLayout = QVBoxLayout(MaterialEditor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.create_button = QPushButton(MaterialEditor)
        self.create_button.setObjectName(u"create_button")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.create_button.sizePolicy().hasHeightForWidth())
        self.create_button.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.create_button)

        self.delete_button = QPushButton(MaterialEditor)
        self.delete_button.setObjectName(u"delete_button")
        sizePolicy.setHeightForWidth(self.delete_button.sizePolicy().hasHeightForWidth())
        self.delete_button.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.delete_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.materials_listView = QListView(MaterialEditor)
        self.materials_listView.setObjectName(u"materials_listView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.materials_listView.sizePolicy().hasHeightForWidth())
        self.materials_listView.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.materials_listView)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.diffuseText_label = QLabel(MaterialEditor)
        self.diffuseText_label.setObjectName(u"diffuseText_label")

        self.gridLayout.addWidget(self.diffuseText_label, 0, 1, 1, 1)

        self.ambientSelectColour_button = QPushButton(MaterialEditor)
        self.ambientSelectColour_button.setObjectName(u"ambientSelectColour_button")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ambientSelectColour_button.sizePolicy().hasHeightForWidth())
        self.ambientSelectColour_button.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.ambientSelectColour_button, 1, 0, 1, 1)

        self.emittedText_label = QLabel(MaterialEditor)
        self.emittedText_label.setObjectName(u"emittedText_label")

        self.gridLayout.addWidget(self.emittedText_label, 2, 0, 1, 1)

        self.ambientText_label = QLabel(MaterialEditor)
        self.ambientText_label.setObjectName(u"ambientText_label")

        self.gridLayout.addWidget(self.ambientText_label, 0, 0, 1, 1)

        self.diffuseSelectColour_button = QPushButton(MaterialEditor)
        self.diffuseSelectColour_button.setObjectName(u"diffuseSelectColour_button")
        sizePolicy2.setHeightForWidth(self.diffuseSelectColour_button.sizePolicy().hasHeightForWidth())
        self.diffuseSelectColour_button.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.diffuseSelectColour_button, 1, 1, 1, 1)

        self.specularText_label = QLabel(MaterialEditor)
        self.specularText_label.setObjectName(u"specularText_label")

        self.gridLayout.addWidget(self.specularText_label, 2, 1, 1, 1)

        self.emittedSelectColour_button = QPushButton(MaterialEditor)
        self.emittedSelectColour_button.setObjectName(u"emittedSelectColour_button")
        sizePolicy2.setHeightForWidth(self.emittedSelectColour_button.sizePolicy().hasHeightForWidth())
        self.emittedSelectColour_button.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.emittedSelectColour_button, 3, 0, 1, 1)

        self.specularSelectColour_button = QPushButton(MaterialEditor)
        self.specularSelectColour_button.setObjectName(u"specularSelectColour_button")
        sizePolicy2.setHeightForWidth(self.specularSelectColour_button.sizePolicy().hasHeightForWidth())
        self.specularSelectColour_button.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.specularSelectColour_button, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBox = QComboBox(MaterialEditor)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout_2.addWidget(self.comboBox, 2, 1, 1, 1)

        self.label = QLabel(MaterialEditor)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(MaterialEditor)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)

        self.horizontalSlider_2 = QSlider(MaterialEditor)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.horizontalSlider_2, 1, 3, 1, 1)

        self.label_3 = QLabel(MaterialEditor)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_4 = QLabel(MaterialEditor)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)

        self.lineEdit = QLineEdit(MaterialEditor)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.lineEdit_2 = QLineEdit(MaterialEditor)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_2.addWidget(self.lineEdit_2, 0, 3, 1, 1)

        self.horizontalSlider = QSlider(MaterialEditor)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.horizontalSlider, 1, 1, 1, 1)

        self.label_5 = QLabel(MaterialEditor)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)

        self.comboBox_2 = QComboBox(MaterialEditor)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout_2.addWidget(self.comboBox_2, 3, 1, 1, 1)

        self.comboBox_3 = QComboBox(MaterialEditor)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.gridLayout_2.addWidget(self.comboBox_3, 4, 1, 1, 1)

        self.checkBox = QCheckBox(MaterialEditor)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_2.addWidget(self.checkBox, 3, 3, 1, 1)

        self.checkBox_2 = QCheckBox(MaterialEditor)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout_2.addWidget(self.checkBox_2, 2, 3, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.sceneviewerWidgetPreview = SceneviewerWidget(MaterialEditor)
        self.sceneviewerWidgetPreview.setObjectName(u"sceneviewerWidgetPreview")

        self.verticalLayout.addWidget(self.sceneviewerWidgetPreview)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.apply_button = QPushButton(MaterialEditor)
        self.apply_button.setObjectName(u"apply_button")

        self.horizontalLayout_2.addWidget(self.apply_button)

        self.revert_button = QPushButton(MaterialEditor)
        self.revert_button.setObjectName(u"revert_button")

        self.horizontalLayout_2.addWidget(self.revert_button)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(MaterialEditor)

        QMetaObject.connectSlotsByName(MaterialEditor)
    # setupUi

    def retranslateUi(self, MaterialEditor):
        MaterialEditor.setWindowTitle(QCoreApplication.translate("MaterialEditor", u"Material Editor", None))
        self.create_button.setText(QCoreApplication.translate("MaterialEditor", u"Create", None))
        self.delete_button.setText(QCoreApplication.translate("MaterialEditor", u"Delete", None))
        self.diffuseText_label.setText(QCoreApplication.translate("MaterialEditor", u"Diffuse Colour:", None))
        self.ambientSelectColour_button.setText(QCoreApplication.translate("MaterialEditor", u"Select Color", None))
        self.emittedText_label.setText(QCoreApplication.translate("MaterialEditor", u"Emitted Colour:", None))
        self.ambientText_label.setText(QCoreApplication.translate("MaterialEditor", u"Ambient Colour:", None))
        self.diffuseSelectColour_button.setText(QCoreApplication.translate("MaterialEditor", u"Select Color", None))
        self.specularText_label.setText(QCoreApplication.translate("MaterialEditor", u"Specular Colour:", None))
        self.emittedSelectColour_button.setText(QCoreApplication.translate("MaterialEditor", u"Select Color", None))
        self.specularSelectColour_button.setText(QCoreApplication.translate("MaterialEditor", u"Select Color", None))
        self.label.setText(QCoreApplication.translate("MaterialEditor", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("MaterialEditor", u"Shininess : ", None))
        self.label_3.setText(QCoreApplication.translate("MaterialEditor", u"Texture : ", None))
        self.label_4.setText(QCoreApplication.translate("MaterialEditor", u"Region : ", None))
        self.label_5.setText(QCoreApplication.translate("MaterialEditor", u"Image Field : ", None))
        self.checkBox.setText(QCoreApplication.translate("MaterialEditor", u"CheckBox", None))
        self.checkBox_2.setText(QCoreApplication.translate("MaterialEditor", u"CheckBox", None))
        self.apply_button.setText(QCoreApplication.translate("MaterialEditor", u"Apply", None))
        self.revert_button.setText(QCoreApplication.translate("MaterialEditor", u"Revert", None))
    # retranslateUi

