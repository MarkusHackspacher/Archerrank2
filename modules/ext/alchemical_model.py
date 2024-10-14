#!/usr/bin/env python3
# © 2013 Mark Harviston, BSD License
# 2016: update to use PyQt5/Python3, some enhancements by Christian González
"""
Qt data models that bind to SQLAlchemy queries
"""
try:
    from PyQt6.QtCore import Qt, QVariant
    from PyQt6.QtSql import QSqlTableModel
    from PyQt6.QtWidgets import QMessageBox
except ImportError as err:
    from PyQt5.Qt import Qt, QVariant
    from PyQt5.QtSql import QSqlTableModel
    from PyQt5.QtWidgets import QMessageBox
    print(f"alchemical_model.py: ImportError {err=}, {type(err)=}")
except Exception as err:
    print(f"alchemical_model.py: Unexpected {err=}, {type(err)=}")
    raise


class SqlAlchemyTableModel(QSqlTableModel):
    """A Qt Table Model that binds to a SQLAlchemy query

    Example:
    >>> model = AlchemicalTableModel(Session,
            Entity,
            [('Name', Entity.name, "name", {"editable": True} )])
    >>> table = QTableView()
    >>> table.setModel(model)
    """

    def __init__(self, session, entity, columns,  parent=None):
        """Constructor for the model.

        @param session: The SQLAlchemy session object.
        @param entity: The entity class that represents the SQLAlchemy data object
        @param columns: A list of column 4-tuples
          (header, sqlalchemy column, column name, extra parameters as dict)
          if the sqlalchemy column object is 'Entity.name', then column name
          should probably be 'name'.
          'Entity.name' is what will be used when setting data and sorting,
          'name' will be used to retrieve the data.
        """
        super(SqlAlchemyTableModel, self).__init__(parent)
        # TODO self.sort_data = None
        self.session = session
        self.fields = columns
        self.query = session.query
        self.entity = entity

        self.results = None
        self.count = None
        self.sort = None
        self.filter = None

        self.refresh()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return QVariant(self.fields[col][0])
        return QVariant()

    def setFilter(self, newFilter):
        """Sets or clears the newFilter.

        Clear the filter by setting newFilter to None
        """
        self.filter = newFilter
        self.refresh()

    def refresh(self):
        """Recalculates self.results and self.count"""

        self.layoutAboutToBeChanged.emit()

        q = self.session.query

        if self.sort is not None:
            order, col = self.sort
            col = self.fields[col][1]
            if order == Qt.SortOrder.DescendingOrder:
                col = col.desc()
        else:
            col = None

        if self.filter is not None:
            # not working
            # AttributeError: 'function' object has no attribute 'filter'
            q = q.filter(self.filter)

        self.results = q(self.entity).all()
        self.count = len(self.results)
        self.layoutChanged.emit()

    def flags(self, index):
        _flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

        if self.sort is not None:
            order, col = self.sort

            if self.fields[col][3].get('dnd', False) and index.column() == col:
                _flags |= Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled

        if self.fields[index.column()][3].get('editable', False):
            _flags |= Qt.ItemFlag.ItemIsEditable

        return _flags

    def supportedDropActions(self):
        return Qt.DropAction.MoveAction

    def dropMimeData(self, data, action, row, col, parent):
        if action != Qt.DropAction.MoveAction:
            return
        return False

    def rowCount(self, parent=None):
        return self.count or 0

    def columnCount(self, parent=None):
        return len(self.fields)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        elif role not in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return QVariant()

        row = self.results[index.row()]
        name = self.fields[index.column()][2]

        return getattr(row, name)

    def setData(self, index, value, role=None):
        row = self.results[index.row()]
        name = self.fields[index.column()][2]

        try:
            setattr(row, name, str(value))
            self.session.commit()
        except Exception as ex:
            QMessageBox.critical(None, 'SQL Error', '{0} Check autocommit=False'.format(ex))
            return False
        else:
            self.dataChanged.emit(index, index)
            return True
