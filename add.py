from PyQt5.QtWidgets import QTableWidget, QApplication, QPushButton, \
    QDialog, QVBoxLayout, QHeaderView, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent

import data


class Window(QDialog):
    def __init__(self, parent_window, title, column_count, column_headers, row_count=1):
        super(Window, self).__init__(parent_window)
        self.setGeometry(0, 0, 800, 300)
        self.setModal(True)
        self.setWindowFlags((self.windowFlags() | Qt.CustomizeWindowHint) & ~Qt.WindowContextHelpButtonHint)
        self.place_center()
        self.setWindowTitle(title)

        self.box = None

        self.table = None

        self.table_layout = None

        self.buttons_layout = None

        self.data = []

        self.row_count = row_count

        self.column_count = column_count

        self.column_headers = column_headers

        self.design_layout()

        print("Created Window")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            self.focusNextChild()
        elif event.key() == Qt.Key_Tab and event.key() == Qt.Key_Shift:
            self.focusPreviousChild()
        else:
            super(Window, self).keyPressEvent(event)

    def design_layout(self):
        self.box = QVBoxLayout()
        self.add_table()
        self.add_buttons()
        self.setLayout(self.box)

    def add_table(self):
        self.table_layout = QVBoxLayout()
        self.table = AddTable()
        self.table.setRowCount(self.row_count)
        self.table.setColumnCount(self.column_count)
        self.table.setHorizontalHeaderLabels(self.column_headers)
        header = self.table.horizontalHeader()
        self.table.verticalHeader().hide()
        self.table.setStyleSheet("QHeaderView::section{Background-color: rgb(70,70,70); color:rgb(255,255,255)}")
        # self.table.horizontalHeader().setStyleSheet("border-top: 0px;border-left: 1px;"
        #                                             "border-right: 0px;border-bottom: 1px;"
        #                                             )

        for index in range(self.column_count):
            header.setSectionResizeMode(index, QHeaderView.Stretch)

        self.table_layout.addWidget(self.table)
        self.box.addLayout(self.table_layout)

    def add_buttons(self):
        self.buttons_layout = QHBoxLayout()
        add_button = QPushButton()
        add_button.setText('ADD')
        add_button.clicked.connect(self.on_add)
        self.buttons_layout.addWidget(add_button)

        clear_all_button = QPushButton()
        clear_all_button.setText('CLEAR ALL')
        clear_all_button.clicked.connect(self.on_clear_all)
        self.buttons_layout.addWidget(clear_all_button)

        close_button = QPushButton()
        close_button.setText('CLOSE')
        close_button.clicked.connect(self.on_close)
        self.buttons_layout.addWidget(close_button)

        self.box.addLayout(self.buttons_layout)

    def on_add(self):
        try:
            if self.table.validate_rows():
                self.data = self.table.rows
                data.runtime.set(self.data)
            # self.close()
            self.table.clear_all()
        except Exception as e:
            print(e)

    def on_clear_all(self):
        self.data = []
        self.table.clear_all()

    def on_close(self):
        self.close()

    def place_center(self):
        frame = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center = QApplication.desktop().screenGeometry(screen).center()
        frame.moveCenter(center)
        self.move(frame.topLeft())


class AddTable(QTableWidget):
    def __init__(self):
        self.rows = []
        super(AddTable, self).__init__()

    def keyReleaseEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.on_return_key(event)
                pass
            elif event.key() == Qt.Key_Backspace:
                self.on_backspace_key(event)
            else:
                super(AddTable, self).keyReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            if self.state() == 0 and self.currentRow() == self.rowCount() - 1 \
                    and self.currentColumn() == self.columnCount() - 1:
                self.parent().focusNextChild()
            else:
                super(AddTable, self).keyPressEvent(event)
        else:
            super(AddTable, self).keyPressEvent(event)

    def on_return_key(self, event):
        if self.currentRow() == self.rowCount()-1 and self.state() == 0:
            if self.check_row_data(self.currentRow()):
                self.insertRow(self.rowCount())
                index = self.model().index(self.rowCount()-1, 0)
                self.setCurrentIndex(index)

    def check_row_data(self, row):
        for column in range(self.columnCount()):
            if self.item(row, column):
                if not self.item(row, column).text().lstrip().rstrip():
                    return False
                else:
                    self.item(row, column).setText(self.item(row, column).text().lstrip().rstrip())
            else:
                return False
        return True

    def on_backspace_key(self, event):
        if self.state() == 0:
            if not self.check_row_data(self.currentRow()):
                if self.currentRow() != 0:
                    self.removeRow(self.currentRow())
                    index = self.model().index(self.rowCount() - 1, 0)
                    self.setCurrentIndex(index)

    def validate_rows(self):
        self.rows = []
        bad_rows = []
        for i in range(self.rowCount()):
            if self.check_row_data(i):
                row_data = []
                for j in range(self.columnCount()):
                    row_data.append(self.item(i, j).text())

                self.rows.append(row_data)
            else:
                bad_rows.append(i)

        for index in bad_rows:
            self.removeRow(index)

        if self.rows:
            return True
        else:
            return False

    def clear_all(self):
        self.setRowCount(1)
        for index in range(self.columnCount()):
            if self.item(0, index):
                self.item(0, index).setText('')

        self.rows = []
