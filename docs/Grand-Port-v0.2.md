# Grand Port — passe de détails v0.2

La demande est d'améliorer nettement les détails en conservant la base de l'île validée. La signature des positions, tailles et rotations des fondations, plages, plateaux et côtes des 14 îles est comparée à la livraison Git `c035d98` : identique. Les emplacements des bâtiments et le spawn sont également conservés.

La passe transforme les volumes du hub en quartier portuaire : architecture à colombages, ardoises, ouvertures encadrées et volets ; commerces meublés, auvents et enseignes ; repères propres aux quartiers Marine et Pirate ; équipements portuaires et coque en construction ; espace public pavé et jardins côtiers. Toutes les créations sont locales, sans dépendance à des assets externes.

Les détails sont organisés dans `Workspace.Archipelago.grand_port.HarborDetails` et dans le sous-modèle `Architecture` de chaque bâtiment. Les murs et sols de base conservent leurs collisions ; les garnitures, cordages, feuillages et petits objets sont décoratifs. Les plus petits éléments ne projettent pas d'ombres. Les lanternes détaillées éclairantes ne calculent pas d'ombres dynamiques.

Les canons, fruits, armures, armes, grues, fontaine et navire du chantier sont des **décors**, sans achat, équipement, animation, dégâts ou pilotage. Le panneau maritime est une signalétique statique, pas une carte interactive.

Neuf contrôles automatisés couvrent la structure, la répartition des îles, les espaces maritimes, les bases inchangées, la présence des éléments, les budgets géométriques/lumineux et l'absence d'obstacles statiques dans les principaux accès pour une enveloppe de personnage de quatre studs de large et six studs de haut. Ces contrôles ne remplacent pas une session Studio.

À vérifier dans Roblox Studio : textures et couleurs réelles, face et lisibilité des enseignes, apparitions, collisions en mouvement, accès latéraux et sorties d'eau, intensité du brouillard/lanternes, performance sur mobile et streaming. L'aperçu technique fourni n'est pas une capture en jeu.

La livraison complète est `studio/OP-Empire-Wars-Map-v0.2.rbxlx`. Pour la reconstruire avec les sources : `python3 tools/build_release.py`. Pour conserver des retouches réalisées directement dans Studio, enregistrer une copie séparée avant de reconnecter Rojo : le modèle généré reste la source de la synchronisation.
