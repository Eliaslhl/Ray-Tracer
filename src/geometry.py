# geometry.py - Formes géométriques

from math_utils import Vec3
import math

class Ray:
    """Rayon: origine + t * direction"""
    
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()
    
    def at(self, t):
        """Point sur le rayon à la distance t"""
        return self.origin + self.direction * t


class Sphere:
    """Sphère définie par son centre et son rayon"""
    
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    
    def intersect(self, ray):
        """Calcule l'intersection rayon-sphère"""
        oc = ray.origin - self.center
        
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return False, None, None
        
        sqrt_discriminant = math.sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / (2 * a)
        t2 = (-b + sqrt_discriminant) / (2 * a)
        
        t = None
        if t1 > 0.001:
            t = t1
        elif t2 > 0.001:
            t = t2
        else:
            return False, None, None
        
        hit_point = ray.at(t)
        normal = (hit_point - self.center).normalize()
        
        return True, t, normal


class Plane:
    """Plan défini par un point et une normale"""
    
    def __init__(self, point, normal, material):
        self.point = point
        self.normal = normal.normalize()
        self.material = material
    
    def intersect(self, ray):
        """Calcule l'intersection rayon-plan"""
        denom = ray.direction.dot(self.normal)
        
        if abs(denom) < 1e-6:
            return False, None, None
        
        t = (self.point - ray.origin).dot(self.normal) / denom
        
        if t < 0.001:
            return False, None, None
        
        return True, t, self.normal
