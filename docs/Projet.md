# Notes du projet

## Direction active après la v0.5

Le nouveau [brief premium](Direction-artistique-premium.md) remplace les compromis artistiques précédents : pas de feuillage en sphères, vrais meshes d'arbres avec textures, relief natif et validation en Studio par phases A–G. L'[audit de phase A](Audit-premium-A.md) est effectué ; les 21 contrôles géométriques passent mais ne valident pas la qualité visuelle. Le module de phase B est préparé pour un aperçu d'éditeur, compilé, non appliqué et non validé visuellement. Le Sky manque et la météo en jeu devra être alignée sur le nouveau profil avant validation.

Les meshes et textures nécessaires ne sont pas disponibles. Respecter l'arrêt demandé au lieu de fabriquer une nouvelle végétation en primitives. Le premier prérequis est l'import du lot décrit dans [Assets-premium.md](Assets-premium.md), transmis comme modèle `.rbxm`/`.rbxmx`. Ne pas réexécuter le générateur v0.5 pour prétendre satisfaire ce brief. Les sources, la map existante, le spawn et les collisions sont conservés pendant cette préparation. La migration du sol et les étapes suivantes ne sont pas réalisées.

## Demande et direction

L'assistant réalise le projet et le porteur du projet le guide. Commencer par la map. Préférence explicitement choisie : **plus sombre, ports fortifiés et réalistes**. L'image ensuite fournie sert de référence pour un archipel lisible, avec de grandes étendues de mer, des îles distinctes et des silhouettes à thèmes. Pas de reproduction des lieux, noms ou formes exactes de l'image.

La première livraison est une maquette 3D modifiable. Les volumes simples ne constituent pas le décor réaliste final.

## Cahier des charges

La V6 est conservée intégralement dans `Cahier-des-charges-V6.md`. Elle décrit la cible : stratégie maritime multijoueur PC/mobile, hub commun, équipement, navigation, conquête, puis construction et gestion des ressources, troupes et défenses. Races, factions Pirate/Marine, fruits, progression, équipages et alliances seront réalisés par étapes.

Le document évoque un prototype et contient des cases déjà cochées. Le dépôt initial ne contenait qu'un README : aucun de ces systèmes n'était disponible. Les instructions du document sont une référence de conception, pas une preuve d'implémentation ni une demande de tout développer immédiatement.

Point à retenir : les premières sections évoquent une possession persistante ; la section 18 octies précise ensuite des **îles de session**, avec progression personnelle persistante. La maquette ne sauvegarde rien. Retenir cette distinction lors de l'implémentation à venir.

## Carte v0.1

- Grand Port au centre, boutiques proches du spawn et axe vers le quai au sud (+Z).
- 4 îles débutantes à 850 studs du centre ; 5 intermédiaires à environ 1 700 ; 4 avancées à environ 2 687. Positions d'essai, trajets en bateau non validés.
- 4 parcelles visuelles par île : proposition de disposition, sans limite finale de construction.
- Quais avec escaliers bas prévus pour le débarquement et la sortie d'eau.
- Zone sûre prévue au hub ; aucune arme ou système de dégâts. La protection devra être validée côté serveur lors de l'ajout des combats.
- L'océan remplit une zone prédéfinie de terrain au lancement. Ne pas y ajouter de terrain sculpté sans adapter le script ; les îles actuelles utilisent des Parts.

## Grand Port v0.2

La base de l'île a été validée par le porteur du projet. La passe suivante détaille Grand Port sans changer les bases des îles : façades et intérieurs, commerces, remparts, tour Marine, quais équipés, chantier naval, espaces publics et végétation. Voir `Grand-Port-v0.2.md` pour les détails et limites.

Validation cloud actuelle : neuf tests structurels/disposition, régénération déterministe et build de la place complète. La v0.1 est conservée à titre de comparaison ; utiliser le fichier v0.2 dans `studio/` pour la dernière livraison.

## Prochaine étape

La v0.3 corrige ensuite les pignons et recouvrements signalés par captures, ajoute les façades arrière et remplace l'ambiance sombre par un ciel couvert plus lisible et une brume maritime locale progressive. Voir `Corrections-v0.3.md`.

La v0.4 reconstruit les angles des 11 bâtiments après une nouvelle capture et ajoute l'enceinte complète, six bastions périphériques et deux accès au chemin de ronde. Voir `Fort-v0.4.md`.

La v0.5 répond aux nouvelles références de qualité par une porte monumentale avec arche, chaînes et braseros, des arbres fleuris sculptés, des fleurs, une cascade et des effets locaux légers. Voir `Art-v0.5.md`. Utiliser maintenant le fichier v0.5 dans `studio/` ; les versions antérieures sont des archives. Les bases des îles sont conservées ; la qualité finale reste à juger dans le moteur Roblox.

Ouvrir la version détaillée dans Studio, contrôler le rendu, les accès et les performances, puis créer un premier bateau pilotable pour éprouver les distances avant de finaliser les autres îles.

Restent à faire dans Studio : rendu, collisions en mouvement, nage, streaming et performances mobile. Aucun de ces tests de jeu n'est déclaré passé.
