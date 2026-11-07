import sys
import types
import unittest

class FakeRect:
    def __init__(self, x, y, w, h): self.x, self.y, self.width, self.height = x, y, w, h
    def collidepoint(self, p): return self.x <= p[0] < self.x + self.width and self.y <= p[1] < self.y + self.height
class FakeSurface:
    def __init__(self, *a, **k): pass
    def fill(self, *a, **k): pass
class FakeFont:
    def render(self, *a, **k): return FakeSurface()
class FakeSound:
    def __init__(self, *a, **k): pass
    def play(self): pass
pygame = types.ModuleType("pygame")
pygame.Rect, pygame.Surface, pygame.SRCALPHA = FakeRect, FakeSurface, 1
pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN = 1, 2
pygame.K_1, pygame.K_KP1, pygame.K_2, pygame.K_KP2 = 49, 257, 50, 258
pygame.K_3, pygame.K_KP3, pygame.K_RETURN, pygame.K_SPACE = 51, 259, 13, 32
pygame.error = Exception
pygame.mixer = types.SimpleNamespace(get_init=lambda: False, init=lambda: None, Sound=FakeSound)
pygame.font = types.SimpleNamespace(SysFont=lambda *a, **k: FakeFont())
pygame.draw = types.SimpleNamespace(circle=lambda *a, **k: None, rect=lambda *a, **k: None)
sys.modules["pygame"] = pygame
from game.game_engine import GameEngine

class GameEngineTests(unittest.TestCase):
    def setUp(self): self.engine = GameEngine(500, 560)
    def test_hitboxes_do_not_overlap(self):
        a, b = self.engine.holes[0], self.engine.holes[1]
        self.assertLessEqual(a.rect().x + a.rect().width, b.rect().x)
    def test_one_click_scores_at_most_one_point(self):
        a, b = self.engine.holes[0], self.engine.holes[1]
        a.active = b.active = True
        b.rect = lambda: FakeRect(a.rect().x, a.rect().y, a.rect().width, a.rect().height)
        self.engine._handle_click((a.center_x, a.center_y))
        self.assertEqual(self.engine.score, 1)
        self.assertEqual(sum(h.active for h in self.engine.holes[:2]), 1)
    def test_miss_does_not_score(self):
        self.engine._handle_click((0, 0))
        self.assertEqual(self.engine.score, 0)
        self.assertEqual(self.engine.misses, 1)
    def test_timer_ends_round(self):
        self.engine.time_left_frames = 1
        self.engine.update()
        self.assertTrue(self.engine.game_over)
        self.assertEqual(self.engine.time_left_frames, 0)
    def test_replay_resets_and_changes_difficulty(self):
        self.engine.score, self.engine.game_over = 7, True
        self.engine.start_new_round("Hard")
        self.assertEqual(self.engine.difficulty, "Hard")
        self.assertEqual(self.engine.score, 0)
        self.assertFalse(self.engine.game_over)

if __name__ == "__main__": unittest.main()
