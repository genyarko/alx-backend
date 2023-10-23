#!/usr/bin/env python3
"""
Hypermedia pagination sample.
"""
import csv
import math
from typing import Dict, List, Tuple


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
        """Retrieve and cache the dataset.

        Returns:
            List[List]: Dataset as list of lists.
        """
        if self.__dataset is None:
            try:
                with open(self.DATA_FILE) as f:
                    reader = csv.reader(f)
                    dataset = [row for row in reader]
                self.__dataset = dataset[1:]  # Exclude the header row
            except FileNotFoundError:
                print(f"{self.DATA_FILE} not found.")
                self.__dataset = []

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Retrieve a specific page of data.

        Args:
            page (int): Page number. Defaults to 1.
            page_size (int): Number of items per page. Defaults to 10.

        Returns:
            List[List]: Data for the specified page.
        """
        assert isinstance(page, int) and page > 0, "page must be a positive integer"
        assert isinstance(page_size, int) and page_size > 0, "page_size must be a positive integer"

        data = self.dataset()
        
        if (page - 1) * page_size >= len(data):
            return []

        start, end = index_range(page, page_size)
        
        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Retrieve information about a specific page.

        Args:
            page (int): Page number. Defaults to 1.
            page_size (int): Number of items per page. Defaults to 10.

        Returns:
            Dict: Information about the specified page.
        """
        data = self.get_page(page, page_size)
        
        if not data:
            return {}

        total_pages = math.ceil(len(self.dataset()) / page_size)

        hyper_info = {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': page + 1 if (page + 1) <= total_pages else None,
            'prev_page': page - 1 if (page - 1) > 0 else None,
            'total_pages': total_pages,
        }

        return hyper_info
