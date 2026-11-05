# OP Empire Wars — première map

Jeu Roblox de conquête maritime et de gestion d'îles. Version **0.2 : Grand Port détaillé**, avec les côtes et la disposition de la première maquette conservées. Direction : ports sombres et fortifiés, pierre grise, bois vieilli, ardoise et mer froide. L'image de référence guide la séparation des îles, leurs thèmes et leur lisibilité ; les formes restent originales.

## Ouvrir dans Roblox Studio

1. Depuis GitHub, cliquer sur **Code → Download ZIP**, puis extraire le ZIP. Si la branche `main` ne contient qu'un README, sélectionner d'abord la branche `map-v0.1` dans le sélecteur de branche.
2. Dans le dossier extrait, repérer [`studio/OP-Empire-Wars-Map-v0.2.rbxlx`](studio/OP-Empire-Wars-Map-v0.2.rbxlx). C'est la version détaillée prête à ouvrir. Le fichier seul peut aussi être téléchargé depuis sa page GitHub avec **Download raw file**. La v0.1 est conservée pour comparaison.
3. Dans Studio, **Fichier → Ouvrir depuis un fichier**, sélectionner ce fichier.
4. La map est visible et modifiable dans `Workspace.Archipelago` avant de jouer.
5. Cliquer sur **Jouer** pour apparaître au centre et remplacer la surface maritime de prévisualisation par de l'eau native Roblox.

Le modèle seul est également disponible dans `assets/Archipelago.rbxmx`. Le fichier place complet contient en plus l'éclairage, le streaming et le script de l'océan. Aucun plugin requis pour ouvrir la place.

[Voir le plan de disposition](docs/Plan-archipel-v0.1.png).

![Vue d'ensemble de la géométrie de Grand Port](docs/Grand-Port-v0.2-overview.png)

[Vue rapprochée des rues](docs/Grand-Port-v0.2-street.png). Ces aperçus sont des rendus techniques de la géométrie générée, **pas des captures Roblox Studio** ; ils ne reproduisent ni ses textures, ni son éclairage, ni ses effets.

Pour Rojo, conserver le dossier complet extrait : ouvrir un terminal dans celui contenant `default.project.json`, installer les outils avec `rokit install` si Rokit est disponible, puis lancer `rojo serve default.project.json`. Garder le terminal ouvert et connecter le plugin Studio à `localhost:34872`. Le plugin seul ne lance pas le serveur. Le fichier dans `studio/` est une livraison figée ; les prochains changements synchronisés utilisent les sources, pas ce fichier place.

## Contenu

- Grand Port : spawn, boutiques d'armes/armures/fruits, marché, missions/tutoriel, quartiers Marine et Pirate, chantier naval, phare, avenue, remparts et quais.
- 4 îles débutantes, 5 intermédiaires, 4 avancées, avec côtes variées, thèmes, ports et 52 parcelles visuelles au total.
- Eau native au lancement, lumière de fin de journée et streaming activé.
- Modèles construits avec des primitives Roblox, sans assets tiers.

### Détails ajoutés à Grand Port en v0.2

- Façades à colombages et soubassements en pierre, toitures à rangées d'ardoise, pignons, gouttières, cheminées, fenêtres à croisillons et volets, enseignes physiques et auvents.
- Présentoirs d'épées et d'armures, paniers de fruits, comptoirs, étagères, étals de marché et enclume.
- Tour de signal Marine, mât et roue maritime de la guilde, bannières et détails des remparts ; canons purement décoratifs.
- Rues pavées et bordures, place à motif de boussole, fontaine décorative, bancs, lanternes et panneau maritime physique.
- Quais habillés de planches, cordages, bollards, défenses de bois, tonneaux et cargaisons ; grues statiques et coque en construction au chantier.
- Jardinières, arbres, herbes côtières et rochers. Les petites décorations ne bloquent pas les personnages ni les raycasts.
- Atmosphère, correction colorimétrique et halo discret des lumières. Budget : moins de 4 000 pièces pour tout l'archipel, au plus 16 lumières ponctuelles ; performances réelles à mesurer sur mobile.

Cette passe porte sur **Grand Port**. Les 13 autres îles restent des maquettes thématiques ; leurs côtes et leurs parcelles n'ont pas été déplacées.

Les commerces, panneaux et parcelles sont des **emplacements et décors**. Pas encore de bateaux pilotables, capture, économie, carte interactive, combats, protection PvP, races ou factions jouables. Les bonus d'île sont des données de conception sans effet actuel.

## Développement

Python 3 (bibliothèque standard) et Rojo **7.6.1** sont nécessaires. `rokit.toml` épingle Rojo pour les postes équipés de Rokit (`rokit install`). Le binaire testé dans le cloud est `/workspace/tooling/rojo-7.6.1/rojo`.

Depuis la racine du dépôt :

```sh
python3 tools/build_map.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
mkdir -p build
rojo build default.project.json -o build/OP-Empire-Wars-Map-v0.2.rbxlx
```

Si `rojo` n'est pas dans le PATH, utiliser son chemin cloud ci-dessus. Pour la synchronisation avec le plugin Rojo officiel de Studio : `rojo serve default.project.json`.

Pour régénérer, exécuter les contrôles, construire et actualiser la copie dans `studio/` en une commande : `python3 tools/build_release.py`. Le rendu optionnel `tools/render_harbor.py` utilise NumPy et Pillow ; ces dépendances ne sont pas nécessaires pour générer la map ou ouvrir Studio.

- `tools/world.json` : positions, tailles, thèmes, difficultés et bonus prévus.
- `tools/build_map.py` : générateur déterministe du modèle.
- `tools/harbor_details.py` : composition et détails de Grand Port.
- `assets/Archipelago.rbxmx` : modèle généré inclus par Rojo.
- `src/server/Ocean.server.luau` : eau native au lancement.
- `docs/Cahier-des-charges-V6.md` : référence fournie par le porteur du projet.
- `docs/Projet.md` : décisions et prochaine étape.

**Régénérer écrase le modèle généré.** Conserver les retouches Studio séparément avant régénération ou synchronisation ; reporter les changements durables dans le générateur. Ce flux ne sauvegarde pas automatiquement les retouches Studio.

## Validation

Vérifié dans le cloud : génération déterministe, neuf contrôles structurels et de disposition, bases des îles identiques à la v0.1, dégagement géométrique des accès principaux et construction de la place avec Rojo. **Roblox Studio n'est pas disponible ici : aucun test de jeu n'a été exécuté.**

À vérifier dans Studio : apparition, accès aux boutiques et au quai, nage et escalier de sortie d'eau, collisions des côtes, visibilité et streaming sur mobile. Les distances seront ajustées après réalisation du premier bateau. Aucun accès API ni DataStore nécessaire pour cette version.
