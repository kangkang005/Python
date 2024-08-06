from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from multiprocessing import Process, Queue
import sys

class MyApp(QMainWindow):
    receive_data = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('My App')

        self.receive_data.connect(self.update_text)

        self.show()

    def update_text(self, data):
        print('Received data:', data)

def run_gui_process(queue):
    app = QApplication(sys.argv)
    my_app = MyApp()

    data = 'Hello from the parent process!'
    my_app.receive_data.emit(data)

    print(queue.get())
    sys.exit(app.exec_())

def run_main_app():
    data_queue = Queue()
    data_queue.put('Hello from the parent process!')

    gui_process = Process(target=run_gui_process, args=(data_queue,))
    gui_process.start()

if __name__ == "__main__":
    run_main_app()