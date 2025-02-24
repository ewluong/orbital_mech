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
    states = [(b.pos[0], b.pos[1], b.vel[0], b.vel[1]) for b in bodies]
    a1 = compute_accelerations(states, bodies, G)
    k1 = [(dt * s[2], dt * s[3], dt * a1[i][0], dt * a1[i][1]) for i, s in enumerate(states)]
    states_k1 = [(s[0] + k1[i][0] / 2, s[1] + k1[i][1] / 2, s[2] + k1[i][2] / 2, s[3] + k1[i][3] / 2) for i, s in enumerate(states)]
    a2 = compute_accelerations(states_k1, bodies, G)
    k2 = [(dt * s[2], dt * s[3], dt * a2[i][0], dt * a2[i][1]) for i, s in enumerate(states_k1)]
    states_k2 = [(s[0] + k2[i][0] / 2, s[1] + k2[i][1] / 2, s[2] + k2[i][2] / 2, s[3] + k2[i][3] / 2) for i, s in enumerate(states)]
    a3 = compute_accelerations(states_k2, bodies, G)
    k3 = [(dt * s[2], dt * s[3], dt * a3[i][0], dt * a3[i][1]) for i, s in enumerate(states_k2)]
    states_k3 = [(s[0] + k3[i][0], s[1] + k3[i][1], s[2] + k3[i][2], s[3] + k3[i][3]) for i, s in enumerate(states)]
    a4 = compute_accelerations(states_k3, bodies, G)
    k4 = [(dt * s[2], dt * s[3], dt * a4[i][0], dt * a4[i][1]) for i, s in enumerate(states_k3)]
    for i, b in enumerate(bodies):
        b.pos = (states[i][0] + (k1[i][0] + 2 * k2[i][0] + 2 * k3[i][0] + k4[i][0]) / 6,
                 states[i][1] + (k1[i][1] + 2 * k2[i][1] + 2 * k3[i][1] + k4[i][1]) / 6)
        b.vel = (states[i][2] + (k1[i][2] + 2 * k2[i][2] + 2 * k3[i][2] + k4[i][2]) / 6,
                 states[i][3] + (k1[i][3] + 2 * k2[i][3] + 2 * k3[i][3] + k4[i][3]) / 6)
        b.trail.append(b.pos)
        if len(b.trail) > 200:
            b.trail.pop(0)

def update_physics_verlet(bodies, dt, G):
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
        if not hasattr(body, 'prev_pos'):
            body.prev_pos = (body.pos[0] - body.vel[0] * dt, body.pos[1] - body.vel[1] * dt)
        new_pos = (2 * body.pos[0] - body.prev_pos[0] + body.acc[0] * dt ** 2,
                   2 * body.pos[1] - body.prev_pos[1] + body.acc[1] * dt ** 2)
        body.prev_pos = body.pos
        body.pos = new_pos
        body.vel = ((body.pos[0] - body.prev_pos[0]) / dt, (body.pos[1] - body.prev_pos[1]) / dt)
        body.trail.append(body.pos)
        if len(body.trail) > 200:
            body.trail.pop(0)