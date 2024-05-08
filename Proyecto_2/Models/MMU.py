#from Algorithms.OPT import OPT
from Models.Page import Page
from Models.Process import Process

class MMU:
    def __init__(self, algorithm: object | None, real_mem_size: int=100):
        self.real_mem_size: int = real_mem_size        
        self.algorithm: object = algorithm
        self.real_memory: list = [None] * self.real_mem_size
        self.virtual_memory: list = [None]
        self.memory_map: dict = {}
        self.page_count: int = 0
        self.pointer_count: int = 0
        self.total_time: int = 1
        self.thrashing_time: int = 1
        self.set_algorithm(algorithm)

    def set_algorithm(self, algorithm: object):
        self.algorithm = algorithm
        self.algorithm.memory = self.real_memory

    def new(self, pid: int, size: int):
        # Get the required pages for the process
        pages = size // 4
        if size % 4 != 0:
            pages += 1
                    
        inserted_pages = 0
        created_pages = []
        for page_counter in range(pages):            
            for space_in_real_memory in range(self.real_mem_size):
                if self.real_memory[space_in_real_memory] is None:
                    page = Page(self.page_count, space_in_real_memory, True) 
                    page.timestamp = self.total_time                   
                    self.page_count += 1
                    self.real_memory[space_in_real_memory] = page
                    created_pages.append(page)
                    inserted_pages += 1
                    self.total_time += 1
                    break     
                
        if inserted_pages < pages:
            while inserted_pages < pages:
                page = Page(self.page_count, -1, False)
                self.page_count += 1
                page, time = self.algorithm.reference_page(page)
                self.virtual_memory.append(page)
                created_pages.append(page)
                inserted_pages += 1       
                self.total_time += time
                self.thrashing_time += time
                
                        
            
        current_pointer = self.pointer_count
        self.memory_map[current_pointer] = created_pages
        self.pointer_count += 1
        
        return current_pointer
        
    def get_key_for_page(self, target_page):
        for key, pages in self.memory_map.items():
            if target_page in pages:
                return key
        return None

    def use(self, pointer: int):
        if len(self.memory_map) == 0:
            return
        
        # Get the pages from the memory map
        pages = self.memory_map[pointer]
        
        for page in pages:
            new_page, time = self.algorithm.reference_page(page)
            page.last_access = self.total_time
            if new_page is not None: 
                self.virtual_memory.append(new_page) # New = pag a virtual
                page.timestamp = self.total_time
                self.real_memory[new_page.physical_address] = page # page = pag a real
                self.thrashing_time += time
            self.total_time += time

    def delete(self, pointer: int):        
        pages = self.memory_map[pointer]
        for page in pages:
            if (page.position_flag == True):
                self.algorithm.delete(page)
                self.real_memory[page.physical_address] = None
                self.total_time += 1
            else:
                self.virtual_memory.remove(page)
                self.total_time += 5
                self.thrashing_time += 5
        self.memory_map.pop(pointer)

    def kill(self, process: Process):
        for pointer in process.page_table:
            self.delete(pointer)
        process.page_table = []

    def get_time(self):
        return self.total_time
    
    def get_thrashing_time(self):
        return self.thrashing_time