# OP Empire Wars — Cahier des charges complet

> **Statut :** vision cible et spécifications de développement, distinctes du prototype actuel.  
> **Plateforme :** Roblox, PC et mobile.  
> **Outils :** Roblox Studio, Luau, Rojo, Rokit.  
> **Genre :** stratégie multijoueur, conquête maritime, construction et gestion d'îles.  
> **Inspiration :** Mini Empires, avec une identité propre et une gestion territoriale approfondie.

## 1. Vision fondamentale

**OP Empire Wars doit être facile à comprendre dès les premières minutes, mais offrir une vraie profondeur stratégique.** Le joueur ne commence **pas** sur sa propre île. Il apparaît **au centre de la carte, sur une grande île centrale neutre et sécurisée**, qui sert de point de rencontre, de commerce et de départ pour tous les joueurs.

Sur cette île centrale se trouvent notamment **les boutiques d'armes, d'armures et de fruits/pouvoirs**, ainsi qu'un **port**. Le joueur s'équipe, se rend au port, prend ou obtient un navire, navigue vers une île disponible, la conquiert, puis y construit et gère son empire. Il peut ensuite repartir à la conquête d'autres îles.

**L'intérêt du jeu ne s'arrête pas à la capture : c'est surtout ce que le joueur décide de construire, de produire, de défendre et d'améliorer sur ses îles qui détermine sa puissance.**

### Principes de conception

- **Accessible :** un nouveau joueur sait toujours où aller et quoi faire.
- **Stratégique :** les choix de bâtiments, de ressources, de défense et de troupes ont des conséquences.
- **Progressif :** peu de systèmes au départ, davantage de possibilités à mesure que l'empire grandit.
- **Multijoueur :** commerce, concurrence, alliances et conflits entre joueurs.
- **Persistant :** l'empire, les bâtiments et la progression doivent pouvoir être retrouvés à la reconnexion, selon les règles de possession définies.
- **Équilibré :** les joueurs débutants disposent de protections et d'objectifs atteignables.

## 2. Parcours exact d'un nouveau joueur

```text
Apparition sur l'ÎLE CENTRALE (hub sécurisé)
       ↓
Découverte des boutiques : ARMES / ARMURES / FRUITS
       ↓
Obtention d'un équipement de départ simple
       ↓
Direction le PORT CENTRAL (objectif indiqué à l'écran)
       ↓
Choix / obtention d'un premier NAVIRE
       ↓
Navigation vers une ÎLE NEUTRE recommandée
       ↓
Débarquement et destruction des défenses ennemies
       ↓
Pose d'un avant-poste et CAPTURE de l'île
       ↓
Ouverture du MENU DE GESTION DE L'ÎLE
       ↓
Construction des premiers CHAMPS et d'un ENTREPÔT
       ↓
Production de NOURRITURE et d'ARGENT
       ↓
Construction d'une CASERNE et recrutement de TROUPES
       ↓
Construction de DÉFENSES pour protéger l'île
       ↓
Développement de l'économie, des bâtiments et de l'armée
       ↓
Départ en navire vers d'autres îles
       ↓
Expansion de l'empire, commerce, alliances, guerres
```

**Important :** l'île centrale n'est pas la première île personnelle du joueur. C'est un **hub commun**. La première île conquise devient son premier territoire à gérer.

## 2 bis. Création du personnage : tirage de race avant de jouer

**Fonctionnalité cible à développer :** avant sa première apparition sur l'île centrale, le joueur arrive sur un écran de création de personnage. Il choisit son apparence de base, puis découvre ou relance sa **race**, qui modifie visuellement son avatar et sa manière de jouer. Une fois validé, il entre dans le hub central, visite les boutiques et part au port. Le choix de race ne doit jamais remplacer la stratégie : il crée des styles de jeu différents.

### 2 bis.1 Règles du tirage et raretés

Il y a **exactement 10 races jouables**. L'Humain est **la seule race commune**. La liste reprend les inspirations de la capture, mais **la race « 3 Eyed Tribe » est écartée** pour respecter le total de 10 (1 + 4 + 2 + 2 + 1). Elle pourra éventuellement arriver lors d'une saison ultérieure, sans faire partie du lancement.

| Rareté | Probabilité par tirage | Races (chance individuelle si équiprobables dans le palier) | Nombre de bonus / malus |
|---|---:|---|---|
| Commune | **55 %** | Humain (55 %) | **1 bonus / 0 malus** |
| Peu commune | **35 %** | Skypiean, Mink, Fishman, Cyborg (8,75 % chacune) | **3 bonus / 1 malus** |
| Rare / Épique | **8,9 %** | Demon, Celestial Dragon (4,45 % chacune) | **5 bonus / 1 ou 2 malus** |
| Légendaire | **1 %** | Lunarian, Dragonoid (0,5 % chacune) | **7 bonus / 2 malus** |
| Mythique | **0,1 %** | D. Clan (0,1 %) | **10 bonus / 0 malus** |

La somme des chances est **100 %**. La chance individuelle est conditionnée à une répartition égale entre les races d'un palier ; elle doit rester configurable. **La rareté augmente la puissance et la polyvalence globale**, sans permettre à une race de rendre les autres inutiles. Les statistiques ci-dessous sont des **valeurs initiales de conception, à équilibrer en tests** ; elles ne sont pas des faits canoniques de One Piece.

**Écran avant de jouer :** avatar 3D tournant, nom de race, couleur de rareté, probabilité, présentation des bonus/malus, aperçu des changements physiques, bouton « Lancer la race », confirmation explicite avant de conserver ou remplacer une race déjà possédée, bouton « Jouer » et rappel du prochain objectif (« Trouve le port central »). Un premier tirage gratuit est prévu ; les règles d'éventuels nouveaux tirages, coûts, protections et garanties doivent être affichées avant toute dépense. Pas de reroll caché, pas de suppression silencieuse d'une race rare. Prévoir une protection contre les tirages accidentels et un historique côté serveur.

### 2 bis.2 Catalogue détaillé des dix races

Les pourcentages sont des propositions de **modificateurs relatifs**, pas des gains d'argent absolus. Les bonus ne s'appliquent que dans les situations indiquées ; un même effet ne doit pas se cumuler indéfiniment.

#### 1. Humain — Commun (55 %)

**Apparence :** avatar humain standard, sans mutation obligatoire.

**Bonus (1) :**
1. **Polyvalence** : +5 % de vitesse d'apprentissage des technologies générales.

**Malus :** aucun. Race simple, idéale pour découvrir le jeu, sans mécanique supplémentaire à gérer.

#### 2. Skypiean — Peu commun (8,75 %)

**Apparence :** petites ailes blanches dans le dos, accessoires et coiffures inspirés des peuples célestes.

**Bonus (3) :**
1. +12 % de vitesse de déplacement sur les reliefs et structures en hauteur.
2. +10 % de portée de reconnaissance depuis une tour ou un point élevé.
3. +8 % d'efficacité des défenses installées en hauteur.

**Malus (1) :** -10 % de vitesse de nage ; les ailes ne permettent pas un vol libre permanent.

**Stratégie :** observation, éclaireurs et fortifications surélevées.

#### 3. Mink — Peu commun (8,75 %)

**Apparence :** oreilles et queue animales, fourrure ou marques corporelles personnalisables ; variantes esthétiques sans avantage caché.

**Bonus (3) :**
1. +12 % de vitesse de course.
2. +10 % de dégâts au corps à corps.
3. +15 % de dégâts électriques pendant une compétence « Electro » à temps de recharge.

**Malus (1) :** +10 % de consommation de nourriture pour maintenir les performances des troupes personnelles.

**Stratégie :** raids rapides et combats rapprochés ; attention à la logistique.

#### 4. Fishman / Homme-poisson — Peu commun (8,75 %)

**Apparence :** nageoires aux bras et au dos, branchies, mains palmées, couleurs de peau aquatiques ; formes différentes selon le style choisi.

**Bonus (3) :**
1. +35 % de vitesse de nage.
2. +20 % de dégâts au corps à corps **dans l'eau** ou en zone immergée.
3. +15 % d'efficacité de pêche et de collecte de ressources marines.

**Malus (1) :** -12 % de marge commerciale lors des ventes à certains **marchands PNJ discriminatoires**, en référence aux tensions sociales de l'univers ; pas de pénalité universelle dans tous les commerces, ni de discrimination entre joueurs. Des quêtes et alliances peuvent permettre de surmonter cette barrière.

**Stratégie :** domination aquatique, économie de pêche, attaques côtières.

#### 5. Cyborg — Peu commun (8,75 %)

**Apparence :** bras mécaniques, plaques métalliques, œil lumineux, éléments technologiques visibles ; accessoires personnalisables.

**Bonus (3) :**
1. +12 % de résistance aux dégâts physiques.
2. +10 % de vitesse de réparation des navires et bâtiments.
3. +10 % d'efficacité de production des ateliers mécaniques.

**Malus (1) :** +15 % de consommation de pièces et de métal lors des réparations personnelles.

**Stratégie :** industrie, défense et flotte ; besoin de réserves de matériaux.

#### 6. Demon — Rare / Épique (4,45 %)

**Apparence :** petites cornes, yeux lumineux, marques sombres et aura discrète, sans silhouette illisible.

**Bonus (5) :**
1. +12 % de dégâts au corps à corps.
2. +10 % de résistance aux effets de peur.
3. +10 % de puissance des compétences offensives de fruits.
4. +8 % de vitesse de capture en présence du joueur.
5. +10 % de régénération d'énergie après une victoire.

**Malus (2) :**
1. -10 % de réputation auprès des marchands PNJ prudents, affectant certains prix.
2. -10 % d'efficacité des soins reçus hors d'un bâtiment de soin.

**Stratégie :** conquête agressive, mais économie et soutien médical plus délicats.

#### 7. Celestial Dragon — Rare / Épique (4,45 %)

**Apparence :** tenue noble, insignes et coiffe distinctive ; l'apparence n'impose aucun privilège sur les autres joueurs.

**Bonus (5) :**
1. +12 % de revenus des commerces de luxe.
2. -8 % de coût d'achat auprès de certains marchands PNJ affiliés.
3. +10 % de vitesse de négociation diplomatique avec des factions PNJ.
4. +10 % de capacité de stockage des entrepôts commerciaux.
5. +8 % de revenus fiscaux des villes développées.

**Malus (2) :**
1. -15 % de réputation auprès de factions PNJ hostiles aux nobles.
2. -10 % de vitesse de course en équipement cérémoniel lourd (équipement échangeable).

**Stratégie :** économie et diplomatie ; vulnérabilité lors des expéditions hostiles.

#### 8. Lunarian — Légendaire (0,5 %)

**Apparence :** grandes ailes sombres, cheveux clairs, flammes visuelles dans le dos ; les effets peuvent être réduits pour les performances.

**Bonus (7) :**
1. +18 % de résistance physique quand la flamme défensive est active.
2. +12 % de dégâts de feu.
3. +10 % de résistance au feu.
4. +12 % de vitesse de déplacement en terrain difficile.
5. +10 % de dégâts lors de la défense d'une île alliée.
6. +10 % de résistance aux dégâts des canons côtiers.
7. +8 % de vitesse de récupération d'énergie hors combat.

**Malus (2) :**
1. -12 % de vitesse de déplacement dans l'eau.
2. Quand la flamme passe en mode offensif, perte temporaire du bonus de résistance de la flamme (choix tactique obligatoire).

**Stratégie :** défense exceptionnelle, mais alternance entre puissance et protection.

#### 9. Dragonoid — Légendaire (0,5 %)

**Apparence :** écailles, petites cornes, queue et yeux reptiliens ; pas de transformation géante gratuite.

**Bonus (7) :**
1. +15 % de dégâts physiques.
2. +12 % de points de vie.
3. +10 % de résistance aux explosions.
4. +10 % de dégâts des attaques de zone.
5. +10 % de vitesse d'entraînement des unités d'assaut.
6. +8 % d'efficacité des sièges contre les fortifications.
7. +10 % de résistance aux effets de recul.

**Malus (2) :**
1. +15 % de consommation de nourriture pour les troupes d'élite associées.
2. -12 % de vitesse de déplacement furtif.

**Stratégie :** sièges et armées puissantes, avec une logistique coûteuse.

#### 10. D. Clan — Mythique (0,1 %)

**Apparence :** marque ou emblème discret « D. », regard et aura personnalisables ; la race ne doit pas imposer un modèle de personnage unique.

**Bonus (10) :**
1. +12 % de dégâts physiques.
2. +12 % de points de vie.
3. +10 % de résistance aux dégâts.
4. +10 % de vitesse de déplacement.
5. +10 % de vitesse de récupération d'énergie.
6. +10 % d'expérience gagnée.
7. +10 % de moral des troupes commandées.
8. +10 % de vitesse de capture en présence du joueur.
9. +8 % de revenus de l'ensemble des bâtiments économiques.
10. +10 % de vitesse de recherche technologique.

**Malus : aucun**, conformément à la règle mythique demandée.

