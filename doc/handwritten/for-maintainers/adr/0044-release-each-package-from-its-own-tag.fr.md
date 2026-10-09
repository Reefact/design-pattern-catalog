# ADR-0044 | Livrer chaque paquet depuis son propre tag, avec cascade depuis Core

🌍 🇬🇧 [English](0044-release-each-package-from-its-own-tag.md) · 🇫🇷 Français (ce fichier)

**Statut :** Accepté
**Proposé :** 2026-10-09
**Accepté :** 2026-10-09
**Décideurs :** Reefact

## Contexte

**Rien n'est publié.** La version est un espace réservé de développement, un seul numéro pour tous les
paquets, tenu dans `build/Packaging.props`, et aucun workflow ne publie quoi que ce soit : la CI empaquette la
solution pour prouver qu'elle peut l'être, et s'arrête là.

Il y a quatorze paquets. `Core` porte le marqueur de base et est référencé par tous les catalogues. Douze
catalogues portent chacun une œuvre, indépendante des autres
([ADR-0027](0027-ship-one-independent-package-per-catalogued-work.fr.md)). Un méta-paquet ne contient aucun
code et référence les treize autres, pour qu'un consommateur qui veut tout installe un seul paquet.

L'ADR-0027 a choisi des paquets indépendants pour leur turbulence : un changement dans une œuvre ne doit pas
republier les autres. Il a aussi prescrit que **la première livraison les versionne en bloc**, parce que
relâcher plus tard est facile et resserrer plus tard ne l'est pas.

**Un changement dans `Core` atteint tous les paquets.** Ses règles de lecture décident de ce que chaque
annotation de chaque catalogue veut dire pour le lecteur d'un consommateur, et tous les catalogues en
dépendent. Un changement du gabarit du générateur ou de `Packaging.props` atteint lui aussi tous les paquets.

Le méta-paquet dépend de ses treize paquets à des versions exactes : il doit donc être republié chaque fois
que l'un d'eux l'est.

Qu'un changement soit cassant est un jugement sur ce qu'un consommateur compile et sur ce qu'il relit
([ADR-0021](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.fr.md)). Aucun outil ne le déduit.

## Décision

Un paquet est livré depuis un tag qui porte son nom et sa version : un tag de `Core` livre tous les paquets,
un tag de catalogue livre ce catalogue et le méta-paquet, et un tag du méta-paquet le livre seul.

## Justification

Le tag est le seul endroit où une livraison est énoncée : c'est donc la seule entrée. Une version tenue aussi
dans un fichier versionné serait une seconde affirmation de ce qui a été livré, libre de contredire la
première ; ici, les numéros des paquets qu'un tag ne nomme pas sont lus dans leurs propres derniers tags, et
nulle part ailleurs.

Des tags indépendants donnent la turbulence réduite pour laquelle l'ADR-0027 a été choisi : un nouveau pattern
dans un catalogue republie ce catalogue et le méta-paquet, pas douze paquets dont le contenu n'a pas changé.

Un tag de `Core` se propage parce qu'un changement de `Core` est un changement pour tout le monde. Ce que
devient chaque paquet suit le pas donné à `Core` : un pas majeur est cassant, et chaque paquet prend la
majeure suivante ; tout autre pas ne l'est pas, et chaque paquet prend le patch suivant. Le workflow ne peut
pas juger de la casse, mais le mainteneur le fait déjà en choisissant le numéro, et la cascade lit ce choix au
lieu de le demander deux fois. Un numéro qui n'est pas exactement un pas au-dessus du tag précédent de son
paquet est refusé, si bien qu'une faute de frappe ne passe pas pour une décision.

Le méta-paquet suit le niveau du pas qui l'a déclenché : un patch d'un catalogue est un patch du méta-paquet,
et un nouveau mineur est un mineur. Le tout premier tag d'un catalogue, qui ajoute une dépendance, est un
mineur.

La première livraison est un tag de `Core` en `1.0.0`. Aucun paquet n'a de version antérieure, donc la
cascade les livre tous en `1.0.0`, ce qui est le lot que demandait l'ADR-0027, obtenu sans mécanisme propre.
Les livraisons suivantes le relâchent, comme cet ADR le prévoyait.

La version est lue par projet, par nom de projet, dans un fichier que le planificateur écrit pour la
livraison. C'est ce qui fait qu'une référence de projet devienne une dépendance sur la version à laquelle ce
projet est livré ; une version globale unique donnerait à chaque dépendance le numéro du paquet en cours
d'empaquetage.

Un tag doit pointer un commit de `main`, et le workflow lance les tests avant d'empaqueter. Sans clé NuGet,
c'est une répétition à blanc : on peut donc l'exercer avant qu'une clé existe.

## Alternatives envisagées

### Un tag livre tout, à une seule version

Le lot de l'ADR-0027, conservé. Envisagé parce que c'est le plus simple à rendre correct et que le
planificateur serait trivial.

Rejeté comme règle permanente : un nouveau pattern dans un catalogue republierait les quatorze paquets, soit
la turbulence que la séparation des catalogues devait faire cesser. Il subsiste, en pratique, pour la
première livraison.

### Les versions dans un fichier versionné

Envisagé parce qu'une version peut alors être relue dans une pull request.

Rejeté parce que le fichier et le tag deviennent deux affirmations d'un même fait, et qu'un workflow de
livraison devrait vérifier qu'ils concordent. Le tag est de toute façon nécessaire.

### Un outil de versionnement piloté par les tags

Envisagé parce qu'il existe et qu'il est très utilisé.

Rejeté parce que la cascade a besoin de la version suivante de paquets que le tag ne nomme pas, ce qu'un outil
qui lit les tags de chaque projet ne sait pas calculer.

## Conséquences

### Positives

* Une livraison est un tag poussé.
* Un catalogue peut sortir sans les autres, et la première livraison les sort tout de même ensemble.
* Les versions sur nuget.org sont celles des tags ; rien d'autre ne les enregistre.

### Négatives

* Un changement dans `Core` republie les quatorze paquets, y compris ceux dont le contenu n'a pas changé.
* Le workflow crée des tags : il lui faut le droit d'écrire dans le dépôt.
* Quatorze préfixes de tag à connaître.

### Risques

* La décision cassant-ou-non est celle du mainteneur, et un mauvais numéro est livré. Le planificateur refuse
  un pas invalide, pas un pas erroné.
* Une publication qui échoue en cours de route laisse certains paquets publiés et aucun tag créé. Le workflow
  ignore un paquet déjà sur nuget.org : le relancer termine la livraison.
* Un catalogue ajouté après la première livraison n'a pas de tag. Le méta-paquet en dépend, donc aucun tag
  autre que `core-v…` ou le sien ne peut rien livrer tant qu'il n'en a pas ; le planificateur le dit.

## Actions de suivi

* Créer le secret `NUGET_API_KEY`, et vérifier que les identifiants `DesignPatternCatalog.` sont libres sur
  nuget.org, avant le premier tag.
* Mettre à jour la description et les étiquettes du méta-paquet, qui datent d'avant la plupart des catalogues.

## Références

* [ADR-0021](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.fr.md),
  [ADR-0027](0027-ship-one-independent-package-per-catalogued-work.fr.md),
  [ADR-0038](0038-name-the-packages-after-the-catalogue-rather-than-the-vendor.fr.md)
* [ADR-0045](0045-start-every-package-at-version-1-0-0.fr.md) — la version à laquelle démarre la première livraison
* `.github/workflows/release.yml`, `tools/release/plan.py`, et la section *Releasing* de `CONTRIBUTING.md`
