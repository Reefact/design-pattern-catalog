# ADR-0045 | Démarrer chaque paquet à la version 1.0.0

🌍 🇬🇧 [English](0045-start-every-package-at-version-1-0-0.md) · 🇫🇷 Français (ce fichier)

**Statut :** Proposé
**Proposé :** 2026-10-09
**Décideurs :** Reefact

## Contexte

L'[ADR-0021](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.fr.md) fixe un versionnement
sémantique sur deux contrats et ajoute que les paquets **restent sous `1.0.0`** jusqu'à ce qu'aucun pattern
catalogué ne doive plus changer de catalogue : un pattern est dans `Idioms` parce qu'aucune œuvre ne le
revendique encore, et le jour où l'une le fait il change à la fois de namespace et de paquet.
`CONTRIBUTING.md` en tire la conséquence : sous `1.0.0`, son tableau s'applique d'un cran plus bas, un
changement cassant faisant monter le mineur et tout le reste le patch.

Rien n'a été publié, et la version est un espace réservé de développement.

L'[ADR-0044](0044-release-each-package-from-its-own-tag.fr.md) livre chaque paquet depuis son propre tag et
décide, pour un tag de `Core`, si chaque autre paquet prend un patch ou la majeure suivante. Sous la
convention `0.x`, cette décision aurait un sens différent selon la plage de versions, et le planificateur
devrait tenir un second tableau.

`Idioms` contient deux patterns. Le tableau de `CONTRIBUTING.md` classe déjà le déplacement d'un pattern entre
catalogues parmi les changements majeurs.

## Décision

La première livraison de chaque paquet est en `1.0.0`, et les paquets sont versionnés à partir de là avec le
tableau complet.

## Justification

Une version qui démarre à `1.0.0` veut dire la même chose pour chaque paquet dès le premier tag : un pas
majeur est cassant, un mineur est un ajout, un patch n'atteint aucun consommateur. La convention `0.x` fait
dépendre le sens d'un numéro du côté de `1.0.0` où il tombe, et le planificateur de l'ADR-0044 devrait
connaître les deux.

Le coût contre lequel l'ADR-0021 se gardait est réel et il est accepté : un pattern qui sort d'`Idioms` vers un
catalogue propre change de namespace et de paquet, et à partir de `1.0.0` c'est une version majeure d'`Idioms`
et du méta-paquet. C'était déjà un changement majeur dans le tableau ; ce qui change, c'est qu'il n'est plus
excusé par une version qui ne promettait rien. Deux patterns vivent dans `Idioms`, donc l'exposition est
petite aujourd'hui.

Ceci remplace l'ADR-0021 sur un seul point. Le versionnement sémantique sur ce qu'un consommateur compile et ce
qu'il relit tient, ainsi que tout ce que l'ADR-0021 argumente d'autre ; seule sa clause selon laquelle les
paquets restent sous `1.0.0` est remplacée.

## Alternatives envisagées

### Rester sous `1.0.0` jusqu'à ce que les catalogues cessent de bouger

La position de l'ADR-0021. Envisagée parce qu'elle dit honnêtement que le vocabulaire est jeune.

Rejetée parce que les règles de livraison porteraient alors deux sens pour un numéro, et que l'exposition
dont elle protège est de deux patterns dans `Idioms`.

### Démarrer à `1.0.0` pour `Core` et à `0.x` pour les catalogues

Envisagée parce que les catalogues sont la partie qui grandit encore.

Rejetée parce que la cascade les déplace avec `Core`, et que leurs numéros devraient franchir `1.0.0` à un
moment que rien dans le code ne marque.

## Conséquences

### Positives

* Une seule lecture de chaque numéro de version, pour chaque paquet, dès la première livraison.
* Le planificateur de livraison tient un seul tableau.

### Négatives

* Un pattern qui quitte `Idioms` est une version majeure d'`Idioms` et du méta-paquet.
* `CONTRIBUTING.md` ne porte plus le paragraphe `0.x`, et tant que ce record n'est pas accepté il contredit
  l'ADR-0021.

### Risques

* Un consommateur lit `1.0.0` comme la promesse que rien ne bougera. Le tableau dit ce qu'est un changement
  majeur, et un pattern qui quitte un catalogue en est un.

## Actions de suivi

* Décider si l'ADR-0021 est marqué comme remplacé, ou laissé tel quel avec ce record qui nomme la seule clause
  qu'il remplace.

## Références

* [ADR-0021](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.fr.md),
  [ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.fr.md),
  [ADR-0044](0044-release-each-package-from-its-own-tag.fr.md)