**Stratégie :** race polyvalente extrêmement rare. Pour préserver un jeu compétitif, des plafonds globaux de statistiques, des contre-stratégies et des tests PvP restent obligatoires.

### 2 bis.3 Application aux mécaniques d'empire

Les races doivent influer sur **plusieurs couches du jeu**, et pas seulement sur les combats :

- **Combat personnel :** dégâts, résistance, mobilité, compétences contextuelles.
- **Économie :** commerces, pêche, production, réparation, fiscalité et prix PNJ.
- **Gestion des îles :** efficacité des bâtiments, ravitaillement, reconnaissance et garnisons.
- **Marine :** nage, abordage, réparation, exploration des côtes.
- **Diplomatie PNJ :** réputation par faction et événements scénarisés, jamais discrimination réelle entre utilisateurs.
- **Apparence :** modifications visibles persistantes du corps et des accessoires.

**Exemple concret :** un Fishman navigue vers une île côtière, nage rapidement pour débarquer, gagne un bonus en combat aquatique, installe une pêcherie rentable, mais rencontre des prix moins favorables chez une faction PNJ hostile. Il peut investir dans la diplomatie, changer de partenaire commercial ou vendre ailleurs. La race crée ainsi **des décisions stratégiques**, pas seulement un chiffre de dégâts.

### 2 bis.4 Personnalisation visuelle et lisibilité

Chaque race possède un **kit visuel** : éléments du corps, textures, couleurs, accessoires, animations et éventuellement effets. Les attributs de race doivent être visibles sur les avatars R15, rester compatibles avec les vêtements et ne pas masquer l'interface. Le joueur peut personnaliser les couleurs et les variantes esthétiques sans supprimer les signes essentiels de sa race. Prévoir des modes graphiques allégés et des effets désactivables.

La race est distincte des **fruits**, des **armes**, des **armures** et des **héros** : un joueur peut combiner ces systèmes, mais les synergies doivent avoir des plafonds pour éviter les multiplicateurs abusifs. Les références à One Piece sont une inspiration de conception ; pour une publication commerciale, créer des noms, visuels et éléments narratifs originaux plutôt que reprendre sans autorisation des éléments protégés.

### 2 bis.5 Sauvegarde, réseau et sécurité

Le profil sauvegarde au minimum :

```text
RaceId
RaceRarity
RaceRollHistory
RaceAppearanceVariant
RaceConfirmed
```

Le serveur génère le tirage avec un RNG côté serveur, vérifie les chances et applique les modificateurs. Le client affiche le résultat et ne peut **jamais choisir directement** `RaceId`, inventer une rareté ou modifier ses statistiques. Les nouveaux tirages doivent être atomiques pour éviter la duplication ou la perte de races en cas de déconnexion. Le chargement de la race doit précéder l'apparition du personnage et l'application de ses statistiques. Les valeurs des bonus/malus vivent dans une configuration centralisée, par exemple `RaceConfig`, avec un `RaceService` serveur et un `RaceSelectionController` client.

### 2 bis.6 Tutoriel de race et règles d'équilibrage

1. Présenter le tirage avec une explication simple : « Ta race change ton apparence et tes avantages ».
2. Afficher **les probabilités exactes**, tous les bonus et tous les malus avant validation.
3. Après validation, montrer **trois informations utiles maximum à l'écran** (ex. « nage plus vite », « combat aquatique », « commerce PNJ plus cher »), avec un bouton « Voir tous les détails ».
4. Guider ensuite vers les boutiques puis le port, sans forcer le joueur à lire dix pages.
5. Tester l'équilibre en PvE, PvP, économie, défense hors ligne et progression : une race rare est plus puissante selon le cahier des charges, mais ne doit pas rendre les joueurs débutants incapables de progresser.
6. Vérifier que les bonus de race ne s'appliquent pas deux fois après une mort, un respawn ou un changement de serveur.

**Critères d'acceptation :** 10 races exactement, Humain seul commun, chances totalisant 100 %, visuels distincts, nombre exact de bonus/malus par palier, tirage serveur sécurisé, sauvegarde fiable, effets mesurables dans le jeu et interface claire avant le premier spawn.

---

## 3. L'île centrale : hub de départ

### 3.1 Rôle

- Point de spawn de tous les nouveaux joueurs.
- Zone sûre : pas de PvP libre ni de destruction de boutiques.
- Point de rencontre et d'information.
- Accès aux équipements, aux services et au port.
- Retour possible pour acheter, échanger ou préparer une expédition.

### 3.2 Lieux obligatoires

| Lieu | Fonction | Compréhension immédiate |
|---|---|---|
| Boutique d'armes | Acheter ou améliorer les armes | Icône d'épée, prix visible |
| Boutique d'armures | Acheter de la protection | Icône de bouclier, comparaison des statistiques |
| Boutique de fruits | Obtenir des fruits/pouvoirs | Aperçu simple du pouvoir et de ses limites |
| Port central | Obtenir, sélectionner, faire apparaître ou améliorer un navire | Icône de bateau, bouton « Prendre la mer » |
| Tableau des îles | Voir les îles disponibles et leur difficulté | Carte, distance, niveau recommandé |
| Zone de tutoriel | Comprendre équipement, navire et capture | Objectifs courts et guidage visuel |

Les boutiques doivent être **visibles, proches du spawn et clairement signalées**. Le port doit être facile à rejoindre, avec un chemin lisible ou un marqueur d'objectif.

### 3.3 Première session

Le joueur reçoit gratuitement ou à très faible coût un équipement et un navire de départ adaptés à une première conquête. Il ne doit pas pouvoir rester bloqué au hub faute d'argent. Les équipements plus puissants restent à débloquer.

## 4. Navigation et conquête

### 4.1 Départ du port

1. Le joueur se rend au port central.
2. Il interagit avec le responsable du port ou le panneau de navigation.
3. Il choisit son navire et consulte la carte des îles.
4. Il voit la difficulté, la distance et les récompenses possibles.
5. Il prend la mer et rejoint une île.

### 4.2 Types de navires

- **Barque / navire de départ :** accès aux îles proches, faible capacité.
- **Navire de transport :** transport de soldats et de ressources.
- **Navire de combat :** protection et attaques navales.
- **Navire avancé :** meilleure résistance, vitesse ou capacité.

Les navires possèdent un coût, une vitesse, une résistance, une capacité de transport et éventuellement un armement. Leur utilisation doit rester simple au début.

### 4.3 Capture d'une île

- Choisir une île neutre ou ennemie accessible.
- Débarquer, attaquer ses défenses et neutraliser les menaces.
- Installer un avant-poste ou un drapeau de conquête.
- Tenir la position pendant une durée configurable (30 secondes dans le prototype).
- Recevoir la propriété de l'île et accéder à sa gestion.

Le serveur valide chaque étape. Les îles plus difficiles exigent une armée, de meilleurs équipements ou une flotte adaptée.

## 5. Le cœur du jeu : gestion stratégique d'une île

**Chaque île conquise devient un territoire vivant à organiser.** Le joueur ne se contente pas d'y placer des objets décoratifs : chaque bâtiment remplit une fonction économique, militaire, logistique ou défensive.

Le joueur doit faire des choix : construire davantage de champs pour nourrir les troupes, investir dans des bars et commerces pour gagner de l'argent, recruter plus de soldats ou privilégier les défenses automatiques pour protéger l'île pendant son absence.

### 5.1 Ressources

| Ressource | Production / acquisition | Utilité |
|---|---|---|
| Argent | Bars, commerces, impôts, échanges, récompenses | Acheter, construire, recruter, améliorer |
| Nourriture | Champs, fermes, pêche | Entretenir et approvisionner les troupes |
| Bois | Scieries et récolte | Bâtiments, fortifications, navires |
| Pierre | Carrières | Murs, tours, constructions |
| Fer | Mines | Armes, armures, unités, navires |
| Ressources rares | Îles spéciales et événements | Technologies, héros, pouvoirs avancés |

Les ressources sont stockées dans des entrepôts dont la capacité peut être améliorée. Les ressources insuffisantes doivent être indiquées clairement.

### 5.2 Bâtiments et rôles

| Bâtiment | Rôle stratégique | Conséquence concrète |
|---|---|---|
| **Champs** | Produire de la nourriture | Nourrir les soldats et soutenir une armée plus grande |
| **Fermes** | Augmenter la production alimentaire | Sécuriser les réserves pour les longues guerres |
| **Bars / tavernes** | Repos des troupes et activité économique | Récupération de fatigue/moral et génération de revenus |
| **Commerces / marchés** | Produire de l'argent et faciliter les échanges | Financer les constructions et les unités |
| **Mines** | Extraire pierre, fer ou autres matériaux | Alimenter les améliorations et l'équipement |
| **Scieries** | Produire du bois | Construire et réparer |
| **Entrepôts** | Stocker les ressources | Éviter le plafonnement et soutenir les expéditions |
| **Casernes** | Recruter et former les soldats | Créer des troupes pour défendre ou attaquer |
| **Hôpitaux / infirmeries** | Soigner les unités | Réduire les pertes et le coût de reconstitution |
| **Tours de garde** | Surveiller et attaquer les intrus | Première ligne de défense automatique |
| **Murs / portes** | Retarder les ennemis | Protéger les zones de production et les casernes |
| **Canons / batteries côtières** | Défendre les approches maritimes | Freiner les navires ennemis |
| **Fort / quartier général** | Centre de contrôle de l'île | Améliorer les capacités et organiser la défense |
| **Port local** | Transport et soutien naval | Déployer des troupes et relier les îles |
| **Atelier / arsenal** | Produire et améliorer l'équipement | Renforcer soldats et défenses |
| **Laboratoire** | Rechercher des technologies | Débloquer de nouvelles stratégies |

Les noms, coûts et effets exacts seront définis dans les configurations, puis équilibrés pendant les tests.

### 5.3 Bars et repos des troupes

Les bars ne sont **pas seulement décoratifs**. Ils remplissent deux fonctions :

1. **Économie :** générer de l'argent grâce à l'activité de l'île.
2. **Soutien militaire :** permettre aux troupes affectées au repos de récupérer leur fatigue ou leur moral selon un système simple.

Un bar peut consommer une petite quantité de nourriture ou d'autres ressources pour fonctionner. Le joueur doit voir ce qu'il produit et ce qu'il consomme. Les soldats ne deviennent pas invincibles grâce aux bars : il faut équilibrer repos, soins et défense.

### 5.4 Champs et nourriture

Les champs produisent de la nourriture à intervalles réguliers. La nourriture sert à **approvisionner les troupes**, soutenir la population et préparer les expéditions.

Si la production est insuffisante, l'armée peut perdre de l'efficacité, voir son recrutement limité ou consommer ses réserves. **Le jeu ne doit pas punir brutalement un débutant** : les conséquences sont annoncées et progressives.

Exemple :

```text
Production : +120 nourriture / cycle
Consommation des troupes : -80 / cycle
Bilan : +40 / cycle → île autonome
```

Si la consommation atteint 150, le bilan devient négatif : il faut construire un champ, améliorer une ferme, réduire l'armée ou importer de la nourriture.

### 5.5 Dépendances entre bâtiments

Les bâtiments doivent former un système cohérent :

```text
CHAMPS → nourriture → entretien des TROUPES
BAR / TAVERNE → argent + repos des TROUPES
MINES / SCIERIES → matériaux → CONSTRUCTIONS
COMMERCES → argent → AMÉLIORATIONS
CASERNE + nourriture + argent → NOUVELLES TROUPES
ENTREPÔT → réserves pour résister à un siège
TOURS + MURS + GARNISON → DÉFENSE DE L'ÎLE
PORT → ravitaillement et conquêtes suivantes
```

## 6. Défendre une île même lorsque le joueur n'est pas présent

La défense autonome est **une fonctionnalité centrale**, pas un détail.

### 6.1 Système de garnison

Le joueur affecte des soldats à la défense de l'île. Ils ne doivent pas obligatoirement être contrôlés manuellement. Les garnisons suivent des ordres simples :

- défendre le quartier général ;
- protéger les bâtiments de production ;
- surveiller le port ;
- tenir les murs ;
- patrouiller dans une zone.

### 6.2 Défenses automatiques

- Tours de garde et canons attaquant les ennemis autorisés à être ciblés.
- Murs et portes ralentissant l'avancée adverse.
- Garnisons IA protégeant les points importants.
- Alertes envoyées au propriétaire lors d'une attaque.
- Réserves de nourriture et de matériaux pour tenir un siège.
- Possibilité de définir des priorités de défense depuis un menu simple.

### 6.3 Absence du joueur : règles d'équité

**Deux situations doivent être distinguées :**

- **Le joueur est connecté mais ailleurs sur la carte :** son île reste active et les défenses automatiques la protègent.
- **Le joueur est déconnecté :** il faut définir un système juste, compatible avec Roblox, par exemple une protection hors ligne, des attaques asynchrones simulées, ou des fenêtres de siège. Une île ne doit pas dépendre d'un serveur Roblox qui continuerait à fonctionner en permanence après le départ du joueur.

