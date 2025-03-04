
"""Geometry module containing various geometric shapes and algorithms."""
from geometry.geometry import Circle, Rectangle
from geometry.collision_detection import (
    detect_circle_collision,
    detect_aabb_collision,
    detect_circle_rectangle_collision,
)

__all__ = [
    'Circle',
    'Rectangle',
    'detect_circle_collision',
    'detect_aabb_collision',
    'detect_circle_rectangle_collision',
]
