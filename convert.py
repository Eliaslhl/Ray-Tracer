# =============================================================================
# convert.py - Convertit les fichiers PPM en PNG
# =============================================================================

"""
Script de conversion PPM vers PNG.
Usage: python convert.py fichier.ppm [fichier_sortie.png]

Exemples:
    python convert.py output/simple.ppm
    python convert.py output/simple.ppm output/simple.png
"""

import sys
import os

def convert_ppm_to_png_with_pillow(input_file, output_file):
    """
    Convertit un fichier PPM en PNG en utilisant Pillow.
    """
    try:
        from PIL import Image
        
        # Ouvre et convertit l'image
        img = Image.open(input_file)
        img.save(output_file, 'PNG')
        print(f"✓ Conversion réussie avec Pillow: {output_file}")
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"✗ Erreur avec Pillow: {e}")
        return False

def convert_ppm_manually(input_file, output_file):
    """
    Convertit un fichier PPM en PNG manuellement (sans bibliothèque externe).
    Cette version crée un PNG basique sans compression optimale.
    """
    try:
        import struct
        import zlib
        
        # Lit le fichier PPM
        with open(input_file, 'r') as f:
            lines = f.readlines()
        
        # Parse l'en-tête PPM
        line_idx = 0
        # Ignore les commentaires et lignes vides
        while line_idx < len(lines) and (lines[line_idx].strip().startswith('#') or not lines[line_idx].strip()):
            line_idx += 1
        
        # Format (doit être P3)
        format_line = lines[line_idx].strip()
        if format_line != 'P3':
            print(f"✗ Format non supporté: {format_line} (seul P3 est supporté)")
            return False
        line_idx += 1
        
        # Dimensions
        while line_idx < len(lines) and (lines[line_idx].strip().startswith('#') or not lines[line_idx].strip()):
            line_idx += 1
        dims = lines[line_idx].strip().split()
        width, height = int(dims[0]), int(dims[1])
        line_idx += 1
        
        # Max value
        while line_idx < len(lines) and (lines[line_idx].strip().startswith('#') or not lines[line_idx].strip()):
            line_idx += 1
        max_val = int(lines[line_idx].strip())
        line_idx += 1
        
        # Lit les données de pixels
        pixel_data = []
        for i in range(line_idx, len(lines)):
            values = lines[i].strip().split()
            pixel_data.extend([int(v) for v in values])
        
        # Crée les données PNG
        png_data = bytearray()
        
        # En-tête PNG
        png_data.extend(b'\x89PNG\r\n\x1a\n')
        
        # Chunk IHDR (header)
        ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)  # RGB, 8-bit
        png_data.extend(struct.pack('>I', len(ihdr)))
        png_data.extend(b'IHDR')
        png_data.extend(ihdr)
        png_data.extend(struct.pack('>I', zlib.crc32(b'IHDR' + ihdr) & 0xffffffff))
        
        # Chunk IDAT (image data)
        raw_data = bytearray()
        for y in range(height):
            raw_data.append(0)  # Filter type (0 = none)
            for x in range(width):
                idx = (y * width + x) * 3
                if idx + 2 < len(pixel_data):
                    raw_data.append(pixel_data[idx])      # R
                    raw_data.append(pixel_data[idx + 1])  # G
                    raw_data.append(pixel_data[idx + 2])  # B
        
        compressed = zlib.compress(bytes(raw_data), 9)
        png_data.extend(struct.pack('>I', len(compressed)))
        png_data.extend(b'IDAT')
        png_data.extend(compressed)
        png_data.extend(struct.pack('>I', zlib.crc32(b'IDAT' + compressed) & 0xffffffff))
        
        # Chunk IEND (end)
        png_data.extend(struct.pack('>I', 0))
        png_data.extend(b'IEND')
        png_data.extend(struct.pack('>I', zlib.crc32(b'IEND') & 0xffffffff))
        
        # Écrit le fichier PNG
        with open(output_file, 'wb') as f:
            f.write(png_data)
        
        print(f"✓ Conversion réussie (manuelle): {output_file}")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de la conversion manuelle: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale."""
    
    # Vérifie les arguments
    if len(sys.argv) < 2:
        print("Usage: python convert.py fichier.ppm [fichier_sortie.png]")
        print("\nExemples:")
        print("  python convert.py output/simple.ppm")
        print("  python convert.py output/simple.ppm output/simple.png")
        return 1
    
    input_file = sys.argv[1]
    
    # Vérifie que le fichier existe
    if not os.path.exists(input_file):
        print(f"✗ Erreur: Le fichier '{input_file}' n'existe pas!")
        return 1
    
    # Détermine le nom du fichier de sortie
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # Change l'extension .ppm en .png
        base_name = os.path.splitext(input_file)[0]
        output_file = base_name + '.png'
    
    print("=" * 60)
    print("CONVERSION PPM → PNG")
    print("=" * 60)
    print(f"Entrée:  {input_file}")
    print(f"Sortie:  {output_file}")
    print("=" * 60)
    
    # Essaie d'abord avec Pillow (plus simple et plus fiable)
    print("\nTentative de conversion avec Pillow...")
    success = convert_ppm_to_png_with_pillow(input_file, output_file)
    
    # Si Pillow n'est pas disponible, utilise la conversion manuelle
    if not success:
        print("\n⚠ Pillow n'est pas installé. Utilisation de la conversion manuelle...")
        print("Pour de meilleurs résultats, installez Pillow: pip install Pillow")
        print("\nConversion en cours...")
        success = convert_ppm_manually(input_file, output_file)
    
    if success:
        print("\n" + "=" * 60)
        print("CONVERSION TERMINÉE AVEC SUCCÈS!")
        print("=" * 60)
        
        # Affiche les tailles de fichiers
        input_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file)
        ratio = (1 - output_size / input_size) * 100
        print(f"\nTaille PPM: {input_size:,} octets")
        print(f"Taille PNG: {output_size:,} octets")
        print(f"Compression: {ratio:.1f}%")
        return 0
    else:
        print("\n" + "=" * 60)
        print("✗ ÉCHEC DE LA CONVERSION")
        print("=" * 60)
        print("\nSolutions alternatives:")
        print("1. Installer Pillow: pip install Pillow")
        print("2. Utiliser GIMP (gratuit): ouvrir le PPM et exporter en PNG")
        print("3. Utiliser ImageMagick: magick convert fichier.ppm fichier.png")
        return 1

if __name__ == "__main__":
    sys.exit(main())