**Décision de conception recommandée :** protéger les îles des joueurs hors ligne contre la perte totale de territoire, tout en permettant des événements limités ou des attaques planifiées avec des règles explicites. Cette règle est à valider avant l'implémentation du PvP.

### 6.4 Exemple de stratégie défensive

```text
                   MER
             [Canon côtier]
                   |
             [Mur + Porte]
              /         \
        [Tour]           [Tour]
           |               |
       [Casernes]      [Entrepôt]
           \               /
          [Quartier général]
             /          \
         [Champs]      [Bar]
```

Le joueur choisit les emplacements selon les contraintes du terrain, la portée des défenses, les accès maritimes et la valeur des bâtiments. Les meilleures défenses ne doivent pas être simplement « acheter la tour la plus chère ».

## 7. Décisions stratégiques et équilibre

Chaque île possède une superficie et un nombre limité d'emplacements constructibles ou de zones aménageables. Le joueur doit arbitrer :

- **Économie ou armée :** plus de bars et commerces, ou plus de casernes ?
- **Production ou protection :** un champ supplémentaire, ou une tour ?
- **Expansion ou consolidation :** attaquer une autre île, ou renforcer celle-ci ?
- **Troupes offensives ou garnison :** envoyer tous les soldats en mer, ou en garder pour défendre ?
- **Autonomie ou importation :** produire sur place, ou ravitailler depuis une autre île ?
- **Spécialisation :** transformer une île en centre agricole, commercial, industriel ou militaire.

Une île mal gérée peut avoir beaucoup de soldats mais manquer de nourriture ; une île riche peut devenir une cible facile si elle n'a aucune défense.

## 8. Spécialisation des îles

Le prototype comporte six types d'îles. Dans la version finale, leurs bonus doivent influencer réellement la stratégie.

| Île | Spécialité | Style de gestion encouragé |
|---|---|---|
| Agricole | Bonus de production agricole | Champs, fermes, ravitaillement |
| Commerciale | Bonus de revenus | Bars, marchés, commerces |
| Industrielle | Bonus de production militaire | Mines, ateliers, arsenal |
| Militaire | Bonus aux unités et défenses | Casernes, garnisons, fortifications |
| Des Fruits | Amélioration des fruits/pouvoirs | Capacités spéciales et soutien |
| Ancienne | Technologies rares | Recherche et améliorations uniques |

Les bonus du prototype sont des valeurs de départ, pas des valeurs d'équilibrage définitives.

## 9. Gestion de plusieurs îles

Après avoir conquis plusieurs îles, le joueur doit disposer d'une **vue globale de son empire** :

- liste de ses îles ;
- ressources produites et consommées par île ;
- niveau de défense ;
- garnisons ;
- constructions en cours ;
- alertes de pénurie ;
- routes de ravitaillement ;
- accès rapide à chaque île.

Le transfert de ressources entre îles peut nécessiter des navires de transport et introduire une dimension logistique. La gestion doit rester possible sans effectuer des dizaines de clics.

## 10. Interface : facile à comprendre dès le début

### 10.1 Règles UX obligatoires

1. **Une action principale visible à la fois** pendant le tutoriel.
2. Des boutons avec **icône + texte**, jamais une icône incompréhensible seule.
3. Toujours afficher **coût, production, consommation et bénéfice** d'un bâtiment.
4. Montrer immédiatement pourquoi une action est impossible.
5. Afficher les ressources essentielles en permanence, sans surcharger l'écran.
6. Utiliser des couleurs et des symboles cohérents pour production, danger, défense et manque de ressources.
7. Fournir une aide courte et consultable à nouveau.
8. Prévoir PC et mobile dès la conception.
9. Proposer des modèles de construction recommandés, sans supprimer la liberté stratégique.
10. Ne jamais obliger le joueur à comprendre toutes les mécaniques dès la première partie.

### 10.2 HUD général

```text
┌──────────────────────────────────────────────────────────┐
│ Argent | Nourriture | Bois | Pierre | Fer | Niveau       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│                   MONDE / ÎLE                             │
│                                                          │
│ Objectif : « Va au port et prends un navire »             │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Carte | Construire | Armée | Défense | Empire | Inventaire│
└──────────────────────────────────────────────────────────┘
```

### 10.3 Menu de gestion d'une île

```text
ÎLE AGRICOLE — Niveau 2

Argent : +90/min       Nourriture : +40/min net
Défense : 180          Garnison : 12 soldats

[Construire] [Améliorer] [Troupes] [Défenses] [Production]

Alerte : « Vos réserves nourrissent l'armée pendant 25 min »
Conseil : « Construisez un champ pour augmenter l'autonomie »
```

Les chiffres ci-dessus sont **illustratifs**, pas des valeurs finales.

## 11. Tutoriel progressif obligatoire

### Mission 1 — Découvrir le hub

- Apparition sur l'île centrale.
- Repérer les boutiques d'armes, d'armures et de fruits.
- Récupérer un équipement de départ.
- Indicateur clair : « Rejoins le port ».

### Mission 2 — Prendre la mer

- Parler au responsable du port.
- Obtenir son premier bateau.
- Voir une île neutre recommandée sur la carte.
- Naviguer jusqu'à cette île.

### Mission 3 — Première conquête

- Débarquer.
- Vaincre une défense simple.
- Construire un avant-poste.
- Attendre la capture.
- Recevoir une confirmation claire.

### Mission 4 — Faire vivre son île

- Construire un champ.
- Voir la nourriture augmenter.
- Construire un bar ou un commerce.
- Comprendre les revenus.
- Construire un entrepôt.

### Mission 5 — Préparer sa défense

- Construire une caserne.
- Recruter quelques soldats.
- Affecter une garnison.
- Placer une tour de garde.
- Comprendre que l'île peut se défendre pendant que le joueur voyage.

### Mission 6 — Devenir stratège

- Lire le bilan ressources/consommation.
- Choisir entre renforcer l'île et préparer une nouvelle conquête.
- Naviguer vers une deuxième île.

**Chaque mission explique une mécanique par une action pratique.** Les joueurs expérimentés peuvent passer le tutoriel, mais l'aide reste accessible.

## 12. Armées et combat

- Soldats, archers, unités lourdes, unités spéciales et autres catégories à définir.
- Statistiques : vie, dégâts, défense, portée, vitesse, coût, entretien, fatigue/moral éventuel.
- Recrutement dans les casernes.
- Affectation à une garnison ou à une expédition.
- Ordres simples pour les débutants ; tactiques plus poussées pour les joueurs avancés.
- Les combats et dégâts sont validés par le serveur.
- Les troupes consomment de la nourriture selon une fréquence définie.
- Les bars/tavernes et infirmeries soutiennent la récupération, sans remplacer la stratégie.

## 13. Marine et logistique

- Le **port central** sert de point de départ à la première conquête.
- Les **ports locaux** permettent de repartir depuis les îles possédées.
- Les navires transportent soldats et éventuellement ressources.
- Les routes de ravitaillement relient les îles.
- Les batailles navales peuvent couper ou protéger ces routes.
- La capacité d'un navire limite les expéditions : le joueur doit planifier.

## 14. Équipements, héros et fruits

- **Armes :** achetées dans la boutique centrale, avec dégâts et conditions de déblocage.
- **Armures :** protection et caractéristiques visibles avant achat.
- **Fruits/pouvoirs :** compétences spéciales avec cooldown, progression et limites.
- **Héros :** personnages spéciaux apportant des bonus économiques, militaires ou défensifs.
- **Technologies :** améliorations de production, d'unités, de navires et de défenses.

Ces systèmes enrichissent la stratégie mais **ne doivent pas masquer la gestion des îles**, qui reste au centre du jeu.

## 15. Multijoueur, PvP et alliances

- Hub central commun et sécurisé.
- Îles neutres pour les premières conquêtes.
- Conflits territoriaux entre joueurs selon des règles claires.
- Alliances, commerce et coopération possibles : dégâts alliés désactivés, mais revenus séparés.
- Équipages Pirates avec drapeaux sur plusieurs îles, propriété collective et partage des revenus avec bonus.
- Tous les Marines sont protégés des dégâts entre eux.
- Protections pour les nouveaux joueurs.
- Limites contre le harcèlement et les attaques répétées.
- Les territoires sont temporaires : aucun siège ni revenu d’île hors ligne ; voir section 16.

## 16. Persistance : progression permanente, territoires de session

**Règle définitive prioritaire : quitter le serveur fait perdre toutes les îles contrôlées, personnelles ou d'équipage.** Les îles et leurs bâtiments, garnisons, stocks locaux, revenus et drapeaux sont des possessions **de session uniquement**, jamais restaurées comme propriété du joueur à sa reconnexion. Cela remplace toute ancienne mention de sauvegarde des îles ou de production hors ligne. Il n'existe **aucun revenu d'île hors ligne**.

**Conservé après déconnexion :** Berrys personnels, race et apparence, faction, prime/honneur, niveau/XP, Haki et compétences débloquées, armes, armures, équipements permanents, fruits sécurisés dans le sac, capacité de stockage, progression des quêtes permanentes, paramètres et historique de tutoriel. L'appartenance à un équipage et ses rôles peuvent persister ; **ses îles ne persistent pas au-delà de la session de conquête**.

**Perdu en quittant :** toutes les îles contrôlées, bâtiments et défenses de ces îles, garnisons et stocks locaux, drapeaux territoriaux ; tout fruit **physiquement tenu dans la main et non sécurisé**. Les règles de mort des fruits sont détaillées à la section 18 octies.

**Cas équipage :** si un membre quitte, il perd son contrôle personnel des îles de session ; les îles d'équipage **restent actives tant qu'au moins un membre autorisé de l'équipage demeure dans ce même serveur**. Quand le dernier membre quitte, elles sont libérées et leurs revenus cessent. Aucun transfert d'îles entre serveurs. En cas de déconnexion/reconnexion, le joueur ne récupère pas automatiquement un territoire ; il peut rejoindre la session de ses coéquipiers si les mécanismes Roblox le permettent. Le système doit gérer proprement une fermeture de serveur.

**Profil persistant minimal :** `Money`, `RaceId`, `Faction`, `BountyOrHonor`, `Level`, `XP`, `Weapons`, `Armor`, `PermanentEquipment`, `StoredFruits`, `FruitStorageCapacity`, `UnlockedHaki`, `Quests`, `Settings`, `CrewId`. **Ne jamais inclure `OwnedIslands` dans le profil persistant.**

Les données sont enregistrées par le serveur avec DataStore et une gestion des erreurs. La perte des fruits tenus et la conservation des fruits stockés doivent être atomiques et résistantes aux déconnexions.

---

## 17. Architecture technique existante

Le projet est développé sur Windows avec VS Code, Rojo et Roblox Studio.

```text
Projet roblox/
├── src/
│   ├── shared/
│   │   ├── Config/
│   │   └── Modules/
│   ├── server/
│   │   └── Services/
│   └── client/
├── docs/
├── default.project.json
├── rokit.toml
├── selene.toml
├── aftman.toml
└── README.md
```

Correspondance Rojo :

```text
src/shared → ReplicatedStorage.Shared
src/server → ServerScriptService.Server
src/client → StarterPlayerScripts.Client
```

### Services à conserver ou développer

| Service | Rôle |
|---|---|
| DataService | Sauvegarde, chargement, profil |
| PlayerService | Joueurs, progression, équipement |
| MapService | Hub, génération et localisation des îles |
| IslandService | Capture, propriété, bonus |
| EconomyService | Production, consommation, ressources |
| BuildingService | Placement, construction, améliorations |
| GarrisonService | Affectation des troupes et défense autonome |
| DefenseService | Tours, murs, priorités, alertes |
| ArmyService | Recrutement et ordres |
| CombatService | Calcul des combats |
| ShipService | Navires, ports, transport |
| LogisticsService | Transferts et ravitaillement |
| TechnologyService | Recherches et déblocages |
| HeroService | Héros |
| FruitService | Fruits et pouvoirs |
| TutorialService | Parcours guidé et aide |
| SeasonService | Événements et saisons |

Les nouveaux services sont **proposés**, pas déclarés comme déjà codés.

### Configurations data-driven

```text
IslandConfig
BuildingConfig
ResourceConfig
UnitConfig
DefenseConfig
ShipConfig
TechnologyConfig
WeaponConfig
ArmorConfig
FruitConfig
HeroConfig
TutorialConfig
GameConfig
```

Tout contenu configurable doit être ajouté dans `src/shared/Config` et non dispersé dans les scripts du moteur.

### Règle de sécurité

Le client affiche et demande ; **le serveur décide**. Achats, constructions, ressources, dégâts, capture, recrutement, transport et récompenses sont vérifiés côté serveur. Les RemoteEvents doivent être validés et limités pour empêcher les abus.

## 18. État actuel confirmé du prototype

Les tests réalisés montrent :

