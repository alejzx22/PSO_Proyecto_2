import sys, os
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont
from params import ALGORITHMS
from PyQt5.QtWidgets import QHBoxLayout
import table_interface

from Models.MMU import MMU
from Algorithms.FIFO import FIFO
from Algorithms.MRU import MRU
from Algorithms.OPT import OPT
from Algorithms.RND import RND
from Algorithms.SC import SC

from main import read_file, generate_file, run_operations


import params as p
file_path = ""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.start_simulation_signal = False        

        self.setFont(p.MAIN_FONT)

        self.setWindowTitle("Computer Simulation")
        self.setGeometry(100, 100, 700, 525)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Title
        title_label = QLabel("Computer Simulation")
        title_label.setFont(p.TITLE_FONT) 
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)



        # Random seed
        random_label = QLabel("Enter seed:")
        layout.addLayout(self.create_centered_widget(random_label, p.LABEL_WIDTH, p.LABEL_HEIGHT))

        self.seed_spinbox = QSpinBox()
        layout.addLayout(self.create_centered_widget(self.seed_spinbox, p.SB_WIDTH, p.SB_HEIGHT))

        # Algorithm
        algorithm_label = QLabel("Select the algorithm:")
        layout.addLayout(self.create_centered_widget(algorithm_label, p.LABEL_WIDTH, p.LABEL_HEIGHT))

        self.algorithm_combobox = QComboBox()
        self.algorithm_combobox.addItems(p.ALGORITHMS)
        self.algorithm_combobox.setCurrentText('Algorithm')
        layout.addLayout(self.create_centered_widget(self.algorithm_combobox, p.SB_WIDTH, p.SB_HEIGHT))
        
        # Processes
        process_label = QLabel("Select the amount of processes:")
        layout.addLayout(self.create_centered_widget(process_label, p.LABEL_WIDTH, p.LABEL_HEIGHT))
        
        self.process_combobox = QComboBox()
        self.process_combobox.addItems(p.PROCESS_NUM)
        self.process_combobox.setCurrentText('0')
        layout.addLayout(self.create_centered_widget(self.process_combobox, p.SB_WIDTH, p.SB_HEIGHT))

        # Operations
        operations_label = QLabel("Select the amount of operations:")
        layout.addLayout(self.create_centered_widget(operations_label, p.LABEL_WIDTH, p.LABEL_HEIGHT))
        
        self.operations_combobox = QComboBox()
        self.operations_combobox.addItems(p.OPERATIONS_NUM)
        self.operations_combobox.setCurrentText('0')
        layout.addLayout(self.create_centered_widget(self.operations_combobox, p.SB_WIDTH, p.SB_HEIGHT))

        layout.addSpacing(20)

        # Pick file button
        self.pick_file_button = QPushButton("Pick File")
        self.pick_file_button.clicked.connect(self.pick_file)
        layout.addLayout(self.create_centered_widget(self.pick_file_button, p.SB_WIDTH, p.SB_HEIGHT))

        self.file_path_label = QLabel("No file selected")
        layout.addLayout(self.create_centered_widget(self.file_path_label, p.LABEL_WIDTH, p.LABEL_HEIGHT))

        layout.addSpacing(20)

        # Start simulation button
        self.start_simulation_button = QPushButton("Start Simulation")
        self.start_simulation_button.clicked.connect(self.start_simulation)
        self.start_simulation_button.setStyleSheet("background-color: rgb(65, 105, 255); color: white; border-radius: 15px;")  # Add border-radius property
        self.start_simulation_button.setFont(self.font()) 
        layout.addLayout(self.create_centered_widget(self.start_simulation_button, 200, 50))

    def pick_file(self):
        global file_path
        
        file_path, _ = QFileDialog.getOpenFileName(self, "Pick File", "", "All Files (*)")
        if file_path:
            self.file_path_label.setText("Selected file: " + os.path.basename(file_path))
        else:
            self.file_path_label.setText("No file selected")

    def start_simulation(self):
        process_amount = self.process_combobox.currentText()
        operations_amount = self.operations_combobox.currentText()
        algorithm = self.algorithm_combobox.currentText()
        seed = self.seed_spinbox.value()

        if process_amount == 0 or operations_amount == 0 or algorithm == "Algorithm":
            QMessageBox.warning(self, "Warning", "Please fill all the fields.")
        else:
            self.table_window = table_interface.TableWindow(int(process_amount), int(operations_amount), algorithm, int(seed), file_path)
            
        
    def create_centered_widget(self, widget, width, height):
        if width == 0:
            width = widget.sizeHint().width()
        else:
            widget.setFixedWidth(width)
        if height == 0:
            height = widget.sizeHint().height()
        else:
            widget.setFixedHeight(height)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(widget)
        hbox.addStretch(1)
        return hbox

                
    def is_running(self):
        return self.start_simulation_signal
    
    def get_params(self):
        return self.process_combobox.currentText(), self.operations_combobox.currentText(), self.algorithm_combobox.currentText(), self.seed_spinbox.value(), file_path

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
