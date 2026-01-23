# scene.py

from math_utils import Vec3
import math

class Material:
    
    def __init__(self, color, ambient=0.1, diffuse=0.7, specular=0.2, 
                 shininess=32, reflectivity=0.0):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflectivity = reflectivity


class Light:
    
    def __init__(self, position, intensity=1.0, color=None):
        self.position = position
        self.intensity = intensity
        self.color = color if color else Vec3(1, 1, 1)
        self.is_directional = False  # Lumière ponctuelle


class DirectionalLight:
    
    def __init__(self, direction, intensity=1.0, color=None):
        self.direction = direction.normalize()  # Direction normalisée
        self.intensity = intensity
        self.color = color if color else Vec3(1, 1, 1)
        self.is_directional = True  # Lumière directionnelle


class AmbientLight:
    
    def __init__(self, intensity=0.1, color=None):
        self.intensity = intensity
        self.color = color if color else Vec3(1, 1, 1)
        self.is_ambient = True  # Lumière ambiante


class Camera:
    
    def __init__(self, position, look_at, up, fov, aspect_ratio):
        self.position = position
        self.look_at = look_at
        self.up = up.normalize()
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        
        self.forward = (look_at - position).normalize()
        self.right = self.forward.cross(self.up).normalize()
        self.up_corrected = self.right.cross(self.forward).normalize()

        theta = math.radians(fov)
        half_height = math.tan(theta / 2)
        half_width = aspect_ratio * half_height
        
        self.lower_left_corner = (self.position + self.forward 
                                  - self.right * half_width 
                                  - self.up_corrected * half_height)
        self.horizontal = self.right * (2 * half_width)
        self.vertical = self.up_corrected * (2 * half_height)
    
    def get_ray(self, u, v):
        from geometry import Ray
        point = (self.lower_left_corner 
                + self.horizontal * u 
                + self.vertical * v)
        direction = (point - self.position).normalize()
        return Ray(self.position, direction)


class Scene:
    
    def __init__(self):
        self.objects = []  # Liste des objets (sphères, plans)
        self.lights = []   # Liste des sources de lumière
        self.camera = None  # Caméra
        self.background_color = Vec3(0.1, 0.1, 0.2)  # Couleur de fond par défaut
    
    def add_object(self, obj):
        self.objects.append(obj)
    
    def add_light(self, light):
        self.lights.append(light)
    
    def set_camera(self, camera):
        self.camera = camera
    
    def set_background(self, color):
        self.background_color = color