- [x] Rokit et Rojo fonctionnent sous Windows.
- [x] Roblox Studio est connecté à Rojo.
- [x] Le personnage apparaît.
- [x] Le backend démarre avec cinq services.
- [x] L'interface client démarre.
- [x] Six îles spécialisées apparaissent pendant le test.
- [x] Une interaction de conquête est visible.
- [x] Les erreurs DataStore précédemment observées ne sont plus présentes dans la dernière sortie montrée.
- [ ] Sauvegarde persistante vérifiée sur plusieurs sessions (non confirmée).
- [ ] Île centrale aménagée avec boutiques et port (à développer/vérifier).
- [ ] Navigation en navire (à développer/vérifier).
- [ ] Économie stratégique complète (à développer).
- [ ] Construction de champs, bars, casernes et défenses (à développer).
- [ ] Garnisons et protection autonome (à développer).
- [ ] Tutoriel complet (à développer).
- [ ] PvP, alliances, héros, fruits avancés et saisons (à développer).

**Ne pas confondre les fonctionnalités décrites dans ce document avec des fonctionnalités déjà présentes dans le code.**

## 18 bis. Factions jouables : Pirates ou Marine — système complet

> **Fonctionnalité à développer.** Ce chapitre est une spécification de gameplay et non une fonctionnalité déjà implémentée. Les valeurs sont des propositions d'équilibrage, à tester sur serveur multijoueur. Les grades et l'univers sont inspirés des codes des jeux de pirates ; prévoir des appellations et visuels originaux pour une diffusion commerciale.

### 18 bis.1 Choix de faction et parcours du joueur

Après la création du personnage et le tirage de race, le joueur choisit **Pirate** ou **Marine**. Ce choix est indépendant de la race : toutes les races peuvent rejoindre les deux factions. L'île centrale reste le point de départ commun, avec boutiques d'armes, d'armures, de fruits et deux quais distincts. Les combats sont désactivés dans la zone de départ.

**Parcours Pirate :** création → race → Pirate → boutiques → port pirate → navire → capture d'une île → champs, bars, casernes, fortifications et économie → nouvelles conquêtes → prime et réputation. Le Pirate construit son empire et gère ses ressources.

**Parcours Marine :** création → race → Marine → armurerie et équipement réglementaire → base/port de la Marine → navire de patrouille → mission de sécurisation → reprise d'une île aux pirates ou arrestation → honneur, salaire et promotions. **Le Marine ne gère pas de champs, bars, taxes ni empire économique personnel.** Il joue principalement le combat, la navigation, la coopération et la défense des territoires libérés. Les îles reprises passent sous contrôle de la faction Marine/PNJ, pas en propriété économique individuelle du joueur.

Le changement de faction ne doit pas servir à effacer sa prime ou à multiplier les récompenses : procédure encadrée, délai de changement, confirmation, conséquences visibles et historique persistant. Les récompenses de progression Pirate et Marine restent séparées et ne se convertissent jamais automatiquement.

### 18 bis.2 Deux scores distincts

- **Pirate : Prime** (`Bounty`), de **0 à 5 000 000 000**, affichée sur l'avis de recherche. Elle augmente surtout par les exploits dangereux et les victoires légitimes ; elle ne constitue **pas** de l'argent dépensable.
- **Marine : Honneur** (`Honor`), de **0 à 5 000 000 000**, qui mesure les services rendus, les arrestations et la libération d'îles. Ce n'est **pas** de la monnaie.
- **Argent** (`Money`) : monnaie de jeu indépendante, gagnée par l'économie pirate, le butin ou le salaire de la Marine. Une arrestation peut donner de l'argent **en plus** de l'honneur.
- **Grade** : titre calculé côté serveur à partir du score de faction, avec progression et bonus. Les grades ne se débloquent pas seulement avec du temps de connexion.

### 18 bis.3 Barème des grades — Pirates (maximum 5 milliards)

| Prime minimale | Titre pirate | Rôle / réputation |
|---:|---|---|
| 0 | Moussaillon | Débute en mer |
| 10 000 | Pirate novice | Premières missions |
| 50 000 | Pirate confirmé | Premiers combats |
| 250 000 | Pirate redouté | Premières prises d'îles |
| 1 000 000 | Capitaine pirate | Dirige son équipage |
| 5 000 000 | Capitaine recherché | Reconnu dans une région |
| 15 000 000 | Capitaine de renom | Menace régionale |
| 40 000 000 | Supernova | Pirate de nouvelle génération |
| 100 000 000 | Supernova redoutée | Recherché en haute mer |
| 200 000 000 | Seigneur des mers | Contrôle plusieurs routes |
| 350 000 000 | Grand Capitaine | Puissance régionale |
| 500 000 000 | Corsaire redouté | Figure majeure des mers |
| 750 000 000 | Grand Corsaire | Influence internationale |
| 1 000 000 000 | Empereur émergent | Menace mondiale |
| 1 500 000 000 | Empereur des mers | Domine de vastes territoires |
| 2 000 000 000 | Grand Empereur | Figure historique |
| 3 000 000 000 | Seigneur des océans | Exploits exceptionnels |
| 4 000 000 000 | Légende des mers | Proche du sommet |
| **5 000 000 000** | **Roi des Pirates** | **Titre ultime, extrêmement rare** |

**Important :** « Corsaire » est ici un titre de prestige inspiré du thème, pas une affiliation à la Marine. Si une mécanique de corsaires au service du gouvernement est ajoutée, prévoir une autre dénomination pour éviter la confusion.

### 18 bis.4 Barème des grades — Marine (maximum 5 milliards d'honneur)

| Honneur minimal | Grade Marine |
|---:|---|
| 0 | Recrue |
| 10 000 | Matelot |
| 50 000 | Matelot de première classe |
| 250 000 | Quartier-maître |
| 1 000 000 | Maître |
| 5 000 000 | Premier maître |
| 15 000 000 | Enseigne |
| 40 000 000 | Lieutenant junior |
| 100 000 000 | Lieutenant |
| 200 000 000 | Lieutenant-commandant |
| 350 000 000 | Commandant |
| 500 000 000 | Capitaine de vaisseau |
| 750 000 000 | Commodore |
| 1 000 000 000 | Contre-amiral |
| 1 500 000 000 | Vice-amiral |
| 2 000 000 000 | Amiral |
| 3 000 000 000 | Amiral de flotte |
| 4 000 000 000 | Grand amiral |
| **5 000 000 000** | **Amiral de flotte légendaire** |

Ces seuils sont volontairement bien plus élevés que ceux des captures d'écran de référence, car le plafond souhaité est **5 milliards** et le parcours doit durer longtemps. Les noms peuvent être ajustés pour la cohérence de l'univers.

### 18 bis.5 Bonus de puissance selon la prime ou l'honneur

Les **mêmes paliers** de puissance s'appliquent aux deux factions : l'une n'est pas intrinsèquement plus forte que l'autre. Ils sont **non cumulables** : à chaque palier, le bonus précédent est remplacé par le nouveau. Le score exact n'accorde pas de puissance supplémentaire entre deux seuils.

| Prime / honneur minimal | Défense | Dégâts |
|---:|---:|---:|
| 0 | +0 % | +0 % |
| 10 000 | +0,5 % | +0,3 % |
| 50 000 | +1 % | +0,6 % |
| 250 000 | +2 % | +1 % |
| 1 000 000 | +3 % | +2 % |
| 5 000 000 | +4 % | +3 % |
| 15 000 000 | +5 % | +4 % |
| 40 000 000 | +6 % | +5 % |
| 100 000 000 | +8 % | +6 % |
| 200 000 000 | +10 % | +7,5 % |
| 350 000 000 | +12 % | +9 % |
| 500 000 000 | +14 % | +10 % |
| 750 000 000 | +16 % | +12 % |
| 1 000 000 000 | +18 % | +14 % |
| 1 500 000 000 | +21 % | +16 % |
| 2 000 000 000 | +24 % | +18 % |
| 3 000 000 000 | +28 % | +20 % |
| 4 000 000 000 | +32 % | +22 % |
| **5 000 000 000** | **+35 %** | **+25 %** |

Les bonus s'appliquent au **personnage en combat**, pas automatiquement à tous les bâtiments, navires et troupes. Les bonus de race, d'équipement, de fruit et de grade sont combinés avec des **plafonds globaux**, sans multiplication illimitée. Exemple de calcul recommandé : `dégâts finaux = dégâts de base × (1 + bonus_total_plafonné)` avant résistances et effets contextuels. La rareté doit être gratifiante, mais un nouveau joueur doit garder des possibilités de fuite et de contre-jeu.

### 18 bis.6 Comment un Pirate gagne sa prime

**Actions éligibles (valeurs de départ proposées) :**

| Action | Prime de base proposée | Conditions |
|---|---:|---|
| Mission pirate débutant | 500 à 3 000 | Première réalisation, plafond journalier |
| Victoire contre un PNJ de niveau comparable | 1 000 à 8 000 | Pas de farm de PNJ faibles |
| Première capture d'une île neutre | 10 000 à 40 000 | Uniquement si difficulté adaptée |
| Capture d'une île d'un autre joueur | 25 000 à 250 000 | Défense réelle, propriétaire actif ou règles de siège validées |
| Victoire sur un joueur ennemi | Selon formule ci-dessous | Combat légitime, anti-farm |
| Victoire sur un boss maritime / événement | 50 000 à 1 000 000 | Limites et difficulté évolutives |
| Conquête d'une forteresse de haut niveau | 100 000 à 2 000 000 | Récompense rare, anti-répétition |

Ces valeurs ne doivent **pas** permettre d'atteindre les milliards en répétant des activités faciles. **Multiplicateur de progression décroissant** : à partir de 100 M, les gains ordinaires sont divisés par 2 ; à 500 M par 5 ; à 1 Md par 10 ; à 3 Md par 25 ; à 4 Md par 50. Les grands événements et victoires contre des adversaires réellement comparables conservent une récompense spécifique, mais avec plafonds.

**Victoire contre un autre Pirate :** récompense calculée selon la prime et la puissance réelle de la cible, pas seulement sa prime. Exemple de formule de départ :

```text
ratio = puissance_cible / puissance_attaquant
facteur_equilibre = clamp(ratio, 0.10, 1.50)
base = clamp(prime_cible × 0.002, 100, 200000)
gain_brut = base × facteur_equilibre
prime_gagnee = arrondi(gain_brut × multiplicateur_progression)
```

La puissance réelle prend en compte niveau, équipement, statistiques et force de combat, avec une mesure serveur résistante à la manipulation. **Une cible très faible rapporte peu**, même si elle a une prime artificiellement élevée ; une cible puissante rapporte davantage. Un Marine vaincu peut également donner une récompense selon son honneur, avec le même mécanisme. La prime **n'est pas transférée** depuis la victime : elle est attribuée comme réputation au vainqueur. Le perdant peut subir une pénalité de score limitée en PvP classé, clairement annoncée, mais jamais une confiscation arbitraire de toute sa progression.

### 18 bis.7 Comment un Marine gagne son honneur et son argent

| Action Marine | Honneur de base proposé | Argent |
|---|---:|---|
| Patrouille / mission d'entraînement | 500 à 2 000 | Solde de mission |
| Éliminer un PNJ pirate dangereux | 1 000 à 8 000 | Récompense de mission |
| Arrêter un Pirate joueur | Selon sa prime et sa puissance | Prime de capture en argent |
| Libérer une île pirate | 25 000 à 250 000 | Prime d'opération |
| Défendre une île libérée | 5 000 à 50 000 | Prime de défense |
| Boss pirate / événement | 50 000 à 1 000 000 | Récompense spéciale |

**Arrestation :** après avoir vaincu un Pirate, le Marine doit pouvoir déclencher une interaction d'arrestation courte et contestable (ou un système équivalent). Le Pirate est envoyé en détention temporaire avec sortie garantie ; aucune privation longue du jeu. La récompense dépend de la prime de la cible, de sa puissance et de l'authenticité du combat. L'arrestation n'efface pas automatiquement la prime de la cible. Pour les primes d'argent, utiliser une **fraction plafonnée** de la prime affichée, jamais une conversion 1:1 qui ruinerait l'économie. Exemple : `argent = clamp(prime_cible × 0,0001, 100, 50 000)` puis facteur d'équilibrage et limites anti-farm.

**Salaire passif de la Marine :** versé **uniquement pendant le temps de jeu actif**, toutes les 10 minutes, sans ferme AFK. Proposition : Recrue 100 pièces/10 min ; Matelot 150 ; Lieutenant 350 ; Capitaine 700 ; Contre-amiral 1 000 ; Vice-amiral 1 500 ; Amiral 2 000 ; Amiral de flotte légendaire 3 000. Les grades intermédiaires sont interpolés par configuration. Les missions donnent un complément. Le salaire finance équipement, réparations et consommables, mais **pas** une économie de champs et de commerces. Aucune progression d'honneur ne doit être accordée simplement parce que le joueur est connecté.

### 18 bis.8 Reprise d'îles, défenses et PvP

