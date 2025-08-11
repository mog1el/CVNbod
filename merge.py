import numpy as np
import random
import pygame

width = 1500
height = 1000
screen = pygame.display.set_mode((width, height))

class Particle():
    def __init__(self, x, y, density, radius, color, elasticity):
        self.x = x
        self.y = y
        self.density = density
        self.radius = radius
        self.mass = density * (4/3) * np.pi * radius ** 3
        self.color = color
        self.elasticity = elasticity

        self.x_vel = 0
        self.y_vel = 0
    
    def display(self, camx, camy, zoom):
        screen_x = (self.x - camx) * zoom
        screen_y = (self.y - camy) * zoom
        if self.radius + screen_x < width and self.radius + screen_y < height and screen_x > 0 and screen_y > 0:
            pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), int(self.radius * zoom))

def merger(particles, G, masslim, c): 
    merged = set()

    max_radius = max(p.radius for p in particles) if particles else 1
    cell_size = max_radius * 2.0
    grid = {}
    for p in particles:
        grid_key = (int(p.x / cell_size), int(p.y / cell_size))
        if grid_key not in grid:
            grid[grid_key] = []
        grid[grid_key].append(p)

    new_particles = []
    for p in particles:
        if p in merged:
            continue

        code = 0
        key = (int(p.x / cell_size), int(p.y / cell_size))
        (gx, gy) = key
        
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                neighbour = (gx + x, gy + y)
                if neighbour in grid:
                    for neighbor in grid[neighbour]:
                        if neighbor in merged or neighbor == p:
                            continue

                        dx = p.x - neighbor.x
                        dy = p.y - neighbor.y

                        dist = np.sqrt(dx**2 + dy**2)

                        if dist <= (p.radius + neighbor.radius):
                            x_vel_combi = p.x_vel - neighbor.x_vel
                            y_vel_combi = p.y_vel - neighbor.y_vel

                            speed2 = x_vel_combi ** 2 + y_vel_combi ** 2
                            if speed2 > (2 * G * (p.mass + neighbor.mass) / dist):    
                                nx = dx / dist
                                ny = dy / dist
                                
                                tx = -ny
                                ty = nx
                                
                                vpn = p.x_vel * nx + p.y_vel * ny
                                vpt = p.x_vel * tx + p.y_vel * ty
                                vnn = neighbor.x_vel * nx + neighbor.y_vel * ny
                                vnt = neighbor.x_vel * tx + neighbor.y_vel * ty
                                
                                vpn_new = ((p.mass - neighbor.mass) * vpn + 2 * neighbor.mass * vnn) / (p.mass + neighbor.mass)
                                vnn_new = ((neighbor.mass - p.mass) * vnn + 2 * p.mass * vpn) / (p.mass + neighbor.mass)

                                p.x_vel = p.elasticity * (vpn_new * nx + vpt * tx)
                                p.y_vel = p.elasticity * (vpn_new * ny + vpt * ty)
                                neighbor.x_vel = neighbor.elasticity * (vnn_new * nx + vnt * tx)
                                neighbor.y_vel = neighbor.elasticity * (vnn_new * ny + vnt * ty)

                                overlap = (p.radius + neighbor.radius) - dist
                                if overlap > 0:
                                    separation = overlap / 2 + 1
                                    p.x += separation * nx
                                    p.y += separation * ny
                                    neighbor.x -= separation * nx
                                    neighbor.y -= separation * ny

                            else:
                                mass_new = p.mass + neighbor.mass

                                x_vel = (p.x_vel * p.mass + neighbor.x_vel * neighbor.mass) / mass_new
                                y_vel = (p.y_vel * p.mass + neighbor.y_vel * neighbor.mass) / mass_new
                                masscentrx = (p.x * p.mass + neighbor.x * neighbor.mass) / mass_new
                                masscentry = (p.y * p.mass + neighbor.y * neighbor.mass) / mass_new
                                if mass_new > masslim:
                                    r_new = (2 * G * mass_new) / (c ** 2)
                                    col_new = (255, 255, 255) 
                                    density_new = mass_new / ((4/3) * np.pi * (r_new ** 3))
                                else:
                                    r_new = (p.radius ** 3 + neighbor.radius ** 3) ** (1/3)
                                    density_new = mass_new / ((4/3) * np.pi * (r_new ** 3))
                                    col_new = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                                merged_particle = Particle(masscentrx, masscentry, density_new, r_new, col_new, random.randint(0,10)/10)
                                merged_particle.x_vel = x_vel
                                merged_particle.y_vel = y_vel
                                new_particles.append(merged_particle)
                                merged.add(p)
                                merged.add(neighbor)
                                code = 1
                            break

        if code == 0:
            new_particles.append(p)
    
    return new_particles