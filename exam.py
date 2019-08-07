# class Exam:
#     def __init__(self, name, maximum, grade_range):
#         self.name = name
#         self.maximum = maximum
#         self.grade = grade_range
#
#     def delete(self):
#         del self
#
#
# class ExamUI:
#     def __init__(self, window, exam, target_layout):
#         self.exam = exam
#         self.target_layout = target_layout
#         self.window = window
#         self.layout = None
#         self.exam_button = None
#         self.del_button = None
#         self.edit_button = None
#         self.exam_text = None
#         self.place_text = None
#         self.msg = None
#         self.student_ui = None
#
#         self.create()
#
#     def create(self):
#         self.layout = QHBoxLayout()
#         self.layout.setSpacing(2)
#
#         # Create Church Button
#         self.exam_button = Button(self.exam.name, width=None, height=40)
#         self.exam_button.align_text()
#
#         # Create church Text
#         self.exam_text = TextBox(self.exam.name, height=40)
#
#         # Create Place Text
#         self.place_text = TextBox(self.exam.maximum, height=40)
#
#         # Create Edit Button
#         self.edit_button = Button('EDIT', width=40, height=40)
#
#         # Create Del button
#         self.del_button = Button('DEL', width=40, height=40)
#
#         self.layout.addWidget(self.church_text)
#         self.layout.addWidget(self.place_text)
#         self.layout.addWidget(self.church_button)
#         self.layout.addWidget(self.edit_button)
#         self.layout.addWidget(self.del_button)
#
#         self.target_layout.insertLayout(self.target_layout.count() - 1, self.layout)
#
#         self.church_button.clicked.connect(self.select)
#         self.church_text.returnPressed.connect(self.finish_edit)
#         self.place_text.returnPressed.connect(self.finish_edit)
#         self.edit_button.clicked.connect(self.edit)
#         self.del_button.clicked.connect(self.passive_delete)
#
#     def delete(self):
#         if self.layout is not None:
#             while self.layout.count():
#                 item = self.layout.takeAt(0)
#                 widget = item.widget()
#                 if widget is not None:
#                     widget.deleteLater()
#                 else:
#                     pass
#             self.church.delete()
#             del self
#
#     def hide(self):
#         pass
#
#     def select(self):
#         try:
#             if not self.student_ui:
#                 self.student_ui = student.Students(self.window, self.church)
#
#             data.selection.select(self.student_ui)
#         except Exception as e:
#             print(e)
#
#     def deselect(self):
#         self.window.setCentralWidget(None)
#
#     def passive_delete(self):
#         self.msg = display.QuestionMessageBox(
#             self.window, 'Delete Church',
#             'Do You want to delete church '+self.church.name+' and all the students?',
#             self.delete)
#
#     def edit(self):
#         if self.church_button.isVisible():
#             data.editing.start_edit(self)
#         else:
#             data.editing.finish_edit()
#
#     def start_edit(self):
#         self.church_button.hide()
#         # self.box_layout
#         self.church_text.show()
#         self.place_text.show()
#
#     def finish_edit(self):
#         if self.church_text.text() and self.place_text.text():
#             self.church_text.hide()
#             self.place_text.hide()
#             self.church.name = self.church_text.text()
#             self.church.place = self.place_text.text()
#             self.church_button.setText(self.church.get_name())
#             self.church_button.show()
#
#     def revert_edit(self):
#         self.church_text.hide()
#         self.place_text.hide()
#         self.church_button.setText(self.church_text.text() + ', ' + self.place_text.text())
#         self.church_button.show()
#
#
# class Churches:
#
#     def __init__(self, window):
#         self.window = window
#         self.scroll = None
#         self.widget = None
#         self.layout = None
#         self.scroll_layout = None
#         self.add_data = None
#         self.ui = []
#         self.exams = []
#
#         self.add_win = add.Window(self.window, 'Add Exam', 3, ['Name', 'Maximum', 'Grade Range'])
#         self.create()
#
#     def add_window(self):
#         try:
#             self.add_win.on_clear_all()
#             self.add_win.exec_()
#
#         except Exception as e:
#             print(e)
#
#     def passive_delete(self):
#         if self.ui:
#             display.QuestionMessageBox(self.window, 'Delete All Churches',
#                                        'Are you sure to delete all churches and their students?',
#                                        self.delete)
#
#     def set(self, exam_data):
#         self.add_data = exam_data
#         self.add()
#
#     def add(self):
#         for exam in self.add_data:
#             self.exams.append(Exam(exam[0], exam[1], exam[2]))
#             self.add_ui(self.exams[len(self.exams) - 1])
#
#         self.add_data = None
#
#     def delete(self):
#         for exam in self.ui:
#             exam.delete()
#
#         self.ui.clear()
#
#     def create(self):
#         self.scroll = QScrollArea()
#         self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
#         self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.scroll.setWidgetResizable(True)
#         widget = QWidget()
#         self.scroll.setWidget(widget)
#
#         self.scroll_layout = QVBoxLayout(widget)
#         self.scroll_layout.addStretch()
#
#         self.widget = QWidget()
#         self.layout = QVBoxLayout()
#         self.widget.setLayout(self.layout)
#         self.layout.addWidget(self.scroll)
#
#     def add_ui(self, church):
#         church_ui = ExamUI(self.window, church, self.scroll_layout)
#         self.ui.append(church_ui)
#
#     def select(self):
#         self.window.setCentralWidget(self.widget)
#
#     def deselect(self):
#         self.window.setCentralWidget(None)
#
#
