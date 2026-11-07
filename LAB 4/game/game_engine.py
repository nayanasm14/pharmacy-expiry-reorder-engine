import random
import pygame
from .hole import Hole

DARK_BROWN = (60, 40, 20)
MOLE_BROWN = (140, 95, 55)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DIFFICULTIES = {
    "Easy": (0.012, 60),
    "Medium": (0.020, 45),
    "Hard": (0.032, 32),
}


class GameEngine:
    def __init__(self, width, height, rows=3, cols=3, sound_enabled=True):
        self.width, self.height = width, height
        self.rows, self.cols = rows, cols
        self.sound_enabled = sound_enabled
        self._init_sounds()
        self.font = pygame.font.SysFont("Arial", 25)
        self.title_font = pygame.font.SysFont("Arial", 38, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.difficulty = "Medium"
        self.best_score = 0
        self._build_holes()
        self._reset_round()

    def _init_sounds(self):
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            import math, array
            rate = 22050
            for name, frequency, duration in (("hit", 880, .10), ("miss", 220, .12), ("end", 440, .28)):
                length = int(rate * duration)
                wave = array.array("h", (int(5000 * math.sin(2 * math.pi * frequency * i / rate) * (1 - i / length)) for i in range(length)))
                self.sounds[name] = pygame.mixer.Sound(buffer=wave)
        except (pygame.error, OSError):
            self.sounds = {}

    def _play(self, name):
        sound = self.sounds.get(name) if self.sound_enabled else None
        if sound:
            try:
                sound.play()
            except pygame.error:
                pass

    def _build_holes(self):
        self.holes = []
        sx = self.width // (self.cols + 1)
        sy = (self.height - 100) // (self.rows + 1)
        hit_size = max(54, min(86, int(min(sx, sy) * .58)))
        for row in range(self.rows):
            for col in range(self.cols):
                self.holes.append(Hole(sx * (col + 1), 90 + sy * (row + 1), hit_size))

    def _reset_round(self):
        self.spawn_chance, self.mole_up_frames = DIFFICULTIES[self.difficulty]
        self.round_seconds = 30
        self.time_left_frames = self.round_seconds * 60
        self.score = 0
        self.misses = 0
        self.game_over = False
        self._game_over_sound_played = False
        for hole in self.holes:
            hole.active = False
            hole.timer = 0

    def start_new_round(self, difficulty):
        if difficulty not in DIFFICULTIES:
            raise ValueError(f"Unknown difficulty: {difficulty}")
        self.difficulty = difficulty
        self._reset_round()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.game_over:
                self._handle_game_over_click(event.pos)
            else:
                self._handle_click(event.pos)
        if event.type == pygame.KEYDOWN and self.game_over:
            if event.key in (pygame.K_1, pygame.K_KP1): self.start_new_round("Easy")
            elif event.key in (pygame.K_2, pygame.K_KP2, pygame.K_RETURN, pygame.K_SPACE): self.start_new_round("Medium")
            elif event.key in (pygame.K_3, pygame.K_KP3): self.start_new_round("Hard")

    def _handle_game_over_click(self, pos):
        width, gap = 120, 12
        start_x = (self.width - (width * 3 + gap * 2)) // 2
        y = self.height // 2 + 105
        for i, difficulty in enumerate(("Easy", "Medium", "Hard")):
            rect = pygame.Rect(start_x + i * (width + gap), y, width, 44)
            if rect.collidepoint(pos):
                self.start_new_round(difficulty)
                return

    def _handle_click(self, pos):
        candidates = [h for h in self.holes if h.active and h.rect().collidepoint(pos)]
        if candidates:
            hole = min(candidates, key=lambda h: (h.center_x - pos[0]) ** 2 + (h.center_y - pos[1]) ** 2)
            if hole.whack():
                self.score += 1
                self.best_score = max(self.best_score, self.score)
                self._play("hit")
                return
        self.misses += 1
        self._play("miss")

    def handle_input(self):
        pass

    def update(self):
        if self.game_over:
            if not self._game_over_sound_played:
                self._play("end")
                self._game_over_sound_played = True
            return
        self.time_left_frames -= 1
        if self.time_left_frames <= 0:
            self.time_left_frames = 0
            self.game_over = True
            self.best_score = max(self.best_score, self.score)
            return
        for hole in self.holes:
            hole.update()
            if not hole.active and random.random() < self.spawn_chance:
                hole.pop_up(self.mole_up_frames)

    def render(self, screen):
        for hole in self.holes:
            pygame.draw.circle(screen, DARK_BROWN, (hole.center_x, hole.center_y), 40)
            if hole.active:
                pygame.draw.circle(screen, MOLE_BROWN, (hole.center_x, hole.center_y), 32)
        screen.blit(self.font.render(f"Score: {self.score}", True, BLACK), (12, 12))
        screen.blit(self.font.render(f"Time: {max(0, self.time_left_frames // 60)}s", True, BLACK), (self.width - 145, 12))
        screen.blit(self.small_font.render(f"Best: {self.best_score}", True, BLACK), (12, 48))
        if self.game_over:
            self._render_game_over(screen)

    def _render_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 155))
        screen.blit(overlay, (0, 0))
        items = [("GAME OVER", self.title_font, self.height // 2 - 65),
                 (f"Final score: {self.score}", self.font, self.height // 2 - 20),
                 (f"Best score: {self.best_score}", self.font, self.height // 2 + 15),
                 ("Choose a difficulty to replay", self.small_font, self.height // 2 + 65)]
        for label, font, y in items:
            surf = font.render(label, True, WHITE)
            screen.blit(surf, surf.get_rect(center=(self.width // 2, y)))
        width, gap, height = 120, 12, 44
        start_x, y = (self.width - (width * 3 + gap * 2)) // 2, self.height // 2 + 105
        for i, difficulty in enumerate(("Easy", "Medium", "Hard")):
            rect = pygame.Rect(start_x + i * (width + gap), y, width, height)
            pygame.draw.rect(screen, (235, 235, 235), rect, border_radius=8)
            label = self.small_font.render(difficulty, True, BLACK)
            screen.blit(label, label.get_rect(center=rect.center))
        keys = self.small_font.render("Or press 1 / 2 / 3  |  Esc to quit", True, WHITE)
        screen.blit(keys, keys.get_rect(center=(self.width // 2, y + 65)))
