# Notes du projet

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

## Prochaine étape

Ouvrir la maquette dans Studio et valider avec le porteur les proportions, l'orientation visuelle et Grand Port. Détailler ensuite les côtes et fortifications, puis créer un premier bateau pilotable pour éprouver les distances avant de finaliser l'archipel.

Validation cloud : génération, six tests structurels/disposition et build Rojo. Restent à faire dans Studio : rendu, collisions en mouvement, nage, streaming et performances mobile. Aucun de ces tests de jeu n'est déclaré passé.
