class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Select(metaclass=Singleton):

    def __init__(self):
        self.obj = None

    def select(self, obj):
        if self.obj:
            if self.obj != obj:
                self.obj.deselect()
        self.obj = obj
        self.obj.select()

    def deselect(self):
        self.obj.deselect()


class Edit(metaclass=Singleton):

    def __init__(self):
        self.obj = None

    def start_edit(self, obj):
        if self.obj:
            if self.obj != obj:
                self.obj.finish_edit()
        self.obj = obj
        self.obj.start_edit()

    def finish_edit(self):
        self.obj.finish_edit()
        self.obj = None

    def revert_edit(self):
        self.obj.revert_edit()


class RunTime(metaclass=Singleton):

    def __init__(self):
        self.data = []

    @staticmethod
    def set(data):
        selection.obj.set(data)


selection = Select()
editing = Edit()
runtime = RunTime()



