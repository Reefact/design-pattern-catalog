# ADR-0041 | Détenir un pattern nommé dans une édition de référence ultérieure de l'auteur

🌍 🇬🇧 [English](0041-hold-a-pattern-named-in-an-authors-later-reference-edition.md) · 🇫🇷 Français (ce fichier)

**Statut :** Accepté
**Proposé :** 2026-08-12
**Accepté :** 2026-10-08
**Décideurs :** Reefact

## Contexte

`DomainDrivenDesign/DomainEvent` est catalogué depuis l'écriture du catalogue Domain-Driven
Design, avec une référence portant *Eric Evans, Domain-Driven Design, 2003*.

L'écriture du guide des patrons a fait apparaître un problème avec cette référence. Domain
Event n'est pas un pattern du livre de 2003 : il ne figure pas dans le langage de patterns que
le livre expose, et Evans n'y traite des événements qu'en passant. L'affirmation repose sur la
liste que le livre donne lui-même de ce qu'il nomme, non sur une lecture intégrale du texte, et
elle est énoncée ici pour pouvoir être vérifiée plutôt que crue sur parole.

Evans nomme le pattern dans *Domain-Driven Design Reference: Definitions and Pattern
Summaries*, 2015. Cette œuvre n'est pas un nouveau livre. C'est Evans qui reprend les résumés
de patterns du livre de 2003, avec un petit nombre d'ajouts faits dans les onze ans qui les
séparent — Domain Events parmi eux. Elle porte le même vocabulaire, le même auteur et le même
langage de patterns.

Martin Fowler a publié un *Domain Event* sur son propre site en 2005, dans le matériel eaaDev.
Ce matériel a été examiné pour une admission comme catalogue à part entière et le contrôle est
sorti négatif : rien dans ce dépôt ne le détient.

L'[ADR-0028](0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.fr.md) décide qu'un
pattern est détenu dans chaque catalogue dont l'œuvre le présente comme un des siens — le test
étant la paternité, non la mention.
L'[ADR-0027](0027-ship-one-independent-package-per-catalogued-work.fr.md) livre un package
indépendant par œuvre cataloguée.
L'[ADR-0026](0026-follow-an-authors-own-supersession-of-a-catalogued-chapter.fr.md) décide que,
là où un auteur énonce qu'une œuvre ultérieure de sa main supplante une partie d'une œuvre
cataloguée, le catalogue suit l'œuvre ultérieure et la catalogue comme un catalogue à part
entière. Sa condition préalable — une supplantation énoncée — n'est pas remplie ici : la
Reference ne supplante pas le livre, elle le résume.

`catalog/pattern.schema.json` décrit la référence comme porteuse et non éditoriale : c'est elle
qui dit quelle œuvre détient le pattern.

Tous les autres catalogues du dépôt portent exactement une œuvre de référence sur l'ensemble de
leurs entrées. L'unique exception est `Idioms`, qui en porte deux, et que
l'[ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.fr.md) a précisément
bâti comme le catalogue sans corpus propre.

Rien n'est publié à ce jour ([ADR-0021](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.fr.md)).

## Décision

Un pattern nommé dans une édition de référence ultérieure d'une œuvre cataloguée, due à son
auteur, est détenu dans le catalogue de cette œuvre, et sa propre référence nomme l'édition qui
le nomme.

## Justification

La référence est ce qui rend le catalogue vérifiable : une entrée dont la référence est fausse
est donc pire qu'une entrée manquante. Un lecteur qui installe
`DesignPatternCatalog.DomainDrivenDesign`, rencontre `[DomainEvent]` crédité à un livre de 2003
et va le chercher dans ce livre ne trouve rien — et n'a aucun moyen de savoir si c'est le
catalogue qui a tort ou sa propre lecture. Corriger la référence n'est pas facultatif une fois
l'écart connu.

La question que la correction ouvre est celle de l'endroit où l'entrée appartient alors, et la
réponse découle de ce que l'ADR-0028 a érigé en test. Cet ADR demande si une **œuvre présente le
pattern comme un des siens** — le nomme, le décrit, lui donne une place dans son propre langage
de patterns. La Reference fait les trois. Le livre de 2003 n'en fait aucune. L'entrée est donc
légitime, et elle l'est du fait de la Reference.

Cataloguer la Reference à part, comme l'ADR-0026 le fait pour *Accounting Patterns*, serait une
mauvaise lecture de cet ADR. Ce qui justifiait là-bas un catalogue à part entière était une
**supplantation** énoncée par l'auteur, et un vocabulaire qui avait réellement changé : des
quinze noms de patterns du chapitre 6 de Fowler, un seul survit dans le papier. Rien de tel
n'est vrai ici. La Reference reprend le vocabulaire du livre au lieu de le remplacer, et un
package `DomainDrivenDesignReference` livrerait vingt-deux entrées identiques à celles de son
voisin pour en loger une vingt-troisième.

Détenir l'entrée dans le catalogue Domain-Driven Design correspond aussi à ce que les packages
promettent à un lecteur. La revendication d'indépendance de l'ADR-0027 est qu'un catalogue est
le rendu complet d'une œuvre ; pour un lecteur, l'œuvre est le Domain-Driven Design d'Evans, et
la Reference est l'endroit où le vocabulaire de cette œuvre se trouve aujourd'hui le plus
commodément. Détacher un pattern des vingt-deux auxquels il appartient satisferait une règle sur
les éditions au prix de la promesse pour laquelle cette règle existe.

