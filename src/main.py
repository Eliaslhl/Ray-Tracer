# =============================================================================
# main.py - Point d'entrée du ray tracer
# =============================================================================

"""
Programme principal du ray tracer.
Usage: python main.py [scene_file] [output_file] [width] [height] [samples_per_pixel]

Exemples:
    python main.py
    python main.py scenes/simple.txt output/simple.ppm
    python main.py scenes/simple.txt output/simple.ppm 1920 1080 4
    python main.py scenes/simple.txt output/hq.ppm 1920 1080 8
"""

import sys
import os
from scene_loader import load_scene
from renderer import Renderer
from ppm_writer import write_ppm

def main():
    """Fonction principale du programme."""
    
    # Paramètres par défaut (résolution plus élevée pour meilleure qualité)
    scene_file = "scenes/simple.txt"
    output_file = "output/render.ppm"
    width = 1920
    height = 1080
    samples_per_pixel = 4  # Anti-aliasing activé par défaut
    
    # Parse les arguments de la ligne de commande
    if len(sys.argv) > 1:
        scene_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    if len(sys.argv) > 3:
        width = int(sys.argv[3])
    if len(sys.argv) > 4:
        height = int(sys.argv[4])
    if len(sys.argv) > 5:
        samples_per_pixel = int(sys.argv[5])
    
    # Affiche les paramètres
    print("=" * 60)
    print("RAY TRACER - Rendu d'images 3D")
    print("=" * 60)
    print(f"Scène: {scene_file}")
    print(f"Sortie: {output_file}")
    print(f"Résolution: {width}x{height}")
    if samples_per_pixel > 1:
        print(f"Anti-aliasing: {samples_per_pixel} échantillons/pixel")
    else:
        print(f"Anti-aliasing: désactivé")
    print("=" * 60)
    
    # Vérifie que le fichier de scène existe
    if not os.path.exists(scene_file):
        print(f"ERREUR: Le fichier de scène '{scene_file}' n'existe pas!")
        return 1
    
    # Crée le dossier de sortie si nécessaire
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Création du dossier: {output_dir}")
    
    try:
        # Charge la scène
        print("\nChargement de la scène...")
        scene = load_scene(scene_file)
        
        # Vérifie que la scène est valide
        if scene.camera is None:
            print("ERREUR: La scène n'a pas de caméra!")
            return 1
        
        # Crée le moteur de rendu avec anti-aliasing
        renderer = Renderer(scene, width, height, max_depth=3, samples_per_pixel=samples_per_pixel)
        
        # Effectue le rendu
        print("\nDémarrage du rendu...")
        image = renderer.render()
        
        # Sauvegarde l'image
        print("\nSauvegarde de l'image...")
        write_ppm(output_file, image)
        
        print("\n" + "=" * 60)
        print("RENDU TERMINÉ AVEC SUCCÈS!")
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"\nERREUR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
