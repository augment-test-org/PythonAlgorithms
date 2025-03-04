"""
This is a Python implementation for collision detection between geometric shapes.
The implementation supports detecting intersections between basic shapes like circles
and rectangles in 2D space.

Question :-
Given two geometric shapes and their positions in 2D space, determine if they intersect
or overlap with each other. The shapes can be:
- Circles (defined by center point and radius)
- Rectangles (defined by center point and dimensions)

The implementation uses Axis-Aligned Bounding Box (AABB) technique for efficient
rectangle collision detection.

Example:
    >>> detector = CollisionDetector()
    >>> # Test circle-circle collision
    >>> circle1, circle2 = Circle(5), Circle(3)
    >>> detector.detect_circle_collision(circle1, circle2, (0, 0), (7, 0))
    True  # circles overlap as distance (7) < sum of radii (8)
    >>> detector.detect_circle_collision(circle1, circle2, (0, 0), (9, 0))
    False  # circles don't overlap as distance (9) > sum of radii (8)
    >>> # Test rectangle-rectangle collision
    >>> rect1, rect2 = Rectangle(4, 6), Rectangle(2, 2)
    >>> detector.detect_aabb_collision(rect1, rect2, (0, 0), (1, 1))
    True  # rectangles overlap
    >>> detector.detect_aabb_collision(rect1, rect2, (0, 0), (5, 5))
    False  # rectangles don't overlap
    >>> # Test circle-rectangle collision
    >>> circle, rect = Circle(2), Rectangle(4, 4)
    >>> detector.detect_circle_rectangle_collision(circle, rect, (0, 0), (3, 0))
    True  # shapes overlap as circle edge reaches rectangle
    >>> detector.detect_circle_rectangle_collision(circle, rect, (0, 0), (5, 0))
    False  # shapes don't overlap
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
    """
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    @classmethod
    def from_rectangle(cls, rect: Rectangle, center: Point) -> AABB:
        """Convert a Rectangle at given center point to AABB representation."""
        half_width = rect.short_side.length / 2
        half_height = rect.long_side.length / 2
        return cls(
            center[0] - half_width,
            center[1] - half_height,
            center[0] + half_width,
            center[1] + half_height,
        )


class CollisionDetector:
    """
    A class that provides methods for detecting collisions between different geometric shapes.
    Supports collision detection between:
    - Circle to Circle
    - Rectangle to Rectangle (using AABB)
    - Circle to Rectangle
    """

    @staticmethod
    def detect_circle_collision(circle1: Circle, circle2: Circle, pos1: Point, pos2: Point) -> bool:
        """
        Detect collision between two circles at given positions.
        Returns True if circles overlap or touch, False otherwise.
        """
        # Calculate distance between circle centers using Pythagorean theorem
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Circles collide if distance is less than or equal to sum of radii
        return distance <= (circle1.radius + circle2.radius)

    @staticmethod
    def detect_aabb_collision(rect1: Rectangle, rect2: Rectangle, pos1: Point, pos2: Point) -> bool:
        """
        Detect collision between two rectangles using AABB method.
        Returns True if rectangles overlap, False otherwise.
        """
        # Convert rectangles to AABB representation
        box1 = AABB.from_rectangle(rect1, pos1)
        box2 = AABB.from_rectangle(rect2, pos2)

        # Check for overlap in both x and y axes
        return (
            box1.min_x <= box2.max_x
            and box1.max_x >= box2.min_x
            and box1.min_y <= box2.max_y
            and box1.max_y >= box2.min_y
        )

    @staticmethod
    def detect_circle_rectangle_collision(
        circle: Circle, rect: Rectangle, circle_pos: Point, rect_pos: Point
    ) -> bool:
        """
        Detect collision between a circle and a rectangle.
        Returns True if shapes overlap, False otherwise.
        """
        # Convert rectangle to AABB
        box = AABB.from_rectangle(rect, rect_pos)

        # Find the closest point on rectangle to circle center
        closest_x = max(box.min_x, min(circle_pos[0], box.max_x))
        closest_y = max(box.min_y, min(circle_pos[1], box.max_y))

        # Calculate distance between closest point and circle center
        dx = circle_pos[0] - closest_x
        dy = circle_pos[1] - closest_y
        distance = math.sqrt(dx * dx + dy * dy)

        # Collision occurs if distance is less than circle radius
        return distance < circle.radius


if __name__ == "__main__":
    # Run doctest examples
    import doctest
    doctest.testmod()

    # Additional test cases
    detector = CollisionDetector()
    
    # Test circle-circle collision
    print("\nTesting circle-circle collision:")
    circle1, circle2 = Circle(5), Circle(3)
    test_cases = [
        ((0, 0), (7, 0), True, "Overlapping circles"),
        ((0, 0), (8, 0), True, "Touching circles"),
        ((0, 0), (9, 0), False, "Non-overlapping circles"),
        ((0, 0), (5, 5), True, "Diagonal overlap"),
    ]
    for pos1, pos2, expected, desc in test_cases:
        result = detector.detect_circle_collision(circle1, circle2, pos1, pos2)
        print(f"{desc}: {'✓' if result == expected else '✗'}")

    # Test rectangle-rectangle collision
    print("\nTesting rectangle-rectangle collision:")
    rect1, rect2 = Rectangle(4, 6), Rectangle(2, 2)
    test_cases = [
        ((0, 0), (1, 1), True, "Overlapping rectangles"),
        ((0, 0), (3, 0), True, "Touching rectangles"),
        ((0, 0), (5, 5), False, "Non-overlapping rectangles"),
        ((0, 0), (2, 2), True, "Partial overlap"),
    ]
    for pos1, pos2, expected, desc in test_cases:
        result = detector.detect_aabb_collision(rect1, rect2, pos1, pos2)
        print(f"{desc}: {'✓' if result == expected else '✗'}")

    # Test circle-rectangle collision
    print("\nTesting circle-rectangle collision:")
    circle, rect = Circle(2), Rectangle(4, 4)
    test_cases = [
        ((0, 0), (3, 0), True, "Circle overlapping rectangle edge"),
        ((0, 0), (0, 0), True, "Circle inside rectangle"),
        ((0, 0), (5, 0), False, "No collision"),
        ((0, 0), (3, 3), True, "Corner overlap"),
    ]
    for circle_pos, rect_pos, expected, desc in test_cases:
        result = detector.detect_circle_rectangle_collision(circle, rect, circle_pos, rect_pos)
        print(f"{desc}: {'✓' if result == expected else '✗'}")
