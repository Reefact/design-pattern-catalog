# ADR-0042 | Admettre un catalogue pour les patterns du mainteneur

🌍 🇬🇧 [English](0042-admit-a-catalogue-for-the-maintainers-own-patterns.md) · 🇫🇷 Français (ce fichier)

**Statut :** Proposé
**Proposé :** 2026-10-08
**Décideurs :** Reefact

## Contexte

Dix œuvres sont cataloguées, plus `Idioms` : **343 patterns, 619 rôles**. Chacune des dix est l'œuvre
de quelqu'un d'autre, publiée et lue en entier ou en partie ; `Idioms` tient les patterns qui ont une
source et pas de corpus propre
([ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.fr.md)), et a été gardé exempt de
« catalogues à entrée unique » à dessein.

Le 6 octobre 2026, le mainteneur a publié sur `reefact.net` un article, *Value Objects avancés en .NET*.
Il y décrit une manière de construire des value objects en .NET et nomme, parmi ses attributs, quatre
éléments que le catalogue ne sait pas exprimer aujourd'hui : la méthode de réhydratation, la méthode de
déshydratation et l'objet déshydraté qui franchit la frontière d'un value object, ainsi qu'un membre
ouvert à un seul collaborateur nommé. Le catalogue tient `ValueObject` deux fois — celui d'Evans, et celui
de Fowler dans *Patterns of Enterprise Application Architecture* — et aucun ne dit comment un value object
franchit une frontière ni qui peut appeler ce qu'il cache.

Quatre contraintes pèsent sur l'endroit où de tels patterns peuvent aller.

* Un pattern est tenu par chaque catalogue dont l'œuvre le présente comme sien
  ([ADR-0028](0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.fr.md)). Le livre d'Evans ne
  présente pas ces quatre-là : `DomainDrivenDesign` ne peut donc pas les tenir.
* Une relation ne franchit jamais un catalogue, chaque œuvre cataloguée étant un paquet indépendant
  ([ADR-0027](0027-ship-one-independent-package-per-catalogued-work.fr.md)). Un pattern admis dans un
  nouveau catalogue ne peut pas restreindre `ValueObject`.
* Les paquets sont nommés d'après le catalogue plutôt que l'éditeur
  ([ADR-0038](0038-name-the-packages-after-the-catalogue-rather-than-the-vendor.fr.md)).
* `Idioms` est l'endroit que l'ADR-0013 prévoit pour un pattern qui a une source et pas de catalogue
  propre. L'article n'est pas une simple ligne d'index : il porte, pour chacun des quatre, un problème,
  une solution et des participants nommés, le seuil que l'[ADR-0035](0035-index-the-pattern-language-and-require-a-write-up.fr.md)
  applique.

L'article n'est pas le dernier texte que le mainteneur écrira, et les attributs qu'il nomme ne sont pas
les seuls, utilisés au quotidien, qu'aucune œuvre cataloguée ne nomme. Le mainteneur a dit que le
catalogue devait tous les tenir.

## Décision

Un catalogue nommé `Reefact` tient les patterns que son mainteneur utilise et qu'aucune œuvre cataloguée
ne nomme, chacun entré avec le texte qui le présente — un article, un chapitre, une conférence — pour
référence.

## Justification

Le vide est réel et ne peut être comblé ailleurs. L'ADR-0028 tranche à qui il appartient : à l'œuvre qui
présente le pattern, et c'est ici celle du mainteneur. Les autres catalogues ne peuvent pas le prendre
sans mal l'attribuer, et une référence mal attribuée est la seule chose que la donnée ne peut pas se
permettre, puisque c'est la référence qui dit quel catalogue tient un pattern.

`Idioms` est la mauvaise étagère, pour la raison même qu'avance l'ADR-0013 pour son existence. Il répond
*aucune œuvre en particulier* ; ici il y a une œuvre, avec un titre, une date et un auteur, et les entrées
y renvoient. Les ranger sous `Idioms` ferait perdre la citation qui donne sa valeur à une entrée — l'argument
même de l'ADR-0036 pour Scoped Locking. Le souhait de l'ADR-0013 d'éviter les catalogues à entrée unique est
respecté dans l'esprit : celui-ci s'ouvre sur deux patterns et quatre rôles, et doit grandir, ce que peut
faire un catalogue nommé d'après un auteur sans que la question *de quel livre vient ceci* se pose à nouveau.

