
from PyQt5.QtGui import QFont

ALGORITHMS = ["FIFO", "SC", "MRU", "RND", "Algorithm"]
PROCESS_NUM = ["10", "50", "100", "0"]
OPERATIONS_NUM = ["500", "1000", "5000", "0"]
MAIN_FONT = QFont("Roboto", 13) 
TITLE_FONT = QFont("Roboto", 20, QFont.Bold) 
TEXT_FONT = ("Roboto", 15)
TEXT_FONT_BOLD = ("Roboto", 15, "bold")
APPEARANCE_MODE = "light"
COLOR_THEME = "blue"

SB_WIDTH = 100
SB_HEIGHT = 50

LABEL_WIDTH = 0
LABEL_HEIGHT = 0

MMU_TABLE_COLUMNS = ["PAGE ID", "PID", "LOADED", "L-ADDR", "M-ADDR", "LOADED-T", "MARK"]
PROCESSES_SIMTIME_LABELS = ["Processes", "Simulation time"]
RAM_DATA_LABELS = ["RAM KB", "RAM %", "V-RAM KB", "V-RAM %"]
PAGES_LABELS = ["LOADED Pages", "UNLOADED Pages"]
THRASHING_LABELS = ["Thrashing", "Fragmentación"]

SMALL_TABLES_WIDTH = 350