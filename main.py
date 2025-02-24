import pygame
import sys
import math
import random
import copy

from entities import CelestialBody
from physics import update_physics_euler, update_physics_rk4
from gui import Button, Slider, BACKGROUND_COLOR, NEON_YELLOW, NEON_MAGENTA, NEON_CYAN
from utils import scale, distance

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyberpunk Orbital Mechanics Simulator")
clock = pygame.time.Clock()

# Simulation parameters
dt = 0.1  # Time step

# Global simulation state
simulation_running = True
simulation_time = 0.0

# Integration method toggle: "euler" or "rk4"
integration_method = "euler"

# Debug mode toggle
debug_mode = False

# These functionalities are always on by default
collisions_enabled = True
fade_trails = True
show_energy = True

# Toggle for predicted trajectory display and body selection
prediction_enabled = False
selected_body = None

# Variables for interactive body creation (in world coordinates)
creating_body = False
creation_start = None
current_mouse_pos = None

# Camera variables for pan and zoom
camera_offset = [WIDTH / 2, HEIGHT / 2]
zoom_factor = 1.0
panning = False
pan_last_pos = None

# Generate starfield (world coordinates)
starfield = []
num_stars = 300
for _ in range(num_stars):
    x = random.uniform(-5000, 5000)
    y = random.uniform(-5000, 5000)
    starfield.append((x, y))

def world_to_screen(pos):
    return (int((pos[0] - camera_offset[0]) * zoom_factor + WIDTH / 2),
            int((pos[1] - camera_offset[1]) * zoom_factor + HEIGHT / 2))

def screen_to_world(pos):
    return ((pos[0] - WIDTH / 2) / zoom_factor + camera_offset[0],
            (pos[1] - HEIGHT / 2) / zoom_factor + camera_offset[1])

def draw_starfield(surface):
    for star in starfield:
        s_pos = world_to_screen(star)
        if 0 <= s_pos[0] <= WIDTH and 0 <= s_pos[1] <= HEIGHT:
            surface.fill((255, 255, 255), (s_pos[0], s_pos[1], 1, 1))

def draw_minimap(surface):
    if bodies:
        xs = [b.pos[0] for b in bodies]
        ys = [b.pos[1] for b in bodies]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        margin = 50
        min_x -= margin; max_x += margin; min_y -= margin; max_y += margin
    else:
        min_x, max_x, min_y, max_y = -1000, 1000, -1000, 1000
    minimap_rect = pygame.Rect(WIDTH - 210, 10, 200, 200)
    pygame.draw.rect(surface, (50, 50, 50), minimap_rect)
    pygame.draw.rect(surface, (255, 255, 255), minimap_rect, 2)
    for b in bodies:
        norm_x = (b.pos[0] - min_x) / (max_x - min_x)
        norm_y = (b.pos[1] - min_y) / (max_y - min_y)
        mini_x = minimap_rect.x + int(norm_x * minimap_rect.width)
        mini_y = minimap_rect.y + int(norm_y * minimap_rect.height)
        pygame.draw.circle(surface, b.color, (mini_x, mini_y), 3)
        if selected_body is b:
            pygame.draw.circle(surface, NEON_CYAN, (mini_x, mini_y), 5, 1)

