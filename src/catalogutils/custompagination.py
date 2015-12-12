# custom pagination class
from math import ceil


class cusotmPaginator(object):

    def __init__(self, page, items_per_page, items):
        """
        the constructor for the custom pagination class
        Arguments:
        page : the current page number
        items_per_page :  how many records to show in each page
        items : the collection of items to be paginated
        """
        self.current_page = page
        self.items_per_page = items_per_page
        self.total_count = len(items)
        self.items = items

    @property
    def totalPages(self):
        """
        returns the total number of pages required
        """
        tot_pages = ceil(self.total_count / float(self.items_per_page))
        return int(tot_pages)

    @property
    def hasPagesBefore(self):
        """
         return if there are pages before the current page number

        """
        return self.current_page > 1

    @property
    def hasPagesAfter(self):
        """
         returns true if there are pages after the current page.

        """
        return self.current_page < self.totalPages

    def pages_list(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """
        returns a collection of page numbers
        """

        last = 0
        for num in xrange(1, self.totalPages + 1):
            if num <= left_edge or \
               (num > self.current_page - left_current - 1 and
                num < self.current_page + right_current) or \
               num > self.totalPages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

    def getPageSlice(self):
        """
        returns the slice of the object according to the page
        """
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page

        return self.items[start:end]
