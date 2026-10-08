#region Usings declarations

using DesignPatternCatalog.DomainDrivenDesign;
using DesignPatternCatalog.Reefact;

#endregion

namespace DesignPatternCatalog.Usage.Reefact.RestrictedToSample {

    // Public transport: a fare is what a passenger pays, a concession rate is the share the operator waives
    // for a category of passenger — pensioners, students, children.
    //
    // The rate knows how to take its share off an amount, and that is the whole of its business. What it
    // must not know is how the result is rounded: that is the fare's policy, the one place the operator
    // decides whether a half-cent goes up, down or to the even neighbour. So the rate hands back an exact
    // amount and the fare rounds it.
    //
    // That makes ApplyTo a method with exactly one legitimate caller. Making it public would let any use
    // case in the application layer take a percentage off a bare decimal and round it as it saw fit —
    // which is how a pensioner's fare comes to be one cent different on the receipt and in the ledger.
    // Making it internal keeps the application layer out, and RESTRICTED TO says who is let in, so a
    // second caller shows up in a review rather than in a reconciliation.
    //
    // The attribute is repeatable, and a member that needs two of them is worth looking at: it usually means
    // an abstraction both collaborators share has not been named.

    [ValueObject]
    public sealed class ConcessionRate {

        private readonly decimal _percent;

        private ConcessionRate(decimal percent) {
            if (percent is < 0 or > 100) { throw new ArgumentOutOfRangeException(nameof(percent)); }

            _percent = percent;
        }

        public static ConcessionRate FromPercent(decimal percent) => new(percent);

        // Exact on purpose: rounding is the fare's decision.
        [RestrictedTo(Collaborator = typeof(Fare))]
        internal decimal ApplyTo(decimal amount) => amount * (1 - _percent / 100m);

    }

    [ValueObject]
    public sealed class Fare {

        private readonly decimal _euros;

        private Fare(decimal euros) {
            if (euros < 0) { throw new ArgumentOutOfRangeException(nameof(euros)); }

            _euros = euros;
        }

        public static Fare FromEuros(decimal euros) => new(euros);

        public Fare Apply(ConcessionRate rate) =>
            new(Math.Round(rate.ApplyTo(_euros), 2, MidpointRounding.ToEven));

        public override string ToString() => $"{_euros:0.00} EUR";

    }

}
