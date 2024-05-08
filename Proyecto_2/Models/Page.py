from datetime import datetime

class Page:
    def __init__(self, page_id: int, physical_address: int, position_flag: bool):
        self.page_id: int = page_id
        self.physical_address: int = physical_address
        self.position_flag: bool = position_flag # true = real, false = virtual
        self.timestamp: int = 0
        self.last_access: int = 0
        self.second_chance: int = 1

    