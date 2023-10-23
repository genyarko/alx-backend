#!/usr/bin/env python3
"""
Module for index_range function
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate start and end index for pagination

    Parameters:
    page (int): page number
    page_size (int): number of items per page

    Returns:
    tuple: a tuple of size two containing a start index and an end index
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return start_index, end_index
