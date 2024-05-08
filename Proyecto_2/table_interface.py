from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QMainWindow, QVBoxLayout, QTableWidget, QApplication, QWidget, QMessageBox, QLabel, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer
from Algorithms.FIFO import FIFO
from Algorithms.MRU import MRU
from Algorithms.OPT import OPT
from Algorithms.RND import RND
from Algorithms.SC import SC
from Models.Computer import Computer
from Models.MMU import MMU
from Models.Session import Session
from Models.Page import Page
from main import generate_file, read_file
import params as p
import time
import random
from PyQt5.QtGui import QColor, QFont

class BaseTable(QTableWidget):
    def __init__(self, num_cols, num_rows, column_labels):
        super().__init__()
        self.setRowCount(num_rows)
        self.setColumnCount(num_cols)
        if column_labels != "none":
            self.setHorizontalHeaderLabels(column_labels)
        
        font = QFont()
        font.setBold(True)
        self.horizontalHeader().setFont(font)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        font = self.font()
        font.setPointSize(7) 
        self.setFont(font)

        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


    def update_data(self, data):
        pass
    
class RAMTable(BaseTable):
    def __init__(self, col_num):
        super().__init__(col_num, 1, "none") 
        self.setFixedHeight(30)
        # self.setFixedWidth(2000)

        for i in range(self.columnCount()):
            self.setColumnWidth(i, 10)

        #self.update_data([["" for _ in range(8)]])

        self.horizontalHeader().setVisible(False)
    
    def update_data(self, data): # data = [RAM data] 
                                 # RAM data = color of the pages of the processess in RAM
        # For each process paint the pages in the table with a random color
        physical_addresses = []
        for i in range(len(data)):
            for j in range(1, len(data[i])):
                page: Page = data[i][j]
                if page.physical_address != -1:
                    item = QTableWidgetItem("")
                    color = QColor(*data[i][0])
                    item.setBackground(color)
                    self.setItem(0, page.physical_address, item)
                    physical_addresses.append(page.physical_address)
        for i in range(100):
            if i not in physical_addresses:
                item = QTableWidgetItem("")
                item.setBackground(QColor(255, 255, 255))
                self.setItem(0, i, item)
        

class MMUTable(BaseTable):
    def __init__(self, row_num):
        super().__init__(7, row_num, p.MMU_TABLE_COLUMNS) 
        self.setFixedHeight(200)
        self.setFixedWidth(570)

        for i in range(self.columnCount()):
            self.setColumnWidth(i, 80)
        for i in range(self.rowCount()):
            self.setRowHeight(i, 30)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
    
    def update_data(self, data): # data = [ [page data], [page data], ... , 
                                 # [page data] page data: [ID,PID,is_loaded, L-AADR, M-AADR,D-AADR,
                                 # LOADED-T, MARK, process color((r,g,b) of the process))] ]
                                 
        total, processes, pages_info, computer = data                         

        self.setRowCount(total)
        
        # for process in processes:
        #     pid = process.pid
        
        # pages_info = [[color, p1, p2, p3...], [color, p1, p2, p3...], [color, p1, p2, p3...], [color, p1, p2, p3...
        
        # info: [color, p1, p2, p3...]                    
        
        
        for info in pages_info:
            color = info[0]
            for i, page in enumerate(info[1:]): #rows
                for j in range(7): #cols
                    if j == 0:
                        item = QTableWidgetItem(str(page.page_id))
                    if j == 1:
                        process = computer.get_process_by_color(color)
                        item = QTableWidgetItem(str(process.pid))
                    if j == 2:
                        if page.position_flag:
                            item = QTableWidgetItem("X")
                        else:
                            item = QTableWidgetItem("")
                    if j == 3:
                        ptr = computer.get_pointer_by_page(page)
                        item = QTableWidgetItem(str(ptr))
                    if j == 4:
                        item = QTableWidgetItem(str(page.physical_address))                            
                    if j == 5:                        
                        item = QTableWidgetItem(str(page.timestamp) + "s")
                    if j == 6:
                        item = QTableWidgetItem(str(page.second_chance))
                    
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setBackground(QColor(*color))
                    self.setItem(i, j, item)
            # page_id = page.page_id
            # loaded = page.position_flag
            # mark = page.second_chance
            # time = page.timestamp
            
            # for j in range(8):
            #     if j == 2:
            #         if loaded:
            #             item = QTableWidgetItem("X")  # if it is loaded, mark with x
            #         else:
            #             item = QTableWidgetItem("")
            #     elif j == 6:
            #         item = QTableWidgetItem(str(page.timestamp) + "s")  # loaded time in seconds
            #     else:
            #         item = QTableWidgetItem('')
            #     item.setTextAlignment(Qt.AlignCenter)

            #     # item.setBackground(QColor(data[i][8])) # color of the process

            #     self.setItem(i, j, item)

