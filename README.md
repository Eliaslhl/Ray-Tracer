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

## Format de scène

Fichier texte simple:

```
CAMERA 0 2 8  0 0 0  50
LIGHT 5 10 5  1.0
BACKGROUND 0.2 0.2 0.3

PLANE 0 0 0  0 1 0  0.5 0.5 0.5
SPHERE -2 1 0  1.0  0.8 0.2 0.2  0.1 0.7 0.3 50 0.2
```

## Fonctionnalités

- Sphères et plans
- Éclairage Phong
- Ombres et réflexions
- Anti-aliasing

---

Projet ESIEE Paris
