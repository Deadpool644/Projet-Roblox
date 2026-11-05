# Corrections et ambiance maritime — v0.3

## Défauts identifiés sur les captures

Les bâtiments détaillés n'avaient de pignon triangulaire qu'en façade avant. La hauteur du faîtage était aussi fixée indépendamment de la largeur, et les bâtiments non détaillés n'avaient aucun pignon. Les toits sont désormais reconstruits depuis un profil unique : pente de 26°, débord de 3 studs, sous-face continue, deux versants et fermeture aux deux extrémités. Les façades arrière du hub sont maintenant fenêtrées et les murs utilisent un enduit moins chargé visuellement.

Les anciennes courtines traversaient le volume des tours et plusieurs créneaux étaient noyés dans les tours, avec des faces communes. Les courtines s'arrêtent maintenant exactement aux tours. Les parements décoratifs ont une séparation positive de leur support. Les chemins secondaires sont découpés à partir de leur union pour supprimer les faces superposées aux intersections. La place et son motif central sont séparés verticalement de leurs supports.

Les dimensions et positions des fondations, plages, plateaux et côtes sont inchangées.

## Ciel, lumière et mer

- Milieu d'après-midi (15,4 heures), lumière ambiante relevée, contraste réduit et ombres moins dures pour conserver une île lisible.
- Sky utilisant les textures intégrées de Roblox, nuages natifs sur Terrain, colorimétrie froide et léger halo des lanternes. Aucun skybox téléchargé ou asset tiers requis.
- Atmosphère côtière : densité 0,29, haze 1,9 ; pleine mer : densité jusqu'à 0,39, haze jusqu'à 3. Transition spatiale lissée et interpolation temporelle de 1,8 seconde.
- La proximité de chaque île et de son quai protège les zones de débarquement. Les données de position sont partagées avec le client, indépendamment du streaming des modèles.
- Deux émetteurs locaux de brume basse, au maximum 1,25 particule/seconde chacun et durée de vie 6–8 secondes. Ils cessent sur terre et sont nettoyés à la réapparition ou à la destruction du script. Particules désactivées aux niveaux graphiques 1–3 ; brume atmosphérique conservée. En qualité automatique, le budget réduit est conservé, sans supposer connaître le niveau choisi par le moteur.
- Mer légèrement plus claire et mouvement de vagues doux, avec deux bouées signalant l'approche du port. Les anneaux autour des bouées sont décoratifs, non une simulation physique de vagues.

Le brouillard renforcé et les nappes locales se voient après **Jouer**, lorsque le personnage navigue en mer. La météo reste visuelle et locale à chaque joueur ; aucun serveur n'est continuellement modifié par un client.

## Contrôles exécutés

- 12 tests Python : structure, disposition, accès, budgets, bases préservées ; couverture volumique des pignons avant/arrière des 11 bâtiments ; absence d'intersection entre courtines, tours et créneaux ; absence de surfaces superposées dans les chemins fusionnés.
- Luau : 14 centres d'îles, 14 quais, pleine mer et 800 échantillons de transition géographique.
- Véritable script client exécuté sous Luau avec des API Roblox simulées, pour trois réglages initiaux (automatique, 2, 8) : transitions terre/mer, changements de qualité, absence de personnage/caméra, réapparition, caméra verticale et nettoyage.
- Build Rojo de la place complète et vérification qu'elle contient le script client, le module partagé, les nuages, un seul Sky et une seule Atmosphere.
- Aperçus de géométrie avant/arrière inspectés hors Studio. Ils ne montrent pas le ciel, les textures natives ou la brume en jeu.

Ces contrôles ciblent les défauts identifiés ; ils ne garantissent pas l'absence de tout défaut visuel dans Roblox. Restent à valider en Studio : matériaux et ciel réellement chargés, lisibilité selon la qualité graphique, brouillard sur l'eau, déplacements, collisions en mouvement et performances mobile.

## Ouvrir la bonne version

Ouvrir **`studio/OP-Empire-Wars-Map-v0.3.rbxlx`** comme nouvelle place. Ne pas importer le modèle par-dessus une ancienne copie : deux archipels ou plusieurs effets d'éclairage superposés peuvent recréer des scintillements. Pour Rojo, mettre à jour le dossier complet, arrêter le test en cours, reconnecter puis relancer Jouer. Conserver séparément les retouches Studio non reportées dans les sources.
