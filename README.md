# Mission Japon

Appli web pour apprendre le japonais du voyage, 15 minutes par jour, avant un départ au Japon le 18 février 2027.

**Ouvrir l'appli : https://ogur1-cap.github.io/mission-japon/**

Sur téléphone, utilise « Ajouter à l'écran d'accueil » pour l'installer et t'en servir hors-ligne.

## Ce qu'il y a dedans

- Test de niveau au premier lancement (4 minutes)
- Session quotidienne avec répétition espacée : kana, kanji du voyage, phrases de survie
- Trajet Osaka → Nara → Kyoto → Kanazawa → Fuji → Tokyo, un thème par gare
- Scènes guidées (konbini, restaurant, guichet JR, hôtel capsule)
- Plusieurs profils par appareil, partage du score au groupe

## Pour le développement

Tout le code de l'appli est dans `app/source.html`. `python3 tools/build.py` génère `index.html`, le manifeste, le service worker et les icônes. Ne modifie pas `index.html` à la main.
