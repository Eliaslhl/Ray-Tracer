"""
Le format PPM (Portable Pixmap) est un format d'image simple et lisible.
Structure d'un fichier PPM (P3 = ASCII):
    P3
    largeur hauteur
    255
    r1 g1 b1  r2 g2 b2  r3 g3 b3  ...
"""

def write_ppm(filename, image):
    """
    Écrit une image au format PPM.
    filename: nom du fichier de sortie (str)
    image: liste 2D de Vec3 (couleurs entre 0 et 1)
    """
    height = len(image)
    width = len(image[0]) if height > 0 else 0
    
    with open(filename, 'w') as f:
        # En-tête PPM
        f.write("P3\n")  # P3 = format ASCII
        f.write(f"{width} {height}\n")
        f.write("255\n")  # Valeur maximale pour chaque composante
        
        # Pour chaque pixel
        for row in image:
            for color in row:
                # Convertit les couleurs de [0,1] vers [0,255]
                r = int(color.x * 255.999)
                g = int(color.y * 255.999)
                b = int(color.z * 255.999)
                
                # Assure que les valeurs sont dans la plage [0, 255]
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                
                # Écrit les valeurs RGB
                f.write(f"{r} {g} {b}  ")
            f.write("\n")
    
    print(f"Image sauvegardée: {filename}")
