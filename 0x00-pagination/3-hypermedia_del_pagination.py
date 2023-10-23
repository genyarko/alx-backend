#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination
"""
import csv
from typing import List, Dict

class Server:
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]  # Limit the indexed dataset to the first 1000 rows
            self.__indexed_dataset = {
                i: row for i, row in enumerate(truncated_dataset)
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """Retrieve a specific page of data based on its index.

        Args:
            index (int): Index number. Defaults to 0.
            page_size (int): Number of items per page. Defaults to 10.

        Returns:
            Dict: Information about the specified page.
        """
        assert isinstance(index, int) and index >= 0, "index must be a non-negative integer"
        assert isinstance(page_size, int) and page_size > 0, "page_size must be a positive integer"

        indexed_data = self.indexed_dataset()
        
        data = []
        next_index = index
        for _ in range(page_size):
            # Skip over deleted rows
            while indexed_data.get(next_index) is None and next_index < len(indexed_data):
                next_index += 1
            if next_index >= len(indexed_data):
                break
            data.append(indexed_data[next_index])
            next_index += 1

        hyper_info = {
            'index': index,
            'next_index': next_index,
            'page_size': len(data),
            'data': data,
        }

        return hyper_info