- **Pirate :** conquiert et possède des îles ; construit des bâtiments économiques, recrute des troupes, installe des défenses autonomes et gère le ravitaillement.
- **Marine :** reprend les îles pirates, détruit ou neutralise les défenses hostiles, sécurise la zone, puis remet l'île à une garnison Marine gérée par le jeu. Il ne peut pas exploiter les champs ou encaisser des taxes personnelles.
- **Île libérée :** devient une zone de contrôle Marine temporaire ou une île neutre sécurisée, selon le scénario ; les Pirates peuvent tenter de la reconquérir après une période de protection.
- **Hors ligne :** pas de pillage instantané sans défense possible ; fenêtre de siège, défense automatique, avertissement au propriétaire et limitation des pertes. Les Marines ne doivent pas pouvoir détruire définitivement l'empire d'un joueur absent sans contre-jeu.
- **Conflit :** zones PvP clairement signalées, protection des nouveaux joueurs, immunité courte après réapparition et interdiction de tuer en boucle dans le port central.
- **Coopération :** escouades Marine, équipages Pirates, partage de récompenses proportionnel à la contribution et prévention des doubles gains.

### 18 bis.9 Progression vraiment longue jusqu'à 5 milliards

Le sommet ne doit pas s'obtenir en quelques jours. **Objectif de conception**, à confirmer par télémétrie : les premiers millions sont accessibles en découvrant le jeu ; 100 M demande une progression avancée ; 1 Md correspond à un vétéran ; 3–4 Md nécessite de nombreux exploits de haut niveau ; **5 Md est un accomplissement exceptionnel sur le long terme**, pas une récompense d'AFK. Ne pas promettre une durée exacte avant d'avoir mesuré le rythme réel des joueurs.

Garde-fous : rendements décroissants, plafonds par type d'action et par adversaire, récompenses de première conquête non répétables, matchmaking par puissance, missions de haut niveau, événements rares, contrôle des comptes secondaires, et journal serveur des gains. Une progression par **saisons** peut proposer des classements réinitialisés, mais **la prime/honneur historique de carrière reste persistante** sauf règle explicitement annoncée.

### 18 bis.10 Anti-abus et règles serveur

- Aucun gain si la victime est alliée, dans le même groupe d'exploitation suspect ou a été vaincue récemment par le même attaquant.
- Rendement nul ou presque nul sur une cible trop faible ; récompense réduite en cas de déséquilibre extrême.
- Pas de récompense pour une mort volontaire, un suicide ou une élimination arrangée détectée.
- Temps de recharge par paire de joueurs (ex. 60 minutes pour une récompense complète), décroissance des gains répétés et plafonds journaliers adaptatifs.
- Récompense accordée une seule fois par événement, avec identifiant d'opération unique et validation serveur.
- Les captures ne rapportent pas de prime à répétition si la même île change artificiellement de mains.
- Pas de modification de `Bounty`, `Honor`, `Faction`, `Rank`, `Salary` ou `Reward` depuis le client.
- Les races, fruits, équipements et grades ne doivent jamais permettre de contourner les protections PvP.

### 18 bis.11 Interface simple et progression visible

**Avant de jouer :** « Choisis ta voie : Pirate (construire et conquérir) ou Marine (combattre et protéger) ». Deux cartes lisibles avec avantages, contraintes et aperçu des activités. Après sélection, tutoriel spécifique.

**HUD Pirate :** prime, titre, prochaine promotion, argent, îles possédées, ressources et objectif. Avis de recherche personnalisable, affichage de la progression vers le grade suivant.

**HUD Marine :** honneur, grade, prochaine promotion, argent, prochaine solde, mission de patrouille, îles à libérer et pirates recherchés. Tableau des primes avec filtres par danger et distance.

**Après un combat :** afficher séparément `+Honneur` ou `+Prime`, `+Argent`, contribution, et explication si gain réduit (« adversaire trop faible », « combat déjà récompensé »). Prévoir un onglet de tous les paliers et bonus. Ne pas surcharger le tutoriel de chiffres.

### 18 bis.12 Architecture et données à ajouter

```text
src/shared/Config/
  FactionConfig.lua
  RankConfig.lua
  ReputationRewardConfig.lua
  MarineSalaryConfig.lua
  PvPBalanceConfig.lua
src/server/Services/
  FactionService.lua
  ReputationService.lua
  RankService.lua
  MarineMissionService.lua
  ArrestService.lua
  SalaryService.lua
  PvPRewardService.lua
src/client/Controllers/
  FactionSelectionController.lua
  RankHudController.lua
  WantedPosterController.lua
  MarineMissionController.lua
```

Données persistantes recommandées : `Faction`, `Bounty`, `Honor`, `CareerBounty`, `CareerHonor`, `Rank`, `LastFactionChange`, `LastSalaryGrant`, `PvPRewardHistory`, `ArrestHistory`, `IslandLiberationHistory`, `FactionMissions`. Les grades sont recalculés depuis les seuils de configuration, et non acceptés tels quels depuis une requête client. **Conserver l'architecture Rojo existante** et adapter les noms de fichiers au schéma réellement présent.

### 18 bis.13 Critères de validation et ordre d'implémentation

1. Choix de faction avant le spawn, sauvegardé et visible sur le personnage.
2. Deux tutoriels : premier navire et première conquête pour Pirate ; premier navire et première patrouille pour Marine.
3. Un Pirate peut capturer et exploiter une île ; un Marine peut la libérer sans accéder à sa gestion économique.
4. Les Pirates gagnent une prime ; les Marines gagnent de l'honneur et une solde active.
5. Victoires PvP et arrestations récompensées selon la force réelle de la cible ; anti-farm vérifié.
6. Grades, titres et bonus cohérents pour les deux factions ; plafond strict de 5 Md.
7. Les récompenses restent correctes après mort, changement de serveur, déconnexion et reconnexion.
8. Les joueurs faibles et les territoires hors ligne sont protégés contre les abus.
9. Tests multijoueurs à plusieurs niveaux de puissance, simulations de farm, et vérification du temps nécessaire pour atteindre les hauts grades.

---

## 18 ter. Carte maritime originale : archipel, biomes et progression

**Objectif artistique :** s'inspirer de la lisibilité de la carte de référence (îles distinctes, silhouettes reconnaissables, mer bleue, ambiance colorée) **sans copier** ses formes, bâtiments, positions ou illustrations. Construire une vraie carte Roblox 3D avec reliefs, côtes, végétation, ports, villages et espaces constructibles. La carte de référence est une inspiration visuelle, pas un asset à importer.

### Disposition générale

- **Au centre : Grand Port**, île neutre sûre, très identifiable, contenant spawn, boutiques d'armes/armures/fruits, marché, panneaux de missions, quartier général Marine, guilde des Pirates, chantier naval, embarcadères et tutoriel. Aucun combat PvP dans la zone protégée.
- **Première couronne (débutants) :** 4 îles accessibles rapidement en petit navire ; faible défense, ressources élémentaires et espaces de construction simples.
- **Deuxième couronne (intermédiaire) :** 5 îles à thèmes, avec défenses plus complexes, routes maritimes exposées et ressources spécialisées.
- **Troisième couronne (avancée) :** 4 îles dangereuses, conquêtes difficiles, boss, ports fortifiés et bonus puissants.
- **Îles événementielles :** apparaissent selon une saison ou un événement, sans empêcher l'accès aux zones de départ.
- Les îles doivent être **réellement éloignées**, avec un trajet en navire intéressant mais pas pénible ; ajuster les distances après tests. Afficher la carte, la position du joueur, la difficulté et les ports disponibles. Les distances et le nombre final d'îles sont configurables.

### Catalogue initial d'îles (13 îles conquérables + hub)

| Zone | Île | Identité visuelle | Bonus de propriété | Défi principal |
|---|---|---|---|---|
| Hub | Grand Port | cité portuaire, phare, marchés, docks | aucun bonus de conquête ; services publics | zone sûre |
| Débutant | Île des Moissons | champs en terrasses, moulins | +15 % nourriture | petites garnisons |
| Débutant | Île des Pins | forêt dense, scieries | +15 % bois | sentiers étroits |
| Débutant | Île des Échanges | village marchand, quais | +12 % revenus commerciaux | contrebandiers PNJ |
| Débutant | Île des Roches | falaises, carrière | +15 % pierre | tours sur relief |
| Intermédiaire | Île des Forges | hauts fourneaux, mines | +15 % fer et métal | défenses industrielles |
| Intermédiaire | Île des Vents | collines, moulins, port aérien décoratif | +10 % vitesse de navigation locale | vents et patrouilles |
| Intermédiaire | Île Corallienne | récifs, lagons | +20 % pêche | navigation dans les récifs |
| Intermédiaire | Île des Remparts | forteresse en pierre | +12 % efficacité des tours | siège fortifié |
| Intermédiaire | Île des Brumes | marais, ruines, brouillard | +10 % reconnaissance furtive | visibilité limitée |
| Avancé | Île du Volcan | lave, roche noire | +15 % forge d'armes | zones brûlantes et boss |
| Avancé | Île des Tempêtes | côte escarpée, orages | +12 % dégâts des défenses côtières | tempêtes et flotte hostile |
| Avancé | Île des Anciens | temples, jardins suspendus | +12 % vitesse de recherche | énigmes et gardiens |
| Avancé | Île du Trône | citadelle monumentale | +10 % moral des troupes de l'empire | siège de haut niveau |

**Règle :** chaque bonus doit être unique ou offrir un intérêt tactique clair ; les bonus cumulés de plusieurs îles sont plafonnés pour éviter une économie exponentielle. L'île capturée dispose d'emplacements constructibles pour champs, tavernes, casernes, entrepôts, ateliers, ports et tours. Les Marines peuvent reprendre/libérer les territoires mais **ne gèrent pas** une économie privée de bâtiments ; leurs victoires apportent honneur, solde de mission et contrôle temporaire au profit de la faction.

### Confort de navigation

- Navire de départ gratuit, vitesse correcte, commandes simples, indication de destination et possibilité de retour au hub après un délai hors combat.
- Mini-carte, carte du monde zoomable, filtre « débutant/intermédiaire/avancé », propriétaire et bonus de chaque île.
- Port d'arrivée clair, eau navigable, récifs signalés, pas de voyages obligatoires de 15 minutes entre îles proches.
- Streaming et chargement progressif des décors pour préserver les performances sur mobile.

---

## 18 quater. Armes : six standards et une premium

**Six armes non premium** couvrant plusieurs raretés, avec styles distincts et obtention par boutique, progression ou quêtes. Les prix sont des **hypothèses d'équilibrage** en monnaie de jeu (Berrys), à tester selon le revenu réel d'un débutant.

| Arme | Rareté | Style / compétence simple à développer | Obtention cible |
|---|---|---|---|
| Sabre du Marin | Commune | enchaînement de 3 coups, parade | boutique, **2 000 Berrys** |
| Masse du Dock | Peu commune | coup lent, repousse l'ennemi | boutique, **12 000 Berrys** |
| Deux Lames du Vent | Peu commune | coups rapides, courte ruée | quête « Gardien du port » + **25 000 Berrys** |
| Lance des Marées | Rare | allonge supérieure, attaque circulaire | quête de l'Île Corallienne + **90 000 Berrys** |
| Lame du Bastion | Légendaire | parade renforcée, contre-attaque | quête de siège de l'Île des Remparts + **350 000 Berrys** |
| Triple Lame du Trône | Mythique | combo exigeant, attaque spéciale à recharge longue | chaîne de quêtes difficiles + boss de l'Île du Trône + **1 500 000 Berrys** |

**Septième arme, premium : Lame de l'Aurore.** Apparence spectaculaire, traînée lumineuse et animations exclusives. Vendue via une offre Roblox clairement annoncée, **mais équilibrée comme une arme Rare**, sans domination statistique sur les armes légendaires/mythiques gagnées en jouant. Proposer idéalement une voie d'obtention alternative longue ou une version purement cosmétique pour limiter le pay-to-win. Aucun prix en Robux n'est fixé avant la politique de monétisation.

### Principes des armes

- Chaque arme possède dégâts, vitesse, portée, coût, rareté, animations, effets, recharge et prérequis, définis dans `WeaponConfig`.
- La puissance dépend aussi de la maîtrise du joueur ; la rareté ne signifie pas « victoire automatique ».
- Les quêtes ont des étapes visibles, des objectifs vérifiés côté serveur, une récompense non duplicable et un journal de progression.
- Les armes achetées ou débloquées sont sauvegardées. Le serveur valide coups, portée, dégâts et cooldowns.
- Prévoir une boutique d'armes au Grand Port, et des forgerons spécialisés sur certaines îles.

---

## 18 quinquies. Huit fruits : pouvoirs accessibles, raretés et équilibrage

**Huit fruits au lancement**, volontairement choisis pour être réalisables sans systèmes de transformations géantes ou physiques complexes. Les noms ci-dessous sont des noms de travail originaux inspirés de grandes familles de pouvoirs ; les pouvoirs, modèles et icônes définitifs doivent être originaux.

