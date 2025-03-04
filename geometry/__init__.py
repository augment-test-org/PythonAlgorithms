
"""Geometry module containing various geometric shapes and algorithms."""
from geometry.collision_detection import (
    detect_aabb_collision,
    detect_circle_collision,
    detect_circle_rectangle_collision,
)
from geometry.geometry import Circle, Rectangle

__all__ = [
    'Circle',
    'Rectangle',
    'detect_aabb_collision',
    'detect_circle_collision',
    'detect_circle_rectangle_collision',
]
