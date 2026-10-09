# ADR-0021 | Versionner ce qu'un consommateur lit, et pas seulement ce qu'il compile

🌍 🇬🇧 [English](0021-version-what-a-consumer-reads-and-not-only-what-it-compiles.md) · 🇫🇷 Français (ce fichier)

**Statut :** Remplacé par l'[ADR-0045](0045-start-every-package-at-version-1-0-0.fr.md), sur une seule clause : que les paquets restent sous `1.0.0`. Le reste de ce record tient.
**Proposé :** 2026-08-05
**Accepté :** 2026-08-06
**Décideurs :** Reefact

## Contexte

La bibliothèque a désormais une identité de paquet et aucune politique de version.
`0.1.0-dev` est un placeholder, et rien ne dit ce qu'un numéro signifierait.

Plusieurs enregistrements énoncent déjà, séparément, ce qui est additif et ce qui
ne l'est pas. Ajouter un rôle à un pattern publié est additif
([ADR-0003](0003-give-each-role-its-own-attribute-nested-in-its-pattern.fr.md)) et
est désormais gardé par la baseline d'API
([ADR-0018](0018-hold-the-public-surface-to-a-committed-baseline.fr.md)). Élargir
l'ensemble de cibles d'un rôle est additif, le restreindre casse les consommateurs
qui avaient annoté légitimement
([ADR-0009](0009-let-each-role-declare-what-it-applies-to.fr.md)). Un pattern qui
acquiert plus tard un corpus change d'espace de noms, ce qui casse les
consommateurs quel que soit son point de départ
([ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.fr.md)).
Aucun n'a été écrit comme une règle de versionnage, et ensemble ils n'en font pas
une.

Cette bibliothèque a un second contrat qu'aucun compilateur ne défend. Les
attributs ne portent aucun comportement et la bibliothèque ne publie aucun
lecteur : un consommateur copie les règles de lecture et se les approprie
([ADR-0004](0004-keep-the-attribute-base-a-pure-marker.fr.md)). Deux sortes de
changements modifient donc ce qu'obtient un consommateur en laissant la surface
publique identique à l'octet :

* **Une relation.** Déclarer qu'un pattern en décline un autre change ce que
  répond `IdentityOf` pour des annotations déjà écrites. Un décompte qui
  rapportait deux patterns en rapporte un, et aucun type n'a été ajouté, retiré ni
  renommé
  ([ADR-0005](0005-relate-patterns-by-inheritance-and-read-identity-from-it.fr.md),
  [ADR-0019](0019-stop-the-identity-climb-at-the-pattern-boundary.fr.md)).
* **Une règle de lecture.** L'ADR-0019 a changé le calcul de l'identité. Rien n'a
  changé dans l'assembly ; tout consommateur qui copie le lecteur obtient d'autres
  réponses à la copie suivante.

`Inherited` relève du même endroit : le basculer change ce qu'un lecteur trouve
sur un sous-type, et compile dans les deux cas.

Le catalogue est appelé à croître d'un ordre de grandeur, et l'essentiel de cette
croissance est additif par construction. Les déplacements ne le sont pas : PoEAA
porte deux entrées sur une cinquantaine, `Idioms` n'existe pas encore, et ce sont
deux endroits d'où des patterns seront relogés à mesure que les ouvrages voisins
seront catalogués.

Rien n'a été publié : aucun consommateur n'a encore droit à quoi que ce soit.

## Décision

Le paquet suit le versionnage sémantique à la fois sur ce contre quoi un
consommateur compile et sur ce qu'il relit — un changement d'identité d'un pattern
ou d'une règle de lecture est donc une version majeure même si la surface publique
est intacte — et il reste en dessous de `1.0.0` tant qu'un pattern catalogué est
susceptible de changer de catalogue.

## Justification

Ne versionner que la surface serait précis et faux. Toute la raison d'être de
cette bibliothèque est qu'un consommateur lit du sens dans les types : une version
qui conserve chaque type en changeant leur sens est donc une rupture, par la seule
définition qui compte ici. La baseline d'API rend déjà visibles les changements de
surface ; ce qu'elle ne peut pas voir est exactement ce à quoi cette politique
étend la règle.

Énoncer la correspondance est ce qui rend la règle utilisable plutôt que
velléitaire, et presque tout y est déjà décidé ailleurs — ceci le rassemble :

| | |
|---|---|
| **Majeure** | un rôle ou un pattern retiré ou renommé · un ensemble de cibles restreint · `AllowMultiple` ou `Inherited` modifié · un pattern déplacé d'un catalogue à l'autre · une relation ajoutée, retirée ou changée de nature · une règle de lecture modifiée |
| **Mineure** | un pattern ajouté · un rôle ajouté à un pattern publié · un ensemble de cibles élargi · un lien ajouté à un rôle |
| **Corrective** | la documentation, les exemples, l'index du catalogue, tout ce qui n'atteint aucun consommateur |

Deux entrées de ce tableau sont celles qu'un mainteneur sera tenté de mal classer.
Une relation ressemble à un énoncé éditorial sur deux livres et constitue en fait
un changement du regroupement de tous les consommateurs. Une règle de lecture
ressemble à de la documentation et c'est ce que les consommateurs copient.

