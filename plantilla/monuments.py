from dataclasses import dataclass
from segments import Point, Box
from typing import TypeAlias


@dataclass
class Monument:
    name: str
    location: Point

Monuments: TypeAlias = list[Monument]


def download_monuments() -> Monuments:
    """Download monuments from Catalunya Medieval."""
    ...

def load_monuments(box: Box, filename: str) -> Monuments:
    """Load monuments from a file."""
    ...

def get_monuments(box: Box, filename: str) -> Monuments:
    """
    Get all monuments in the box.
    If filename exists, load monuments from the file.
    Otherwise, download monuments and save them to the file.
    """
    ...
