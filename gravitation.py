import numpy as np
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
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

class Quad:
    def __init__(self, x, y, width, height):
        self.left = x
        self.top = y
        self.width = width
        self.height = height

        self.masscentrx = 0
        self.masscentry = 0
        self.totalmass = 0
        self.leaf = True
        self.particle = None

        self.topLeftTree = None
        self.topRightTree = None
        self.botLeftTree = None
        self.botRightTree = None
    
    def inBoundary(self, x, y):
        return self.left <= x < self.left + self.width and self.top <= y < self.top + self.height

    def locate(self, particle):
        if particle.x < self.left + self.width/2:
            if particle.y < self.top + self.height/2:
                return self.topLeftTree
            else:
                return self.botLeftTree
        else:
            if particle.y < self.top + self.height/2:
                return self.topRightTree
            else:
                return self.botRightTree
            
    def insert(self, particle):
        if not self.leaf:
            self.locate(particle).insert(particle)
            return
        
        if self.particle is None:
            self.particle = particle
            return
        
        existing = self.particle
        self.leaf = False
        self.particle = None

        midy = self.height/2
        midx = self.width/2
        x = self.left
        y = self.top

        self.topLeftTree = Quad(x, y, midx, midy)
        self.topRightTree = Quad(x + midx, y, midx, midy)
        self.botLeftTree = Quad(x, y + midy, midx, midy)
        self.botRightTree = Quad(x + midx, y + midy, midx, midy)

        self.locate(existing).insert(existing)
        self.locate(particle).insert(particle)
    
    def massdistro(self):
        if self.leaf:
            if self.particle is not None:
                self.totalmass = self.particle.mass
                self.masscentrx = self.particle.x
                self.masscentry = self.particle.y
            return
        
        children = [self.topLeftTree, self.topRightTree, self.botLeftTree, self.botRightTree]
        for child in children:
            child.massdistro()

        self.totalmass = sum(child.totalmass for child in children)

        if self.totalmass > 0:
            self.masscentrx = sum(child.masscentrx * child.totalmass for child in children)/self.totalmass
            self.masscentry = sum(child.masscentry * child.totalmass for child in children)/self.totalmass
        
def force(particle, node, G, theta):
    if node.leaf and node.particle is not None and node.particle is not particle:
        return newton(particle, node.particle, G)
    
    s = node.width
    dx = particle.x - node.masscentrx
    dy = particle.y - node.masscentry
    dist2 = dx ** 2 + dy ** 2
    dist = np.sqrt(dist2)
    if dist == 0: 
        return 0, 0
    
    if s/dist < theta:
        return newton(particle, Particle(node.masscentrx, node.masscentry, node.totalmass, (3/(4 * np.pi)) ** (1/3), (0,0,0), 0), G)
    Fx = 0
    Fy = 0
    children = [node.topLeftTree, node.topRightTree, node.botLeftTree, node.botRightTree]
    for child in children:
        if child and child.totalmass > 0:
            Fx_child, Fy_child = force(particle, child, G, theta)
            Fx += Fx_child
            Fy += Fy_child
    return Fx, Fy


def newton(p1, p2, G):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dist2 = dx ** 2 + dy ** 2
    dist = np.sqrt(dist2)

    F = (G * p1.mass * p2.mass)/dist2
    return F * dx/dist, F * dy/dist

def gravity(particles, G, dt, theta):
    if len(particles) == 0:
        return
    min_x = min(p.x for p in particles)
    max_x = max(p.x for p in particles)
    min_y = min(p.y for p in particles)
    max_y = max(p.y for p in particles)

    width = max_x - min_x
    height = max_y - min_y

    root = Quad(min_x, min_y, width, height)
    for p in particles:
        root.insert(p)
    root.massdistro()

    for p in particles:
        Fx, Fy = force(p, root, G, theta)  

        p.x_vel += (Fx / p.mass) * dt
        p.y_vel += (Fy / p.mass) * dt

        p.x += p.x_vel * dt
        p.y += p.y_vel * dt