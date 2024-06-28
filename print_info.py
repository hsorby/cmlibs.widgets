import PySide6
from PySide6 import QtCore

app = QtCore.QCoreApplication([])
info = QtCore.QLibraryInfo()
# print("Package paths:", PySide6.__path__)
# print("Prefix path:", info.path(QtCore.QLibraryInfo.LibraryPath.PrefixPath))
# print("Binaries path:", info.path(QtCore.QLibraryInfo.LibraryPath.BinariesPath))
# print("Library executables path:", info.path(QtCore.QLibraryInfo.LibraryPath.LibraryExecutablesPath))
# print("Plugins path:", info.path(QtCore.QLibraryInfo.LibraryPath.PluginsPath))
# print("")
print(info.path(QtCore.QLibraryInfo.LibraryPath.PluginsPath))
