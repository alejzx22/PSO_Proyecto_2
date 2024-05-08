from Models.Page import Page
from Algorithms.PageAlgorithm import PageAlgorithm

class MRU(PageAlgorithm):
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
            
        # If the page is not in memory, replace the page with the most recently used page
        max_time = 9223372036854775807
        max_page = None
        for page in self.memory:
            if page.last_access < max_time: # mayor tiempo es la que se usó más recientemente
                max_time = page.last_access
                max_page = page

        physical_address = max_page.physical_address
        self.memory.remove(max_page)
        
        # Add the new page to memory
        ref_page.physical_address = physical_address
        self.memory.append(ref_page)

        return (max_page, 5)