La page de Fowler de 2005 n'est pas une prétention concurrente à trancher. L'ADR-0028 exige une
œuvre qui présente le pattern comme le sien **et** qui soit cataloguée ici ; le matériel eaaDev
ne l'est pas, donc la question de savoir lequel des deux l'a nommé en premier n'a aucune
conséquence sur ce que ce dépôt détient. Elle est consignée plus haut parce qu'un lecteur qui
connaît l'histoire se demanderait sinon si elle a été négligée.

Le précédent que cela pose est étroit par construction. Il vise une édition ultérieure **du même
auteur, de la même œuvre**, reprenant le même langage de patterns — non n'importe quelle œuvre
ultérieure qui mentionne un pattern, ce que l'ADR-0028 refuse déjà.

## Alternatives envisagées

### Laisser la référence à *Domain-Driven Design, 2003*

Envisagée parce qu'elle ne coûte rien et garde chaque catalogue mono-œuvre.

Rejetée parce qu'elle est fausse, et parce que cette fausseté est de l'espèce que le catalogue
existe pour prévenir. Le schéma qualifie la référence de porteuse ; une entrée qui se
mésattribue sape la crédibilité de toutes les autres, puisqu'un lecteur n'a aucun moyen de
savoir lesquelles ont été vérifiées.

### Cataloguer *Domain-Driven Design Reference* comme un catalogue à part entière

Envisagée parce que l'ADR-0026 a fait exactement cela pour *Accounting Patterns*, et que suivre
un précédent existant coûte moins cher que d'écrire un nouveau record.

Rejetée parce que la condition préalable diffère. L'ADR-0026 repose sur une supplantation
énoncée par l'auteur et sur un vocabulaire qui avait réellement divergé ; la Reference ne
supplante rien et diverge d'une entrée. Le résultat serait un package de vingt-trois patterns
dont vingt-deux dupliquent le package voisin, livré pour qu'une entrée puisse être classée sous
l'édition qui la nomme.

### Retirer l'entrée du catalogue

Envisagée parce qu'elle rétablit l'invariant selon lequel chaque entrée remonte à l'œuvre unique
du catalogue, et parce que l'ADR-0011 laisse déjà de côté ce qui ne peut pas être annoté.

Rejetée parce que le pattern est annotable, qu'il est employé, et qu'il fait partie du
vocabulaire qu'un lecteur de Domain-Driven Design attend — `MicroservicesPatterns/DomainEvent`
existe à côté et crédite DDD dès sa première ligne. Le retirer rendrait le catalogue moins
complet pour rendre une règle plus nette, et l'ADR-0028 existe pour empêcher exactement cet
échange.

## Conséquences

### Positives

* La référence dit vrai, et un lecteur qui la suit trouve le pattern.
* Le test de l'ADR-0028 — l'œuvre présente-t-elle le pattern comme le sien — est appliqué plutôt
  que supposé, et la réponse est désormais consignée.
* Le catalogue Domain-Driven Design peut être déclaré complet : vingt-trois entrées, chacune
  avec une source qui tient.
* Le guide des patrons peut porter une page Domain Event, qu'il refusait d'écrire tant que la
  source était douteuse.

### Négatives

* `DomainDrivenDesign` devient le second catalogue dont les entrées ne partagent pas toutes une
  œuvre de référence, après `Idioms`.
* L'index généré montre une ligne dont l'œuvre diffère du titre de catalogue au-dessus d'elle,
  ce qu'un lecteur peut prendre pour une erreur avant de trouver ce record.
* Une règle voulant qu'un catalogue ait exactement une œuvre de référence — plausible à écrire,
  et jamais écrite — devient indisponible.

### Risques

* L'affirmation que Domain Event est absent du livre de 2003 repose sur la liste de patterns du
  livre lui-même, non sur une lecture intégrale. Si elle est fausse, ce record est inutile et la
  référence doit revenir à 2003.
* L'étroitesse du précédent dépend de sa lecture littérale. Un mainteneur ultérieur pourrait
  étirer *édition de référence ultérieure* jusqu'à couvrir toute œuvre ultérieure du même
  auteur, ce que l'ADR-0028 refuse déjà et que ce record n'entend pas rouvrir.

## Actions de suivi

* Relire la liste de patterns du livre de 2003 pour confirmer l'absence, si un exemplaire est
  sous la main.
* Décider si le *Domain Event* eaaDev de Fowler mérite un record propre, étant donné que le
  contrôle d'admission d'eaaDev est sorti négatif pour des raisons sans rapport avec ce pattern.

## Références

* [ADR-0006](0006-catalogue-a-pattern-where-the-work-that-named-it-put-it.fr.md) — cataloguer un pattern là où l'œuvre qui l'a nommé l'a mis
* [ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.fr.md) — ranger sous Idioms un pattern sans corpus
* [ADR-0026](0026-follow-an-authors-own-supersession-of-a-catalogued-chapter.fr.md) — suivre la supplantation d'un chapitre catalogué par son auteur
* [ADR-0027](0027-ship-one-independent-package-per-catalogued-work.fr.md) — livrer un package indépendant par œuvre cataloguée
* [ADR-0028](0028-hold-a-pattern-in-every-catalogue-whose-work-presents-it.fr.md) — détenir un pattern dans chaque catalogue dont l'œuvre le présente comme le sien
* [ADR-0040](0040-write-the-pattern-guide-by-hand-in-both-languages.fr.md) — écrire le guide des patrons à la main, dans les deux langues
* `catalog/pattern.schema.json` — le champ de référence, et pourquoi il est porteur
