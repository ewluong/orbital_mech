import math
from utils import subtract, normalize, magnitude, scale, add

def update_physics_euler(bodies, dt, G):
    for body in bodies:
        body.acc = (0, 0)
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            body1 = bodies[i]
            body2 = bodies[j]
            r_vec = subtract(body2.pos, body1.pos)
            r = magnitude(r_vec)
            if r == 0:
                continue
            force = G * body1.mass * body2.mass / (r ** 2)
            force_dir = normalize(r_vec)
            force_vec = scale(force_dir, force)
            acc1 = scale(force_vec, 1 / body1.mass)
            acc2 = scale(force_vec, -1 / body2.mass)
            body1.acc = add(body1.acc, acc1)
            body2.acc = add(body2.acc, acc2)
    for body in bodies:
        body.update(dt)

def compute_accelerations(states, bodies, G):
    accelerations = []
    for i, s in enumerate(states):
        ax, ay = 0, 0
        for j, s2 in enumerate(states):
            if i == j:
                continue
            dx = s2[0] - s[0]
            dy = s2[1] - s[1]
            r = math.sqrt(dx * dx + dy * dy)
            if r == 0:
                continue
            factor = G * bodies[j].mass / (r ** 3)
            ax += factor * dx
            ay += factor * dy
        accelerations.append((ax, ay))
    return accelerations

def update_physics_rk4(bodies, dt, G):
    states = []
    for body in bodies:
        states.append((body.pos[0], body.pos[1], body.vel[0], body.vel[1]))
    a1 = compute_accelerations(states, bodies, G)
    k1 = []
    for i, s in enumerate(states):
        vx, vy = s[2], s[3]
        ax, ay = a1[i]
        k1.append((dt * vx, dt * vy, dt * ax, dt * ay))
    states_k1 = []
    for i, s in enumerate(states):
        s_new = (s[0] + k1[i][0] / 2,
                 s[1] + k1[i][1] / 2,
                 s[2] + k1[i][2] / 2,
                 s[3] + k1[i][3] / 2)
        states_k1.append(s_new)
    a2 = compute_accelerations(states_k1, bodies, G)
    k2 = []
    for i, s in enumerate(states_k1):
        vx, vy = s[2], s[3]
        ax, ay = a2[i]
        k2.append((dt * vx, dt * vy, dt * ax, dt * ay))
    states_k2 = []
    for i, s in enumerate(states):
        s_new = (s[0] + k2[i][0] / 2,
                 s[1] + k2[i][1] / 2,
                 s[2] + k2[i][2] / 2,
                 s[3] + k2[i][3] / 2)
        states_k2.append(s_new)
    a3 = compute_accelerations(states_k2, bodies, G)
    k3 = []
    for i, s in enumerate(states_k2):
        vx, vy = s[2], s[3]
        ax, ay = a3[i]
        k3.append((dt * vx, dt * vy, dt * ax, dt * ay))
    states_k3 = []
    for i, s in enumerate(states):
        s_new = (s[0] + k3[i][0],
                 s[1] + k3[i][1],
                 s[2] + k3[i][2],
                 s[3] + k3[i][3])
        states_k3.append(s_new)
    a4 = compute_accelerations(states_k3, bodies, G)
    k4 = []
    for i, s in enumerate(states_k3):
        vx, vy = s[2], s[3]
        ax, ay = a4[i]
        k4.append((dt * vx, dt * vy, dt * ax, dt * ay))
    new_states = []
    for i, s in enumerate(states):
        new_x = s[0] + (k1[i][0] + 2 * k2[i][0] + 2 * k3[i][0] + k4[i][0]) / 6
        new_y = s[1] + (k1[i][1] + 2 * k2[i][1] + 2 * k3[i][1] + k4[i][1]) / 6
        new_vx = s[2] + (k1[i][2] + 2 * k2[i][2] + 2 * k3[i][2] + k4[i][2]) / 6
        new_vy = s[3] + (k1[i][3] + 2 * k2[i][3] + 2 * k3[i][3] + k4[i][3]) / 6
        new_states.append((new_x, new_y, new_vx, new_vy))
    for i, body in enumerate(bodies):
        body.pos = (new_states[i][0], new_states[i][1])
        body.vel = (new_states[i][2], new_states[i][3])
        body.trail.append(body.pos)
        if len(body.trail) > 200:
            body.trail.pop(0)
