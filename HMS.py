#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon

import menu_bar
import tool_bar
import data
import church


class HMS(QMainWindow):

    def __init__(self, *args):
        super(HMS, self).__init__(*args)
        self.status_bar = None
        self.tool_bar = None
        self.menu_bar = None

        self.church = None

        self.init_ui()

    def init_ui(self):

        resolution = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, resolution.width(), resolution.height())
        self.setStyleSheet("QMainWindow{background-color: rgb(245,245,245)}")

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('HMS Sunday School Application Started')

        self.setWindowTitle('HMS Sunday School')
        self.setWindowIcon(QIcon('Sources/hms.png'))

        self.menu_bar = menu_bar.MenuBar(self)

        self.tool_bar = tool_bar.ToolBar(self)

        self.create()

        self.show()
        self.showMaximized()

    def create(self):
        self.church = church.Churches(self)
        data.selection.select(self.church)
        # self.exam

    @staticmethod
    def add_window():
        try:
            data.selection.obj.add_window()
        except Exception as e:
            print(e)

    @staticmethod
    def delete():
        try:
            data.selection.obj.passive_delete()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # QFontDatabase().addApplicationFont('/Fonts/verdana.ttf')
    # app.setFont(QFont('verdana', 9))
    # app.setFont(QFont('Candara', 11))

    ex = HMS()
    sys.exit(app.exec_())
