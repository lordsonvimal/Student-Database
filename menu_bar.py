#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QAction


class MenuBar:
    def __init__(self, main_window):
        self.window = main_window
        self.main_menu = self.window.menuBar()
        # self.main_menu.setStyleSheet("background-color: rgb(240, 240, 250)")
        self.file_menu = self.main_menu.addMenu('File')
        self.edit_menu = self.main_menu.addMenu('Edit')
        self.view_menu = self.main_menu.addMenu('View')

        self.populate_file_menu()
        self.populate_edit_menu()
        self.populate_view_menu()

    def populate_view_menu(self):
        church = MenuButton('Church', None, self.window, short_cut='Ctrl+C', status_tip='View Churches')
        exam = MenuButton('Exam', None, self.window, short_cut='Ctrl+E', status_tip='View Exams')
        prize = MenuButton('Prize', None, self.window, short_cut='Ctrl+P', status_tip='View Prizes')
        self.view_menu.addAction(church.button)
        self.view_menu.addAction(exam.button)
        self.view_menu.addAction(prize.button)

    def populate_edit_menu(self):
        undo = MenuButton('Undo', None, self.window, short_cut='Ctrl+Z', status_tip='Undo Operation')
        redo = MenuButton('Redo', None, self.window, short_cut='Ctrl+Shift+Z', status_tip='Redo Operation')
        add = MenuButton('Add', self.add_window, self.window, short_cut='+', status_tip='Add')
        delete = MenuButton('Delete', self.delete, self.window, short_cut='Del', status_tip='Delete')
        preference = MenuButton('Preferences', None, self.window, short_cut='Ctrl+Shift+P', status_tip='Preferences')

        self.edit_menu.addAction(undo.button)
        self.edit_menu.addAction(redo.button)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(add.button)
        self.edit_menu.addAction(delete.button)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(preference.button)

    def populate_file_menu(self):
        reset = MenuButton('Reset', None, self.window, short_cut='Ctrl+R', status_tip='Reset Application')
        file_open = MenuButton('Open', None, self.window, short_cut='Ctrl+O', status_tip='Open a DB file')
        save = MenuButton('Save', None, self.window, short_cut='Ctrl+S', status_tip='Save file')
        archive = MenuButton('Archive', None, self.window, short_cut='Ctrl+A', status_tip='Archive')
        importer = MenuButton('Import', None, self.window, short_cut='Ctrl+I', status_tip='Append more data')
        export = MenuButton('Export', None, self.window, short_cut='Ctrl+E', status_tip='Export')

        close = MenuButton('Exit', self.window.close, self.window,
                           short_cut='Ctrl+Q', status_tip='Exit Application')

        self.file_menu.addAction(file_open.button)
        self.file_menu.addAction(reset.button)
        self.file_menu.addSeparator()
        self.file_menu.addAction(save.button)
        self.file_menu.addAction(archive.button)
        self.file_menu.addSeparator()
        self.file_menu.addAction(importer.button)
        self.file_menu.addAction(export.button)
        self.file_menu.addSeparator()
        self.file_menu.addAction(close.button)

    def add_window(self):
        self.window.add_window()

    def delete(self):
        self.window.delete()


class MenuButton:
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

