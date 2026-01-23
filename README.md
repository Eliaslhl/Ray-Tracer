# Ray Tracer

Ray tracer en Python qui génère des images 3D avec éclairage, ombres et réflexions.

## Installation

Python 3.7+ requis

```bash
git clone <url>
cd Ray-Tracer
```

## Utilisation

```bash
python src/main.py [scene] [output] [width] [height]
```

**Exemples:**

```bash
# Défaut (1920x1080)
python src/main.py

# Résolution custom
python src/main.py scenes/simple.txt output/test.ppm 800 600
```

**Conversion PPM → PNG:**

```bash
python convert.py output/render.ppm
```

## Génération d'animation GIF

Pour créer une animation de rotation :

```bash
# 1. Génère les fichiers de scène pour chaque frame
python generate_rotation.py

# 2. Rend toutes les frames et crée le GIF
python render_animation.py
```

Le GIF sera créé dans `output/rotation.gif`

## Fonctionnalités

- Sphères et plans
- Éclairage Phong
- Ombres et réflexions
- Anti-aliasing

---

Projet ESIEE Paris
Elias LAHLOUH & Felix Mielcarek