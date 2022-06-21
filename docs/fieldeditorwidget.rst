Field Editor Widget
===================

The **Field Editor Widget** is a control to add, remove, and modify fields in a region.

Field list
----------

Above the field list, there's a region chooser. 
The field list shows all defined fields in the selected region.
Below the field list, two buttons allow you to add new field or delete selected field.

Settings editor
---------------

The settings editor is where each field is set up.
It contains a number of controls.

* Field type chooser: This drop-down menu shows the field type of the current field. It’s disabled for existing fields and enabled when creating a new field.
* Managed checkbox: This checkbox allows you to set if the field is managed.
* Is Coordinate checkbox: This checkbox allows you to set if the field is a coordinate.
* Coordinate system type: This drop-down menu shows the coordinate system type of the current field.
* Focus: This text box shows the focus number.
* Name: This text box is only displayed when creating a new field, and allows you to identify the name of the field.
* Number of source fields: This text box shows the number of source fields needed for the current type of field.
* Source field: This drop-down menu allows you to select an existing field as a source field for a new field, only enabled when creating a new field.
* Component indexes: This text box shows and allows you to change the component indexes of the selected field.

API
---

.. autoclass:: opencmiss.zincwidgets.fieldeditorwidget.FieldEditorWidget
   :members:
