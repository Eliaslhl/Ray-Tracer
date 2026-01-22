# renderer.py - Moteur de rendu

from math_utils import Vec3, reflect
from geometry import Ray
import math

class Renderer:
    """Moteur de rendu ray tracing"""
    
    def __init__(self, scene, width=800, height=600, max_depth=3, samples_per_pixel=4):
        self.scene = scene
        self.width = width
        self.height = height
        self.max_depth = max_depth
        self.samples_per_pixel = samples_per_pixel # nbr rayon/pixel pour anti-aliasing
    
    def render(self):
        """Effectue le rendu de la scène"""
        print(f"Rendu {self.width}x{self.height}...")
        
        image = []
        
        for j in range(self.height):
            row = []
            
            for i in range(self.width):
                # Anti-aliasing: moyenne de plusieurs rayons par pixel
                if self.samples_per_pixel > 1:
                    color_sum = Vec3(0, 0, 0)
                    
                    for _ in range(self.samples_per_pixel):
                        import random
                        u = (i + random.random()) / (self.width - 1)
                        v = 1.0 - ((j + random.random()) / (self.height - 1))
                        ray = self.scene.camera.get_ray(u, v)
                        color_sum = color_sum + self.trace_ray(ray, depth=0)
                    
                    color = color_sum / self.samples_per_pixel
                else:
                    u = i / (self.width - 1)
                    v = 1.0 - (j / (self.height - 1))
                    ray = self.scene.camera.get_ray(u, v)
                    color = self.trace_ray(ray, depth=0)
                
                row.append(color)
            
            image.append(row)
            
            if (j + 1) % 50 == 0 or (j + 1) == self.height:
                progress = ((j + 1) / self.height) * 100
                print(f"{progress:.1f}% ({j + 1}/{self.height})")
        
        return image
    
    def trace_ray(self, ray, depth):
        """Trace un rayon et calcule sa couleur"""
        if depth >= self.max_depth:
            return Vec3(0, 0, 0)
        
        # Trouve l'objet le plus proche
        closest_t = float('inf')
        closest_object = None
        closest_normal = None
        
        for obj in self.scene.objects:
            hit, t, normal = obj.intersect(ray)
            if hit and t < closest_t:
                closest_t = t
                closest_object = obj
                closest_normal = normal
        
        if closest_object is None:
            return self.scene.background_color
        
        hit_point = ray.at(closest_t)
        material = closest_object.material
        
        # Calcule l'éclairage
        color = self.compute_lighting(hit_point, closest_normal, ray.direction, material)
        
        # Ajoute les réflexions
        if material.reflectivity > 0:
            reflect_dir = reflect(ray.direction, closest_normal)
            reflect_ray = Ray(hit_point + closest_normal * 0.001, reflect_dir) # type: ignore
            reflect_color = self.trace_ray(reflect_ray, depth + 1)
            color = color * (1 - material.reflectivity) + reflect_color * material.reflectivity
        
        return color
    
    def compute_lighting(self, point, normal, view_dir, material):
        """Calcule l'éclairage (modèle de Phong)"""
        ambient = material.color * material.ambient
        diffuse = Vec3(0, 0, 0)
        specular = Vec3(0, 0, 0)
        
        for light in self.scene.lights:
            light_dir = (light.position - point).normalize()
            light_distance = (light.position - point).length()
            
            # Vérifie les ombres
            shadow_ray = Ray(point + normal * 0.001, light_dir)
            in_shadow = self.is_in_shadow(shadow_ray, light_distance)
            
            if not in_shadow:
                # Diffuse
                diff_intensity = max(0, normal.dot(light_dir))
                diffuse = diffuse + material.color.multiply_components(light.color) * (
                    material.diffuse * diff_intensity * light.intensity
                )
                
                # Spéculaire
                if diff_intensity > 0:
                    reflect_dir = reflect(-light_dir, normal)
                    spec_intensity = max(0, reflect_dir.dot(-view_dir))
                    spec_intensity = pow(spec_intensity, material.shininess)
                    specular = specular + light.color * (
                        material.specular * spec_intensity * light.intensity
                    )
        
        final_color = ambient + diffuse + specular
        return final_color.clamp(0, 1)
    
    def is_in_shadow(self, shadow_ray, light_distance):
        """Vérifie si un point est dans l'ombre"""
        for obj in self.scene.objects:
            hit, t, _ = obj.intersect(shadow_ray)
            if hit and t < light_distance:
                return True
        return False
