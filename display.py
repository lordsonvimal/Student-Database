from PyQt5.QtWidgets import QMessageBox


class QuestionMessageBox:
    def __init__(self, window, title, message, callback):
        self.msg = message
        self.title = title
        self.window = window
        self.callback = callback
        self.message_box = None
        self.create()

    def create(self):
        try:
            self.message_box = QMessageBox.question(self.window, self.title, self.msg,
                                                    QMessageBox.Yes | QMessageBox.No,
                                                    QMessageBox.No)

            if self.message_box == QMessageBox.Yes:
                if self.callback:
                    self.callback()
            else:
                pass
        except Exception as e:
            print(e)