class ProcessesTable(BaseTable):
    def __init__(self):
        super().__init__(2, 1, p.PROCESSES_SIMTIME_LABELS) 
        self.setFixedHeight(90)
        self.setFixedWidth(p.SMALL_TABLES_WIDTH)

        for i in range(self.columnCount()):
            self.setColumnWidth(i, 175)
        
        self.setRowHeight(0, 60)


        # self.update_data(processes_num, sim_time)
    
    def update_data(self, processes_num, sim_time): # data = [processes_num, sim_time]
        item = QTableWidgetItem(str(processes_num))
        item.setTextAlignment(Qt.AlignCenter)
        self.setItem(0, 0, item)
        item = QTableWidgetItem(str(sim_time) + "s")
        item.setTextAlignment(Qt.AlignCenter)
        self.setItem(0, 1, item)
        
class RAMDataTable(BaseTable):
    def __init__(self):
        super().__init__(4, 1, p.RAM_DATA_LABELS) 
        self.setFixedHeight(70)
        self.setFixedWidth(p.SMALL_TABLES_WIDTH)

        for i in range(self.columnCount()):
            self.setColumnWidth(i, 87)
        for i in range(self.rowCount()):
            self.setRowHeight(i, 37)
    
    def update_data(self, data): # data = [RAM KB, RAM %, V-RAM KB, V-RAM %]
        for i in range(4):
            if i == 1 or i == 3 :
                perc = "{:.2f}".format(data[i])
                item = QTableWidgetItem(perc + " %")
            else:
                item = QTableWidgetItem(str(data[i]))
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(0, i, item)

class PagesTable(BaseTable):
    def __init__(self):
        super().__init__(2, 1, p.PAGES_LABELS) 
        self.setFixedHeight(60)
        self.setFixedWidth(p.SMALL_TABLES_WIDTH)

        for i in range(self.columnCount()):
            self.setColumnWidth(i, 175)
        for i in range(self.rowCount()):
            self.setRowHeight(i, 15)
    
    def update_data(self, data): # data = [LOADED, UNLOADED]
        for i in range(2):
            item = QTableWidgetItem(str(data[i]))
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(0, i, item)

class ThrashingTable(BaseTable):
    def __init__(self):
        super().__init__(2, 1, p.THRASHING_LABELS)
        self.setFixedHeight(60)
        self.setFixedWidth(p.SMALL_TABLES_WIDTH)

        for i in range(self.columnCount()):
            self.setColumnWidth(i, 175)
        for i in range(self.rowCount()):
            self.setRowHeight(i, 15)
    
    def update_data(self, data): # data = [Thrashing seconds, Thrashing percentage, Fragmentación]
        if data[1] > 50:
            color = QColor(244, 113, 116)
        else:
            color = QColor(255, 255, 255)
        percentage = "{:.2f}".format(data[1])
        item = QTableWidgetItem(str(data[0]) + " s" + " (" + percentage + " %)")
        item.setTextAlignment(Qt.AlignCenter)
        item.setBackground(color)
        self.setItem(0, 0, item)
        item = QTableWidgetItem(str(data[2]) + " KB")
        item.setTextAlignment(Qt.AlignCenter)
        self.setItem(0, 1, item)


