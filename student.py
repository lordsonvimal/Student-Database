from PyQt5.QtWidgets import QTableWidget, QApplication, QPushButton, \
    QDialog, QVBoxLayout, QHeaderView, QHBoxLayout, QTableWidgetItem, QComboBox, QDateEdit
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QKeyEvent

import data


####################
# Student Class    #
####################
class Student:
    def __init__(self, name, gender, dob, medium):
        self.name = name
        self.gender = gender
        self.date_of_birth = dob
        self.medium = medium

    def delete(self):
        del self


####################
# Students Class   #
# Controls the UI  #
####################
class Students:
    def __init__(self, window, church):
        self.window = window
        self.church = church
        self.widget = None
        self.layout = None
        self.students = []
        self.add_data = []

        self.add_win = Window(self.window, 'Add Students', 4, ['Name', 'Gender', 'DOB', 'Medium'])

        self.create()

    def add_window(self):
        try:
            self.add_win.on_clear_all()
            self.add_win.exec_()

        except Exception as e:
            print(e)

    def set(self, student_data):
        self.add_data = student_data
        self.add()

    def add(self):
        for student in self.add_data:
            self.students.append(Student(student[0], student[1], student[2], student[3]))
            self.add_ui(self.students[len(self.students)-1])

    def add_ui(self, student):
        self.widget.add(student)

    def select(self):
        self.window.setCentralWidget(self.widget)

    def deselect(self):
        self.window.setCentralWidget(None)

    def create(self):
        self.layout = QVBoxLayout()
        self.widget = StudentTable()
        self.widget.setRowCount(0)
        self.widget.setColumnCount(8)
        self.widget.setHorizontalHeaderLabels(['Name', 'Gender', 'DOB', 'Medium', 'Age', 'Department', '', ''])
        header = self.widget.horizontalHeader()
        # self.widget.verticalHeader().hide()
        self.widget.setStyleSheet("QHeaderView::section{Background-color: rgb(70,70,70); color:rgb(255,255,255)}")
        for index in range(self.widget.columnCount()):
            header.setSectionResizeMode(index, QHeaderView.Stretch)

        self.widget.setLayout(self.layout)
        self.layout.addStretch()


# #######################
# Window Class          #
# Creates new Window    #
# #######################
class Window(QDialog):
    def __init__(self, parent_window, title, column_count, column_headers, row_count=0):
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
        # else:
        #     super(Window, self).keyPressEvent(event)

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
        self.table.add_row()

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
        if self.table.validate_rows():
            self.data = self.table.rows
            data.runtime.set(self.data)

        self.on_clear_all()

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


####################
# Add Student Table#
####################
class AddTable(QTableWidget):
    def __init__(self):
        self.rows = []
        super(AddTable, self).__init__()
        self.gender = ['MALE', 'FEMALE']
        self.medium = ['TAMIL', 'ENGLISH', 'MALAYALAM', 'TELUGU', 'HINDI']
        self.gender_combo = None
        self.medium_combo = None
        self.dob_edit = None

    def add_row(self):
        self.gender_combo = QComboBox()
        self.medium_combo = QComboBox()
        self.gender_combo.addItems(self.gender)
        self.medium_combo.addItems(self.medium)
        self.dob_edit = QDateEdit()
        self.dob_edit.setDisplayFormat('dd/MM/yyyy')
        self.dob_edit.setCalendarPopup(True)
        self.dob_edit.setDate(QDate.currentDate())

        self.insertRow(self.rowCount())

        self.setCellWidget(self.rowCount()-1, 1, self.gender_combo)
        self.setCellWidget(self.rowCount()-1, 2, self.dob_edit)
        self.setCellWidget(self.rowCount()-1, 3, self.medium_combo)

    def keyReleaseEvent(self, event):
        if type(event) == QKeyEvent:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.on_return_key(event)
                pass
            if event.key() == Qt.Key_Backspace:
                self.on_backspace_key(event)

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
                self.add_row()
                index = self.model().index(self.rowCount()-1, 0)
                self.setCurrentIndex(index)

        else:
            super(AddTable, self).keyPressEvent(event)

    def check_row_data(self, row):
        if self.item(row, 0):
            if not self.item(row, 0).text().strip():
                return False
        else:
            return False

        if self.cellWidget(row, 2).date() == QDate.currentDate():
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
                row_data = self.get_row_data(i)
                self.rows.append(row_data)
            else:
                bad_rows.append(i)

        for index in bad_rows:
            self.removeRow(index)

        if self.rowCount() == 0:
            self.add_row()

        if self.rows:
            return True
        else:
            return False

    def get_row_data(self, row):
        row_data = [self.item(row, 0).text(),
                    self.cellWidget(row, 1).currentText(),
                    self.cellWidget(row, 2).date(),
                    self.cellWidget(row, 3).currentText()]

        return row_data

    def clear_all(self):
        self.setRowCount(0)
        self.add_row()
        self.rows = []


class StudentTable(QTableWidget):
    def __init__(self, *args):
        self.rows = []
        super(StudentTable, self).__init__(*args)

        self.gender = ['MALE', 'FEMALE']
        self.medium = ['TAMIL', 'ENGLISH', 'MALAYALAM', 'TELUGU', 'HINDI']
        self.gender_combo = None
        self.medium_combo = None
        self.dob_edit = None

    def add(self, student):
        self.add_row()

        print(self.rowCount())
        self.setItem(self.rowCount()-1, 0, QTableWidgetItem(student.name))
        self.cellWidget(self.rowCount()-1, 1).setCurrentText(student.gender)
        self.cellWidget(self.rowCount()-1, 2).setDate(student.date_of_birth)
        self.cellWidget(self.rowCount()-1, 3).setCurrentText(student.medium)

    def add_row(self):
        self.gender_combo = QComboBox()
        self.medium_combo = QComboBox()
        self.gender_combo.addItems(self.gender)
        self.medium_combo.addItems(self.medium)
        self.dob_edit = QDateEdit()
        self.dob_edit.setDisplayFormat('dd/MM/yyyy')
        self.dob_edit.setCalendarPopup(True)
        self.dob_edit.setDate(QDate.currentDate())

        self.insertRow(self.rowCount())

        self.setCellWidget(self.rowCount()-1, 1, self.gender_combo)
        self.setCellWidget(self.rowCount()-1, 2, self.dob_edit)
        self.setCellWidget(self.rowCount()-1, 3, self.medium_combo)