| Fruit | Rareté | Pouvoir principal simple | Prix fixe au marché (Berrys) |
|---|---|---|---:|
| Fruit du Bond | Commun | saut renforcé, petite impulsion | 60 000 |
| Fruit de la Brume | Commun | écran de fumée court | 75 000 |
| Fruit de la Pierre | Peu commun | projectile rocheux et armure temporaire | 160 000 |
| Fruit du Givre | Peu commun | projectile glacé et ralentissement | 220 000 |
| Fruit des Flammes | Rare | boule de feu et zone brûlante courte | 550 000 |
| Fruit de la Foudre | Rare | éclair ciblé et dash court | 750 000 |
| Fruit de la Gravité | Légendaire | attraction locale et onde de choc | 1 800 000 |
| Fruit du Phénix | Mythique | soin temporaire, dash aérien limité et aura de feu | 4 000 000 |

Les huit fruits ont chacun 2 à 3 compétences maximum pour la première version, avec une capacité de base utilisable dès l'obtention. Les compétences supplémentaires se débloquent par maîtrise. Les effets doivent être légers pour PC et mobile. **Pas de vol infini, d'invulnérabilité permanente ou de destruction totale d'île.** Les coûts et compétences sont à ajuster après tests.

### Marché permanent : réassort toutes les 4 heures

- Marchand fixe dans le Grand Port. Son **stock global** est régénéré à des horaires serveur de référence : **00:00, 04:00, 08:00, 12:00, 16:00, 20:00 UTC**. Afficher un compte à rebours selon l'heure du serveur, pas l'horloge locale du joueur.
- À chaque réassort, chaque fruit a une probabilité **indépendante** d'être disponible. Propositions initiales : Bond 75 %, Brume 70 %, Pierre 50 %, Givre 45 %, Flammes 22 %, Foudre 16 %, Gravité 5 %, Phénix 1 %. Le marché peut donc présenter plusieurs fruits ou aucun fruit rare.
- Le stock et les prix sont validés côté serveur. Pour une expérience équitable, utiliser un stock **commun à tous les serveurs** pour la sélection, avec disponibilité personnelle (un achat autorisé par joueur et par rotation, par fruit) plutôt qu'un stock de 1 exemplaire capturé par le premier connecté.
- Afficher les fruits disponibles, leur rareté, leur prix, leur description et le temps avant le prochain réassort. Les fruits indisponibles restent visibles avec la mention « Hors stock ».
- Les prix doivent nécessiter de jouer : viser environ **1 à 3 heures** pour accéder au premier fruit commun dans une progression normale, à ajuster avec des tests d'économie ; les fruits rares nécessitent nettement plus de temps. Aucun achat gratuit au premier spawn.

### Vendeur itinérant : 15 minutes toutes les heures

- Un **Vendeur de fruits itinérant** apparaît à un emplacement indiqué sur la carte, **au début de chaque heure UTC** (par exemple 10:00–10:15, puis 11:00–11:15), et disparaît après 15 minutes. Il est présent dans chaque serveur pendant cette fenêtre, avec annonces 5 minutes avant et au moment de son arrivée.
- Il vend des **tirages aléatoires (gacha) de fruits** contre une grosse somme en Berrys, par exemple **125 000 Berrys par tirage** pour une première proposition à tester. Un tirage donne **toujours un fruit** ; les fruits communs sont fréquents et les puissants sont très rares.
- Table de probabilité initiale **par tirage** : Commun 60 %, Peu commun 28 %, Rare 10 %, Légendaire 1,8 %, Mythique 0,2 %. Au sein d'une rareté, les fruits disponibles se partagent la probabilité à parts égales (modifiable dans la configuration). **Total : 100 %.** Le gacha est indépendant du stock du marché.
- Pour éviter de tout obtenir trop rapidement : coût élevé, limite de **2 tirages par apparition et par joueur**, aucun reroll gratuit illimité. Afficher les probabilités exactes **avant** chaque tirage. Envisager une protection contre les doublons ou une conversion en fragments, à définir et tester.
- Le tirage, la déduction d'argent, l'attribution du fruit et les limites sont effectués **atomiquement côté serveur**. Les limites persistent pendant toute la fenêtre horaire, même si le joueur change de serveur.
- Aucun paiement Robux n'est prévu pour ce gacha. Si une monétisation est ajoutée ultérieurement, vérifier les règles Roblox applicables aux objets aléatoires payants, à l'affichage des probabilités et aux restrictions régionales avant déploiement.

### Possession et utilisation des fruits

- L’achat ou le tirage attribue un fruit à sécuriser dans le sac si une place existe ; tout fruit tenu en main et non sécurisé est perdu à la mort ou à la déconnexion. Voir section 18 octies.
- **Un seul fruit actif à la fois**. Les autres sont conservés dans l'inventaire selon la capacité autorisée. Ne pas détruire un fruit rare lors d'un changement sans avertissement explicite.
- Compétences, dégâts, durée, énergie et cooldowns vérifiés par le serveur ; les races et équipements peuvent créer des synergies **plafonnées**.
- Fruits et armes doivent être utiles aussi en PvE, sans supprimer le rôle central des troupes, des navires et de la stratégie économique des Pirates.

### Exemple de progression débutant

1. Le joueur choisit race et faction, arrive au Grand Port, reçoit son navire de départ et une arme de base ; **aucun fruit gratuit**.
2. Il termine les missions de découverte, rejoint une première île et gagne ses premiers Berrys.
3. Pirate : il construit champs, taverne, entrepôt et défenses ; Marine : il effectue des patrouilles, missions et arrestations pour recevoir sa solde et ses récompenses.
4. Après une vraie période de jeu, il peut acheter son premier fruit commun **s'il est en stock**, ou économiser pour tenter le vendeur itinérant.
5. Les armes de quête, les fruits rares et les îles difficiles constituent des objectifs de moyen et long terme.

---

## 18 sexies. Intégration technique, UX et critères de validation

**Nouveaux modules à prévoir :** `WorldMapConfig`, `WeaponConfig`, `FruitConfig`, `FruitMarketConfig`, `QuestConfig`, `MapNavigationService`, `WeaponService`, `FruitService`, `FruitMarketService`, `QuestService`, `WorldMapController`, `WeaponShopController`, `FruitMarketController` et `FruitVendorController`. Conserver les services existants lorsqu'ils remplissent déjà une partie de ces fonctions.

**Synchronisation :** horloge serveur UTC, rotation de marché partagée entre serveurs via stockage persistant / mécanisme de synchronisation adapté ; ne pas dépendre de l'horloge du client. Sauvegarder achats, inventaires, quêtes et tirages. Prévoir reprise après crash, redémarrage, déconnexion et double clic. Ne pas faire confiance au client pour les prix, chances, stocks ou dégâts.

**Interface débutant :** une seule mission principale affichée, marqueur vers le port, étiquettes de difficulté sur les îles, menus de boutiques avec prix et rareté, comparaison simple des armes, description courte des fruits, minuteur de stock, minuteur d'arrivée du vendeur, bouton « Détails » pour les probabilités. Ne pas montrer tous les systèmes simultanément.

**Tests obligatoires :** 100 % des probabilités par gacha ; tirage indépendant et sécurisé ; stock rafraîchi à 4 h UTC ; vendeur présent exactement 15 minutes par heure ; limite par joueur respectée après reconnexion ; pas de perte d'argent sans récompense ; quête non répétable si prévu ; îles accessibles en bateau ; bonus d'île correctement appliqués et plafonnés ; joueur débutant capable d'obtenir son premier fruit après progression, mais pas dès le spawn ; absence d'avantage premium écrasant.

---

## 18 septies. Équipages pirates, alliances, dégâts alliés et îles collectives

> **Statut : fonctionnalité cible à développer, pas encore confirmée dans le prototype.** Cette section complète les règles des factions, de la conquête et de l'économie sans les remplacer.

### 18 septies.1 Règles de dégâts : amis, ennemis et zones protégées

Le **serveur** décide si une attaque peut infliger des dégâts, avant de calculer les bonus de race, de fruit, d'arme ou de grade. Les règles s'appliquent aux coups, projectiles, explosions, attaques de zone, dégâts persistants, tourelles, navires et unités contrôlées. Les PNJ hostiles restent attaquables selon leur camp ; les règles de protection entre joueurs ne doivent pas rendre tous les PNJ invulnérables.

| Attaquant → cible | Dégâts PvP | Règle |
|---|---|---|
| Marine → Marine | **Non** | Tous les Marines sont alliés par défaut, même sans escouade |
| Pirate → Pirate du **même équipage** | **Non** | Protection automatique, y compris entre leurs unités et défenses |
| Pirate → Pirate d'un **équipage allié** | **Non** | Alliance active et réciproque |
| Pirate → Pirate **allié individuel** | **Non** | Alliance personnelle active et réciproque |
| Pirate → Pirate sans lien | **Oui**, en zone PvP | Les protections de niveau, de spawn et de siège s'appliquent |
| Marine → Pirate | **Oui**, en zone PvP | Chasse aux pirates et libération des îles |
| Pirate → Marine | **Oui**, en zone PvP | Combat contre les forces de l'ordre |
| N'importe qui → joueur dans le hub central | **Non** | Zone neutre sécurisée, sans exception |

**Priorité de vérification :** 1) zone sûre, 2) protection temporaire de spawn/nouveau joueur, 3) même joueur ou même Marine, 4) même équipage, 5) alliance réciproque, 6) règles de guerre/siège et PvP, 7) autorisation éventuelle des dégâts. Le résultat est recalculé au moment de l'impact : un projectile déjà lancé ne doit pas contourner une alliance fraîchement acceptée. Les attaques de zone doivent filtrer chaque cible individuellement. Une attaque bloquée ne déclenche ni dégâts, ni statut négatif, ni vol de vie, ni prime/honneur, ni destruction de bâtiment.

**Choix de conception :** les alliances entre factions opposées ne sont pas permises dans le système initial : les Marines forment une faction commune et les Pirates s'allient entre eux. Les règles de coopération scénarisée Marine/Pirate, si ajoutées plus tard, devront être définies explicitement.

### 18 septies.2 Créer et gérer un équipage pirate

Un Pirate peut créer un **équipage persistant** depuis un menu simple. Il choisit un nom, un emblème/drapeau et invite des joueurs Pirates. Le chef peut nommer des officiers, accepter ou exclure des membres et gérer les autorisations. Les équipages sont réservés aux Pirates ; les Marines peuvent former des **escouades** pour les missions, sans économie d'îles partagée.

- **Chef :** définit le drapeau, invite/exclut, gère les officiers, diplomatie et règles de propriété.
- **Officiers :** invitations, défense, gestion des garnisons et constructions autorisées par le chef.
- **Membres :** participent aux captures, aux combats, à l'exploitation et aux revenus collectifs.
- **Recrues :** accès restreint jusqu'à validation ; ne peuvent pas vider les stocks ou retirer les bâtiments.

Un joueur ne peut appartenir qu'à **un seul équipage** à la fois. Limite initiale proposée : **10 membres** (configurable). L'équipage a un identifiant serveur permanent, distinct de son nom et du nom du chef. Les noms et emblèmes passent par les règles de modération Roblox. La dissolution et le changement de chef exigent une confirmation et des règles de succession pour les îles collectives.

### 18 septies.3 Drapeau d'équipage et propriété des îles

Après une conquête, un Pirate peut choisir de poser **son drapeau personnel** ou le **drapeau de son équipage** sur le point de capture autorisé. Un drapeau collectif ne peut être posé que par un membre ayant la permission, et uniquement après une capture validée côté serveur.

| Type d'île | Propriétaire enregistré | Construction | Revenus |
|---|---|---|---|
| Personnelle | `PlayerUserId` | Propriétaire et permissions explicites | Propriétaire uniquement |
| D'équipage | `CrewId` | Membres autorisés par leur rôle | Partagés entre membres éligibles, avec bonus |
| Alliance | **Aucune propriété commune** | Chaque propriétaire conserve ses droits | **Aucun partage** |

L'équipage peut contrôler **plusieurs îles**. Toutes les îles d'équipage sont visibles sur une carte commune ; les membres peuvent contribuer aux champs, bars, ports, casernes, entrepôts et défenses. Les garnisons de l'équipage ne blessent jamais les membres ni les alliés. Un membre qui quitte l'équipage **ne conserve pas de droits** sur les îles collectives ; les bâtiments et ressources restent au `CrewId`. Une île personnelle ne devient pas collective sans confirmation du propriétaire. Pour éviter le vol, aucune conversion automatique à l'entrée ou à la sortie d'un équipage.

**Gestion hors ligne :** les défenses automatiques restent actives selon les règles de simulation du serveur ; les revenus sont comptabilisés avec des plafonds et une persistance sécurisée. La déconnexion du chef ne dissout pas l'équipage. Prévoir une succession si le chef est inactif durablement.

### 18 septies.4 Revenus collectifs : partage équitable + petit bonus

