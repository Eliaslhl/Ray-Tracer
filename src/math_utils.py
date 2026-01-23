import math

class Vec3:
    
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    # pour gérer la multiplication scalaire à droite (expl calc direction)
    def __mul__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    # pour gérer la multiplication scalaire à gauche (expl calc reflexion)
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)
    
    # affiche vecteur proprement
    def __repr__(self):
        return f"Vec3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normalize(self):
        length = self.length()
        if length > 0:
            return self / length
        return Vec3(0, 0, 0)
    
    def multiply_components(self, other):
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
    
    def clamp(self, min_val=0.0, max_val=1.0):
        return Vec3(
            max(min_val, min(max_val, self.x)),
            max(min_val, min(max_val, self.y)),
            max(min_val, min(max_val, self.z))
        )


def reflect(incident, normal):
    return incident - normal * 2 * incident.dot(normal)
