class Process:
    def __init__(self, pid: int, size: int, color: tuple):
        self.pid: int = pid
        self.size: int = size
        self.page_table: list = []
        self.color: tuple = color
        