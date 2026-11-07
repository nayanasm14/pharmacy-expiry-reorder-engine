import pygame


class Hole:
    """A single mole location with a non-overlapping click target."""

    def __init__(self, center_x, center_y, hit_size=86):
        self.center_x = center_x
        self.center_y = center_y
        self.hit_size = hit_size
        self.active = False
        self.timer = 0

    def pop_up(self, duration_frames):
        self.active = True
        self.timer = max(1, int(duration_frames))

    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False
                self.timer = 0

    def whack(self):
        if not self.active:
            return False
        self.active = False
        self.timer = 0
        return True

    def rect(self):
        return pygame.Rect(
            self.center_x - self.hit_size // 2,
            self.center_y - self.hit_size // 2,
            self.hit_size,
            self.hit_size,
        )
