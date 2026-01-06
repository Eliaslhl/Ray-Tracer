# =============================================================================
# renderer.py - Moteur de rendu principal
# =============================================================================

from math_utils import Vec3, reflect
from geometry import Ray
import math

class Renderer:
    """
    Classe principale pour le rendu d'une scène.
    Implémente l'algorithme de ray tracing.
    """
    
    def __init__(self, scene, width=800, height=600, max_depth=3, samples_per_pixel=4):
        """
        Initialise le moteur de rendu.
        scene: la scène à rendre (Scene)
        width: largeur de l'image en pixels
        height: hauteur de l'image en pixels
        max_depth: profondeur maximale de récursion pour les réflexions
        samples_per_pixel: nombre d'échantillons par pixel pour l'anti-aliasing
                          (1 = pas d'anti-aliasing, 4 = qualité standard, 16 = haute qualité)
        """
        self.scene = scene
        self.width = width
        self.height = height
        self.max_depth = max_depth
        self.samples_per_pixel = samples_per_pixel
    
    def render(self):
        """
        Effectue le rendu complet de la scène.
        Retourne: une liste 2D de couleurs (Vec3) pour chaque pixel
        """
        if self.samples_per_pixel > 1:
            print(f"Début du rendu: {self.width}x{self.height} pixels avec anti-aliasing (x{self.samples_per_pixel})...")
        else:
            print(f"Début du rendu: {self.width}x{self.height} pixels...")
        
        # Initialise l'image (tableau 2D)
        image = []
        
        # Pour chaque ligne de pixels (de haut en bas)
        for j in range(self.height):
            row = []
            
            # Pour chaque colonne de pixels (de gauche à droite)
            for i in range(self.width):
                # Anti-aliasing: moyenne de plusieurs échantillons par pixel
                if self.samples_per_pixel > 1:
                    color_sum = Vec3(0, 0, 0)
                    
                    # Prend plusieurs échantillons dans le pixel
                    for _ in range(self.samples_per_pixel):
                        # Ajoute un petit décalage aléatoire dans le pixel
                        import random
                        offset_u = random.random() / (self.width - 1)
                        offset_v = random.random() / (self.height - 1)
                        
                        u = (i + random.random()) / (self.width - 1)
                        v = 1.0 - ((j + random.random()) / (self.height - 1))
                        
                        # Génère un rayon pour cet échantillon
                        ray = self.scene.camera.get_ray(u, v)
                        
                        # Trace le rayon et accumule la couleur
                        color_sum = color_sum + self.trace_ray(ray, depth=0)
                    
                    # Moyenne des échantillons
                    color = color_sum / self.samples_per_pixel
                else:
                    # Sans anti-aliasing: un seul rayon au centre du pixel
                    u = i / (self.width - 1)
                    v = 1.0 - (j / (self.height - 1))
                    ray = self.scene.camera.get_ray(u, v)
                    color = self.trace_ray(ray, depth=0)
                
                # Ajoute la couleur à la ligne
                row.append(color)
            
            # Ajoute la ligne à l'image
            image.append(row)
            
            # Affiche la progression
            if (j + 1) % 50 == 0 or (j + 1) == self.height:
                progress = ((j + 1) / self.height) * 100
                print(f"Progression: {progress:.1f}% ({j + 1}/{self.height} lignes)")
        
        print("Rendu terminé!")
        return image
    
    def trace_ray(self, ray, depth):
        """
        Trace un rayon dans la scène et calcule sa couleur.
        ray: le rayon à tracer (Ray)
        depth: profondeur actuelle de récursion (pour les réflexions)
        Retourne: la couleur (Vec3) vue par ce rayon
        """
        # Si on a atteint la profondeur maximale, retourne noir
        if depth >= self.max_depth:
            return Vec3(0, 0, 0)
        
        # Trouve l'objet le plus proche intersecté par le rayon
        closest_t = float('inf')
        closest_object = None
        closest_normal = None
        
        for obj in self.scene.objects:
            hit, t, normal = obj.intersect(ray)
            if hit and t < closest_t:
                closest_t = t
                closest_object = obj
                closest_normal = normal
        
        # Si aucune intersection, retourne la couleur de fond
        if closest_object is None:
            return self.scene.background_color
        
        # Point d'intersection
        hit_point = ray.at(closest_t)
        
        # Récupère le matériau de l'objet
        material = closest_object.material
        
        # Calcule la couleur avec l'éclairage
        color = self.compute_lighting(hit_point, closest_normal, ray.direction, material)
        
        # Ajoute les réflexions si le matériau est réfléchissant
        if material.reflectivity > 0:
            # Direction du rayon réfléchi
            reflect_dir = reflect(ray.direction, closest_normal)
            # Crée un nouveau rayon légèrement décalé pour éviter l'auto-intersection
            reflect_ray = Ray(hit_point + closest_normal * 0.001, reflect_dir)
            # Trace le rayon réfléchi (récursion)
            reflect_color = self.trace_ray(reflect_ray, depth + 1)
            # Mélange la couleur locale et la réflexion
            color = color * (1 - material.reflectivity) + reflect_color * material.reflectivity
        
        return color
    
    def compute_lighting(self, point, normal, view_dir, material):
        """
        Calcule l'éclairage au point d'intersection.
        Implémente le modèle de Phong (ambient + diffuse + specular).
        
        point: point d'intersection (Vec3)
        normal: normale à la surface (Vec3)
        view_dir: direction de la caméra (Vec3)
        material: matériau de la surface (Material)
        Retourne: la couleur éclairée (Vec3)
        """
        # Composante ambiante (lumière indirecte/environnement)
        ambient = material.color * material.ambient
        
        # Composantes diffuse et spéculaire (initialement nulles)
        diffuse = Vec3(0, 0, 0)
        specular = Vec3(0, 0, 0)
        
        # Pour chaque source de lumière
        for light in self.scene.lights:
            # Vecteur du point vers la lumière
            light_dir = (light.position - point).normalize()
            
            # Distance à la lumière
            light_distance = (light.position - point).length()
            
            # Vérifie si le point est dans l'ombre
            shadow_ray = Ray(point + normal * 0.001, light_dir)
            in_shadow = self.is_in_shadow(shadow_ray, light_distance)
            
            if not in_shadow:
                # --- Composante diffuse (Lambert) ---
                # Plus la surface est perpendiculaire à la lumière, plus elle est éclairée
                diff_intensity = max(0, normal.dot(light_dir))
                diffuse = diffuse + material.color.multiply_components(light.color) * (
                    material.diffuse * diff_intensity * light.intensity
                )
                
                # --- Composante spéculaire (Phong) ---
                # Reflet brillant de la source de lumière
                if diff_intensity > 0:  # Seulement si éclairé
                    # Direction du rayon réfléchi
                    reflect_dir = reflect(-light_dir, normal)
                    # Intensité spéculaire (angle entre réflexion et direction de vue)
                    spec_intensity = max(0, reflect_dir.dot(-view_dir))
                    spec_intensity = pow(spec_intensity, material.shininess)
                    specular = specular + light.color * (
                        material.specular * spec_intensity * light.intensity
                    )
        
        # Couleur finale: ambient + diffuse + specular
        final_color = ambient + diffuse + specular
        
        # Limite les valeurs entre 0 et 1
        return final_color.clamp(0, 1)
    
    def is_in_shadow(self, shadow_ray, light_distance):
        """
        Vérifie si un point est dans l'ombre d'une lumière.
        shadow_ray: rayon du point vers la lumière (Ray)
        light_distance: distance à la lumière (float)
        Retourne: True si dans l'ombre, False sinon
        """
        # Parcourt tous les objets
        for obj in self.scene.objects:
            hit, t, _ = obj.intersect(shadow_ray)
            # S'il y a une intersection avant la lumière, le point est dans l'ombre
            if hit and t < light_distance:
                return True
        return False
