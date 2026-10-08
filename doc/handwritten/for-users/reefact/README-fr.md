# Reefact — le guide des patterns

🌍 🇫🇷 Français (ce fichier) · 🇬🇧 [English](README-en.md)

*Value Objects avancés en .NET* — Reefact, 6 octobre 2026. Deux patterns catalogués, quatre rôles, tous deux
rédigés ici.

Ce catalogue n'est pas un livre. Il tient les patterns que son mainteneur utilise et qu'aucune œuvre
cataloguée ne nomme, chacun entré avec le texte qui le présente
([ADR-0042](../../for-maintainers/adr/0042-admit-a-catalogue-for-the-maintainers-own-patterns.fr.md)). Il est
ouvert, donc *complet* ne veut rien dire pour lui : les pages ci-dessous sont ce qui existe, non ce qui manque.

Ce guide n'est pas l'index du catalogue. L'[index](../../../generated/catalog-index.md#reefact) donne
l'annotation à écrire, ce à quoi chaque rôle s'applique et où se trouve l'exemple ; il est généré, complet, et
se consulte. Ces pages disent à quoi sert un pattern, quand l'employer, quand s'en abstenir, et ce qu'il coûte.
Elles sont écrites à la main
([ADR-0040](../../for-maintainers/adr/0040-write-the-pattern-guide-by-hand-in-both-languages.fr.md)).

## Les patterns

*Value Objects avancés en .NET*. Où le modèle s'arrête, et qui peut y atteindre l'intérieur.

| Pattern | À quoi il sert |
|---|---|
| [Hydration](Hydration-fr.md) | L'unique entrée et l'unique sortie d'un value object : le reconstruire à partir de valeurs simples et le réduire à nouveau à elles. |
| [Collaboration Method](CollaborationMethod-fr.md) | Un membre ouvert à un seul collaborateur nommé et à aucun autre appelant. |

## Ce que ces pages ne font pas

Elles n'inventent pas. L'article est celui du mainteneur : une page rapporte donc **une position plutôt qu'un
consensus**, et le dit sous *Source*. Quand l'article ne donne aucun critère — pour écarter un pattern, ou pour
ses avantages sous forme de liste — la page dit qu'il n'en donne pas, et s'arrête.

Les deux patterns sont des conventions que l'article vérifie par des tests d'architecture ; les attributs de ce
catalogue ne vérifient rien, comme tout attribut de ce dépôt
([ADR-0004](../../for-maintainers/adr/0004-keep-the-attribute-base-a-pure-marker.fr.md)).
