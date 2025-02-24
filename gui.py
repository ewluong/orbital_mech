import pygame
import random

NEON_CYAN = (0, 255, 255)
NEON_MAGENTA = (255, 0, 255)
NEON_YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)  # pure black
FONT_NAME = "freesansbold.ttf"

def draw_neon_grid(surface, spacing=20):
    width, height = surface.get_size()
    for x in range(0, width, spacing):
        offset = random.randint(-1, 1)
        pygame.draw.line(surface, NEON_CYAN, (x + offset, 0), (x + offset, height), 1)
    for y in range(0, height, spacing):
        offset = random.randint(-1, 1)
        pygame.draw.line(surface, NEON_CYAN, (0, y + offset), (width, y + offset), 1)

class Button:
    def __init__(self, rect, text, callback, font_size=16, color=NEON_MAGENTA, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(FONT_NAME, font_size)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 2)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Slider:
    def __init__(self, rect, min_val, max_val, initial, label="", font_size=16, color=NEON_CYAN, handle_color=NEON_YELLOW):
        self.rect = pygame.Rect(rect)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial
        self.label = label
        self.color = color
        self.handle_color = handle_color
        self.font = pygame.font.Font(FONT_NAME, font_size)
        self.handle_radius = 8
        self.dragging = False
    
    def draw(self, surface):
        if self.label:
            label_surf = self.font.render(self.label, True, self.color)
            label_rect = label_surf.get_rect(midbottom=(self.rect.centerx, self.rect.top - 4))
            surface.blit(label_surf, label_rect)
        
        track_y = self.rect.centery
        pygame.draw.line(surface, self.color, (self.rect.x, track_y),
                         (self.rect.x + self.rect.width, track_y), 2)
        
        handle_x = self.rect.x + ((self.value - self.min_val) / (self.max_val - self.min_val)) * self.rect.width
        pygame.draw.circle(surface, self.handle_color, (int(handle_x), track_y), self.handle_radius)
        
        value_surf = self.font.render(f"{self.value:.2f}", True, self.color)
        value_rect = value_surf.get_rect(midleft=(self.rect.x + self.rect.width + 10, track_y))
        surface.blit(value_surf, value_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_value(event.pos)
    
    def update_value(self, pos):
        relative_x = pos[0] - self.rect.x
        fraction = max(0, min(1, relative_x / self.rect.width))
        self.value = self.min_val + fraction * (self.max_val - self.min_val)
