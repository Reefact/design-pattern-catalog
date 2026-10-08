#region Usings declarations

using System;

#endregion

namespace DesignPatternCatalog.Reefact {

    /// <summary>
    ///     Hydration (Reefact) — The boundary at which a value object is rebuilt from, and reduced to, its underlying
    ///     values: rehydration enforces the invariants and knows no external format, dehydration yields plain values
    ///     and is called only by other dehydration.
    /// </summary>
    /// <remarks>
    ///     <para>
    ///         Annotate the declaration that introduces the role. When a role is introduced by an interface, annotate
    ///         that interface rather than each of its implementations.
    ///     </para>
    ///     <para>
    ///         Reefact, <i>Advanced Value Objects in .NET</i>, 2026.
    ///     </para>
    /// </remarks>
    public static class Hydration {

        /// <summary>
        ///     Role played by a type or a member in the Hydration design pattern.
        /// </summary>
        public abstract class Role : DesignPatternAttribute { }

        /// <summary>
        ///     Builds a value object from its underlying values, enforcing its invariants and knowing nothing of any
        ///     external format.
        /// </summary>
        [AttributeUsage(AttributeTargets.Method | AttributeTargets.Constructor, AllowMultiple = false, Inherited = false)]
        public sealed class RehydrateAttribute : Role { }

        /// <summary>
        ///     Produces the underlying values of a value object: a boundary with the outer layers, not an API for
        ///     collaborators.
        /// </summary>
        [AttributeUsage(AttributeTargets.Method, AllowMultiple = false, Inherited = false)]
        public sealed class DehydrateAttribute : Role { }

        /// <summary>
        ///     Carries the several underlying values of one value object across the boundary, holding plain values and
        ///     never a value object.
        /// </summary>
        [AttributeUsage(AttributeTargets.Class | AttributeTargets.Struct, AllowMultiple = false, Inherited = false)]
        public sealed class DehydratedObjectAttribute : Role { }

    }

}
