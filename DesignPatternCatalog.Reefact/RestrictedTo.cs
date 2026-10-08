#region Usings declarations

using System;

#endregion

namespace DesignPatternCatalog.Reefact {

    /// <summary>
    ///     RestrictedTo (Reefact) — Opens an otherwise hidden member to one named collaborator, so that the exception
    ///     to encapsulation is declared where it is made and can be verified by an architecture rule.
    /// </summary>
    /// <remarks>
    ///     <para>
    ///         This pattern has a single role, so there is nothing to choose: the attribute is applied on its own.
    ///     </para>
    ///     <para>
    ///         Reefact, <i>Advanced Value Objects in .NET</i>, 2026.
    ///     </para>
    /// </remarks>
    [AttributeUsage(AttributeTargets.Method | AttributeTargets.Property | AttributeTargets.Constructor, AllowMultiple = true, Inherited = false)]
    public sealed class RestrictedToAttribute : DesignPatternAttribute {

        /// <summary>
        ///     The one type allowed to call this member. Stating it is the point of the annotation; left out, the
        ///     annotation says only that the member is restricted.
        /// </summary>
        public Type? Collaborator { get; init; }

    }

}
