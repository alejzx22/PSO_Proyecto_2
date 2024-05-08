from Models.Page import Page
from Algorithms.PageAlgorithm import PageAlgorithm

class SC(PageAlgorithm):
    def __init__(self, memory_capacity: int=100):
        super().__init__(memory_capacity)

    def reference_page(self, ref_page):
        # Increment the usage time of all pages in memory
        for page in self.memory:
            page.last_access += 1

        # Check if the page is already in memory
        for page in self.memory:
            if page.page_id == ref_page.page_id:
                page.last_access = 0  # Reset the usage time
                return (None, 1)
            
        # If the second chance bit is 0, replace the page with the oldest second chance bit
        i = 0
        length = len(self.memory)
        while True:
            page = self.memory[i]
            
            if page.second_chance == 0:
                physical_address = page.physical_address
                self.memory.remove(page)
                break
            else:
                page.second_chance = 0
            i = (i+1) % length

        # Add the new page to memory
        ref_page.physical_address = physical_address
        self.memory.append(ref_page)

        return (page, 5)