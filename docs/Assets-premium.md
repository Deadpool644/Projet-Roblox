# Assets à importer avant la végétation premium

Les noms ci-dessous sont **les noms à donner aux modèles de notre projet**. Ils ne sont pas des titres de packs Creator Store prétendument vérifiés. Aucun ID de mesh, texture ou son n'a été inventé. Aucun outil connecté ne permet actuellement d'importer des assets Creator Store dans Studio à la place du porteur.

## Premier lot nécessaire

Chercher sur [Creator Store — Modèles](https://create.roblox.com/store/models), ou dans la Boîte à outils de Studio avec la source Creator Store. Privilégier un pack de décor cohérent, gratuit ou déjà possédé, dont les droits autorisent l'utilisation dans le jeu.

| Nom dans le projet | Type et quantité | Critères à contrôler | Recherche Creator Store |
|---|---|---|---|
| `Tree_Broadleaf_01` à `04` | 4 variantes de Models contenant des MeshParts | 25–60 studs ; tronc courbé/effilé avec racines, écorce PBR ; feuillage à cartes alpha ou mesh dense avec trous de lumière | `PBR forest trees`, `low poly realistic trees` |
| `Tree_Blossom_01` et `02` | 2 variantes de Models/MeshParts, si l'identité rose est conservée | Même finesse et même famille artistique que les arbres verts ; aucun feuillage composé de sphères | `sakura tree mesh`, `cherry blossom PBR` |
| `Bush_01` à `03` | 3 buissons en MeshParts | 2–5 studs, silhouette irrégulière, cartes alpha correctement détourées | `forest ground cover`, `PBR bushes` |
| `Fern_01`, `TallGrass_01`, `Clover_01`, `Wildflower_01` | 4 modèles de sous-bois | Touffes légères, normales et transparence correctes, sans surface lumineuse artificielle | `forest foliage pack`, `fern grass flowers` |
| `Rock_01` à `04`, `MossyRock_01` | 5 variantes de rochers mesh | Relief irrégulier, PBR roche/mousse cohérent ; dimensions adaptées au rivage, au jardin et aux talus | `PBR rocks moss`, `stylized realistic rocks` |
| `Stump_01`, `FallenLog_01`, `Branch_01`, `LeafLitter_01` | 4 modèles de sol forestier | Bois coupé crédible, usure, écorce compatible avec les arbres, géométrie légère | `forest debris`, `fallen log stump` |

Quatre à six variantes d'arbres suffisent pour le premier passage. Il faut surtout une famille cohérente, avec les textures déjà liées aux modèles ; pas plusieurs packs aux styles incompatibles.

## Deuxième lot : matières, ciel et sons

| Nom dans le projet | Contenu requis | Où chercher |
|---|---|---|
| `Stone_PBR`, `Timber_PBR`, `Roof_PBR` | SurfaceAppearance pour meshes ou MaterialVariant adapté ; Color / Normal / Roughness / Metalness selon le matériau, échelle cohérente | Creator Store → Modèles / matériaux ; recherches `PBR medieval materials`, `stone wood roof material` |
| `Sky_GoldenHour` | Objet Sky complet, six faces cohérentes avec une lumière de fin d'après-midi, soleil correctement orienté | Creator Store → Modèles ; `golden hour skybox`, `overcast sunset sky` |
| `Amb_Wind`, `Amb_Birds`, `Amb_Ocean`, `Amb_Waterfall` | Quatre sons bouclables autorisés dans l'expérience, avec leurs vrais IDs | Creator Store → Audio ; recherches `gentle wind loop`, `forest birds ambient`, `ocean shore loop`, `waterfall loop` |

Ne pas extraire les valeurs des textures à la main si elles sont déjà incluses : conserver les SurfaceAppearance et leurs références dans les modèles exportés. La disponibilité et les permissions de chaque asset doivent être vérifiées dans l'expérience cible ; une image du modèle ne suffit pas.

## Transmettre le premier lot

1. Dans Studio, créer un dossier **`ArtAssets`** dans **ServerStorage**.
2. Ranger les modèles choisis sous `Trees`, `GroundCover`, `Rocks` et `Debris` ; conserver les MeshParts et SurfaceAppearance.
3. Dans l'Explorateur, clic droit sur `ArtAssets` → **Enregistrer dans un fichier… / Save to File…**.
4. Joindre le fichier **`.rbxm` ou `.rbxmx`** dans la conversation. Fournir également les liens des packs choisis si disponibles.

Pour commencer, un seul pack d'arbres et de sous-bois cohérent suffit. Le ciel, les sons et les matières peuvent être fournis dans un deuxième lot. À réception, l'inventaire des meshes et de leurs droits d'accès précédera tout remplacement de décor.

## Organisation future

Les sources importées restent dans `ServerStorage/ArtAssets`. Les instances de décor seront générées sous `Workspace/Archipelago/grand_port/Map/{Terrain,Vegetation,Props,Effects}`. Les racines utilisées par les scripts actuels ne seront pas renommées. Les effets globaux d'éclairage restent dans Lighting, conformément au moteur Roblox.
