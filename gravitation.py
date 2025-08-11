import numpy as np

def gravity(particles, G, dt):
    num = len(particles)
    if num == 0:
        return
    
    for i in range(0, len(particles)):
        for j in range (i + 1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]

            dx = p1.x - p2.x
            dy = p1.y - p2.y

            dist2 = dx**2 + dy**2
            if dist2 == 0:
                return
            dist = np.sqrt(dist2)
            
            Force = G * p1.mass * p2.mass / dist2
            Fx = Force * dx / dist
            Fy = Force * dy / dist

            p1.x_vel += dt * Fx / p1.mass
            p1.y_vel += dt * Fy / p1.mass
            p2.x_vel -= dt * Fx / p2.mass
            p2.y_vel -= dt * Fx / p2.mass
            
    for p in particles:
        p.x += p.x_vel * dt
        p.y += p.y_vel * dt