def draw_dashed_line(surface, color, start, end, dash_length=5, space_length=3):
    start = pygame.math.Vector2(start)
    end = pygame.math.Vector2(end)
    displacement = end - start
    length = displacement.length()
    if length == 0:
        return
    direction = displacement.normalize()
    num_dashes = int(length // (dash_length + space_length))
    for i in range(num_dashes + 1):
        dash_start = start + direction * (i * (dash_length + space_length))
        dash_end = dash_start + direction * dash_length
        if (dash_end - start).length() > length:
            dash_end = end
        pygame.draw.line(surface, color, dash_start, dash_end, 2)

# --- GUI Callback Functions ---
def toggle_simulation():
    global simulation_running
    simulation_running = not simulation_running

def reset_simulation():
    global bodies, simulation_time, simulation_running, selected_body
    bodies = create_bodies()
    simulation_time = 0.0
    simulation_running = True
    selected_body = None

def toggle_integration():
    global integration_method
    if integration_method == "euler":
        integration_method = "rk4"
        integration_button.text = "Integration: RK4"
    else:
        integration_method = "euler"
        integration_button.text = "Integration: Euler"

def toggle_debug():
    global debug_mode
    debug_mode = not debug_mode
    debug_button.text = "Debug: On" if debug_mode else "Debug: Off"

def reset_camera():
    global camera_offset, zoom_factor
    camera_offset = [WIDTH / 2, HEIGHT / 2]
    zoom_factor = 1.0

def take_screenshot():
    pygame.image.save(screen, "screenshot.png")
    print("Screenshot saved as screenshot.png")

def toggle_prediction():
    global prediction_enabled
    prediction_enabled = not prediction_enabled
    prediction_button.text = "Prediction: On" if prediction_enabled else "Prediction: Off"

def clear_selection():
    global selected_body
    selected_body = None

def compute_energy(bodies, G):
    kinetic = 0
    potential = 0
    for body in bodies:
        kinetic += 0.5 * body.mass * (body.vel[0]**2 + body.vel[1]**2)
    for i in range(len(bodies)):
        for j in range(i+1, len(bodies)):
            dx = bodies[i].pos[0] - bodies[j].pos[0]
            dy = bodies[i].pos[1] - bodies[j].pos[1]
            r = math.hypot(dx, dy)
            if r != 0:
                potential += -G * bodies[i].mass * bodies[j].mass / r
    return kinetic, potential

def handle_collisions(bodies):
    used = set()
    new_bodies = []
    for i in range(len(bodies)):
        if i in used:
            continue
        body1 = bodies[i]
        merged = False
        for j in range(i + 1, len(bodies)):
            if j in used:
                continue
            body2 = bodies[j]
            dx = body1.pos[0] - body2.pos[0]
            dy = body1.pos[1] - body2.pos[1]
            if math.hypot(dx, dy) < (body1.radius + body2.radius):
                new_mass = body1.mass + body2.mass
                new_vel = ((body1.vel[0] * body1.mass + body2.vel[0] * body2.mass) / new_mass,
                           (body1.vel[1] * body1.mass + body2.vel[1] * body2.mass) / new_mass)
                new_pos = ((body1.pos[0] * body1.mass + body2.pos[0] * body2.mass) / new_mass,
                           (body1.pos[1] * body1.mass + body2.pos[1] * body2.mass) / new_mass)
                new_radius = int((body1.radius**3 + body2.radius**3) ** (1 / 3))
                new_color = body1.color
                merged_body = CelestialBody(new_mass, new_pos, new_vel, new_radius, new_color)
                new_bodies.append(merged_body)
                used.add(j)
                merged = True
                break
        if not merged:
            new_bodies.append(body1)
    return new_bodies

# --- GUI Elements ---
pause_button = Button(rect=(10, 10, 120, 30), text="Pause/Resume", callback=toggle_simulation, font_size=16)
reset_button = Button(rect=(140, 10, 80, 30), text="Reset", callback=reset_simulation, font_size=16)
integration_button = Button(rect=(230, 10, 150, 30), text="Integration: Euler", callback=toggle_integration, font_size=16)
debug_button = Button(rect=(390, 10, 100, 30), text="Debug: Off", callback=toggle_debug, font_size=16)
reset_camera_button = Button(rect=(930, 10, 140, 30), text="Reset Camera", callback=reset_camera, font_size=16)
screenshot_button = Button(rect=(1070, 10, 140, 30), text="Screenshot", callback=take_screenshot, font_size=16)
# Move prediction and clear selection buttons slightly down
prediction_button = Button(rect=(10, 270, 140, 30), text="Prediction: Off", callback=toggle_prediction, font_size=16)
clear_selection_button = Button(rect=(160, 270, 140, 30), text="Clear Selection", callback=clear_selection, font_size=16)

# Sliders at bottom left
speed_slider = Slider(rect=(10, 640, 200, 20), min_val=0.1, max_val=5.0, initial=1.0, label="Sim Speed", font_size=16)
planet_size_slider = Slider(rect=(10, 670, 200, 20), min_val=4, max_val=20, initial=6.0, label="Planet Size", font_size=16)
g_slider = Slider(rect=(10, 700, 200, 20), min_val=0.01, max_val=1.0, initial=0.1, label="G Constant", font_size=16)

def draw_legend(surface):
    legend_lines = [
        "Shift+Drag: Create planet",
        "Right-drag: Pan camera",
        "Mouse Wheel: Zoom"
    ]
    legend_width = 250
    legend_height = 70
    legend_x = WIDTH - legend_width - 10
    legend_y = HEIGHT - legend_height - 10
    pygame.draw.rect(surface, (30, 30, 30), (legend_x, legend_y, legend_width, legend_height))
    pygame.draw.rect(surface, (255, 255, 255), (legend_x, legend_y, legend_width, legend_height), 2)
    line_y = legend_y + 10
    font = pygame.font.Font("freesansbold.ttf", 12)
    for line in legend_lines:
        text_surf = font.render(line, True, (255, 255, 255))
        surface.blit(text_surf, (legend_x + 10, line_y))
        line_y += 20

def add_new_body(start, end):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    velocity_scale = 0.05
    initial_velocity = (dx * velocity_scale, dy * velocity_scale)
    new_radius = int(planet_size_slider.value)
    new_mass = new_radius * 10
    new_body = CelestialBody(
        mass=new_mass,
        pos=start,
        vel=initial_velocity,
        radius=new_radius,
        color=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    )
    bodies.append(new_body)

def create_bodies():
    center = (WIDTH / 2, HEIGHT / 2)
    sun = CelestialBody(
        mass=10000,
        pos=center,
        vel=(0, 0),
        radius=20,
        color=NEON_YELLOW
    )
    distance_from_sun = 200
    planet_velocity = math.sqrt(g_slider.value * sun.mass / distance_from_sun)
    planet = CelestialBody(
        mass=10,
        pos=(center[0] + distance_from_sun, center[1]),
        vel=(0, -planet_velocity),
        radius=8,
        color=NEON_MAGENTA
    )
    return [sun, planet]

bodies = create_bodies()

debug_font = pygame.font.Font("freesansbold.ttf", 16)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                panning = True
                pan_last_pos = event.pos
            elif event.button == 1:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_SHIFT:
                    creating_body = True
                    creation_start = screen_to_world(event.pos)
                else:
                    buttons = [pause_button, reset_button, integration_button, debug_button,
                               reset_camera_button, screenshot_button, prediction_button, clear_selection_button]
                    if not any(b.is_clicked(event.pos) for b in buttons):
                        click_world = screen_to_world(event.pos)
                        for b in bodies:
                            if distance(click_world, b.pos) < b.radius + 5:
                                selected_body = b
                                break
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                panning = False
            elif event.button == 1:
                mouse_pos_world = screen_to_world(event.pos)
                if pause_button.is_clicked(event.pos):
                    pause_button.callback()
                elif reset_button.is_clicked(event.pos):
                    reset_button.callback()
                elif integration_button.is_clicked(event.pos):
                    integration_button.callback()
                elif debug_button.is_clicked(event.pos):
                    debug_button.callback()
                elif reset_camera_button.is_clicked(event.pos):
                    reset_camera_button.callback()
                elif screenshot_button.is_clicked(event.pos):
                    screenshot_button.callback()
                elif prediction_button.is_clicked(event.pos):
                    prediction_button.callback()
                elif clear_selection_button.is_clicked(event.pos):
                    clear_selection_button.callback()
                if creating_body:
                    add_new_body(creation_start, mouse_pos_world)
                    creating_body = False
                    creation_start = None
        elif event.type == pygame.MOUSEMOTION:
            if panning:
                dx = event.pos[0] - pan_last_pos[0]
                dy = event.pos[1] - pan_last_pos[1]
                camera_offset[0] -= dx / zoom_factor
                camera_offset[1] -= dy / zoom_factor
                pan_last_pos = event.pos
            if creating_body:
                current_mouse_pos = screen_to_world(event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            zoom_factor *= 1.0 + event.y * 0.1
            zoom_factor = max(0.1, min(zoom_factor, 5.0))
        
        speed_slider.handle_event(event)
        planet_size_slider.handle_event(event)
        g_slider.handle_event(event)
    
    screen.fill(BACKGROUND_COLOR)
    
    draw_starfield(screen)
    
    if simulation_running:
        current_G = g_slider.value
        speed_factor = speed_slider.value
        if integration_method == "euler":
            update_physics_euler(bodies, dt * speed_factor, current_G)
        else:
            update_physics_rk4(bodies, dt * speed_factor, current_G)
        simulation_time += dt * speed_factor
    
    if collisions_enabled:
        bodies = handle_collisions(bodies)
    
    for body in bodies:
        body.draw(screen, world_to_screen, zoom_factor, fade=fade_trails)
        if debug_mode:
            pos_screen = world_to_screen(body.pos)
            vel_end = (body.pos[0] + body.vel[0] * 10, body.pos[1] + body.vel[1] * 10)
            vel_end_screen = world_to_screen(vel_end)
            pygame.draw.line(screen, (255, 255, 255), pos_screen, vel_end_screen, 2)
    
    if creating_body and creation_start and current_mouse_pos:
        pygame.draw.line(screen, (255, 255, 255), world_to_screen(creation_start), world_to_screen(current_mouse_pos), 2)
        pygame.draw.circle(screen, (255, 255, 255), world_to_screen(creation_start), 4)
    
    if prediction_enabled and selected_body is not None:
        try:
            index = bodies.index(selected_body)
            predicted_bodies = [copy.deepcopy(b) for b in bodies]
            predicted_positions = []
            steps = 30
            dt_prediction = dt
            for _ in range(steps):
                update_physics_euler(predicted_bodies, dt_prediction, g_slider.value)
                predicted_positions.append(predicted_bodies[index].pos)
            for i in range(len(predicted_positions)-1):
                start_pos = world_to_screen(predicted_positions[i])
                end_pos = world_to_screen(predicted_positions[i+1])
                draw_dashed_line(screen, (57, 255, 20), start_pos, end_pos, dash_length=5, space_length=3)
            pygame.draw.circle(screen, NEON_CYAN, world_to_screen(selected_body.pos), max(5, int(selected_body.radius * zoom_factor)), 2)
        except ValueError:
            selected_body = None
    
    pause_button.draw(screen)
    reset_button.draw(screen)
    integration_button.draw(screen)
    debug_button.draw(screen)
    reset_camera_button.draw(screen)
    screenshot_button.draw(screen)
    prediction_button.draw(screen)
    clear_selection_button.draw(screen)
    speed_slider.draw(screen)
    planet_size_slider.draw(screen)
    g_slider.draw(screen)
    
    time_text = debug_font.render(f"Sim Time: {simulation_time:.2f}s", True, (255, 255, 255))
    method_text = debug_font.render(f"Method: {integration_method.upper()}", True, (255, 255, 255))
    screen.blit(time_text, (10, 210))
    screen.blit(method_text, (10, 230))
    
    kinetic, potential = compute_energy(bodies, g_slider.value)
    energy_text = debug_font.render(f"Kinetic: {kinetic:.2e}  Potential: {potential:.2e}", True, (255, 255, 255))
    screen.blit(energy_text, (10, 250))
    
    draw_legend(screen)
    draw_minimap(screen)
    
    pygame.display.flip()
    clock.tick(60)
