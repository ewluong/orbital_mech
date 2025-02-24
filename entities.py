import pygame

class CelestialBody:
    def __init__(self, mass, pos, vel, radius, color):
        self.mass = mass
        self.pos = pos      # (x, y)
        self.vel = vel      # (vx, vy)
        self.acc = (0, 0)   # acceleration
        self.radius = radius
        self.color = color
        self.trail = []     # store previous positions for orbit trails

    def update(self, dt):
        self.vel = (self.vel[0] + self.acc[0] * dt, self.vel[1] + self.acc[1] * dt)
        self.pos = (self.pos[0] + self.vel[0] * dt, self.pos[1] + self.vel[1] * dt)
        self.trail.append(self.pos)
        if len(self.trail) > 200:
            self.trail.pop(0)
    
    def draw(self, surface, transform, zoom, fade=False):
        if len(self.trail) > 1:
            transformed_trail = [transform(p) for p in self.trail]
            if fade:
                trail_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
                n = len(transformed_trail)
                for i in range(n - 1):
                    alpha = int(50 + 205 * (i / (n - 1)))
                    color_with_alpha = (self.color[0], self.color[1], self.color[2], alpha)
                    pygame.draw.line(trail_surface, color_with_alpha, transformed_trail[i], transformed_trail[i+1], 2)
                surface.blit(trail_surface, (0, 0))
            else:
                pygame.draw.lines(surface, self.color, False, transformed_trail, 1)
        pygame.draw.circle(surface, self.color, transform(self.pos), max(1, int(self.radius * zoom)))
