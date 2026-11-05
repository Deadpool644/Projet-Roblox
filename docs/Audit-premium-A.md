# Phase A — audit de la version existante

## Périmètre et preuve

Audit des sources, du modèle généré `assets/Archipelago.rbxmx`, de `default.project.json` et des contrôleurs clients, après le nouveau brief. Aucun lancement de Roblox Studio n'est possible ici. Les captures antérieures du porteur restent la seule preuve de rendu natif ; les aperçus calculés dans le cloud ne constituent pas cette preuve.

La référence v0.5 contient : **5 883 pièces physiques, 0 MeshPart, 0 SurfaceAppearance, 0 MaterialVariant, 1 spawn et 16 PointLights**. Les 21 tests géométriques et de structure existants passent. Ils ne mesurent ni l'esthétique, ni les performances du moteur Roblox.

## Problèmes constatés

| Domaine | Constat vérifiable | Conséquence / traitement requis |
|---|---|---|
| Feuillage | 96 `BlossomMass`, 405 `BlossomLeaf`, 32 `OakCanopy` et 140 `FernFrond`, construits avec des primitives ; aucun MeshPart | Non conforme au nouveau brief. Remplacer par une famille cohérente de meshes de végétation. Ne pas régénérer des sphères sous un autre nom. |
| Troncs et échelles | Troncs segmentés en cylindres ; arbres fleuris d'environ 72,4 / 53,6 / 49,5 studs, selon leurs boîtes englobantes | Le plus grand dépasse la cible de 60 studs. Les assets importés devront avoir des racines, un effilement, une écorce et une échelle contrôlée. |
| Sol | 264 pièces `Foundation`, `Beach`, `Plateau`, `Coast` pour les 14 îles ; plateaux plats | Ce n'est pas un relief natif. Prévoir une migration Terrain à bruit multi-octaves, en protégeant les zones aménagées et les accès. |
| Matériaux | Aucun PBR / MaterialVariant ; 922 pièces en SmoothPlastic | Les matières de feuillage et les surfaces majeures restent simplifiées. Besoin de textures avec droits d'utilisation et de cartes de surface cohérentes. |
| Éclairage | Future demandé, heure 16,2 et Brightness 2,4 ; Atmosphere Density 0,29, Offset 0,05 ; Bloom 0,18 ; pas de SunRays ni de DepthOfField dans la configuration | Certains réglages correspondent déjà au brief, d'autres demandent un nouveau profil et une validation native. Le ciel utilise encore les textures intégrées par défaut. |
| Brume en jeu | `MaritimeWeather` réécrit la densité, l'offset, le haze et la couleur toutes les 0,1 s | Modifier uniquement Lighting ne suffit pas. Le profil global et le contrôleur devront être unifiés avant de valider la phase B en jeu. |
| Z-fighting | Les tests couvrent les coques de bâtiments, les raccords et les faces supérieures de la muraille ; les défauts montrés sur les dernières captures ne sont pas revérifiés en Studio | Les contrôles ciblés restent utiles, mais ne prouvent pas l'absence de scintillement sur toutes les faces. Revue native au sol, de près et de loin nécessaire. |
| Densité et placement | Arbustes et groupes de décors placés à des coordonnées manuelles ; pas de distribution Poisson-disc ni de placement par raycast sur Terrain | Préparer une distribution par zones, réserves de chemins et pentes après validation du relief et des dimensions des assets. |
| Architecture des outils | Génération XML par Python, scripts de jeu séparés ; décors répartis entre plusieurs sous-modèles | Ce n'est pas encore le flux d'outils d'éditeur modulaire demandé. Prévoir des générations nommées et remplaçables sous `Map/Terrain`, `Map/Vegetation`, `Map/Props`, `Map/Effects` sans renommer les racines utilisées par les scripts. |
| Eau et audio | Océan natif ; bassin et rubans de cascade décoratifs ; aucun son d'ambiance fourni | Réviser les berges avec le Terrain, puis choisir des sons vérifiés et positionnels. Ne pas inventer d'IDs audio. |
| Performance | 5 883 primitives et 16 lumières, avec certaines économies de collisions / ombres | Ce chiffre ne garantit pas la fluidité. Budget de meshes, ombres et cartes alpha à mesurer sur un téléphone cible. |

## Conservation et risque de migration

La map, le spawn et les collisions ne sont pas modifiés dans cette phase. La forme générale de l'île reste la référence souhaitée par le porteur. Le fort et les parcours existants doivent être conservés comme contraintes de la migration.

Le remplacement des pièces de sol par Terrain changera le support des collisions : le porteur doit en être informé avant activation. Il faudra une copie du lieu, un relevé des altitudes d'entrée des bâtiments et des quais, puis des essais de marche, débarquement et réapparition. La création d'eau actuelle remplit toute la zone maritime au lancement ; elle doit être coordonnée avec la génération du nouveau Terrain pour ne pas écraser des voxels de sol.

## Vérification de fin de phase A

- Audit des sources et inventaire : effectué.
- 21 contrôles existants : passés, sans exécuter de génération supplémentaire.
- Contrôle visuel natif des textures et des échelles : non effectué.
- Mesure mobile : non effectuée.

**Décision :** ne pas publier de nouvelle version « premium » avec la végétation actuelle. La phase B dispose d'un outil d'aperçu d'éditeur préparé, non appliqué ; la migration C et les phases suivantes ne sont pas validées. La phase D reste bloquée par l'absence de meshes importés et la validation native nécessite une session Studio. Les besoins exacts sont dans `Assets-premium.md`.
