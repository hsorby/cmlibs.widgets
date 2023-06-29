# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'groupmanagerwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_GroupManagerWidget(object):
    def setupUi(self, GroupManagerWidget):
        if not GroupManagerWidget.objectName():
            GroupManagerWidget.setObjectName(u"GroupManagerWidget")
        GroupManagerWidget.resize(500, 400)
        self.verticalLayout = QVBoxLayout(GroupManagerWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupTableWidget = QTableWidget(GroupManagerWidget)
        if (self.groupTableWidget.columnCount() < 3):
            self.groupTableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.groupTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.groupTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.groupTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.groupTableWidget.setObjectName(u"groupTableWidget")
        self.groupTableWidget.setFocusPolicy(Qt.NoFocus)
        self.groupTableWidget.setAlternatingRowColors(True)
        self.groupTableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.groupTableWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.groupTableWidget.setShowGrid(False)
        self.groupTableWidget.setRowCount(0)
        self.groupTableWidget.setColumnCount(3)
        self.groupTableWidget.horizontalHeader().setVisible(True)
        self.groupTableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.groupTableWidget.horizontalHeader().setHighlightSections(True)
        self.groupTableWidget.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.groupTableWidget, 1, 0, 1, 1)

        self.currentGroupLabel = QLabel(GroupManagerWidget)
        self.currentGroupLabel.setObjectName(u"currentGroupLabel")

        self.gridLayout.addWidget(self.currentGroupLabel, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.clearPushButton = QPushButton(GroupManagerWidget)
        self.clearPushButton.setObjectName(u"clearPushButton")

        self.horizontalLayout.addWidget(self.clearPushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.applyPushButton = QPushButton(GroupManagerWidget)
        self.applyPushButton.setObjectName(u"applyPushButton")

        self.horizontalLayout.addWidget(self.applyPushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(GroupManagerWidget)

        QMetaObject.connectSlotsByName(GroupManagerWidget)
    # setupUi

    def retranslateUi(self, GroupManagerWidget):
        GroupManagerWidget.setWindowTitle(QCoreApplication.translate("GroupManagerWidget", u"Group Manager Widget", None))
#if QT_CONFIG(whatsthis)
        GroupManagerWidget.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        ___qtablewidgetitem = self.groupTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("GroupManagerWidget", u"Group", None));
        ___qtablewidgetitem1 = self.groupTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("GroupManagerWidget", u"Operation", None));
        ___qtablewidgetitem2 = self.groupTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("GroupManagerWidget", u"Complement", None));
        self.currentGroupLabel.setText(QCoreApplication.translate("GroupManagerWidget", u"Managing Group: ", None))
        self.clearPushButton.setText(QCoreApplication.translate("GroupManagerWidget", u"Clear", None))
        self.applyPushButton.setText(QCoreApplication.translate("GroupManagerWidget", u"Apply", None))
    # retranslateUi

