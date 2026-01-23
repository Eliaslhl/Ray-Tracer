from math_utils import Vec3
import math

class Ray:
    
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize() # vecteur unitaire

    def at(self, t):
        return self.origin + self.direction * t


class Sphere:
    
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    
    def intersect(self, ray):
        oc = ray.origin - self.center
        
        # coeff equation quadratique
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        
        discriminant = b * b - 4 * a * c
        
        # si pas d'intersection
        if discriminant < 0:
            return False, None, None
        
        sqrt_discriminant = math.sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / (2 * a)
        t2 = (-b + sqrt_discriminant) / (2 * a)

        # on prend la plus petite valeur positive
        t = None
        if t1 > 0.001: # évite auto-intersection
            t = t1
        elif t2 > 0.001:
            t = t2
        else:
            return False, None, None

        # Calcul du point d'intersection
        hit_point = ray.at(t)
        
        # Calcul de la normale (vecteur perpendiculaire à la surface)
        normal = (hit_point - self.center).normalize()
        
        return True, t, normal


class Plane:
    
    def __init__(self, point, normal, material):
        self.point = point
        self.normal = normal.normalize()
        self.material = material
    
    def intersect(self, ray):
        denom = ray.direction.dot(self.normal)
        
        # Si le dénominateur est proche de 0, le rayon est parallèle au plan
        if abs(denom) < 1e-6:
            return False, None, None
        
        t = (self.point - ray.origin).dot(self.normal) / denom
        
        if t < 0.001:
            return False, None, None
        
        return True, t, self.normal
