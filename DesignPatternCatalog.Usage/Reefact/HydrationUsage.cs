#region Usings declarations

using DesignPatternCatalog.DomainDrivenDesign;
using DesignPatternCatalog.Reefact;

#endregion

namespace DesignPatternCatalog.Usage.Reefact.HydrationSample {

    // Hospital pharmacy: a prescribed dose is an amount and the unit it is counted in.
    //
    // Doses are stored, sent to the ward's dispensing cabinets and read back from prescriptions written
    // years ago, so a dose crosses the boundary of the domain constantly, in both directions. Left to
    // chance, each crossing is a place where a number and a unit can be joined without anyone checking
    // that the pair means something.
    //
    // HYDRATION names the two ways across and the one object that carries a composite across. Rehydrating
    // is the only way in: it enforces what the model says is true of every dose and knows nothing about
    // where the values came from — JSON, a row, a message. Dehydrating is the only way out: it yields
    // plain values and is called from other dehydration methods and from the layer that writes them,
    // never from a collaborator, which has the dose's own behaviour to ask for what it needs.
    //
    // A unit alone is a single value, so it dehydrates straight to its code. A dose is two, so it
    // dehydrates to an object of its own — and that object holds the unit's *code*, never the unit: a
    // dehydrated object that carried a value object would only have moved the boundary one step inside.

    [ValueObject]
    public sealed class DoseUnit : IEquatable<DoseUnit> {

        public static readonly DoseUnit Milligram  = new("mg");
        public static readonly DoseUnit Microgram  = new("mcg");
        public static readonly DoseUnit Millilitre = new("ml");

        private static readonly DoseUnit[] Known = { Milligram, Microgram, Millilitre };

        private readonly string _code;

        private DoseUnit(string code) {
            _code = code;
        }

        // Named values are not a closed set of strings: what comes back from storage must be the same unit
        // as the static member, not merely a unit that prints the same.
        [Hydration.RehydrationMethod]
        public static DoseUnit Rehydrate(string code) {
            DoseUnit? unit = Array.Find(Known, known => known._code == code);

            return unit ?? throw new ArgumentException($"'{code}' is not a unit a dose can be counted in.", nameof(code));
        }

        [Hydration.DehydrationMethod]
        public string ToCode() => _code;

        public bool Equals(DoseUnit? other) => other is not null && other._code == _code;
        public override bool Equals(object? obj) => Equals(obj as DoseUnit);
        public override int GetHashCode() => _code.GetHashCode();

    }

    [ValueObject]
    public sealed class Dose : IEquatable<Dose> {

        private readonly decimal  _amount;
        private readonly DoseUnit _unit;

        private Dose(decimal amount, DoseUnit unit) {
            if (amount <= 0) { throw new ArgumentOutOfRangeException(nameof(amount), "A dose is a positive amount."); }

            _amount = amount;
            _unit   = unit;
        }

        public static Dose Of(decimal amount, DoseUnit unit) => new(amount, unit);

        [Hydration.RehydrationMethod]
        public static Dose Rehydrate(DehydratedDose dehydrated) =>
            new(dehydrated.Amount, DoseUnit.Rehydrate(dehydrated.UnitCode));

        [Hydration.DehydrationMethod]
        public DehydratedDose Dehydrate() => new(_amount, _unit.ToCode());

        public bool Equals(Dose? other) => other is not null && other._amount == _amount && other._unit.Equals(_unit);
        public override bool Equals(object? obj) => Equals(obj as Dose);
        public override int GetHashCode() => HashCode.Combine(_amount, _unit);

    }

    // Plain values only, in the order a dose is written on a prescription. It is not a mirror of Dose: it
    // exists so that the values travel together, and it is shaped by what the storage and the cabinets
    // need to read, not by what the domain does with them.
    [Hydration.DehydratedObject]
    public sealed record DehydratedDose(decimal Amount, string UnitCode);

}
