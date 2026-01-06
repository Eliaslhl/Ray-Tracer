# =============================================================================
# math_utils.py - Vecteurs 3D et opérations mathématiques
# =============================================================================

import math

class Vec3:
    """
    Classe représentant un vecteur 3D (x, y, z).
    Utilisé pour représenter des points, des directions, des couleurs, etc.
    """
    
    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Initialise un vecteur 3D avec ses coordonnées x, y, z"""
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, other):
        """Addition de deux vecteurs: v1 + v2"""
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        """Soustraction de deux vecteurs: v1 - v2"""
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        """Multiplication par un scalaire: v * k"""
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar):
        """Multiplication par un scalaire (inverse): k * v"""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        """Division par un scalaire: v / k"""
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def __neg__(self):
        """Négation du vecteur: -v"""
        return Vec3(-self.x, -self.y, -self.z)
    
    def __repr__(self):
        """Représentation du vecteur pour le débogage"""
        return f"Vec3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"
    
    def dot(self, other):
        """
        Produit scalaire (dot product): v1 · v2
        Résultat: x1*x2 + y1*y2 + z1*z2
        """
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        """
        Produit vectoriel (cross product): v1 × v2
        Résultat: vecteur perpendiculaire à v1 et v2
        """
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def length(self):
        """
        Longueur (magnitude) du vecteur: ||v||
        Résultat: sqrt(x² + y² + z²)
        """
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normalize(self):
        """
        Normalise le vecteur: v / ||v||
        Résultat: vecteur de longueur 1 dans la même direction
        """
        length = self.length()
        if length > 0:
            return self / length
        return Vec3(0, 0, 0)
    
    def multiply_components(self, other):
        """
        Multiplication composante par composante (pour les couleurs)
        Résultat: Vec3(x1*x2, y1*y2, z1*z2)
        """
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
    
    def clamp(self, min_val=0.0, max_val=1.0):
        """
        Limite les valeurs entre min_val et max_val
        Utile pour les couleurs (entre 0 et 1)
        """
        return Vec3(
            max(min_val, min(max_val, self.x)),
            max(min_val, min(max_val, self.y)),
            max(min_val, min(max_val, self.z))
        )


def reflect(incident, normal):
    """
    Calcule le rayon réfléchi.
    incident: direction du rayon incident (normalisé)
    normal: normale de la surface (normalisé)
    Formule: r = d - 2(d·n)n
    """
    return incident - normal * 2 * incident.dot(normal)
