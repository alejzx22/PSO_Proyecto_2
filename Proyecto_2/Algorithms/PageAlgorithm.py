# Superclass for all page replacement algorithms
class PageAlgorithm:
    def __init__(self, memory_capacity: int=100):
        self.memory_capacity: int = memory_capacity # Number of pages that can be stored in memory
        # self.memory: list = real_memory # List of pages currently in memory

    def reference_page(self, page):
        pass

    def delete(self, page):
        self.memory[page.physical_address] = None

    def print_memory(self):
        print("Memory content:")
        for page in self.memory:
            print(f"Page {page.id}")