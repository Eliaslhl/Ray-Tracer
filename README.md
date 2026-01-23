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

## Lancement du gif

python generate_rotation.py
python render_animation.py

## Fonctionnalités

- Sphères et plans
- Éclairage Phong
- Ombres et réflexions
- Anti-aliasing

---

Projet ESIEE Paris
