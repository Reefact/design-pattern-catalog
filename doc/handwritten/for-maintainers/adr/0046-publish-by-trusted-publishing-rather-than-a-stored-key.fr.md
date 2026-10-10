# ADR-0046 | Publier par publication de confiance plutôt qu'avec une clé stockée

🌍 🇬🇧 [English](0046-publish-by-trusted-publishing-rather-than-a-stored-key.md) · 🇫🇷 Français (ce fichier)

**Statut :** Proposé
**Proposé :** 2026-10-10
**Décideurs :** Reefact

## Contexte

L'[ADR-0044](0044-release-each-package-from-its-own-tag.fr.md) fait publier quatorze paquets sur nuget.org par
un workflow quand un tag est poussé. Pour cela, le workflow doit prouver à nuget.org qu'il agit pour le
propriétaire des paquets. Cet ADR cite une clé d'API NuGet stockée, tenue comme secret du dépôt : sa
justification dit qu'un tag poussé échoue sans elle, et ses actions de suivi comptent la création de ce
secret.

Une clé d'API NuGet est durable, a une échéance que le mainteneur doit retenir, et reste valable partout où
elle fuit. nuget.org propose une autre voie, la **publication de confiance** : le workflow demande à GitHub un
jeton d'identité signé, nuget.org le confronte à une règle qui nomme un dépôt et un fichier de workflow, et
rend une clé d'API qui vit une heure. La documentation de NuGet la présente comme la meilleure façon de publier.

Le mainteneur publie déjà ainsi les paquets d'un autre dépôt, `just-dummies` : une action `NuGet/login`
épinglée, la permission `id-token: write`, et le nom d'utilisateur nuget.org tenu comme *variable* du dépôt,
puisqu'il est public. Le pipeline de ce dépôt sert d'exemple éprouvé.

La règle appartient à un dépôt et à un nom de fichier de workflow, pas à un identifiant de paquet : une seule
règle couvre tous les paquets de ce dépôt. Un identifiant que personne ne détient encore est réservé au
compte par son premier envoi réussi.

## Décision

Le workflow de livraison s'authentifie auprès de nuget.org par publication de confiance, en échangeant son
identité GitHub contre une clé de courte durée, et aucune clé NuGet n'est stockée dans le dépôt.

## Justification

Il n'y a rien à retenir. Une clé stockée expire, et le jour où elle le fait la livraison échoue pour une raison
étrangère à la livraison ; une clé émise pour l'exécution n'existe plus l'heure d'après. Rien ne peut non plus
fuiter des réglages du dépôt, puisqu'il n'y a rien à y fuiter.

C'est ainsi que l'autre dépôt du mainteneur publie déjà : il y a une seule manière de faire plutôt que deux, et
son exemple est connu pour fonctionner.

La connexion est demandée avant tout travail, et aussi lors d'une répétition, si bien qu'une règle absente ou
un nom d'utilisateur absent échoue en quelques secondes, sur l'exécution faite pour le trouver, au lieu de
l'être après la construction ou pendant une vraie livraison. La clé vit une heure et l'exécution dure quelques
minutes : la demander tôt ne coûte rien.

Le nom d'utilisateur est tenu comme variable du dépôt parce que c'est un identifiant, pas un secret ; stocké
comme secret, il serait seulement masqué dans les journaux, ce qui rend un échec de connexion plus difficile à
lire et ne protège rien.

Ceci remplace un détail de l'ADR-0044 et laisse sa décision en place : qu'une livraison est un tag, comment un
tag se traduit en paquets, et la cascade. Seul le mécanisme que sa justification et ses actions de suivi
nomment pour l'authentification — un secret `NUGET_API_KEY` stocké — est remplacé.

## Alternatives envisagées

### Une clé d'API NuGet stockée

Ce que nomme l'ADR-0044. Envisagée parce que c'est la façon la plus courante et qu'elle se met en place en cinq
minutes.

Rejetée à cause de l'échéance, qui devient un échec le jour d'une livraison, et parce qu'une clé est un
justificatif que peut lire tout ce qui accède aux réglages du dépôt.

### Publier à la main depuis la machine du mainteneur

Envisagée parce qu'elle n'exige aucune automatisation.

Rejetée parce que l'ADR-0044 existe pour qu'une livraison soit un tag poussé, et qu'un envoi manuel ferait du
tag une affirmation que rien ne garantit.

## Conséquences

### Positives

* Aucun justificatif n'est stocké, renouvelé ni remplacé.
* La répétition vérifie la règle autant que le pipeline.
* Une seule manière de publier dans les dépôts du mainteneur.

### Négatives

* La mise en place demande la session authentifiée du propriétaire des paquets sur nuget.org ; personne ne peut
  la faire à sa place.
* Une action tierce, `NuGet/login`, se trouve dans le chemin de livraison. Elle est épinglée à un commit comme
  toutes les autres.
* Tant que la règle et la variable n'existent pas, chaque exécution du workflow échoue à la connexion, la
  répétition comprise.

### Risques

* La règle nomme le dépôt et le fichier de workflow. Renommer l'un ou l'autre casse la publication jusqu'à ce
  que la règle soit changée sur nuget.org.
* Un identifiant que quelqu'un d'autre détient déjà sur nuget.org ne peut pas être publié, et ne se découvre
  qu'au premier envoi.

## Actions de suivi

* Créer la règle de publication de confiance sur nuget.org et la variable `NUGET_USER` sur GitHub, comme
  indiqué dans *Releasing* de `CONTRIBUTING.md`.
* Vérifier que personne d'autre ne détient d'identifiant `DesignPatternCatalog.` sur nuget.org avant le
  premier tag.

## Références

* [ADR-0044](0044-release-each-package-from-its-own-tag.fr.md) — le mécanisme de livraison dont ce record
  remplace le détail d'authentification
* `.github/workflows/release.yml`, et la section *Releasing* de `CONTRIBUTING.md`
* NuGet, *Trusted Publishing* — `learn.microsoft.com/nuget/nuget-org/trusted-publishing`
