#!/usr/bin/env python3
"""Simple pagination sample.
"""
import csv
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Calculate index range for pagination.

    Args:
        page (int): Page number.
        page_size (int): Number of items per page.

    Returns:
        Tuple[int, int]: Start index and end index.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize a new Server instance.
        """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Retrieve cached dataset.

        Returns:
            List[List]: Dataset as list of lists.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Retrieve a page of data.

        Args:
            page (int): Page number. Defaults to 1.
            page_size (int): Number of items per page. Defaults to 10.

        Returns:
            List[List]: Page of data.
        """
        assert isinstance(page, int) and page > 0, "page must be a positive integer"
        assert isinstance(page_size, int) and page_size > 0, "page_size must be a positive integer"

        data = self.dataset()
        
        if (page - 1) * page_size >= len(data):
            return []

        start, end = index_range(page, page_size)
        
        return data[start:end]
