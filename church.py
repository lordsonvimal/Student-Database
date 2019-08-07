from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QLineEdit, QWidget, QScrollArea, QVBoxLayout
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, Qt

import data
import display
import add
import student


class Church:
    def __init__(self, name, place):
        self.name = name
        self.place = place

    def delete(self):
        del self

    def get_name(self):
        return self.name+', '+self.place


class ChurchUI:
    def __init__(self, window, church, target_layout):
        self.church = church
        self.target_layout = target_layout
        self.window = window
        self.layout = None
        self.church_button = None
        self.del_button = None
        self.edit_button = None
        self.church_text = None
        self.place_text = None
        self.msg = None
        self.student_ui = None

        self.create()

    def create(self):
        self.layout = QHBoxLayout()
        self.layout.setSpacing(2)

        # Create Church Button
        self.church_button = Button(self.church.get_name(), width=None, height=40)
        self.church_button.align_text()

        # Create church Text
        self.church_text = TextBox(self.church.name, height=40)

        # Create Place Text
        self.place_text = TextBox(self.church.place, height=40)

        # Create Edit Button
        self.edit_button = Button('EDIT', width=40, height=40)

        # Create Del button
        self.del_button = Button('DEL', width=40, height=40)

        self.layout.addWidget(self.church_text)
        self.layout.addWidget(self.place_text)
        self.layout.addWidget(self.church_button)
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.del_button)

        self.target_layout.insertLayout(self.target_layout.count() - 1, self.layout)

        self.church_button.clicked.connect(self.select)
        self.church_text.returnPressed.connect(self.finish_edit)
        self.place_text.returnPressed.connect(self.finish_edit)
        self.edit_button.clicked.connect(self.edit)
        self.del_button.clicked.connect(self.passive_delete)

    def delete(self):
        if self.layout is not None:
            while self.layout.count():
                item = self.layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    pass
            self.church.delete()
            del self

    def hide(self):
        pass

    def select(self):
        try:
            if not self.student_ui:
                self.student_ui = student.Students(self.window, self.church)

            data.selection.select(self.student_ui)
        except Exception as e:
            print(e)

    def deselect(self):
        self.window.setCentralWidget(None)

    def passive_delete(self):
        self.msg = display.QuestionMessageBox(
            self.window, 'Delete Church',
            'Do You want to delete church '+self.church.name+' and all the students?',
            self.delete)

    def edit(self):
        if self.church_button.isVisible():
            data.editing.start_edit(self)
        else:
            data.editing.finish_edit()

    def start_edit(self):
        self.church_button.hide()
        # self.box_layout
        self.church_text.show()
        self.place_text.show()

    def finish_edit(self):
        if self.church_text.text() and self.place_text.text():
            self.church_text.hide()
            self.place_text.hide()
            self.church.name = self.church_text.text()
            self.church.place = self.place_text.text()
            self.church_button.setText(self.church.get_name())
            self.church_button.show()

    def revert_edit(self):
        self.church_text.hide()
        self.place_text.hide()
        self.church_button.setText(self.church_text.text() + ', ' + self.place_text.text())
        self.church_button.show()


class Button(QPushButton):
    def __init__(self, *args, width=None, height=None):
        super(Button, self).__init__(*args)
        self.button_width = width
        self.button_height = height

        self.set_width()
        self.set_height()

    def set_width(self):
        if self.button_width:
            self.setFixedWidth(self.button_width)

    def set_height(self):
        if self.button_height:
            self.setFixedHeight(self.button_height)

    def align_text(self, align="left"):
        self.setStyleSheet("Text-Align: "+align+";")


class TextBox(QLineEdit):
    def __init__(self, *args, width=None, height=None, hide=True):
        super(TextBox, self).__init__(*args)
        self.text_width = width
        self.text_height = height
        self.should_hide = hide
        self.set_validation()
        self.set_width()
        self.set_height()
        self.set_visibility()

    def set_visibility(self):
        if self.should_hide:
            self.hide()

    def set_validation(self):
        regex = QRegExp("[a-z-A-Z_]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)

    def set_width(self):
        if self.text_width:
            self.setFixedWidth(self.text_width)

    def set_height(self):
        if self.text_height:
            self.setFixedHeight(self.text_height)


class Churches:
    
    def __init__(self, window):
        self.window = window
        self.scroll = None
        self.widget = None
        self.layout = None
        self.scroll_layout = None
        self.add_data = None
        self.ui = []
        self.churches = []
        self.student_layout = None

        self.add_win = add.Window(self.window, 'Add Church', 2, ['Name', 'Place'])
        self.create()

    def add_window(self):
        try:
            self.add_win.on_clear_all()
            self.add_win.exec_()

        except Exception as e:
            print(e)

    def passive_delete(self):
        if self.ui:
            display.QuestionMessageBox(self.window, 'Delete All Churches',
                                       'Are you sure to delete all churches and their students?',
                                       self.delete)

    def set(self, church_data):
        self.add_data = church_data
        self.add()

    def add(self):
        for church in self.add_data:
            self.churches.append(Church(church[0], church[1]))
            self.add_ui(self.churches[len(self.churches)-1])

        self.add_data = None

    def delete(self):
        for church in self.ui:
            church.delete()

        self.ui.clear()

    def create(self):
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        widget = QWidget()
        self.scroll.setWidget(widget)

        self.scroll_layout = QVBoxLayout(widget)
        self.scroll_layout.addStretch()

        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.layout.addWidget(self.scroll)

    def add_ui(self, church):
        church_ui = ChurchUI(self.window, church, self.scroll_layout)
        self.ui.append(church_ui)

    def select(self):
        self.window.setCentralWidget(self.widget)

    def deselect(self):
        self.window.setCentralWidget(None)

