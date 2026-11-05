# Grand Port — direction artistique v0.5

Le porteur du projet demande une qualité de décor inspirée des captures fournies : forteresse imposante à l'arrivée en mer et cadre de jeu plus riche, organique et coloré à l'intérieur. La passe conserve le fort, le spawn, les bâtiments, les parcours et le découpage maritime, mais introduit des éléments dessinés spécifiquement pour ce projet.

## Composition

**Entrée maritime :** tours rehaussées jusqu'aux couronnements de 76 studs, arche à douze segments et écoinçons jointifs, corniche, boussole de bronze, longues chaînes à maillons alternés, braseros et lierre. L'ouverture conserve sa largeur de 42 studs et le dégagement pour les personnages. Les chaînes sont un décor, pas un mécanisme de porte ou de pont-levis.

**Intérieur :** trois grands arbres fleuris à troncs courbes et branches fourchues, feuillage rose à masses irrégulières et feuilles individuelles, petites lanternes suspendues. Fougères et fleurs ponctuent les zones secondaires. Les toitures reçoivent des couleurs coordonnées, bleu profond et bordeaux, ainsi que des terminaisons sculptées.

**Jardin de cascade :** rochers bleutés, mousse, eau turquoise, embruns et pierres de traversée. La chute et le bassin sont décoratifs ; la mer conserve le terrain d'eau natif. Le bassin ne dispose pas d'une simulation physique d'eau, de nage ou d'écoulement. Les rubans de la chute sont statiques, l'embrun est animé.

**Ambiance :** éclairage Future demandé dans la place, fin d'après-midi 16,2, ciel légèrement plus rosé, mer bleue, lanternes et feux dorés. La brume maritime de la version précédente reste active. Le moteur peut adapter ses ombres et son mode d'éclairage selon le matériel et la qualité choisie.

## Effets et ressources

Les sculptures utilisent les primitives natives Roblox et les textures/effets intégrés, sans mesh ou modèle tiers à autoriser. Ce choix rend la place directement ouvrable, mais ne remplace pas une validation de direction artistique en Studio.

`GardenAmbience` crée un pool de huit petits pétales par client. Seulement quatre sont visibles en qualité automatique, aucun aux qualités 1–3 ; ils apparaissent à moins de 130 studs d'un arbre. Un émetteur d'embruns de trois particules/seconde complète la cascade aux qualités supérieures. Les sources sont enregistrées et retirées selon le streaming. Toutes les instances locales et connexions sont nettoyées à la destruction du contrôleur.

La scène contient **5 883 pièces physiques** pour tout l'archipel, sous un budget de 6 000, et 16 lumières ponctuelles sans ombres dynamiques locales pour les nouvelles lampes. Les feuillages fins ne projettent pas d'ombres et ne bloquent ni personnages ni raycasts. Les performances sur téléphone ne sont pas mesurées ici.

## Validation et limites

- 21 tests Python : structure et parcours existants, arche pleine au-dessus d'une ouverture libre, présence des décors, nature non bloquante des feuilles/eaux décoratives, validité des couleurs et budget lumineux.
- Nouveau script client exécuté sous Luau dans un environnement d'API simulées : qualités automatique/2/8, proximité, pool réutilisé, disparition/réapparition des sources au streaming, absence de personnage, nettoyage des instances.
- Compilation Luau, build Rojo et présence des deux contrôleurs clients dans la place complète.
- Aperçus de géométrie de la porte, du jardin et de l'ensemble inspectés hors Roblox. Ces vues ne représentent ni les textures natives, ni le feu, ni l'éclairage réel.

La qualité artistique et les performances ne sont pas déclarées équivalentes aux références. Il faut encore juger le résultat dans Roblox Studio : voir l'arrivée depuis la mer, le spawn, les arbres, la cascade et les ombres à plusieurs qualités graphiques ; vérifier que les pétales et les embruns restent discrets. Les modèles, matières et textures pourront ensuite être affinés à partir du rendu natif.

## Livraison

Ouvrir `studio/OP-Empire-Wars-Map-v0.5.rbxlx` dans un nouveau document, puis cliquer sur Jouer. Pour reconstruire : `python3 tools/build_release.py`. Avec Rojo, actualiser tout le dossier avant de reconnecter. Conserver à part les retouches Studio non reportées dans les sources.
