# Ray Tracer - Projet de Rendu 3D

Ray tracer simple en Python qui génère des images 3D réalistes avec éclairage, ombres, réflexions et anti-aliasing.

## 🚀 Installation

**Prérequis :** Python 3.7+

```bash
# Cloner le projet
git clone <url_du_repo>
cd Ray-Tracer

# Vérifier Python
python --version
```

---

## 💻 Utilisation

### Commande de base

```bash
python src/main.py [scene] [output] [width] [height] [anti-aliasing]
```

**Paramètres :**

- `scene` : Fichier de scène (défaut: `scenes/simple.txt`)
- `output` : Image de sortie (défaut: `output/render.ppm`)
- `width` : Largeur en pixels (défaut: 1920)
- `height` : Hauteur en pixels (défaut: 1080)
- `anti-aliasing` : Échantillons par pixel (défaut: 4)
  - `1` = Rapide mais pixelisé
  - `4` = Qualité standard (recommandé)
  - `8-16` = Haute qualité (plus lent)

### Exemples

```bash
# Rendu haute qualité par défaut (Full HD, anti-aliasing x4)
python src/main.py

# Rendu rapide pour test (800x600, sans anti-aliasing)
python src/main.py scenes/simple.txt output/test.ppm 800 600 1

# Rendu haute qualité personnalisé
python src/main.py scenes/simple.txt output/hq.ppm 1920 1080 8
```

### Conversion en PNG

```bash
# Convertir le PPM en PNG
python convert.py output/render.ppm

# Avec nom personnalisé
python convert.py output/render.ppm mon_image.png

# Installer Pillow pour meilleure qualité (optionnel)
pip install Pillow
```

---

## 📝 Format de scène

Fichier texte simple :

```
# Commentaire
CAMERA pos_x pos_y pos_z look_x look_y look_z fov
LIGHT pos_x pos_y pos_z intensity
SPHERE center_x center_y center_z radius r g b [ambient diffuse specular shininess reflectivity]
PLANE point_x point_y point_z normal_x normal_y normal_z r g b
BACKGROUND r g b
```

**Exemple (`scenes/simple.txt`) :**

```
CAMERA 0 2 8  0 0 0  50
LIGHT 5 10 5  1.0
BACKGROUND 0.2 0.2 0.3

PLANE 0 0 0  0 1 0  0.5 0.5 0.5
SPHERE -2 1 0  1.0  0.8 0.2 0.2  0.1 0.7 0.3 50 0.2
SPHERE 0 0.7 -0.5  0.7  0.2 0.8 0.2
SPHERE 2.5 1.2 -1  1.2  0.2 0.3 0.9  0.1 0.6 0.5 80 0.3
```

---

## 🎓 Fonctionnalités

- ✅ Sphères et plans
- ✅ Éclairage de Phong (ambient, diffuse, specular)
- ✅ Ombres portées
- ✅ Réflexions
- ✅ Anti-aliasing configurable
- ✅ Export PPM et conversion PNG

---

## 📚 Ressources

- [Computer Graphics from Scratch](https://gabrielgambetta.com/computer-graphics-from-scratch/)
- [Format PPM](https://fr.wikipedia.org/wiki/Portable_pixmap)

---

**Projet réalisé dans le cadre du cours de mathématiques - ESIEE Paris**
