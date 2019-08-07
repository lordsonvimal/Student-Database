#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QAction, QWidget, QSizePolicy, QLineEdit, QCompleter, QLabel, QComboBox
from PyQt5.QtCore import Qt


class ToolBar:
    def __init__(self, window):
        self.window = window
        self.tool_bar = self.window.addToolBar('Toolbar')
        self.tool_bar.setFixedHeight(50)
        self.tool_bar.layout().setSpacing(10)
        self.tool_bar.setMovable(False)

        self.view = None
        self.add_button = None
        self.del_button = None

        self.populate_tool_bar()

    def populate_tool_bar(self):
        self.view = QComboBox(self.window)
        self.view.addItem('CHURCH')
        self.view.addItem('EXAM')
        self.view.addItem('PRIZE')
        self.view.setFixedHeight(30)
        self.view.setFixedWidth(100)
        self.tool_bar.addWidget(self.view)
        self.add_button = ToolButton('Add', self.add, self.window,
                                     short_cut='', status_tip='Add Church')
        self.tool_bar.addAction(self.add_button.button)

        self.del_button = ToolButton('Delete', self.delete, self.window,
                                     short_cut='', status_tip='Delete all Church')
        self.tool_bar.addAction(self.del_button.button)

        self.add_spacer()
        self.add_spacer()
        self.add_spacer()
        self.add_spacer()
        self.add_spacer()
        self.add_spacer()
        self.add_spacer()

        search_label = QLabel()
        search_label.setText('Search')
        self.tool_bar.addWidget(search_label)

        self.add_search_bar()

    def add_spacer(self):
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tool_bar.addWidget(spacer)

    def add_search_bar(self):
        line_edit = QLineEdit(self.window)
        str_list = ['test', 'complete']
        completer = QCompleter(str_list, line_edit)
        line_edit.setCompleter(completer)
        line_edit.setFocusPolicy(Qt.ClickFocus)
        line_edit.editingFinished.connect(self.set_focus)
        line_edit.focusNextChild()
        self.window.focusWidget()
        self.tool_bar.addWidget(line_edit)

    def add(self):
        self.window.add_window()

    def delete(self):
        self.window.delete()

    def set_focus(self):
        self.window.setFocus()

    def set_text(self, text):
        self.view.setCurrentText(text)


class ToolButton:
    def __init__(self, name, trigger, parent, short_cut='', status_tip=''):
        self.name = name
        self.trigger = trigger
        self.parent = parent
        self.short_cut = short_cut
        self.status_tip = status_tip
        self.button = None
        self.create()

    def create(self):
        self.button = QAction(self.name, self.parent)
        if self.trigger:
            self.button.triggered.connect(self.trigger)
        if self.short_cut:
            self.button.setShortcut(self.short_cut)
        if self.status_tip:
            self.button.setStatusTip(self.status_tip)