Les revenus économiques des **îles portant le drapeau de l'équipage** sont mutualisés, puis répartis à parts égales entre les membres éligibles. Pour que jouer en groupe soit intéressant, le revenu brut de ces îles reçoit un **bonus coopératif de +10 %**, indépendant du nombre de membres (valeur initiale à équilibrer). **Les revenus des îles personnelles ne sont jamais partagés.**

Formule par période de versement :

```text
R = somme des revenus nets des îles d'équipage
    (production - entretien - coûts de fonctionnement)
B = 0,10  (bonus collectif de 10 %)
N = nombre de membres éligibles, N >= 1
Montant total distribué = max(0, R) × (1 + B)
Part par membre = Montant total distribué / N
```

**Exemple :** trois Pirates partagent deux îles rapportant **3 000 Berrys nets** pendant une période. Bonus collectif **+300**, soit **3 300 Berrys** à répartir : **1 100 Berrys par membre**. Sans équipage, le propriétaire d'une île personnelle conserve 100 % de ses revenus, mais ne reçoit **aucun bonus coopératif**. Le bonus ne s'applique pas aux primes PvP, récompenses de quêtes, achats, objets ou transferts de joueurs.

**Éligibilité anti-abus :** la répartition s'effectue entre les membres actifs selon une règle claire (par exemple présence en jeu ou participation récente et vérifiée, avec période de grâce). Les membres hors ligne peuvent recevoir une part plafonnée dans une réserve à réclamer si la conception le prévoit ; cette règle doit être visible dans le menu. Le chef ne peut pas s'attribuer une part supplémentaire cachée. Un nouveau membre ne reçoit pas rétroactivement les revenus antérieurs à son adhésion. Les montants sont arrondis et les reliquats comptabilisés dans une réserve d'équipage pour éviter de créer ou perdre de l'argent.

**Ressources physiques :** nourriture, bois, pierre, minerai et munitions produits sur les îles collectives vont dans des **stocks d'équipage** avec permissions de retrait et journal des opérations. Ils ne sont pas convertis automatiquement en Berrys ; le partage monétaire concerne uniquement les revenus économiques nets. Les dépenses de défense et d'entretien sont déduites **avant** le bonus et le partage.

### 18 septies.5 Alliances : coopération sans fusion des économies

