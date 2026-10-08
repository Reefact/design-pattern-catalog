# Enterprise Integration Patterns — the pattern guide

🌍 🇬🇧 English (this file) · 🇫🇷 [Français](README-fr.md)

*Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions* — Gregor
Hohpe and Bobby Woolf, Addison-Wesley, 2003. Sixty-five patterns catalogued, and it is the largest
catalogue here; **forty-six of them are written up so far**, and the two chapters still missing are named
below with what stands in for them until they exist.

This guide is not the catalogue index. The
[index](../../../generated/catalog-index.md#enterprise-integration-patterns) gives the annotation to
type, what each role applies to, and where the sample is; it is generated, complete, and consulted.
These pages give what a pattern is for, when to reach for it, when not to, and what it costs. They are
written by hand, and they arrive one instalment at a time
([ADR-0040](../../for-maintainers/adr/0040-write-the-pattern-guide-by-hand-in-both-languages.md)).

Every sample in this catalogue is one system — a container terminal, with its customs declarations, its
cranes, its gate kiosks and its EDI manifests — and the pages cross-refer because the code does.

## The integration styles

Chapter 2. Four ways two applications can be made to work together, presented by the book as one choice
rather than as four techniques. The pages cross-refer for that reason: each is best read against the
other three, and the book's own recommendation is the fourth.

| Style | What it is for |
|---|---|
| [File Transfer](FileTransfer-en.md) | One application produces a file the other consumes, so that neither knows anything of the other beyond an agreed format. |
| [Shared Database](SharedDatabase-en.md) | Both read and write one schema, so that there is no data to transfer and nothing to fall out of step. |
| [Remote Procedure Invocation](RemoteProcedureInvocation-en.md) | One calls a procedure the other exposes, so that data and behaviour travel together and the caller learns the answer at once. |
| [Messaging](Messaging-en.md) | Packets of data travel over channels, so that sender and receiver are decoupled in time as well as in technology. |

## The root patterns

Chapter 3. Six patterns out of which the rest of the book is composed: every later chapter specialises
one of these. They are the shortest pages in the catalogue and the ones the others lean on hardest.

| Pattern | What it is for |
|---|---|
| [Message Channel](MessageChannel-en.md) | The logical path a message travels, so that a sender addresses a channel rather than a receiver. |
| [Message](Message-en.md) | Data wrapped in a packet the channel can carry, so that what is sent is a thing in its own right rather than a call's arguments. |
| [Pipes and Filters](PipesAndFilters-en.md) | A larger task divided into independent steps joined by channels, so that a step can be reordered, reused or replaced. |
| [Message Router](MessageRouter-en.md) | Where a message goes next, decided in one place, so that the steps of a process need not know one another's addresses. |
| [Message Translator](MessageTranslator-en.md) | A message converted from one format to another, so that applications with different formats can talk without either being changed. |
| [Message Endpoint](MessageEndpoint-en.md) | How an application attaches to a channel, so that its code sends and receives without holding the messaging system's API. |

## Messaging Channels

The chapter that turns [Message Channel](MessageChannel-en.md) into decisions. Nine patterns, and they
answer four different questions about one channel — how many receivers, what may travel, what happens to
what cannot be handled, and whether the channel survives its own host. Read the first two together and
the middle two together; the pairs are where the distinctions live.

| Pattern | What it is for |
|---|---|
| [Point-to-Point Channel](PointToPointChannel-en.md) | Each message to exactly one receiver, so that competing consumers share a load without handling anything twice. |
| [Publish-Subscribe Channel](PublishSubscribeChannel-en.md) | A copy to every subscriber, so that an event reaches all interested parties and the sender learns of none of them. |
| [Datatype Channel](DatatypeChannel-en.md) | One kind of message per channel, so that a receiver knows what it is reading without inspecting it. |
| [Invalid Message Channel](InvalidMessageChannel-en.md) | Somewhere for a receiver to put what it read and rejected, so that bad data neither blocks the channel nor disappears. |
| [Dead Letter Channel](DeadLetterChannel-en.md) | Somewhere for the messaging system to put what it could not deliver, so that a delivery failure is visible rather than silent. |
| [Guaranteed Delivery](GuaranteedDelivery-en.md) | A channel that persists what it carries, so that a crash between sending and receiving loses nothing. |
| [Channel Adapter](ChannelAdapter-en.md) | Reaching into an application from outside, so that one that knows nothing of messaging can still take part. |
| [Messaging Bridge](MessagingBridge-en.md) | Two messaging systems joined, so that a migration can be done one application at a time. |
| [Message Bus](MessageBus-en.md) | Shared infrastructure **and** an agreed command set, so that an application can be added or removed without the others being touched. |

## Message Construction

What a message is, and what it carries besides its payload. The first three are one distinction — who
decides what happens next — and the catalogue's only recorded narrowings of
[Message](Message-en.md). The next three are one conversation. The last three are properties a message
of any kind may carry.

| Pattern | What it is for |
|---|---|
| [Command Message](CommandMessage-en.md) | An instruction, so that invoking a procedure in another application is a message rather than a call. |
| [Document Message](DocumentMessage-en.md) | Data with no instruction attached, so that the receiver decides what to do with it. |
| [Event Message](EventMessage-en.md) | A fact in the past tense, so that the sender is relieved of knowing who cares. |
| [Request-Reply](RequestReply-en.md) | A question and an answer as two messages on two channels, so that neither side blocks on the other's availability. |
| [Return Address](ReturnAddress-en.md) | The reply channel carried on the request, so that one replier serves requestors it was never configured for. |
| [Correlation Identifier](CorrelationIdentifier-en.md) | A reply that quotes the request it answers, so that a requestor sending many can tell which is which. |
| [Message Sequence](MessageSequence-en.md) | Which set, which place, how many — so that data too large for one message can be reassembled. |
| [Message Expiration](MessageExpiration-en.md) | When a message stops being worth obeying, so that a stale instruction is discarded rather than acted on late. |
| [Format Indicator](FormatIndicator-en.md) | Which shape the message is in, so that consumers can be redeployed on their own schedules. |

## Message Routing

The book's largest chapter, and the root [Message Router](MessageRouter-en.md) specialises twelve ways.
The first four decide *where*; the middle three change *how many messages there are*; the next two are
composites built from the others; the last three are what happens when a route becomes a process.

| Pattern | What it is for |
|---|---|
| [Content-Based Router](ContentBasedRouter-en.md) | One destination chosen by examining the message, so that the sender knows neither the destinations nor the rule. |
| [Message Filter](MessageFilter-en.md) | A router with one output and the option of none, so that a receiver is spared what it would only ignore. |
| [Dynamic Router](DynamicRouter-en.md) | Destinations that announce themselves, so that adding one is a message rather than a deployment. |
| [Recipient List](RecipientList-en.md) | A set of destinations computed per message, so that who receives it can depend on what it says. |
| [Splitter](Splitter-en.md) | One message per element, so that each can be processed and routed on its own. |
| [Aggregator](Aggregator-en.md) | Related messages held until the set is complete, then one emitted — the only stateful router. |
| [Resequencer](Resequencer-en.md) | What arrived early buffered and released in order, so that sequence survives the transport. |
| [Composed Message Processor](ComposedMessageProcessor-en.md) | Split, route each element, reassemble — one addressable step for a message of mixed elements. |
| [Scatter-Gather](ScatterGather-en.md) | The whole message to several parties, and their replies assembled into the best answer. |
| [Routing Slip](RoutingSlip-en.md) | The itinerary carried on the message, so that a varying sequence needs no central participant. |
| [Process Manager](ProcessManager-en.md) | The state held in one participant, so that the next step can depend on what the replies said. |
| [Message Broker](MessageBroker-en.md) | The whole system's routing in one hub — the arithmetic of point-to-point traded for a single dependency. |

## Message Transformation

What [Message Translator](MessageTranslator-en.md) becomes when the change is more than a format. Two are
opposites — one adds what the sender lacked, one removes what the receiver does not want. Two change a
message's size in opposite directions. Two are the answers to *many formats*.

| Pattern | What it is for |
|---|---|
| [Envelope Wrapper](EnvelopeWrapper-en.md) | Application data put inside what the infrastructure requires, so that a system that knows nothing of headers can take part. |
| [Content Enricher](ContentEnricher-en.md) | What the sender could not supply, fetched from an external source and added. |
| [Content Filter](ContentFilter-en.md) | What the receiver has no use for, removed — and the nesting flattened while doing it. |
| [Claim Check](ClaimCheck-en.md) | The bulk stored once and a key left in its place, so that the steps in between carry a reference. |
| [Normalizer](Normalizer-en.md) | A router and a translator per format, so that many equivalent formats arrive as one. |
| [Canonical Data Model](CanonicalDataModel-en.md) | A format belonging to nobody, so that adding an application costs one translation rather than one per correspondent. |

## Messaging Endpoints

Not written yet. Messaging Gateway, Messaging Mapper, Transactional Client, Polling Consumer,
Event-Driven Consumer, Competing Consumers, Message Dispatcher, Selective Consumer, Durable Subscriber,
Idempotent Receiver, Service Activator — eleven, specialising
[Message Endpoint](MessageEndpoint-en.md). All are catalogued and annotated; only their guide pages are
missing. Until they exist, the
[index entries](../../../generated/catalog-index.md#enterprise-integration-patterns) and the samples
under
[`DesignPatternCatalog.Usage/EnterpriseIntegration`](../../../../DesignPatternCatalog.Usage/EnterpriseIntegration)
are what there is.

## System Management

Not written yet. Control Bus, Detour, Wire Tap, Message History, Message Store, Smart Proxy, Test
Message, Channel Purger — eight, and the only chapter here that is about operating a messaging solution
rather than building one.

## How a page is organised

Every page follows the same order.

| | |
|---|---|
| **Intent** | one sentence |
| **Problem** | the situation that makes the pattern worth considering, in code |
| **Solution** | what the pattern does about it |
| **Structure** | a diagram of the roles — a class diagram, or a flow diagram where the pattern is a step in a pipeline |
| **The roles** | one line each, and the annotation that marks it |
| **The example** | the sample from `DesignPatternCatalog.Usage`, in pieces |
| **Applicability** | what the work itself states |
| **When not to use it** | the cases where the pattern costs more than it earns |
| **Advantages** and **Drawbacks** | two lists |
| **Relations with other patterns** | the neighbours, and what separates them |
| **Source** | the work, and links back to the index and the code |

## What these pages do not do

They do not invent. Where the book does not state something, the page says so rather than filling the
section. Five consequences are worth naming for this catalogue in particular.

**The four integration styles are alternatives, and the pages do not flatten them into one
recommendation.** The book prefers messaging and says so, but it also gives File Transfer and Shared
Database real advantages, and those pages carry them as the authors' own rather than converting them
into warnings.

**One of those names is an anti-pattern in another catalogue.** Hohpe and Woolf present Shared Database
as a style to choose; Richardson presents it as the thing *Database per Service* exists to escape.
The catalogue holds both entries — the same schema, the opposite recommendation — and the
[Shared Database](SharedDatabase-en.md) page follows this book's reading and names the other.

**The samples in this catalogue are terser than in the others.** Most elide their bodies with `// ...`,
because what a pattern here asserts is usually a signature and an absence rather than an
implementation — a router that returns a channel name has nowhere to put a payload. The pages therefore
lean more on explaining what is *missing* from a signature than on quoting what is in it.

**One sample takes a shortcut, and its page says so.** The
[Pipes and Filters](PipesAndFilters-en.md) sample's pipeline calls its filters directly rather than
through the pipes it declares. The book admits both arrangements, so the sample is not wrong — but a
reader comparing the diagram to the code would notice, and the page names it first.

**Several of these patterns are usually configuration rather than code, and the pages say so instead of
pretending otherwise.** A dead letter channel is normally a broker setting; a channel is often a
configured queue name with no type to annotate. Where that is so there is nothing for the annotation to
attach to, which is the ordinary condition of every role rather than a gap in the entry — the ground
[ADR-0029](../../for-maintainers/adr/0029-admit-enterprise-integration-patterns-as-a-catalogue.md)
records for admitting the channels at all. The affected pages name it in *The roles*, where a reader
deciding whether to annotate anything will be looking.
