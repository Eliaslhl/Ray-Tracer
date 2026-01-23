# =============================================================================
# scene_loader.py - Parser de fichier de scène
# =============================================================================

from math_utils import Vec3
from geometry import Sphere, Plane
from scene import Scene, Camera, Material, Light, DirectionalLight

def load_scene(filename):
    """
    Charge une scène depuis un fichier texte.
    filename: chemin du fichier de scène (str)
    Retourne: un objet Scene
    
    Format du fichier:
    # Commentaire (ignoré)
    CAMERA position_x position_y position_z look_at_x look_at_y look_at_z fov
    LIGHT position_x position_y position_z intensity [color_r color_g color_b]
    SPHERE center_x center_y center_z radius color_r color_g color_b [ambient diffuse specular shininess reflectivity]
    PLANE point_x point_y point_z normal_x normal_y normal_z color_r color_g color_b [ambient diffuse specular]
    BACKGROUND color_r color_g color_b
    """
    scene = Scene()
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # Enlève les espaces et saute les lignes vides ou commentaires
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Divise la ligne en tokens
            tokens = line.split()
            if not tokens:
                continue
            
            command = tokens[0].upper()
            
            try:
                if command == 'CAMERA':
                    # CAMERA pos_x pos_y pos_z look_x look_y look_z fov
                    if len(tokens) < 8:
                        print(f"Ligne {line_num}: CAMERA nécessite 7 paramètres")
                        continue
                    position = Vec3(float(tokens[1]), float(tokens[2]), float(tokens[3]))
                    look_at = Vec3(float(tokens[4]), float(tokens[5]), float(tokens[6]))
                    fov = float(tokens[7])
                    up = Vec3(0, 1, 0)  # Vecteur "haut" par défaut
                    aspect_ratio = 16.0 / 9.0  # Ratio par défaut
                    camera = Camera(position, look_at, up, fov, aspect_ratio)
                    scene.set_camera(camera)
                
                elif command == 'LIGHT':
                    # LIGHT pos_x pos_y pos_z intensity [color_r color_g color_b]
                    if len(tokens) < 5:
                        print(f"Ligne {line_num}: LIGHT nécessite au moins 4 paramètres")
                        continue
                    position = Vec3(float(tokens[1]), float(tokens[2]), float(tokens[3]))
                    intensity = float(tokens[4])
                    color = Vec3(1, 1, 1)  # Blanc par défaut
                    if len(tokens) >= 8:
                        color = Vec3(float(tokens[5]), float(tokens[6]), float(tokens[7]))
                    light = Light(position, intensity, color)
                    scene.add_light(light)
                
                elif command == 'DIRECTIONAL_LIGHT':
                    # DIRECTIONAL_LIGHT dir_x dir_y dir_z intensity [color_r color_g color_b]
                    if len(tokens) < 5:
                        print(f"Ligne {line_num}: DIRECTIONAL_LIGHT nécessite au moins 4 paramètres")
                        continue
                    direction = Vec3(float(tokens[1]), float(tokens[2]), float(tokens[3]))
                    intensity = float(tokens[4])
                    color = Vec3(1, 1, 1)  # Blanc par défaut
                    if len(tokens) >= 8:
                        color = Vec3(float(tokens[5]), float(tokens[6]), float(tokens[7]))
                    light = DirectionalLight(direction, intensity, color)
                    scene.add_light(light)
                
                elif command == 'SPHERE':
                    # SPHERE center_x center_y center_z radius color_r color_g color_b [ambient diffuse specular shininess reflectivity]
                    if len(tokens) < 8:
                        print(f"Ligne {line_num}: SPHERE nécessite au moins 7 paramètres")
                        continue
                    center = Vec3(float(tokens[1]), float(tokens[2]), float(tokens[3]))
                    radius = float(tokens[4])
                    color = Vec3(float(tokens[5]), float(tokens[6]), float(tokens[7]))
                    
                    # Paramètres optionnels du matériau
                    ambient = float(tokens[8]) if len(tokens) > 8 else 0.1
                    diffuse = float(tokens[9]) if len(tokens) > 9 else 0.7
                    specular = float(tokens[10]) if len(tokens) > 10 else 0.2
                    shininess = float(tokens[11]) if len(tokens) > 11 else 32.0
                    reflectivity = float(tokens[12]) if len(tokens) > 12 else 0.0
                    
                    material = Material(color, ambient, diffuse, specular, shininess, reflectivity) # type: ignore
                    sphere = Sphere(center, radius, material)
                    scene.add_object(sphere)
                
                elif command == 'PLANE':
                    # PLANE point_x point_y point_z normal_x normal_y normal_z color_r color_g color_b [ambient diffuse specular]
                    if len(tokens) < 10:
                        print(f"Ligne {line_num}: PLANE nécessite au moins 9 paramètres")
                        continue
                    point = Vec3(float(tokens[1]), float(tokens[2]), float(tokens[3]))
                    normal = Vec3(float(tokens[4]), float(tokens[5]), float(tokens[6]))
                    color = Vec3(float(tokens[7]), float(tokens[8]), float(tokens[9]))
                    
                    # Paramètres optionnels du matériau
                    ambient = float(tokens[10]) if len(tokens) > 10 else 0.1
                    diffuse = float(tokens[11]) if len(tokens) > 11 else 0.7
                    specular = float(tokens[12]) if len(tokens) > 12 else 0.1
                    shininess = 10.0
                    reflectivity = float(tokens[13]) if len(tokens) > 13 else 0.0
                    
                    material = Material(color, ambient, diffuse, specular, shininess, reflectivity) # type: ignore
                    plane = Plane(point, normal, material)
                    scene.add_object(plane)
                
                elif command == 'BACKGROUND':
                    # BACKGROUND color_r color_g color_b
                    if len(tokens) < 4:
                        print(f"Ligne {line_num}: BACKGROUND nécessite 3 paramètres")
                        continue
                    color = Vec3(float(tokens[1]), float(tokens[2]), float(tokens[3]))
                    scene.set_background(color)
                
                else:
                    print(f"Ligne {line_num}: Commande inconnue '{command}'")
            
            except (ValueError, IndexError) as e:
                print(f"Ligne {line_num}: Erreur de parsing - {e}")
                continue
    
    # Vérifications
    if scene.camera is None:
        print("ATTENTION: Aucune caméra définie dans la scène!")
    if len(scene.lights) == 0:
        print("ATTENTION: Aucune lumière définie dans la scène!")
    if len(scene.objects) == 0:
        print("ATTENTION: Aucun objet défini dans la scène!")
    
    return scene