class TableWindow(QMainWindow):
    simulation_paused_signal = pyqtSignal(bool)
    
    def __init__(self, process_amount, operations_amount, algorithm, seed, file_path):
        super().__init__()
        self.setFocus()
        self.computer = None
        self.is_paused = False
        self.setFont(p.MAIN_FONT)

        self.setFocusPolicy(Qt.StrongFocus)

        # Window settings
        self.setWindowTitle("Computer Simulation")
        self.setGeometry(100, 100, 900, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.operations = []
        
        layout = QVBoxLayout(central_widget)


        # RAM TABLES
        layout.addWidget(create_title_label("RAM-OPT", 8))
        self.ram_opt_table = RAMTable(100)
        layout.addWidget(self.ram_opt_table)  

        ram_title = "RAM-" + algorithm
        layout.addWidget(create_title_label(ram_title, 8))
        self.ram_alg_table = RAMTable(100)
        layout.addWidget(self.ram_alg_table)  


        # MMU TABLES
        self.mmu_opt_table = MMUTable(5)
        self.mmu_alg_table = MMUTable(5)

        mmu_layout = QHBoxLayout() 

        mmu_opt_layout = QVBoxLayout()
        label = create_title_label("MMU-OPT", 8)
        mmu_opt_layout.addWidget(label)
        mmu_opt_layout.setAlignment(label, Qt.AlignCenter)
        mmu_opt_layout.addWidget(self.mmu_opt_table)
        mmu_layout.addLayout(mmu_opt_layout)
        
        mmu_alg_layout = QVBoxLayout()
        alg = algorithm
        title = "MMU-" + alg
        label = create_title_label(title, 8)
        mmu_alg_layout.addWidget(label)
        mmu_alg_layout.setAlignment(label, Qt.AlignCenter) 
        mmu_alg_layout.addWidget(self.mmu_alg_table)
        mmu_layout.addLayout(mmu_alg_layout)

        layout.addLayout(mmu_layout) 

        # Processes and sim-time 
        self.processes_sim_time_opt = ProcessesTable()

        self.processes_sim_time_alg = ProcessesTable()

        process_simtime_layout = QHBoxLayout() 
        process_simtime_layout.addWidget(self.processes_sim_time_opt)
        process_simtime_layout.addWidget(self.processes_sim_time_alg)
        layout.addLayout(process_simtime_layout)

        # RAM data tables
        self.ram_data_opt = RAMDataTable()

        self.ram_data_alg = RAMDataTable()

        ram_data_layout = QHBoxLayout()
        ram_data_layout.addWidget(self.ram_data_opt)
        ram_data_layout.addWidget(self.ram_data_alg)
        layout.addLayout(ram_data_layout)

        # Pages tables
        self.pages_opt = PagesTable()
        self.pages_alg = PagesTable()

        pages_layout = QHBoxLayout()
        pages_layout.addWidget(self.pages_opt)
        pages_layout.addWidget(self.pages_alg)

        layout.addLayout(pages_layout)

        # Thrashing tables
        self.thrashing_opt = ThrashingTable()
        self.thrashing_alg = ThrashingTable()

        thrashing_layout = QHBoxLayout()
        thrashing_layout.addWidget(self.thrashing_opt)
        thrashing_layout.addWidget(self.thrashing_alg)

        layout.addLayout(thrashing_layout)
        
        self.algorithm = self.choose_algorithm(algorithm)
        
        self.start_simulation(seed, operations_amount, process_amount, algorithm, file_path)
        
        
    def start_simulation(self, seed, operations_amount, process_amount,algorithm, file_path):
        opt = OPT()
        print(file_path)
        if file_path == "":
            print("Generating file")
            self.generate_file_thread = GenerateFileThread(seed, operations_amount, process_amount)
            self.generate_file_thread.finished.connect(self.on_generate_file_finished)
            self.generate_file_thread.start()
            self.operations = read_file("operations.txt")
                        
        else:
            self.operations = read_file(file_path)
                     
        
        main_mmu = MMU(opt)
        other_mmu = MMU(self.algorithm)
        
        session = Session(len(self.operations), self.operations)
        
        self.computer = Computer(main_mmu, other_mmu, session)
                
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_window_data)

        # Start the timer to update data every second
        self.update_window_data()
 
    def update_window_data(self):
        # Check if there are more operations to execute
        if self.operations:
            if not self.is_paused:
                operation = self.operations.pop(0)  # Get the next operation
                # Execute the operation (replace this with your operation)
                # For demonstration purposes, we'll just display the operation in the label
                self.computer.execute_instruction(operation)
                # Update the window with the new data
                self.update_data()
                self.show()
            # Call update_window_data again after 1000 milliseconds (1 second)
            self.timer.start(1000)
            
        else:
            # All operations executed, stop the timer
            self.timer.stop()
 

    def choose_algorithm(self, algorithm):
        if algorithm == "FIFO":
            return FIFO()            
        elif algorithm == "MRU":
            return MRU()
        elif algorithm == "OPT":
            return OPT()
        elif algorithm == "SC":
            return SC()
        elif algorithm == "RND":
            return RND()

          
             

    def on_generate_file_finished(self, file_path):
        self.operations = read_file(file_path)
          
        

    def update_data(self):
        other_processes = self.computer.other_processes
        main_processes = self.computer.main_processes
        other_ram_pages = []
        opt_ram_pages = []
        for process in other_processes:
            pointers = process.page_table
            color = process.color
            process_pages = []
            process_pages.append(color)
            for pointer in pointers:
                process_pages.extend(self.computer.other_mmu.memory_map[pointer])
            other_ram_pages.append(process_pages)
           
        for process in main_processes:
            pointers = process.page_table
            color = process.color
            process_pages = []
            process_pages.append(color)
            for pointer in pointers:
                process_pages.extend(self.computer.opt_mmu.memory_map[pointer])
            opt_ram_pages.append(process_pages)

        self.ram_alg_table.update_data(other_ram_pages)
        self.ram_opt_table.update_data(opt_ram_pages)
        
        opt_pages_list = opt_ram_pages
        alg_pages_list = other_ram_pages
        

        #SIMULATION TIME
        opt_total_sim_time, other_total_sim_time = self.computer.get_time()
        self.processes_sim_time_opt.update_data(len(self.computer.main_processes), opt_total_sim_time)
        self.processes_sim_time_alg.update_data(len(self.computer.other_processes), other_total_sim_time)
        
        # THRASHING
        opt_thrashing_time, other_thrashing_time = self.computer.get_thrashing_time()
        opt_thrashing_perc = (opt_thrashing_time * 100) / opt_total_sim_time
        other_thrashing_perc = (other_thrashing_time * 100) / other_total_sim_time
        self.thrashing_opt.update_data([opt_thrashing_time, opt_thrashing_perc, 0])
        self.thrashing_alg.update_data([other_thrashing_time, other_thrashing_perc, 0])

        #RAM DATA TABLE
        opt_ram_pages, other_ram_pages = self.computer.get_ram_pages() # real memory
        opt_ram_size = opt_ram_pages * 4
        other_ram_size = other_ram_pages * 4

        opt_ram_perc = (opt_ram_size * 100) / 400
        other_ram_perc = (other_ram_size * 100) / 400

        #vram
        opt_vram_pages, opt_vram_total_size, other_vram_pages, other_vram_total_size = self.computer.get_vram_size() # virtual memory
        
        opt_vram_size = opt_vram_pages * 4
        other_vram_size = other_vram_pages * 4
    
        opt_vram_perc = (opt_vram_size * 100) / opt_vram_total_size 
        other_vram_perc = (other_vram_size * 100) / other_vram_total_size 

        self.ram_data_opt.update_data([opt_ram_size, opt_ram_perc, opt_vram_size, opt_vram_perc])
        self.ram_data_alg.update_data([other_ram_size, other_ram_perc, other_vram_size, other_vram_perc])

        #PAGES TABLE
        self.pages_opt.update_data([opt_ram_pages, opt_vram_pages])
        self.pages_alg.update_data([other_ram_pages, other_vram_pages])
        
        # MMU TABLES [ opt_total_pages, main_processes, opt_ram_pages]
        self.mmu_opt_table.update_data([(opt_ram_pages + opt_vram_pages), main_processes, opt_pages_list, self.computer])
        self.mmu_alg_table.update_data([(other_ram_pages + other_vram_pages), other_processes, alg_pages_list, self.computer])
        



    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.operations = []
            self.close()
        elif event.key() == Qt.Key_Space:
            print("Space pressed")
            self.pause_simulation()

        super().keyPressEvent(event)

    def pause_simulation(self):
        if self.is_paused:
            self.is_paused = False
            print("Simulation resumed")
        else:
            self.is_paused = True
            print("Simulation paused")
    



def create_title_label(text, font_size):
    label = QLabel(text)
    font = label.font()
    font.setPointSize(font_size)
    label.setFont(font)
    return label




class GenerateFileThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, seed, operations_amount, process_amount):
        super().__init__()
        self.seed = seed
        self.operations_amount = operations_amount
        self.process_amount = process_amount

    def run(self):
        generate_file(int(self.seed), int(self.operations_amount), int(self.process_amount))
        self.finished.emit('operations.txt')



