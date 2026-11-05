# Enceinte et angles de bâtiments — v0.4

## Façades

La nouvelle capture montrait que la correction des remparts de la v0.3 ne suffisait pas : les petites pierres décoratives des angles traversaient encore les murs et les autres habillages de façade. Les `CornerQuoin`, `StonePlinth`, `FrontPlinth`, `RearPlinth` et les poteaux enterrés dans les angles sont supprimés.

Les 11 bâtiments utilisent maintenant une coque assemblée sans chevauchement : quatre piliers d'angle de 3,2 × 3,2 studs ; murs hauts et soubassements distincts, arrêtés aux piliers ; ouverture centrale conservée. Les piliers et soubassements reçoivent un matériau natif à grain sobre plutôt que de petites plaques de pavés contrastés. Les pignons sont également élargis pour couvrir le stud de mur qui dépassait de chaque côté.

Les fenêtres, enseignes, auvents, portes ouvertes, aménagements intérieurs et positions des bâtiments sont conservés. Le contrôle de volumes concerne la coque porteuse, pas les accessoires volontairement fixés aux façades.

## Enceinte

`Workspace.Archipelago.grand_port.IslandFortress` contient l'enceinte, ses six bastions périphériques et ses deux escaliers. Les deux tours de la porte existante sont conservées. Le tracé suit le bord réel des plateaux existants, légèrement décalé vers la plage, sans remodeler le terrain. Les fondations descendent dans l'eau aux endroits où les tours avancent au-delà du rivage.

- Courtines de 10 studs d'épaisseur, chemin de ronde à hauteur 22.
- Parapets sur les bords intérieur et extérieur et créneaux sur le bord extérieur.
- Découpe des virages en prismes triangulaires ajustés : les tronçons voisins partagent une arête, pas une surface supérieure superposée. Matériau de pierre non directionnel pour éviter les changements de sens du motif entre prismes.
- Six bastions cylindriques et leurs couronnements, créneaux et bannières. Les corps des bastions sont pleins et ne disposent pas d'intérieur visitable.
- Escaliers intérieurs est et ouest : 14 marches d'un stud, largeur 5 studs, paliers reliés au chemin de ronde. Les parapets intérieurs sont interrompus au droit de ces accès.
- Passage d'environ 42 studs entre les tours de la porte, axe vers les quais conservé. Il n'y a pas de porte mobile ni de système de siège dans cette version.

Le budget géométrique global passe de 4 000 à 4 500 pièces pour inclure cette enceinte d'environ 1 500 studs de longueur. La livraison comporte **4 414 pièces physiques**, sans nouvelle lumière dynamique. Le streaming reste activé ; les performances sur appareil mobile ne sont pas mesurées ici.

## Contrôles

17 tests automatisés couvrent notamment : coque des 11 bâtiments sans intersections entre piliers et murs ; pignons fermés ; bases d'îles identiques à la v0.1 ; continuité de l'épaisseur du rempart ; absence de surfaces supérieures concurrentes sur le chemin de ronde ; dégagement d'un personnage de 4 studs de large et 6 studs de haut le long du parcours ; hauteur et largeur des marches ; accès habituels au hub et au port ; budgets de géométrie et de lumières. Un audit final du modèle n'a trouvé aucune pièce physique de géométrie exactement dupliquée ; la copie Studio est identique au build.

La construction Rojo vérifie aussi la présence des scripts, nuages, ciel et atmosphère dans le fichier place complet. Les aperçus illustrent la géométrie ; ils ne reproduisent pas les textures natives du moteur Roblox.

À vérifier dans Studio : aspect réel des matériaux aux angles, absence de scintillement en déplaçant la caméra, montée des deux escaliers et parcours complet du rempart, collisions aux raccords, éclairage dans l'enceinte et performances mobile. Ces vérifications natives ne sont pas déclarées effectuées.

## Livraison

Ouvrir `studio/OP-Empire-Wars-Map-v0.4.rbxlx` dans un nouveau document Studio. Ne pas importer le modèle par-dessus les anciennes versions. Si des retouches ont été réalisées localement, en conserver une copie avant de synchroniser les sources avec Rojo.
