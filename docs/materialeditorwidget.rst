Material Editor Widget
======================

The **Material Editor Widget** is a control to add, remove, and modify materials.

Material list
-------------

The material list shows all the currently defined material; it will always contain the default material if no others have been defined.
Two buttons at the top of the window allow you to create, or delete material.

Settings editor
---------------

Below the list of material are some controls that allow you to set some of the general properties of the selected material.
The ambient colour, diffuse colour, emitted colour and specular colour. Also can adjust the alpha and shininess of the material.

Preview panel
-------------

This panel shows a sphere, coloured using the selected material.

API
---

.. autoclass:: opencmiss.zincwidgets.materialeditorwidget.MaterialEditorWidget
   :members:

.. autoclass:: opencmiss.zincwidgets.materialeditorwidget.MaterialModel
   :members: