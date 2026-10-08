# Enterprise Integration Patterns — le guide des patrons

🌍 🇫🇷 Français (ce fichier) · 🇬🇧 [English](README-en.md)

*Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions* — Gregor
Hohpe et Bobby Woolf, Addison-Wesley, 2003. Soixante-cinq patrons catalogués, et c'est le plus grand
catalogue d'ici ; **quarante-six sont écrits à ce jour**, et les deux chapitres qui manquent encore sont
nommés ci-dessous avec ce qui en tient lieu jusqu'à leur existence.

Ce guide n'est pas l'index du catalogue.
L'[index](../../../generated/catalog-index.md#enterprise-integration-patterns) donne l'annotation par
type, ce à quoi chaque rôle s'applique et où est l'exemple ; il est généré, complet et consulté. Ces
pages donnent à quoi sert un patron, quand y recourir, quand ne pas le faire et ce qu'il coûte. Elles
sont écrites à la main, et elles arrivent un volet à la fois
([ADR-0040](../../for-maintainers/adr/0040-write-the-pattern-guide-by-hand-in-both-languages.md)).

Tous les exemples de ce catalogue sont un seul système — un terminal à conteneurs, avec ses
déclarations en douane, ses portiques, ses guérites et ses manifestes EDI — et les pages se renvoient
l'une à l'autre parce que le code le fait.

## Les styles d'intégration

Chapitre 2. Quatre façons de faire travailler deux applications ensemble, présentées par le livre comme
un seul choix plutôt que comme quatre techniques. Les pages se renvoient l'une à l'autre pour cette
raison : chacune se lit mieux face aux trois autres, et la recommandation propre du livre est la
quatrième.

| Style | À quoi il sert |
|---|---|
| [File Transfer](FileTransfer-fr.md) | Une application produit un fichier que l'autre consomme, de sorte qu'aucune ne sache rien de l'autre au-delà d'un format convenu. |
| [Shared Database](SharedDatabase-fr.md) | Les deux lisent et écrivent un seul schéma, de sorte qu'il n'y ait aucune donnée à transférer et rien qui puisse se désynchroniser. |
| [Remote Procedure Invocation](RemoteProcedureInvocation-fr.md) | L'une appelle une procédure que l'autre expose, de sorte que données et comportement voyagent ensemble et que l'appelant apprenne la réponse tout de suite. |
| [Messaging](Messaging-fr.md) | Des paquets de données voyagent sur des canaux, de sorte qu'émetteur et receveur soient découplés dans le temps autant que dans la technologie. |

## Les patrons racines

Chapitre 3. Six patrons dont tout le reste du livre est composé : chaque chapitre ultérieur en spécialise
un. Ce sont les pages les plus courtes du catalogue et celles sur lesquelles les autres s'appuient le
plus.

| Patron | À quoi il sert |
|---|---|
| [Message Channel](MessageChannel-fr.md) | Le chemin logique qu'emprunte un message, de sorte qu'un émetteur adresse un canal plutôt qu'un receveur. |
| [Message](Message-fr.md) | Des données enveloppées dans un paquet que le canal sait porter, de sorte que ce qui est envoyé soit une chose à part entière plutôt que les arguments d'un appel. |
| [Pipes and Filters](PipesAndFilters-fr.md) | Une tâche divisée en étapes indépendantes reliées par des canaux, de sorte qu'une étape puisse être réordonnée, réutilisée ou remplacée. |
| [Message Router](MessageRouter-fr.md) | Où va ensuite un message, décidé à un seul endroit, de sorte que les étapes d'un processus n'aient pas à connaître leurs adresses respectives. |
| [Message Translator](MessageTranslator-fr.md) | Un message converti d'un format vers un autre, de sorte que des applications aux formats différents puissent se parler sans qu'aucune soit changée. |
| [Message Endpoint](MessageEndpoint-fr.md) | La façon dont une application s'attache à un canal, de sorte que son code envoie et reçoive sans détenir l'API du système de messagerie. |

## Les canaux de messagerie

Le chapitre qui transforme [Message Channel](MessageChannel-fr.md) en décisions. Neuf patrons, et ils
répondent à quatre questions différentes au sujet d'un même canal — combien de receveurs, ce qui peut
voyager, ce qu'il advient de ce qui ne peut pas être traité, et si le canal survit à son propre hôte. Les
deux premiers se lisent ensemble, et les deux du milieu aussi ; c'est dans les paires que vivent les
distinctions.

| Patron | À quoi il sert |
|---|---|
| [Point-to-Point Channel](PointToPointChannel-fr.md) | Chaque message à exactement un receveur, de sorte que des consommateurs concurrents se partagent une charge sans rien traiter deux fois. |
| [Publish-Subscribe Channel](PublishSubscribeChannel-fr.md) | Une copie à chaque abonné, de sorte qu'un événement atteigne tous les intéressés et que l'émetteur n'en connaisse aucun. |
| [Datatype Channel](DatatypeChannel-fr.md) | Une sorte de message par canal, de sorte qu'un receveur sache ce qu'il lit sans l'inspecter. |
| [Invalid Message Channel](InvalidMessageChannel-fr.md) | Un endroit où un receveur met ce qu'il a lu et rejeté, de sorte qu'une donnée mauvaise ne bloque pas le canal et ne disparaisse pas. |
| [Dead Letter Channel](DeadLetterChannel-fr.md) | Un endroit où le système de messagerie met ce qu'il n'a pas pu délivrer, de sorte qu'un échec de délivrance soit visible plutôt que silencieux. |
| [Guaranteed Delivery](GuaranteedDelivery-fr.md) | Un canal qui fait persister ce qu'il porte, de sorte qu'une panne entre l'envoi et la réception ne perde rien. |
| [Channel Adapter](ChannelAdapter-fr.md) | Tendre le bras dans une application depuis l'extérieur, de sorte qu'une application qui ne connaît rien à la messagerie puisse tout de même y prendre part. |
| [Messaging Bridge](MessagingBridge-fr.md) | Deux systèmes de messagerie joints, de sorte qu'une migration puisse se faire une application à la fois. |
| [Message Bus](MessageBus-fr.md) | Une infrastructure partagée **et** un jeu de commandes convenu, de sorte qu'une application puisse être ajoutée ou retirée sans que les autres soient touchées. |

## La construction des messages

Ce qu'est un message, et ce qu'il porte outre sa charge utile. Les trois premiers sont une seule
distinction — qui décide de ce qui arrive ensuite — et les seules restrictions de
[Message](Message-fr.md) que le catalogue enregistre. Les trois suivants sont une seule conversation.
Les trois derniers sont des propriétés qu'un message de n'importe quelle sorte peut porter.

| Patron | À quoi il sert |
|---|---|
| [Command Message](CommandMessage-fr.md) | Une instruction, de sorte qu'invoquer une procédure dans une autre application soit un message plutôt qu'un appel. |
| [Document Message](DocumentMessage-fr.md) | Des données sans instruction attachée, de sorte que le receveur décide quoi en faire. |
| [Event Message](EventMessage-fr.md) | Un fait au passé, de sorte que l'émetteur soit dispensé de savoir qui s'y intéresse. |
| [Request-Reply](RequestReply-fr.md) | Une question et une réponse en deux messages sur deux canaux, de sorte qu'aucun côté ne se bloque sur la disponibilité de l'autre. |
| [Return Address](ReturnAddress-fr.md) | Le canal de réponse porté sur la requête, de sorte qu'un répondeur serve des demandeurs pour lesquels il n'a jamais été configuré. |
| [Correlation Identifier](CorrelationIdentifier-fr.md) | Une réponse qui cite la requête à laquelle elle répond, de sorte qu'un demandeur qui en envoie plusieurs puisse dire laquelle est laquelle. |
| [Message Sequence](MessageSequence-fr.md) | Quel ensemble, quelle place, combien — de sorte que des données trop grandes pour un message puissent être réassemblées. |
| [Message Expiration](MessageExpiration-fr.md) | Quand un message cesse de valoir d'être obéi, de sorte qu'une instruction périmée soit écartée plutôt que suivie tardivement. |
| [Format Indicator](FormatIndicator-fr.md) | Dans quelle forme est le message, de sorte que les consommateurs puissent être redéployés selon leurs propres calendriers. |

## Le routage des messages

Le plus grand chapitre du livre, et la racine [Message Router](MessageRouter-fr.md) spécialisée de douze
façons. Les quatre premiers décident *où* ; les trois du milieu changent *combien il y a de messages* ;
les deux suivants sont des composites bâtis à partir des autres ; les trois derniers sont ce qui arrive
quand une route devient un processus.

| Patron | À quoi il sert |
|---|---|
| [Content-Based Router](ContentBasedRouter-fr.md) | Une destination choisie en examinant le message, de sorte que l'émetteur ne connaisse ni les destinations ni la règle. |
| [Message Filter](MessageFilter-fr.md) | Un routeur à une sortie avec la possibilité d'aucune, de sorte qu'un receveur soit épargné de ce qu'il ne ferait qu'ignorer. |
| [Dynamic Router](DynamicRouter-fr.md) | Des destinations qui s'annoncent, de sorte qu'en ajouter une soit un message plutôt qu'un déploiement. |
| [Recipient List](RecipientList-fr.md) | Un ensemble de destinations calculé par message, de sorte que qui le reçoit dépende de ce qu'il dit. |
| [Splitter](Splitter-fr.md) | Un message par élément, de sorte que chacun puisse être traité et routé pour lui-même. |
| [Aggregator](Aggregator-fr.md) | Des messages apparentés retenus jusqu'à ce que l'ensemble soit complet, puis un seul émis — le seul routeur doté d'un état. |
| [Resequencer](Resequencer-fr.md) | Ce qui arrive tôt tamponné et relâché dans l'ordre, de sorte que la séquence survive au transport. |
| [Composed Message Processor](ComposedMessageProcessor-fr.md) | Diviser, router chaque élément, réassembler — une étape adressable pour un message d'éléments mêlés. |
| [Scatter-Gather](ScatterGather-fr.md) | Le message entier à plusieurs parties, et leurs réponses assemblées en la meilleure. |
| [Routing Slip](RoutingSlip-fr.md) | L'itinéraire porté sur le message, de sorte qu'une séquence variable n'ait besoin d'aucun participant central. |
| [Process Manager](ProcessManager-fr.md) | L'état détenu par un participant, de sorte que l'étape suivante puisse dépendre de ce que les réponses ont dit. |
| [Message Broker](MessageBroker-fr.md) | Le routage du système entier dans un pivot — l'arithmétique du point à point échangée contre une seule dépendance. |

## La transformation des messages

Ce que devient [Message Translator](MessageTranslator-fr.md) quand le changement dépasse un format. Deux
sont opposés — l'un ajoute ce qui manquait à l'émetteur, l'autre retire ce que le receveur ne veut pas.
Deux changent la taille d'un message en sens contraires. Deux sont les réponses à *beaucoup de formats*.

| Patron | À quoi il sert |
|---|---|
| [Envelope Wrapper](EnvelopeWrapper-fr.md) | Des données applicatives mises dans ce que l'infrastructure exige, de sorte qu'un système qui ne connaît rien aux en-têtes puisse prendre part. |
| [Content Enricher](ContentEnricher-fr.md) | Ce que l'émetteur n'a pas pu fournir, cherché auprès d'une source externe et ajouté. |
| [Content Filter](ContentFilter-fr.md) | Ce dont le receveur n'a pas l'usage, retiré — et l'imbrication aplatie au passage. |
| [Claim Check](ClaimCheck-fr.md) | Le volume stocké une fois et une clé laissée à sa place, de sorte que les étapes intermédiaires ne portent qu'une référence. |
| [Normalizer](Normalizer-fr.md) | Un routeur et un traducteur par format, de sorte que de nombreux formats équivalents arrivent comme un seul. |
| [Canonical Data Model](CanonicalDataModel-fr.md) | Un format n'appartenant à personne, de sorte qu'ajouter une application coûte une traduction plutôt qu'une par correspondant. |

## Les points de terminaison

Pas encore écrits. Messaging Gateway, Messaging Mapper, Transactional Client, Polling Consumer,
Event-Driven Consumer, Competing Consumers, Message Dispatcher, Selective Consumer, Durable Subscriber,
Idempotent Receiver, Service Activator — onze, qui spécialisent
[Message Endpoint](MessageEndpoint-fr.md). Tous sont catalogués et annotés ; seules leurs pages de guide
manquent. En attendant qu'elles existent, les
[entrées d'index](../../../generated/catalog-index.md#enterprise-integration-patterns) et les exemples
sous
[`DesignPatternCatalog.Usage/EnterpriseIntegration`](../../../../DesignPatternCatalog.Usage/EnterpriseIntegration)
sont ce qu'il y a.

## L'exploitation

Pas encore écrits. Control Bus, Detour, Wire Tap, Message History, Message Store, Smart Proxy, Test
Message, Channel Purger — huit, et le seul chapitre d'ici qui porte sur l'exploitation d'une solution de
messagerie plutôt que sur sa construction.

## Comment une page est organisée

Toutes les pages suivent le même ordre.

| | |
|---|---|
| **Intention** | une phrase |
| **Problème** | la situation qui rend le patron digne d'être considéré, en code |
| **Solution** | ce que le patron y fait |
| **Structure** | un diagramme des rôles — un diagramme de classes, ou un diagramme de flux là où le patron est une étape d'un pipeline |
| **Les rôles** | une ligne chacun, et l'annotation qui le marque |
| **L'exemple** | l'exemple de `DesignPatternCatalog.Usage`, par morceaux |
| **Possibilités d'application** | ce que l'œuvre énonce elle-même |
| **Quand ne pas l'utiliser** | les cas où le patron coûte plus qu'il ne rapporte |
| **Avantages** et **Inconvénients** | deux listes |
| **Liens avec les autres patrons** | les voisins, et ce qui les sépare |
| **Source** | l'œuvre, et les liens de retour vers l'index et le code |

## Ce que ces pages ne font pas

Elles n'inventent pas. Là où le livre n'énonce pas quelque chose, la page le dit plutôt que de remplir la
section. Cinq conséquences méritent d'être nommées pour ce catalogue en particulier.

**Les quatre styles d'intégration sont des alternatives, et les pages ne les aplatissent pas en une seule
recommandation.** Le livre préfère la messagerie et le dit, mais il donne aussi à File Transfer et à
Shared Database de véritables avantages, et ces pages les portent comme ceux des auteurs plutôt que de
les convertir en avertissements.

**L'un de ces noms est un anti-patron dans un autre catalogue.** Hohpe et Woolf présentent Shared
Database comme un style à choisir ; Richardson le présente comme ce que *Database per Service* existe
pour fuir. Le catalogue tient les deux entrées — le même schéma, la recommandation inverse — et la page
[Shared Database](SharedDatabase-fr.md) suit la lecture de ce livre-ci et nomme l'autre.

**Les exemples de ce catalogue sont plus laconiques que ceux des autres.** La plupart élident leur corps
par `// ...`, parce que ce qu'un patron affirme ici est d'ordinaire une signature et une absence plutôt
qu'une implémentation — un routeur qui rend un nom de canal n'a nulle part où mettre une charge utile.
Les pages s'appuient donc davantage sur l'explication de ce qui *manque* à une signature que sur la
citation de ce qui y est.

**Un exemple prend un raccourci, et sa page le dit.** Le pipeline de l'exemple de
[Pipes and Filters](PipesAndFilters-fr.md) appelle ses filtres directement plutôt qu'à travers les tuyaux
qu'il déclare. Le livre admet les deux agencements, l'exemple n'est donc pas faux — mais un lecteur qui
compare le diagramme au code le remarquerait, et la page le nomme d'abord.

**Plusieurs de ces patrons sont d'ordinaire de la configuration plutôt que du code, et les pages le disent
au lieu de faire comme si.** Un canal de lettres mortes est normalement un réglage de courtier ; un canal
est souvent un nom de file configuré, sans type à annoter. Là où c'est le cas, il n'y a rien à quoi
l'annotation puisse s'attacher, ce qui est la condition ordinaire de tout rôle plutôt qu'un manque dans
l'entrée — le motif que consigne
l'[ADR-0029](../../for-maintainers/adr/0029-admit-enterprise-integration-patterns-as-a-catalogue.md) pour
avoir admis les canaux. Les pages concernées le nomment dans *Les rôles*, là où regardera un lecteur qui
se demande s'il faut annoter quoi que ce soit.
