#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import Dict, List

class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize a new Server instance and fetch the dataset."""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Retrieve and cache the dataset.

        Returns:
            List[List]: Cached dataset.
        """
        if self.__dataset is None:
            try:
                with open(self.DATA_FILE) as f:
                    reader = csv.reader(f)
                    self.__dataset = list(reader)[1:]  # Exclude the header row
            except FileNotFoundError:
                print(f"File {self.DATA_FILE} not found.")
                self.__dataset = []

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Create an indexed dataset based on sorting position, starting at 0.

        Returns:
            Dict[int, List]: Indexed dataset.
        """
        if self.__indexed_dataset is None:
            truncated_dataset = self.dataset()[:1000]  # Limit the indexed dataset to the first 1000 rows
            self.__indexed_dataset = {i: row for i, row in enumerate(truncated_dataset)}

        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """Retrieve information about a specific page based on its index and size.

        Args:
            index (int, optional): Index number. Defaults to 0.
            page_size (int): Number of items per page. Defaults to 10.

        Returns:
            Dict: Information about the specified page.
        """
        data = self.indexed_dataset()

        # Check that the provided index is valid
        if index < 0 or index > max(data.keys()):
            raise ValueError("Invalid index value.")

        page_data = []
        data_count = 0
        next_index = None

        for i, item in data.items():
            if i >= index and data_count < page_size:
                page_data.append(item)
                data_count += 1
            elif data_count == page_size:
                next_index = i
                break

        return {
            'index': index,
            'next_index': next_index,
            'page_size': len(page_data),
            'data': page_data,
        }
