from Models.Process import Process
from Models.Session import Session
from Models.MMU import MMU
import random

class Computer:
    def __init__(self, main_mmu, other_mmu, session: Session):
        self.instructions_per_second: int = 1
        self.disk_access_time: int = 5
        self.RAM_size: int = 800 #KB
        self.hard_drive: int = 999999
        self.page_size: int = 4 #KB
        self.session: Session = session
        self.opt_mmu: MMU = main_mmu
        self.other_mmu: MMU = other_mmu
        self.main_processes = []
        self.other_processes = []
        self.used_colors = []

    
        

    def execute_instruction(self, operation: str):
        
        if operation[0] == 'n':
            operation = operation[4:] # remove 'new('
            operation = operation[:-1] # remove ')'
            operation = operation.split(',')

            operation[0] = operation[0].strip()
            operation[1] = operation[1].strip()

            self.run_new(operation[0], operation[1])

        elif operation[0] == 'u':
            operation = operation[4:] # remove 'use('
            operation = operation[:-1] # remove ')'
            for process in self.main_processes:
                if process.pid == int(operation):
                    self.run_use(operation)
                    return
            for process in self.other_processes:
                if process.pid == int(operation):
                    self.run_use(operation)
                    return
            print('Process not found')


        elif operation[0] == 'd':
            operation = operation[7:] # remove 'delete('
            operation = operation[:-1] # remove ')'
            for process in self.main_processes:
                if process.pid == int(operation):
                    self.run_delete(operation)
                    return
            for process in self.other_processes:
                if process.pid == int(operation):
                    self.run_delete(operation)
                    return
            self.run_delete(operation)

        elif operation[0] == 'k':
            operation = operation[5:] # remove 'kill('
            operation = operation[:-1] # remove ')'
            for process in self.main_processes:
                if process.pid == int(operation):
                    self.run_kill(operation)
                    return
            for process in self.other_processes:
                if process.pid == int(operation):
                    self.run_kill(operation)
                    return
        else:
            print('Invalid operation')
            
                
    def run_new(self, pid, size):
        color = generate_random_color(self.used_colors)
        self.used_colors.append(color)
        opt_pointer = self.opt_mmu.new(int(pid), int(size))
        other_pointer = self.other_mmu.new(int(pid), int(size))
        exists = False
        for process in self.main_processes:
            if process.pid == int(pid):
                process.page_table.append(opt_pointer)
                exists = True
                break
        for process in self.other_processes:
            if process.pid == int(pid):
                process.page_table.append(other_pointer)
                exists = True
                break
        if not exists:
            opt_process = Process(int(pid), int(size), color)
            other_process = Process(int(pid), int(size), color)
            opt_process.page_table.append(opt_pointer)
            other_process.page_table.append(other_pointer)      
            self.main_processes.append(opt_process)
            self.other_processes.append(other_process)

    def run_use(self, ptr):
        self.opt_mmu.use(int(ptr))
        self.other_mmu.use(int(ptr))

    def run_delete(self, ptr):        
        self.opt_mmu.delete(int(ptr))
        self.other_mmu.delete(int(ptr))
        for process in self.main_processes:
            if int(ptr) == process.pid:
                process.page_table.clear()
                break
        for process in self.other_processes:
            if int(ptr) == process.pid:
                process.page_table.clear()
                break

    def run_kill(self, pid):
        index_of = 0
        
        for process in self.main_processes:
            if process.pid == int(pid):
                self.main_processes.remove(process)
                break
            index_of += 1
        
        process_to_kill = self.other_processes.pop(index_of)
        
        
        self.opt_mmu.kill(process_to_kill)
        self.other_mmu.kill(process_to_kill)
        
    def get_time(self):
        return self.opt_mmu.get_time(), self.other_mmu.get_time()
    
    def get_thrashing_time(self):
        return self.opt_mmu.thrashing_time, self.other_mmu.thrashing_time
        
    def get_vram_size(self):
        opt_pages_count = 0
        other_pages_count = 0

        for page in self.opt_mmu.virtual_memory:
            if page is not None:
                opt_pages_count += 1

        for page in self.other_mmu.virtual_memory:
            if page is not None:
                other_pages_count += 1

        return opt_pages_count, len(self.opt_mmu.virtual_memory), other_pages_count, len(self.other_mmu.virtual_memory)
    
    def get_ram_pages(self):
        opt_pages_count = 0
        other_pages_count = 0 

        for page in self.opt_mmu.real_memory:
            if page is not None:
                opt_pages_count += 1

        for page in self.other_mmu.real_memory:
            if page is not None:
                other_pages_count += 1

        return opt_pages_count, other_pages_count
    
    def get_other_alg(self):
        return self.other_mmu.algorithm
    
    def get_process_by_color(self, color):
        for process in self.main_processes:
            if process.color == color:
                return process
        for process in self.other_processes:
            if process.color == color:
                return process
        return None
    
    def get_pointer_by_page(self, page):
        key = self.opt_mmu.get_key_for_page(page)
        if key is not None:
            return key
        else:
            key = self.other_mmu.get_key_for_page(page)
            return key        
        
    
def generate_random_color(used_colors):
    while True:
        # Generate a random color in RGB format
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # Check if the color is not in the list of used colors
        if color not in used_colors:
            return color