Une **alliance** est un accord réciproque entre deux Pirates, entre un Pirate et un équipage (si le chef et les permissions l'autorisent), ou entre deux équipages. Elle est pensée pour les joueurs plus occasionnels qui veulent **jouer côte à côte sans renoncer à leur indépendance**.

Une alliance permet :

- **Zéro dégât allié** entre tous les membres concernés, y compris leurs troupes, navires et défenses.
- Voir les alliés sur la carte et distinguer leurs drapeaux.
- Défendre volontairement les territoires alliés et voyager ensemble.
- Envoyer des invitations, demandes d'aide et marqueurs de carte.
- Rester propriétaire de ses îles et gérer librement ses bâtiments.

Une alliance **ne permet pas** :

- de partager automatiquement l'argent, les revenus passifs ou les stocks ;
- de construire, retirer des ressources ou déplacer des garnisons sur l'île d'un allié sans permission séparée ;
- de transférer automatiquement une île à un allié ;
- de gagner prime ou honneur en simulant un combat entre alliés.

**Exemple :** deux joueurs ont chacun une île personnelle et concluent une alliance. Ils peuvent repousser ensemble une attaque et leurs canons ne se tirent pas dessus, mais chacun conserve **100 % de ses revenus**, ses ressources et ses décisions. Deux équipages alliés gardent également **leurs drapeaux, leurs stocks et leurs comptes séparés**.

### 18 septies.6 Diplomatie, rupture et prévention des abus

Les alliances doivent être **acceptées des deux côtés** ; pas de protection par simple demande envoyée. Un joueur peut refuser, bloquer ou quitter une alliance. Pour éviter les trahisons instantanées et les abus de protection :

1. Une rupture est annoncée aux deux parties.
2. Un **préavis de non-agression de 5 minutes** s'applique avant que les dégâts PvP entre anciens alliés redeviennent possibles (valeur configurable).
3. Impossible de déclarer/rompre une alliance au milieu d'un siège pour changer instantanément le résultat ; verrouiller l'état diplomatique pour la durée de l'engagement.
4. Les îles et revenus ne changent pas de propriétaire lors d'une rupture.
5. Une alliance n'empêche pas les PNJ ennemis d'attaquer et n'accorde pas l'immunité universelle.
6. Limiter les alliances actives (proposition : **3 par équipage** et **3 par joueur solo**) pour éviter un serveur entier invulnérable.

Les membres d'un équipage sont automatiquement alliés entre eux et ne peuvent pas se déclarer la guerre à l'intérieur du groupe. Les Marines sont déjà protégés entre eux et n'ont pas besoin d'une alliance supplémentaire.

### 18 septies.7 Interface et tutoriel : simplicité d'abord

Ajouter un onglet **Social** avec trois sous-menus : **Équipage**, **Alliances**, **Drapeaux**. Afficher clairement : « Même équipage = pas de dégâts + revenus des îles collectives partagés » et « Alliance = pas de dégâts, mais chacun garde son argent ».

Après la première conquête pirate, proposer deux grands choix :

```text
[ Drapeau personnel ]        [ Drapeau d'équipage ]
Je garde mes revenus.        Nous partageons les revenus
Je gère mon île.             avec +10 % de bonus collectif.
```

Ne pas forcer un joueur débutant à créer un équipage. Montrer un symbole **allié** au-dessus des personnages protégés et une indication « dégâts alliés désactivés » quand une attaque est bloquée, sans spam de notifications. Le menu d'île indique son propriétaire, son drapeau, ses revenus nets, sa garnison et les permissions du joueur. Les règles d'éligibilité au partage et la date du prochain versement doivent être visibles.

### 18 septies.8 Architecture Rojo, sauvegarde et sécurité

Configurations et services à **ajouter** (noms proposés, à adapter au projet réel) :

```text
src/shared/Config/
  CrewConfig.lua
  AllianceConfig.lua
  FriendlyFireConfig.lua
  CrewEconomyConfig.lua
src/server/Services/
  CrewService.lua
  AllianceService.lua
  DamagePermissionService.lua
  CrewIslandService.lua
  CrewRevenueService.lua
src/client/Controllers/
  CrewController.lua
  AllianceController.lua
  FlagController.lua
```

Données persistantes minimales : `CrewId`, `CrewRole`, `CrewMembers`, `CrewFlag`, `CrewOwnedIslands`, `CrewResourceStorage`, `CrewTreasury`, `CrewRevenueLedger`, `AllianceIds`, `AllianceStatus`, `IslandOwnerType`, `IslandOwnerId`, `DiplomacyCooldowns`. Utiliser des identifiants stables, des écritures idempotentes, des transactions protégées contre les doubles versements et des mécanismes de synchronisation inter-serveurs adaptés à Roblox. Les permissions, le propriétaire de l'île, les alliances, les dégâts et les revenus sont **toujours vérifiés par le serveur**. Un RemoteEvent client ne peut jamais déclarer « je suis allié », « j'ai posé un drapeau » ou « verse-moi la caisse » sans validation.

**Important :** une protection contre les dégâts PvP doit être appliquée à **toutes les sources de dégâts**, y compris les effets différés et les bâtiments défensifs, et ne doit pas bloquer les dégâts environnementaux (chute, noyade, pièges neutres) sauf règle explicite.

### 18 septies.9 Tests d'acceptation obligatoires

- [ ] Deux Marines ne peuvent pas se blesser, même avec une explosion ou une tourelle.
- [ ] Deux Pirates d'un même équipage ne peuvent pas se blesser ; deux Pirates ennemis le peuvent dans les zones autorisées.
- [ ] Deux alliés ne se blessent pas, mais ne partagent ni argent ni ressources.
- [ ] Un drapeau personnel laisse les revenus au propriétaire ; un drapeau d'équipage partage uniquement les revenus des îles collectives.
- [ ] Trois membres reçoivent chacun 1 100 Berrys pour 3 000 Berrys nets et +10 % de bonus, sans double versement.
- [ ] Un membre qui quitte l'équipage perd l'accès aux îles et stocks collectifs, sans voler les bâtiments.
- [ ] Les garnisons, canons, navires et attaques de zone respectent les mêmes relations d'amitié.
- [ ] Les alliances et équipages persistent après reconnexion et restent cohérents entre serveurs.
- [ ] Une rupture d'alliance ne permet pas de tuer instantanément un ancien allié.
- [ ] Les protections n'accordent aucun gain de prime/honneur sur des victimes alliées.
- [ ] Les Marines conservent leur gameplay de combat et de solde, sans gestion d'îles économiques collectives.

---

## 18 octies. Mort, déconnexion, stockage des fruits et propriété temporaire

### 18 octies.1 Deux couches de progression

- **Progression permanente :** personnage, race, faction, Berrys, niveau, prime/honneur, Haki, armes, armures, équipements, fruits **rangés dans le sac**, capacités de stockage et quêtes permanentes. Elle survit à la mort et à la déconnexion, sous réserve des règles explicites ci-dessous.
- **Progression de session :** îles conquises, drapeaux, bâtiments posés sur les îles, troupes affectées, stocks de l'île et production de l'île. Elle existe uniquement dans la session serveur en cours. Quitter le serveur met fin à la possession personnelle ; si c'est une île d'équipage, elle reste uniquement tant qu'un membre de l'équipage est encore présent sur ce serveur. Le dernier départ libère les îles. Une mort **ne fait pas perdre les îles** si le joueur reste connecté.

**Interdiction d'ambiguïté :** le jeu ne sauvegarde **pas** les îles, leurs bâtiments, leurs garnisons ou leurs revenus pour les restituer à la prochaine connexion. Les joueurs peuvent conserver leurs ressources personnelles déjà encaissées, pas les stocks laissés dans une île abandonnée.

### 18 octies.2 Fruits : sac sécurisé contre fruit tenu

Le joueur peut obtenir un fruit par le marché (réassort toutes les 4 h), le vendeur itinérant (15 min par heure), une récompense autorisée ou un échange sécurisé si cette fonction est ajoutée.

| Situation | Fruit dans le sac sécurisé | Fruit dans la main (objet physique non sécurisé) |
|---|---|---|
| Mort du personnage | **Conservé** | **Perdu** |
| Déconnexion / changement de serveur | **Conservé** | **Perdu** |
| Reconnexion | **Retrouvé dans le sac** | **Absent** |
| Équipement d'une arme/armure | Sans effet | Sans effet |

**Capacité de base : 1 exemplaire de chaque type de fruit**, pas un seul fruit au total. Exemple : 1 Givre + 1 Flammes autorisés ; un deuxième Givre refusé tant que la capacité de ce type n'a pas été augmentée. Des passes premium de **stockage supplémentaire** peuvent autoriser plusieurs exemplaires d'un même fruit ; la capacité acquise persiste. Les capacités supplémentaires sont annoncées clairement dans le Shop. Elles n'augmentent pas les probabilités d'obtention des fruits.

**Flux d'achat/tirage :** montrer la capacité disponible avant de payer ; si l'achat est un fruit connu et que la place manque, refuser la transaction sans débiter le joueur. Pour un gacha aléatoire, afficher les règles de doublons et éviter toute perte silencieuse : si le fruit tiré ne peut pas être rangé, proposer une décision explicite (par exemple garder l'objet en main à ses risques, ou annuler selon une règle annoncée avant le tirage). Le joueur ne doit jamais croire qu'un fruit tenu est sauvegardé. Une confirmation est requise avant de sortir un fruit du sac si cette action le rend vulnérable.

**Fruit consommé/équipé :** distinguer le fruit **objet** de son **pouvoir appris**. Proposition : consommer un fruit transforme l'objet en pouvoir actif persistant (un seul pouvoir équipé) ; le fruit physique disparaît du sac. La mort n'efface pas le pouvoir appris. Changer de pouvoir demande une confirmation et applique les règles de remplacement prévues par la configuration. Cette proposition doit être validée avant l'implémentation pour éviter une perte d'objet injuste.

**Sécurité :** inventaire, objet tenu et suppression à la mort/déconnexion sont gérés exclusivement côté serveur ; sauvegarde transactionnelle, identifiants d'objets uniques, aucune duplication via reset, reconnexion rapide ou téléportation. En cas d'échec de DataStore, bloquer les transactions risquant une perte définitive et afficher une erreur claire.

### 18 octies.3 Expérience, niveaux et déblocages par prime / honneur

Il existe **deux progressions complémentaires** :

1. **Niveau / XP** : augmente par les quêtes, le combat, la navigation et les objectifs ; sert de prérequis d'accès aux zones, armes, missions et améliorations. Il ne remplace pas la prime/l'honneur.
2. **Prime Pirate / Honneur Marine** : augmente par les exploits PvP/PvE et les objectifs de faction ; détermine le **grade**, les bonus de puissance déjà prévus en section 18 bis et les **Hakis débloquables**. Les grades et seuils de 5 milliards restent inchangés.

Les Hakis ne sont pas simplement offerts : **atteindre le grade ouvre la quête d'apprentissage** auprès d'un maître PNJ ; réussir la quête déverrouille la compétence de manière permanente. La Marine a des équivalents d'honneur au même seuil afin d'éviter une faction désavantagée.

| Déblocage | Pirate : prime / grade requis | Marine : honneur / grade requis | Condition supplémentaire |
|---|---|---|---|
| Techniques de combat de base | 0 / Moussaillon | 0 / Recrue | Tutoriel initial |
| **Haki de l'Armement** | **5 M / Capitaine recherché** | **5 M / Premier maître** | Quête du maître d'Armement, niveau conseillé 25 |
| Armement renforcé | 100 M / Supernova redoutée | 100 M / Lieutenant | Défis de combat et maîtrise de l'Armement |
| **Haki de l'Observation** | **750 M / Grand Corsaire** | **750 M / Commodore** | Quête d'esquive, niveau conseillé 60 |
| Observation avancée | 2 Md / Grand Empereur | 2 Md / Amiral | Épreuves de perception et maîtrise |
| **Haki des Rois** (rare) | 3 Md / Seigneur des océans | 3 Md / Amiral de flotte | Quête d'exception + condition de mérite ; non automatique |
| Maîtrise ultime | 5 Md / Roi des Pirates | 5 Md / Amiral de flotte légendaire | Épreuve finale très difficile |

**Équilibrage :** les seuils sont volontairement longs. Les Hakis ont des coûts en énergie, des durées, des temps de recharge et des contre-mesures ; ils ne doivent pas écraser toute la stratégie d'îles. Les bonus de race, d'arme, de Haki et de grade sont soumis à des plafonds serveur. Les chiffres de niveau sont des propositions à tester. Une baisse éventuelle de prime/honneur ne retire pas une compétence déjà apprise, sauf règle annoncée et explicitement validée.

### 18 octies.4 Mini-menu radial / menu rapide

Un **petit bouton Menu** visible en jeu ouvre une roue de navigation inspirée du principe de la capture, mais avec une **identité visuelle originale**. Fonctionne à la souris, au tactile et à la manette. Le jeu est mis en arrière-plan sans masquer totalement la scène ; fermeture par Échap, bouton retour ou clic extérieur.

**Six entrées principales**, avec libellés et icônes très lisibles :

| Entrée | Contenu |
|---|---|
| **Inventaire** | Sac de fruits, armes, armures, équipements ; distinction « sécurisé » / « en main », capacité et doublons |
| **Progression** | Frise verticale ou horizontale de prime/honneur, grade actuel, prochain seuil, récompenses, Hakis, quêtes requises |
| **Shop** | Boutique cosmétique, passes premium et stockage supplémentaire ; prix et conditions explicites |
| **Équipage / Alliances** | Membres, drapeau, permissions, revenus partagés, alliés et statut de non-agression |
| **Carte / Îles** | Archipel, difficulté, bonus, îles actuellement contrôlées, état des garnisons et du port |
| **Paramètres** | Son, graphismes, commandes, accessibilité, effets et préférences d'interface |

**Frise de progression :** affiche les **19 grades de la faction** (voir section 18 bis), les seuils exacts, le titre, les bonus de dégâts/défense, les nouveaux Hakis et les quêtes accessibles. Mettre en évidence « Actuel », « Prochain », « Verrouillé » et « Débloqué ». Afficher la distance jusqu'au prochain grade et la progression en pourcentage **dans le palier courant**, pas sur 5 milliards (sinon les débuts sembleraient bloqués). Les récompenses majeures sont illustrées par des pictogrammes simples.

**Tutoriel progressif :** lors du premier lancement, expliquer uniquement : (1) où trouver l'inventaire, (2) où lire la prime/honneur et le prochain Haki, (3) où voir la carte et le port. Le reste se découvre au besoin, avec des infobulles et des notifications. Ne pas ouvrir de pop-up obligatoire à chaque progression.

### 18 octies.5 Services, données et tests

**Architecture proposée (à développer, pas encore implémentée) :** `InventoryService`, `FruitStorageService`, `ProgressionService`, `HakiService`, `SessionIslandService` et côté client `QuickMenuController`, `InventoryController`, `ProgressionController`. Configurations : `FruitStorageConfig`, `HakiConfig`, `RankUnlockConfig`, `QuickMenuConfig`. Réutiliser `DataService`, `IslandService`, les configs de fruits et les services de factions existants ; ne pas dupliquer leur logique.

**Tests obligatoires :**

1. Déconnexion Pirate solo : île libérée, mais argent, armes, armures, rang et fruit stocké conservés.
2. Déconnexion du chef d'équipage : l'île reste tant qu'un membre du même équipage est présent dans le serveur ; dernier membre parti = île libérée.
3. Mort : fruit tenu perdu, fruit stocké conservé, île conservée si joueur toujours connecté.
4. Deux exemplaires du même fruit : refus sans capacité premium ; autorisation si stockage supplémentaire disponible.
5. Achat et gacha sans place : pas de perte d'argent ni d'objet silencieuse.
6. Prime 5 M Pirate / honneur 5 M Marine : quête d'Armement visible ; Haki non accordé sans réussite.
7. Prime 750 M / honneur 750 M : quête d'Observation visible.
8. Frise : 19 grades, seuils, bonus, déblocages et progression exacte.
9. Mini-menu : navigation clavier, souris, tactile, manette ; ouverture/fermeture sans conflit avec les commandes de combat.
10. Réseau et sauvegarde : aucun client ne peut se donner un fruit, un Haki, un grade ou conserver une île d'un autre serveur.

---

## 19. Roadmap de réalisation — ordre recommandé

### Phase 0 — Fondations techniques

- [x] Projet Rojo, synchronisation, architecture client/serveur.
- [x] Services de base et génération d'îles prototype.
- [ ] Vérifier la sauvegarde en conditions réelles et les tests multijoueurs.

### Phase 1 — Hub central et voyage initial

- [ ] Concevoir l’archipel original avec hub et 13 îles à bonus, distances progressives et carte du monde.
- [ ] Développer les 6 armes standards, leurs raretés et les premières quêtes ; définir l’arme premium équilibrée.
- [ ] Implémenter les 8 fruits et leur interface de présentation.
- [ ] Préparer le marché (rotation UTC 4 h) et le vendeur itinérant (15 min chaque heure).

- [ ] Créer une île centrale lisible et accueillante.
- [ ] Placer les boutiques d'armes, d'armures et de fruits.
- [ ] Créer le port central.
- [ ] Fournir un navire de départ.
- [ ] Permettre de naviguer jusqu'à une île neutre.
- [ ] Ajouter les premières étapes du tutoriel.

### Phase 2 — Conquête et propriété

- [ ] Conserver/améliorer la capture prototype.
- [ ] Permettre le débarquement depuis un navire.
- [ ] Associer une île capturée au joueur.
- [ ] Afficher un menu de gestion après capture.
- [ ] Sauvegarder la progression.

### Phase 3 — Économie et ressources

- [ ] Argent, nourriture, bois, pierre, fer.
- [ ] Champs et fermes.
- [ ] Bars/tavernes et commerces.
- [ ] Mines, scieries, entrepôts.
- [ ] Production, consommation, bilans lisibles.
- [ ] Alertes de pénurie.

### Phase 4 — Construction et aménagement

- [ ] Menu de construction simple.
- [ ] Aperçu et placement des bâtiments.
- [ ] Coûts, délais, améliorations.
- [ ] Limites d'espace et spécialisation des îles.
- [ ] Sauvegarde de la disposition des bâtiments.

### Phase 5 — Troupes et défense autonome

- [ ] Casernes et recrutement.
- [ ] Consommation alimentaire des troupes.
- [ ] Bars pour repos et revenus.
- [ ] Garnisons avec ordres simples.
- [ ] Tours, murs et canons côtiers.
- [ ] Alertes d'attaque et protection quand le joueur est ailleurs.
- [ ] Définir explicitement les règles hors ligne.

### Phase 6 — Stratégie inter-îles

- [ ] Ports locaux.
- [ ] Transport de troupes et ressources.
- [ ] Vue globale de l'empire.
- [ ] Spécialisation économique/militaire.
- [ ] Routes de ravitaillement.
- [ ] Combats navals.

### Phase 7 — Progression avancée

- [ ] Arbre technologique.
- [ ] Armes et armures évolutives.
- [ ] Héros.
- [ ] Fruits et pouvoirs.
- [ ] Îles rares et objectifs avancés.

### Phase 8 — Multijoueur avancé

- [ ] PvP équilibré.
- [ ] Alliances et commerce.
- [ ] Sièges et conflits territoriaux.
- [ ] Protection des débutants et hors ligne.
- [ ] Classements.

### Phase 9 — Finition et contenu durable

- [ ] UI PC/mobile.
- [ ] Sons, animations et effets.
- [ ] Saisons, missions, événements.
- [ ] Optimisation et anti-exploit.
- [ ] Tests de charge et de sauvegarde.

## 20. Critères d'acceptation prioritaires

Une **première version vraiment représentative** d'OP Empire Wars est prête quand un nouveau joueur peut, sans aide extérieure :

1. Tirer et confirmer sa race (apparence, bonus, malus), choisir Pirate ou Marine, puis apparaître sur l'île centrale et identifier les trois boutiques.
2. Trouver le port et obtenir un navire.
3. Naviguer vers une île neutre.
4. Capturer cette île.
5. Ouvrir un menu de gestion compréhensible.
6. Construire un champ et produire de la nourriture.
7. Construire un bar et constater des revenus ainsi qu'un effet de repos sur les troupes.
8. Construire une caserne, recruter des soldats et les nourrir.
9. Installer une tour et affecter une garnison qui défend l'île pendant qu'il voyage ailleurs.
10. Consulter clairement les gains, consommations et réserves.
11. Quitter puis revenir en conservant sa progression permanente mais **sans ses îles de session**.
12. Repartir en navire pour conquérir une deuxième île.
13. Voir les îles sur une carte lisible, leurs bonus et leur difficulté.
14. Acheter une arme de départ et comprendre comment débloquer les armes de quête.
15. Voir le stock de fruits, le prochain réassort, les chances de tirage et l’arrivée du vendeur itinérant.
16. Obtenir son premier fruit uniquement après avoir suffisamment progressé et économisé.
17. Créer un équipage Pirate, poser son drapeau et vérifier le partage des revenus avec bonus.
18. Conclure une alliance sans partager les revenus et constater que les dégâts alliés sont désactivés.
19. Vérifier qu’aucun Marine ne peut blesser un autre Marine.
20. Quitter et revenir : perdre les îles, conserver les armes, armures, Berrys, niveau et fruits stockés.
21. Mourir ou quitter avec un fruit physique en main : perdre ce fruit, sans toucher aux fruits sécurisés.
22. Ouvrir le menu rapide, lire la frise des grades et consulter les quêtes de Haki débloquées par la prime/honneur.

## 21. Consignes pour toute future IA ou tout développeur

- **Ne jamais sauvegarder les îles comme possessions permanentes ; elles sont propres à la session.**
- **Respecter la distinction fruit sécurisé / fruit tenu et les déblocages de Haki par grade.**
- **Respecter le parcours central : sélection de race → choix Pirate/Marine → spawn au hub → boutiques → port → navire → conquête → gestion d'île → expansion.**
- Ne pas remplacer le gameplay par une simple succession de captures d'îles.
- Faire de la **gestion des ressources, des bâtiments, des troupes et des défenses** la mécanique centrale.
- Donner une vraie utilité aux **champs (nourriture)** et aux **bars/tavernes (revenus et repos)**.
- Permettre de défendre ses territoires **sans être physiquement sur place**, avec des règles hors ligne réalistes.
- Préserver la simplicité des premières minutes et révéler la profondeur stratégique progressivement.
- Réutiliser l'architecture Rojo existante ; ne pas réécrire les systèmes fonctionnels sans nécessité.
- Ajouter les systèmes par étapes testables, en validant la sauvegarde et la sécurité serveur.
- Ne pas affirmer qu'une fonctionnalité est terminée avant qu'elle ait été implémentée et testée.

---

**Résumé en une phrase :** OP Empire Wars est un jeu Roblox multijoueur dans lequel on tire d'abord une race parmi 10 (avec apparence, bonus et malus), puis on apparaît sur une île centrale avec des boutiques d'armes, d'armures et de fruits, on part du port en navire conquérir sa première île, puis on bâtit et gère un véritable empire en équilibrant économie, nourriture, repos des troupes, constructions, garnisons, défenses et expansion maritime — avec une prise en main très simple et une stratégie de plus en plus riche.


**Extension des critères d’acceptation :** vérifier également le choix Pirate/Marine, la progression prime/honneur, les arrestations, la solde active, la reprise d’îles et les bonus par grade décrits au chapitre 18 bis.
