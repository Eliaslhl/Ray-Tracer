# =============================================================================
# scene.py - Scene, Camera, Material, Light
# =============================================================================

from math_utils import Vec3
import math

class Material:
    """
    Classe représentant le matériau d'une surface.
    Définit comment la surface interagit avec la lumière.
    """
    
    def __init__(self, color, ambient=0.1, diffuse=0.7, specular=0.2, 
                 shininess=32, reflectivity=0.0):
        """
        Initialise un matériau.
        color: couleur de base (Vec3 avec valeurs entre 0 et 1)
        ambient: coefficient de lumière ambiante (0-1)
        diffuse: coefficient de diffusion (0-1) - lumière mate
        specular: coefficient spéculaire (0-1) - lumière brillante
        shininess: intensité de la brillance (plus grand = plus brillant)
        reflectivity: coefficient de réflexion (0-1) - comme un miroir
        """
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflectivity = reflectivity


class Light:
    """
    Classe représentant une source de lumière ponctuelle.
    """
    
    def __init__(self, position, intensity=1.0, color=None):
        """
        Initialise une source de lumière.
        position: position de la lumière (Vec3)
        intensity: intensité de la lumière (0-1)
        color: couleur de la lumière (Vec3), blanc par défaut
        """
        self.position = position
        self.intensity = intensity
        self.color = color if color else Vec3(1, 1, 1)
        self.is_directional = False  # Lumière ponctuelle


class DirectionalLight:
    """
    Classe représentant une lumière directionnelle (comme le soleil).
    La lumière vient d'une direction fixe et est infiniment éloignée.
    """
    
    def __init__(self, direction, intensity=1.0, color=None):
        """
        Initialise une lumière directionnelle.
        direction: direction de la lumière (Vec3) - pointe VERS la scène
        intensity: intensité de la lumière (0-1)
        color: couleur de la lumière (Vec3), blanc par défaut
        """
        self.direction = direction.normalize()  # Direction normalisée
        self.intensity = intensity
        self.color = color if color else Vec3(1, 1, 1)
        self.is_directional = True  # Lumière directionnelle


class Camera:
    """
    Classe représentant la caméra virtuelle.
    """
    
    def __init__(self, position, look_at, up, fov, aspect_ratio):
        """
        Initialise une caméra.
        position: position de la caméra (Vec3)
        look_at: point vers lequel la caméra regarde (Vec3)
        up: vecteur "haut" de la caméra (Vec3)
        fov: champ de vision vertical en degrés (field of view)
        aspect_ratio: ratio largeur/hauteur (ex: 16/9)
        """
        self.position = position
        self.look_at = look_at
        self.up = up.normalize()
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        
        # Calcul du repère de la caméra
        # forward: direction dans laquelle regarde la caméra
        self.forward = (look_at - position).normalize()
        # right: direction "droite" de la caméra
        self.right = self.forward.cross(self.up).normalize()
        # up_corrected: direction "haut" corrigée (perpendiculaire à forward et right)
        self.up_corrected = self.right.cross(self.forward).normalize()
        
        # Calcul des dimensions du plan image
        # theta: angle vertical en radians
        theta = math.radians(fov)
        # half_height: moitié de la hauteur du plan image
        half_height = math.tan(theta / 2)
        # half_width: moitié de la largeur du plan image
        half_width = aspect_ratio * half_height
        
        # Coins du plan image (à distance 1 de la caméra)
        self.lower_left_corner = (self.position + self.forward 
                                  - self.right * half_width 
                                  - self.up_corrected * half_height)
        self.horizontal = self.right * (2 * half_width)
        self.vertical = self.up_corrected * (2 * half_height)
    
    def get_ray(self, u, v):
        """
        Génère un rayon pour un pixel donné.
        u, v: coordonnées normalisées du pixel (0-1)
        Retourne: un Ray depuis la caméra vers le pixel
        """
        from geometry import Ray
        # Point sur le plan image
        point = (self.lower_left_corner 
                + self.horizontal * u 
                + self.vertical * v)
        # Direction du rayon (de la caméra vers le point)
        direction = (point - self.position).normalize()
        return Ray(self.position, direction)


class Scene:
    """
    Classe représentant la scène complète.
    Contient tous les objets, lumières et la caméra.
    """
    
    def __init__(self):
        """Initialise une scène vide."""
        self.objects = []  # Liste des objets (sphères, plans)
        self.lights = []   # Liste des sources de lumière
        self.camera = None  # Caméra
        self.background_color = Vec3(0.1, 0.1, 0.2)  # Couleur de fond par défaut
    
    def add_object(self, obj):
        """Ajoute un objet à la scène."""
        self.objects.append(obj)
    
    def add_light(self, light):
        """Ajoute une lumière à la scène."""
        self.lights.append(light)
    
    def set_camera(self, camera):
        """Définit la caméra de la scène."""
        self.camera = camera
    
    def set_background(self, color):
        """Définit la couleur de fond de la scène."""
        self.background_color = color
