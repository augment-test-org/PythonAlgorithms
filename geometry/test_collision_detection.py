"""Unit tests for collision detection algorithms."""
import unittest

from geometry import Circle, Rectangle
from geometry.collision_detection import (
    AABB,
    detect_aabb_collision,
    detect_circle_collision,
    detect_circle_rectangle_collision,
)


class TestCollisionDetection(unittest.TestCase):
    def test_aabb_from_rectangle(self):
        """Test AABB creation from Rectangle."""
        rect = Rectangle(4, 6)  # width=4, height=6
        box = AABB.from_rectangle(rect, (1, 2))  # centered at (1,2)

        self.assertEqual(box.min_x, -1)  # 1 - 4/2
        self.assertEqual(box.max_x, 3)   # 1 + 4/2
        self.assertEqual(box.min_y, -1)  # 2 - 6/2
        self.assertEqual(box.max_y, 5)   # 2 + 6/2

    def test_circle_collision(self):
        """Test circle-circle collision detection."""
        circle1 = Circle(5)
        circle2 = Circle(3)

        # Overlapping circles
        self.assertTrue(detect_circle_collision(circle1, circle2, (0, 0), (7, 0)))
        self.assertTrue(detect_circle_collision(circle1, circle2, (0, 0), (0, 7)))

        # Non-overlapping circles
        self.assertFalse(detect_circle_collision(circle1, circle2, (0, 0), (9, 0)))
        self.assertFalse(detect_circle_collision(circle1, circle2, (0, 0), (0, 9)))

        # Touching circles
        self.assertTrue(detect_circle_collision(circle1, circle2, (0, 0), (8, 0)))

        # Diagonal positions
        self.assertTrue(detect_circle_collision(circle1, circle2, (0, 0), (5, 5)))
        self.assertFalse(detect_circle_collision(circle1, circle2, (0, 0), (7, 7)))

    def test_rectangle_collision(self):
        """Test rectangle-rectangle collision detection using AABB."""
        rect1 = Rectangle(4, 6)  # 4x6 rectangle
        rect2 = Rectangle(2, 2)  # 2x2 rectangle

        # Overlapping rectangles
        self.assertTrue(detect_aabb_collision(rect1, rect2, (0, 0), (1, 1)))
        self.assertTrue(detect_aabb_collision(rect1, rect2, (0, 0), (-1, -1)))

        # Non-overlapping rectangles
        self.assertFalse(detect_aabb_collision(rect1, rect2, (0, 0), (5, 5)))
        self.assertFalse(detect_aabb_collision(rect1, rect2, (0, 0), (-5, -5)))

        # Touching rectangles
        self.assertTrue(detect_aabb_collision(rect1, rect2, (0, 0), (3, 0)))
        self.assertTrue(detect_aabb_collision(rect1, rect2, (0, 0), (0, 4)))

    def test_circle_rectangle_collision(self):
        """Test circle-rectangle collision detection."""
        circle = Circle(2)
        rect = Rectangle(4, 4)

        # Overlapping
        self.assertTrue(detect_circle_rectangle_collision(circle, rect, (0, 0), (3, 0)))
        self.assertTrue(detect_circle_rectangle_collision(circle, rect, (0, 0), (0, 3)))

        # Non-overlapping
        self.assertFalse(detect_circle_rectangle_collision(circle, rect, (0, 0), (5, 0)))
        self.assertFalse(detect_circle_rectangle_collision(circle, rect, (0, 0), (0, 5)))

        # Circle inside rectangle
        self.assertTrue(detect_circle_rectangle_collision(circle, rect, (0, 0), (0, 0)))

        # Circle touching rectangle corner
        self.assertTrue(detect_circle_rectangle_collision(circle, rect, (0, 0), (3, 3)))
        self.assertFalse(detect_circle_rectangle_collision(circle, rect, (0, 0), (4, 4)))


if __name__ == "__main__":
    unittest.main()
