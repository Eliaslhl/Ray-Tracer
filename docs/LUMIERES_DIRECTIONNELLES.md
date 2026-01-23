# 💡 Lumières Directionnelles - Documentation

## 📖 Qu'est-ce qu'une Lumière Directionnelle ?

Une **lumière directionnelle** simule une source de lumière **infiniment éloignée** qui émet des rayons **parallèles** dans une direction fixe, comme le **soleil** ☀️.

### Différences avec les Lumières Ponctuelles

| Caractéristique | Lumière Ponctuelle 💡 | Lumière Directionnelle ☀️ |
|-----------------|----------------------|---------------------------|
| **Position** | Position fixe dans l'espace | Infiniment éloignée |
| **Rayons** | Divergents (partent d'un point) | Parallèles (même direction) |
| **Atténuation** | Diminue avec la distance | Pas d'atténuation |
| **Exemple** | Lampe, bougie | Soleil, lune |

## 🎯 Utilisation dans une Scène

### Syntaxe du Fichier de Scène

```
DIRECTIONAL_LIGHT direction_x direction_y direction_z intensity [color_r color_g color_b]
```

### Paramètres

- **direction_x, direction_y, direction_z** : Direction de la lumière (pointe VERS la scène)
  - Exemple : `1 -1 0` = lumière venant du haut-droite vers le bas-gauche
  - La direction est automatiquement normalisée
  
- **intensity** : Intensité de la lumière (0.0 à 1.0)
  - 0.0 = pas de lumière
  - 1.0 = intensité maximale
  
- **color_r, color_g, color_b** (optionnel) : Couleur de la lumière (0.0 à 1.0)
  - Par défaut : `1.0 1.0 1.0` (blanc)
  - Exemple : `1.0 0.9 0.7` (lumière chaude/orangée comme le soleil couchant)

## 📝 Exemples

### Exemple 1 : Soleil de Midi (lumière du dessus)

```
DIRECTIONAL_LIGHT 0 -1 0 1.0
```
- Direction : (0, -1, 0) = vient du haut, va vers le bas
- Intensité maximale
- Couleur blanche (par défaut)

### Exemple 2 : Soleil Couchant (lumière chaude)

```
DIRECTIONAL_LIGHT 1 -0.3 -0.5 0.8 1.0 0.8 0.6
```
- Direction : vient du haut-droite avec angle faible
- Intensité 0.8
- Couleur orangée (soleil couchant)

### Exemple 3 : Lumière d'Ambiance Bleue

```
DIRECTIONAL_LIGHT -1 -0.5 0 0.3 0.5 0.7 1.0
```
- Direction : vient du haut-gauche
- Faible intensité (0.3)
- Couleur bleue (lumière lunaire)

## 🎨 Scène Complète avec Plusieurs Lumières

```
# Caméra
CAMERA 0 2 8 0 0 0 60

# Lumière principale : soleil
DIRECTIONAL_LIGHT 1 -1 -0.5 0.8 1.0 1.0 0.9

# Lumière d'appoint : ponctuelle à gauche
LIGHT -5 3 5 0.3 0.5 0.7 1.0

# Sol gris
PLANE 0 -1 0 0 1 0 0.8 0.8 0.8

# Sphère rouge
SPHERE 0 0.5 0 1.5 1.0 0.2 0.2

# Fond bleu ciel
BACKGROUND 0.5 0.7 1.0
```

## 🔍 Détails Techniques

### Calcul de l'Éclairage

Pour une lumière directionnelle :

1. **Direction** : La direction est fixe et identique pour tous les points
   ```python
   light_dir = -light.direction  # Inverse car pointe vers la scène
   ```

2. **Distance** : Considérée comme infinie
   ```python
   light_distance = float('inf')
   ```

3. **Ombres** : Les rayons d'ombre sont parallèles
   - Un objet bloque la lumière pour tous les points "derrière" lui
   - Ombres bien définies et parallèles

### Avantages

✅ **Réalisme** : Simule le soleil de manière réaliste  
✅ **Performance** : Pas de calcul de distance  
✅ **Ombres nettes** : Rayons parallèles = ombres bien définies  
✅ **Uniformité** : Même intensité partout dans la scène  

## 🎮 Cas d'Usage

### Scènes Extérieures
- **Jour ensoleillé** : 1 lumière directionnelle intense blanche
- **Coucher de soleil** : 1 lumière directionnelle orangée + 1 lumière ambiante bleue
- **Nuit lunaire** : 1 lumière directionnelle faible bleutée

### Scènes Intérieures
- **Lumière de fenêtre** : 1 lumière directionnelle pour simuler le soleil entrant
- **Éclairage studio** : Plusieurs lumières directionnelles pour contrôler les ombres

### Combinaison Mixte
```
# Soleil principal
DIRECTIONAL_LIGHT 1 -1 -0.5 0.9

# Lampes ponctuelles d'appoint
LIGHT 2 3 2 0.5
LIGHT -2 3 2 0.5
```

## 🧪 Test de la Fonctionnalité

Pour tester les lumières directionnelles :

```bash
# Rendu avec la scène de test
python src/main.py scenes/directional_light.txt output/test.ppm 800 600

# Conversion en PNG
python convert.py output/test.ppm
```

## 📊 Comparaison Visuelle

**Lumière Ponctuelle** :
```
        💡 (point)
       /│\
      / │ \     ← Rayons divergents
     /  │  \
    ●   ●   ●   ← Intensité différente selon distance
```

**Lumière Directionnelle** :
```
    ☀️ (infiniment loin)
    ↓   ↓   ↓   ← Rayons parallèles
    ●   ●   ●   ← Même intensité partout
```

## 🎓 Explication pour la Soutenance

**Pourquoi ajouter les lumières directionnelles ?**

1. **Réalisme** : Le soleil est la source de lumière la plus importante dans la nature
2. **Performance** : Pas de calcul de distance = plus rapide
3. **Contrôle artistique** : Permet de créer des éclairages uniformes
4. **Variété** : Combine bien avec les lumières ponctuelles pour des scènes complexes

**Implémentation** :

- Ajout de la classe `DirectionalLight` dans `scene.py`
- Modification du parser dans `scene_loader.py` 
- Adaptation du calcul d'éclairage dans `renderer.py`
- Support des ombres avec rayons parallèles

---

*Créé le 23 janvier 2026*
