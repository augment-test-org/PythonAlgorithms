"""
Collision detection algorithms for basic geometric shapes.
Supports collision detection between:
- Circles
- Rectangles (Axis-Aligned Bounding Boxes)
- Circle and Rectangle

Example:
    >>> from geometry import Circle, Rectangle
    >>> circle1 = Circle(5)  # circle with radius 5
    >>> circle2 = Circle(3)  # circle with radius 3
    >>> detect_circle_collision(circle1, circle2, (0, 0), (7, 0))
    True  # circles overlap at x=7 (distance less than sum of radii 5+3=8)
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple

from geometry import Circle, Rectangle

Point = Tuple[float, float]


@dataclass
class AABB:
    """
    Axis-Aligned Bounding Box representation of a rectangle.
    Stores the minimum and maximum coordinates of the box.

    >>> box = AABB.from_rectangle(Rectangle(2, 3), (0, 0))
    >>> box.min_x, box.min_y, box.max_x, box.max_y
    (-1.0, -1.5, 1.0, 1.5)
    """

    min_x: float
    min_y: float
    max_x: float
    max_y: float

    @classmethod
    def from_rectangle(cls, rect: Rectangle, center: Point) -> AABB:
        """
        Create an AABB from a Rectangle and its center point.

        >>> box = AABB.from_rectangle(Rectangle(4, 6), (1, 2))
        >>> box.min_x, box.min_y, box.max_x, box.max_y
        (-1.0, -1.0, 3.0, 5.0)
        """
        half_width = rect.short_side.length / 2
        half_height = rect.long_side.length / 2
        return cls(
            center[0] - half_width,
            center[1] - half_height,
            center[0] + half_width,
            center[1] + half_height,
        )


def detect_circle_collision(circle1: Circle, circle2: Circle, pos1: Point, pos2: Point) -> bool:
    """
    Detect collision between two circles at given positions.
    Returns True if circles overlap or touch, False otherwise.

    >>> detect_circle_collision(Circle(5), Circle(3), (0, 0), (7, 0))
    True
    >>> detect_circle_collision(Circle(5), Circle(3), (0, 0), (9, 0))
    False
    >>> detect_circle_collision(Circle(5), Circle(3), (0, 0), (8, 0))  # touching
    True
    """
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    distance = math.sqrt(dx * dx + dy * dy)
    return distance <= (circle1.radius + circle2.radius)  # Changed < to <=


def detect_aabb_collision(rect1: Rectangle, rect2: Rectangle, pos1: Point, pos2: Point) -> bool:
    """
    Detect collision between two rectangles using AABB method.
    Returns True if rectangles overlap, False otherwise.

    >>> detect_aabb_collision(Rectangle(2, 3), Rectangle(2, 2), (0, 0), (1, 1))
    True
    >>> detect_aabb_collision(Rectangle(2, 3), Rectangle(2, 2), (0, 0), (3, 3))
    False
    """
    box1 = AABB.from_rectangle(rect1, pos1)
    box2 = AABB.from_rectangle(rect2, pos2)

    return (
        box1.min_x <= box2.max_x
        and box1.max_x >= box2.min_x
        and box1.min_y <= box2.max_y
        and box1.max_y >= box2.min_y
    )


def detect_circle_rectangle_collision(
    circle: Circle, rect: Rectangle, circle_pos: Point, rect_pos: Point
) -> bool:
    """
    Detect collision between a circle and a rectangle.
    Returns True if shapes overlap, False otherwise.

    >>> detect_circle_rectangle_collision(Circle(2), Rectangle(4, 4), (0, 0), (3, 0))
    True
    >>> detect_circle_rectangle_collision(Circle(2), Rectangle(4, 4), (0, 0), (5, 0))
    False
    """
    box = AABB.from_rectangle(rect, rect_pos)

    # Find the closest point on the rectangle to the circle's center
    closest_x = max(box.min_x, min(circle_pos[0], box.max_x))
    closest_y = max(box.min_y, min(circle_pos[1], box.max_y))

    # Calculate distance between the closest point and circle center
    dx = circle_pos[0] - closest_x
    dy = circle_pos[1] - closest_y
    distance = math.sqrt(dx * dx + dy * dy)

    return distance < circle.radius


if __name__ == "__main__":
    import doctest

    doctest.testmod()
