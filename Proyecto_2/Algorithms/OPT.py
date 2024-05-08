from Models.Page import Page
from Algorithms.PageAlgorithm import PageAlgorithm

class OPT(PageAlgorithm):
    def __init__(self,memory_capacity: int=100):
        super().__init__(memory_capacity)

    def reference_page(self, ref_page):
        # Check if the page is already in memory
        for page in self.memory:
            if page.page_id == ref_page.page_id:
                page.last_access = 0  # Reset the usage time
                return (None, 1)

        # If the page is not in memory, replace the page with the longest time since last access
        max_time = -1
        max_page = None
        for page in self.memory:
            if page.last_access > max_time:
                max_time = page.last_access
                max_page = page
        
        physical_address = max_page.physical_address
        
        
        self.memory.remove(max_page)
        
        # Add the new page to memory
        ref_page.physical_address = physical_address
        self.memory.append(ref_page)

        return (max_page, 5)

        