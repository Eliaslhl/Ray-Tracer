# main.py - Ray tracer

import sys
import os
from scene_loader import load_scene
from renderer import Renderer
from ppm_writer import write_ppm

def main():
    # Paramètres par défaut
    scene_file = "scenes/simple.txt"
    output_file = "output/render.ppm"
    width = 1920
    height = 1080
    
    # Arguments en ligne de commande
    if len(sys.argv) > 1:
        scene_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    if len(sys.argv) > 3:
        width = int(sys.argv[3])
    if len(sys.argv) > 4:
        height = int(sys.argv[4])
    
    print(f"Ray Tracer - Rendu {width}x{height}")
    print(f"Scène: {scene_file}")
    
    if not os.path.exists(scene_file):
        print(f"Erreur: fichier '{scene_file}' introuvable")
        return 1
    
    # Crée le dossier de sortie
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        scene = load_scene(scene_file)
        
        if scene.camera is None:
            print("Erreur: pas de caméra dans la scène")
            return 1
        
        # Rendu avec anti-aliasing
        renderer = Renderer(scene, width, height, max_depth=3, samples_per_pixel=4)
        
        print("Rendu en cours...")
        image = renderer.render()
        
        print("Sauvegarde...")
        write_ppm(output_file, image)
        
        print(f"Terminé! Image: {output_file}")
        return 0
        
    except Exception as e:
        print(f"Erreur: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
