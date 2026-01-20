# generate_rotation.py - Génère des scènes avec rotation des sphères

import math
import os

def rotate_point(x, z, angle, center_x=0, center_z=0):
    """Fait tourner un point (x, z) autour d'un centre"""
    # Translate vers origine
    x -= center_x
    z -= center_z
    
    # Rotation
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    new_x = x * cos_a - z * sin_a
    new_z = x * sin_a + z * cos_a
    
    # Retour à la position
    return new_x + center_x, new_z + center_z

def generate_scene(frame, total_frames, output_dir="scenes/animation"):
    """Génère un fichier de scène pour une frame donnée"""
    
    # Angle de rotation pour cette frame
    angle = (2 * math.pi * frame) / total_frames
    
    # Sphère centrale (verte) - ne bouge pas
    center_x, center_y, center_z = 0, 0.7, -0.5
    
    # Sphère rouge - tourne autour de la verte
    red_x, red_z = rotate_point(-2, 0, angle, center_x, center_z)
    red_y = 1  # Hauteur fixe
    
    # Sphère bleue - tourne autour de la verte
    blue_x, blue_z = rotate_point(2.5, -1, angle, center_x, center_z)
    blue_y = 1.2
    
    # Crée le fichier de scène
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/frame_{frame:03d}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"""# Frame {frame}/{total_frames}

CAMERA 0 2 8  0 0 0  50

LIGHT 5 10 5  1.0
LIGHT -3 5 3  0.5

BACKGROUND 0.2 0.2 0.3

PLANE 0 0 0  0 1 0  0.5 0.5 0.5  0.1 0.6 0.1 0.3

# Sphere rouge (tourne)
SPHERE {red_x:.3f} {red_y} {red_z:.3f}  1.0  0.8 0.2 0.2  0.1 0.7 0.3 50 0.2

# Sphere verte (centrale, fixe)
SPHERE {center_x} {center_y} {center_z}  0.7  0.2 0.8 0.2  0.1 0.7 0.4 60 0.1

# Sphere bleue (tourne)
SPHERE {blue_x:.3f} {blue_y} {blue_z:.3f}  1.2  0.2 0.3 0.9  0.1 0.6 0.5 80 0.3
""")
    
    return filename

def main():
    total_frames = 30  # 30 images pour le GIF
    
    print(f"Génération de {total_frames} scènes...")
    
    for frame in range(total_frames):
        filename = generate_scene(frame, total_frames)
        print(f"  {filename}")
    
    print(f"\nFini! {total_frames} scènes créées dans scenes/animation/")
    print("\nProchaine étape: python render_animation.py")

if __name__ == "__main__":
    main()
