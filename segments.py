from dataclasses import dataclass
from typing import TypeAlias

@dataclass
class Point:
    lat: float
    lon: float

@dataclass
class Segment:
    start: Point
    end: Point

class Box:
    bottom_left: Point
    top_right: Point

Segments: TypeAlias = list[Segment]

def download_segments(box: Box, filename: str) -> None:
    """Download all segments in the box and save them to the file."""
    ...

def load_segments(filename: str) -> Segments:
    """Load segments from the file."""
    ...


def get_segments(box: Box, filename: str) -> Segments:
    """
    Get all segments in the box.
    If filename exists, load segments from the file.
    Otherwise, download segments in the box and save them to the file.
    """
    ...

def show_segments(segments: Segments, filename: str) -> None:
    """Show all segments in a PNG file using staticmaps."""
    ...