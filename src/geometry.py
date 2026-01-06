# =============================================================================
# geometry.py - Classes géométriques: Ray, Sphere, Plane
# =============================================================================

from math_utils import Vec3
import math

class Ray:
    """
    Classe représentant un rayon.
    Un rayon est défini par: origine + t * direction
    où t est un paramètre positif.
    """
    
    def __init__(self, origin, direction):
        """
        Initialise un rayon.
        origin: point de départ (Vec3)
        direction: direction du rayon (Vec3, devrait être normalisé)
        """
        self.origin = origin
        self.direction = direction.normalize()
    
    def at(self, t):
        """
        Retourne le point sur le rayon à la distance t.
        Résultat: origin + t * direction
        """
        return self.origin + self.direction * t


class Sphere:
    """
    Classe représentant une sphère.
    Une sphère est définie par son centre et son rayon.
    """
    
    def __init__(self, center, radius, material):
        """
        Initialise une sphère.
        center: centre de la sphère (Vec3)
        radius: rayon de la sphère (float)
        material: matériau de la sphère (Material)
        """
        self.center = center
        self.radius = radius
        self.material = material
    
    def intersect(self, ray):
        """
        Calcule l'intersection entre un rayon et la sphère.
        
        Équation de la sphère: ||P - C||² = r²
        Équation du rayon: P = O + t*D
        
        On résout: ||O + t*D - C||² = r²
        Cette équation quadratique donne: at² + bt + c = 0
        
        Retourne: (hit, t, normal) où:
        - hit: True si intersection, False sinon
        - t: distance de l'intersection (si hit=True)
        - normal: normale à la surface au point d'intersection
        """
        # Vecteur du centre de la sphère vers l'origine du rayon
        oc = ray.origin - self.center
        
        # Coefficients de l'équation quadratique
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        
        # Discriminant: b² - 4ac
        discriminant = b * b - 4 * a * c
        
        # Pas d'intersection si le discriminant est négatif
        if discriminant < 0:
            return False, None, None
        
        # Calcul des deux solutions possibles
        sqrt_discriminant = math.sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / (2 * a)
        t2 = (-b + sqrt_discriminant) / (2 * a)
        
        # On prend la plus petite valeur positive (l'intersection la plus proche)
        t = None
        if t1 > 0.001:  # 0.001 pour éviter les problèmes d'arrondi
            t = t1
        elif t2 > 0.001:
            t = t2
        else:
            return False, None, None
        
        # Point d'intersection
        hit_point = ray.at(t)
        
        # Normale: vecteur du centre vers le point d'intersection, normalisé
        normal = (hit_point - self.center).normalize()
        
        return True, t, normal


class Plane:
    """
    Classe représentant un plan infini.
    Un plan est défini par un point et une normale.
    """
    
    def __init__(self, point, normal, material):
        """
        Initialise un plan.
        point: un point sur le plan (Vec3)
        normal: normale au plan (Vec3, sera normalisé)
        material: matériau du plan (Material)
        """
        self.point = point
        self.normal = normal.normalize()
        self.material = material
    
    def intersect(self, ray):
        """
        Calcule l'intersection entre un rayon et le plan.
        
        Équation du plan: (P - point) · normal = 0
        Équation du rayon: P = O + t*D
        
        On résout: (O + t*D - point) · normal = 0
        Donc: t = ((point - O) · normal) / (D · normal)
        
        Retourne: (hit, t, normal) où:
        - hit: True si intersection, False sinon
        - t: distance de l'intersection (si hit=True)
        - normal: normale du plan
        """
        # Dénominateur: produit scalaire de la direction et de la normale
        denom = ray.direction.dot(self.normal)
        
        # Si le rayon est parallèle au plan (denom ≈ 0), pas d'intersection
        if abs(denom) < 1e-6:
            return False, None, None
        
        # Calcul de t
        t = (self.point - ray.origin).dot(self.normal) / denom
        
        # L'intersection doit être devant le rayon (t > 0)
        if t < 0.001:
            return False, None, None
        
        return True, t, self.normal
