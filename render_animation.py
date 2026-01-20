# render_animation.py - Rend toutes les frames et crée un GIF

import os
import subprocess
import glob

def render_all_frames():
    """Rend toutes les scènes d'animation"""
    scene_files = sorted(glob.glob("scenes/animation/frame_*.txt"))
    
    if not scene_files:
        print("Erreur: Aucune scène trouvée!")
        print("Lance d'abord: python generate_rotation.py")
        return False
    
    # Crée le dossier de sortie
    os.makedirs("output/animation", exist_ok=True)
    
    print(f"Rendu de {len(scene_files)} frames...")
    print("(Résolution réduite pour aller plus vite)")
    
    for i, scene_file in enumerate(scene_files):
        frame_num = i
        output_file = f"output/animation/frame_{frame_num:03d}.ppm"
        
        print(f"  Frame {frame_num+1}/{len(scene_files)}...", end=" ", flush=True)
        
        # Rend avec résolution réduite (plus rapide)
        cmd = [
            "python", "src/main.py",
            scene_file,
            output_file,
            "640",  # Largeur réduite
            "360"   # Hauteur réduite
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("OK")
        else:
            print(f"ERREUR\n{result.stderr}")
            return False
    
    print("\nRendu terminé!")
    return True

def create_gif():
    """Convertit les PPM en PNG puis crée un GIF"""
    
    try:
        from PIL import Image
    except ImportError:
        print("\nPillow non installé!")
        print("Installe-le: pip install Pillow")
        return False
    
    print("\nConversion PPM → PNG...")
    
    ppm_files = sorted(glob.glob("output/animation/frame_*.ppm"))
    
    for ppm_file in ppm_files:
        png_file = ppm_file.replace(".ppm", ".png")
        print(f"  {os.path.basename(ppm_file)}...", end=" ", flush=True)
        
        try:
            img = Image.open(ppm_file)
            img.save(png_file, 'PNG')
            print("OK")
        except Exception as e:
            print(f"ERREUR: {e}")
    
    # Crée le GIF
    print("\nCréation du GIF...")
    
    png_files = sorted(glob.glob("output/animation/frame_*.png"))
    
    if not png_files:
        print("Erreur: Aucun PNG trouvé!")
        return False
    
    images = [Image.open(f) for f in png_files]
    
    images[0].save(
        "output/rotation.gif",
        save_all=True,
        append_images=images[1:],
        duration=100,  # 100ms par frame = 10 FPS
        loop=0
    )
    
    print("GIF créé: output/rotation.gif")
    return True

def main():
    if not render_all_frames():
        return
    
    create_gif()
    
    print("\n=== Terminé! ===")
    print("GIF disponible: output/rotation.gif")

if __name__ == "__main__":
    main()
