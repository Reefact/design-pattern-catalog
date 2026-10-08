# ADR-0043 | Laisser un rôle pointer vers un type qui n'est pas un rôle

🌍 🇬🇧 [English](0043-let-a-role-link-to-a-type-that-is-not-a-role.md) · 🇫🇷 Français (ce fichier)

**Statut :** Proposé
**Proposé :** 2026-10-08
**Décideurs :** Reefact

## Contexte

Un rôle peut déclarer des liens optionnels vers d'autres rôles de son pattern, portés chacun par un `Type`
([ADR-0008](0008-bind-participants-with-typed-links.fr.md)). Le format du catalogue et le générateur n'en
connaissent pas d'autre sorte : le nom d'un lien doit être celui d'un rôle frère, la propriété générée est
documentée comme pointant vers l'attribut de ce rôle, et un test vérifie que chaque propriété de lien de
chaque attribut livré nomme un frère.

`RestrictedTo`, deuxième pattern du catalogue `Reefact`
([ADR-0042](0042-admit-a-catalogue-for-the-maintainers-own-patterns.fr.md)), marque un membre qu'un seul
collaborateur nommé peut appeler, et personne d'autre. Tout son contenu est un type — le collaborateur —
et ce type n'est pas un participant du pattern : c'est la classe que l'auteur a choisie, annotée de rien.
Le pattern n'a qu'un rôle, donc aucun frère vers qui pointer, et un second rôle ne serait pas honnête,
puisque personne n'annoterait le collaborateur avec.

Aucune autre entrée parmi les 345 n'en a besoin. Jusqu'à `RestrictedTo`, la seule sorte de lien du format
suffisait.

## Décision

Un rôle peut déclarer, à côté de ses liens vers des rôles frères, des liens typés optionnels vers des
types qui ne sont pas des rôles de son pattern.

## Justification

Ce qu'il y a à dire est un type, et les raisons qu'avait l'ADR-0008 de porter un lien par un `Type`
valent sans changement : le compilateur le vérifie, le refactoring le suit, et il nomme quelque chose qui
existe déjà plutôt qu'une clé à garder cohérente à la main. Une restriction qui nommerait son
collaborateur par une chaîne se désynchroniserait en silence au premier renommage — exactement ce que
l'ADR-0008 a refusé pour les liens entre participants.

La capacité est utilisée dès son arrivée : l'objection de
l'[ADR-0031](0031-carry-no-generator-machinery-for-an-unused-capability.fr.md) à de la machinerie qu'aucune
entrée n'exerce ne s'applique donc pas. `RestrictedTo` est l'entrée qui l'exerce.

Les liens sont déclarés dans le catalogue et non déduits, pour la raison qui fait du catalogue une donnée
([ADR-0002](0002-keep-the-pattern-catalog-as-data-and-generate-the-attributes.fr.md)) : une propriété qui
apparaît dans un attribut généré doit y être parce que la donnée l'a dit. Le test qui vérifie les liens
n'accepte une propriété qui ne nomme aucun frère que si le catalogue la déclare, de sorte qu'un
défaut de gabarit ne peut pas en ajouter une sans la donnée.

Ceci complète l'ADR-0008 sans le remplacer. Sa décision — des liens entre rôles d'un pattern — tient pour
toute entrée qui en a ; celle-ci en ajoute une seconde sorte à côté.

## Alternatives envisagées

### Un second rôle pour figurer le collaborateur

Envisagé parce qu'il ne demande rien de nouveau : un rôle `Collaborator`, et `RestrictedTo` lié à lui.

Rejeté parce que personne n'annoterait avec. Ce serait un rôle qui n'existe que pour donner un nom à un
lien, il transformerait un attribut plat en attribut imbriqué (`[RestrictedTo.RestrictedTo]`), et le
catalogue prétendrait à un participant que le code ne déclare jamais.

### Un argument positionnel du constructeur

`[RestrictedTo(typeof(Price))]`. Envisagé parce que c'est la forme la plus courte.

Rejeté parce que tout lien du catalogue est une propriété nommée et optionnelle, et que le lecteur d'un
attribut doit retrouver la même forme dans le suivant. Un argument positionnel est aussi obligatoire, ce
qu'un lien n'a jamais été.

### Une chaîne nommant le collaborateur

Rejeté pour la raison pour laquelle l'ADR-0008 l'a rejeté : c'est une valeur magique que le compilateur ne
vérifie pas.

## Conséquences

### Positives

* Un rôle peut nommer un type que le pattern ne possède pas, vérifié par le compilateur.
* Le changement de format est petit et utilisé immédiatement.

### Négatives

* Le format du catalogue a deux sortes de lien, et l'index montre les deux.

### Risques

* Un lien est optionnel : `[RestrictedTo]` sans collaborateur compile et dit seulement que quelque chose est
  restreint. C'est à une règle d'architecture d'exiger le collaborateur ; l'attribut ne le fait pas.
* Ceci est jugé comme un complément de l'ADR-0008 et non comme son remplacement. Un mainteneur qui y lit
  le second cas doit le dire, et le record serait réémis en conséquence.

## Actions de suivi

* Décider, si une autre entrée en a besoin, si un lien externe peut être obligatoire.

## Références

* [ADR-0008](0008-bind-participants-with-typed-links.fr.md),
  [ADR-0031](0031-carry-no-generator-machinery-for-an-unused-capability.fr.md),
  [ADR-0042](0042-admit-a-catalogue-for-the-maintainers-own-patterns.fr.md)