Le seuil d'admission reste là où l'ADR-0035 l'a mis. Une entrée exige une présentation écrite avec un
problème et une solution, parce que le résumé, les rôles et les assertions en sont tirés ; être quelque
chose que le mainteneur utilise ne suffit pas. C'est ce qui empêche le catalogue de devenir un fourre-tout.

Le nom suit l'instrument déjà employé pour `GangOfFour` et `Posa2` : le nom sous lequel l'œuvre est
connue de ceux qui la cherchent. Ici, l'auteur est l'œuvre. Cela s'accorde mal avec la raison pour laquelle
l'ADR-0038 refuse le nom de l'éditeur — une famille de paquets nommée d'après l'éditeur ne dit rien de leur
contenu — et c'est signalé sous *Risques* plutôt qu'écarté d'un argument : le paquet est
`DesignPatternCatalog.Reefact`, il porte donc le préfixe du catalogue comme tous les autres, et le mot qui
suit nomme le corpus d'un auteur plutôt que le catalogue de tout ce qu'un éditeur publie.

## Alternatives envisagées

### Ranger les quatre sous `Idioms`

Envisagé parce que l'ADR-0013 existe précisément pour un pattern qui a une source et pas de catalogue, et
qu'il n'y aurait rien de nouveau à admettre.

Rejeté parce que les quatre ont un corpus propre, ce qui disqualifie un pattern d'`Idioms`, et parce que
le catalogue perdrait le lien entre un pattern et l'article qui l'explique.

### Les ajouter à `DomainDrivenDesign`

Envisagé parce qu'ils portent sur les value objects, et que `ValueObject` y vit.

Rejeté parce que le livre d'Evans ne les présente pas (ADR-0028), et parce qu'une relation vers
`ValueObject` serait de toute façon impossible depuis un autre catalogue (ADR-0027) — le lecteur verrait
une proximité que la donnée ne peut pas soutenir.

### Un catalogue par article

Par exemple un catalogue réservé aux value objects. Envisagé parce qu'il suit à la lettre « un paquet par
œuvre cataloguée ».

Rejeté parce que les patterns du mainteneur n'arrivent pas tous sous forme d'articles sur un même sujet,
et qu'un paquet par article serait un paquet de deux attributs. Un catalogue du corpus d'un auteur est
l'unité qui reste utile à mesure qu'elle grandit.

## Conséquences

### Positives

* Les quatre attributs ont une place, avec une citation, une page de guide et un exemple travaillé.
* Le prochain pattern que le mainteneur met par écrit a un endroit où aller et un seuil à franchir.

### Négatives

* Le catalogue est ouvert par construction. Le mot *complet* ne veut rien dire pour lui, comme pour
  `Idioms`, et le README le dit.
* Un paquet de plus à maintenir, avec sa propre baseline d'API publique.

### Risques

* Le catalogue devient un fourre-tout pour tout ce que le mainteneur utilise. L'exigence d'un texte est la
  seule garde, et c'est une règle de relecture plutôt que quelque chose que le build impose.
* ⚠️ **Tension avec l'ADR-0013** (ranger un pattern sans corpus propre sous les idiomes) **et l'ADR-0038**
  (nommer les paquets d'après le catalogue plutôt que l'éditeur). Aucun n'est contredit franchement — les
  entrées ont un corpus, et le paquet garde le préfixe du catalogue — mais un mainteneur qui lit le « sans
  inventer de catalogues à entrée unique » de l'ADR-0013 comme une règle plutôt que comme une raison peut
  n'être pas d'accord.
* Un article peut être révisé. La référence porte l'année de première publication, et rien ne remarque une
  entrée dont l'article change sous elle.

## Actions de suivi

* Rédiger le guide des patterns `Hydration` et `RestrictedTo`, dans les deux langues.
* Décider, le jour où un texte d'un autre auteur est proposé, si le catalogue reste celui du mainteneur.

## Références

* [ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.fr.md),
  [ADR-0027](0027-ship-one-independent-package-per-catalogued-work.fr.md),
  [ADR-0028](0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.fr.md),
  [ADR-0035](0035-index-the-pattern-language-and-require-a-write-up.fr.md),
  [ADR-0038](0038-name-the-packages-after-the-catalogue-rather-than-the-vendor.fr.md)
* [ADR-0043](0043-let-a-role-link-to-a-type-that-is-not-a-role.fr.md) — le lien dont `RestrictedTo` a besoin
* Reefact, *Value Objects avancés en .NET*, 2026 — `reefact.net`