Rester sous `1.0.0` est honnête sur celle des deux moitiés qui est instable. Le
mécanisme est arrêté — vingt enregistrements l'argumentent, la forme a survécu à
une refonte, et les tests de convention la tiennent. Ce qui n'est pas arrêté, c'est
le *placement* : un pattern siège dans `Idioms` parce qu'aucun corpus ne le
revendique encore, et le jour où l'un le fait il déménage, ce que l'ADR-0013 a
accepté comme un coût. Avec deux catalogues à peine entamés, ces déplacements sont
probables et groupés, et dépenser une majeure pour chacun dirait que la
bibliothèque est instable alors que seul son classement l'est. `0.x` le dit
clairement et ne coûte rien tant que rien n'est publié.

Le critère de passage en `1.0.0` porte donc sur les catalogues plutôt que sur le
temps ou l'exhaustivité : il est atteint quand les ouvrages auxquels un pattern
catalogué pourrait appartenir sont présents, de sorte qu'un déménagement devienne
un accident et non une attente. C'est un jugement, mais un jugement sur une chose
énoncée, ce qui le rend discutable.

Sous `1.0.0`, les règles ci-dessus s'appliquent décalées d'un cran : une rupture
déplace la mineure, tout le reste la corrective. Le versionnage sémantique autorise
tout en `0.x`, et l'autorisation de casser en silence n'est pas une politique. Se
comporter comme si le numéro comptait est ce qui fera du passage en `1.0.0` une
formalité plutôt qu'un événement.

## Alternatives envisagées

### Ne versionner que la surface publique, comme toute bibliothèque

Envisagé parce que c'est ce que tous les outils comprennent, ce que la baseline
d'API suit déjà, et ce sur quoi le gestionnaire de paquets d'un consommateur sait
agir.

Rejeté parce que cela qualifierait de corrective une version qui change le
regroupement de tous les consommateurs. La surface n'est pas le produit ici — le
sens qu'on y lit l'est — et une politique incapable d'exprimer la différence
garantit qu'elle sera manquée.

### Passer en `1.0.0` dès la première publication

Envisagé parce que le mécanisme est stable, que `0.x` se lit « pas prêt » pour un
consommateur potentiel, et que cela invite à un moindre soin.

Rejeté parce que cela appliquerait un numéro stable à un catalogue dont le
classement est sciemment provisoire. La première entrée d'`Idioms` qui acquiert un
corpus est une majeure sous cette politique, et plusieurs sont attendues
rapprochées ; un `1.x` qui atteint `4.0.0` en une saison communique moins qu'un
`0.x` qui n'a encore rien promis.

### Versionner chaque catalogue séparément

Envisagé parce que les catalogues bougent à des rythmes différents, et qu'un
consommateur qui n'emploie que le Gang of Four ne devrait pas être dérangé par les
remous du Domain-Driven Design.

Rejeté comme une décision d'empaquetage déguisée en décision de versionnage : cela
exigerait un paquet par catalogue, un changement bien plus vaste, avec ses propres
conséquences sur les relations qui traversent les catalogues — une déclinaison lie
deux catalogues par héritage. L'option reste disponible si les remous justifient un
jour la scission.

### Des versions datées ou séquentielles

Envisagé parce que l'essentiel de la croissance est additif, et qu'un train de
publication de catalogue se lit naturellement comme une date.

Rejeté parce que cela jette la seule chose dont un consommateur a besoin d'une
version ici. Toute la difficulté est que certains changements cassent et
ressemblent exactement à ceux qui ne cassent pas ; un schéma qui refuse de dire
lesquels déplace le problème vers un changelog que personne ne lit avant de mettre
à jour.

## Conséquences

### Positives

* Un changement qui altère ce que les consommateurs lisent ne peut pas sortir en
  corrective.
* Les affirmations éparses sur ce qui est additif deviennent un tableau unique, en
  un seul endroit.
* `0.x` énonce laquelle des deux moitiés est provisoire, au lieu de laisser croire
  que tout l'est.
* La condition du `1.0.0` est écrite : l'atteindre est une décision qu'on peut
  contester plutôt qu'une humeur.

### Négatives

* Une relation entre deux patterns — un jugement éditorial — porte désormais le
  coût d'une majeure, ce qui rendra sa déclaration disproportionnée au ressenti.
* Juger qu'un pattern est « susceptible de déménager » n'est pas mécanique : le
  passage en `1.0.0` devra donc être argumenté.

### Risques

* Rien n'impose la moitié « sens ». La baseline d'API attrape un changement de
  surface ; une relation ajoutée au catalogue produit un diff court et anodin, et
  seule la revue le relie à une majeure.
* Un `0.x` qui dure invite les consommateurs à épingler exactement et à ne jamais
  monter de version, soit le contraire de ce que veut un vocabulaire en croissance.

## Actions de suivi

* Prendre la version d'une étiquette de publication plutôt que du fichier projet,
  et promouvoir les entrées accumulées vers `PublicAPI.Shipped.txt` à la première
  publication (ADR-0018).
* Consigner une version propre aux règles de lecture, si un consommateur a un jour
  besoin de dire quelle révision des règles son lecteur implémente.

## Références

* [ADR-0018](0018-hold-the-public-surface-to-a-committed-baseline.fr.md) — la
  baseline, qui voit celle des deux moitiés qui est une surface.
* [ADR-0004](0004-keep-the-attribute-base-a-pure-marker.fr.md) — pourquoi un
  consommateur possède les règles de lecture, et pourquoi les changer l'atteint.
* [ADR-0019](0019-stop-the-identity-climb-at-the-pattern-boundary.fr.md) — une
  règle de lecture qui change, que ceci classe.
* [ADR-0013](0013-shelve-a-pattern-without-a-body-of-work-under-idioms.fr.md) — le
  déménagement qui maintient la version sous `1.0.0`.
* `CONTRIBUTING.md` — le tableau tel qu'un auteur le rencontre.
