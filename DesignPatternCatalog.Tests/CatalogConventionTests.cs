#region Usings declarations

using System.Reflection;
using System.Text.Json;

using DesignPatternCatalog.Usage;

using Xunit;

#endregion

namespace DesignPatternCatalog.Tests {

    /// <summary>
    ///     What every generated attribute in the shipped catalog must look like.
    /// </summary>
    /// <remarks>
    ///     <para>
    ///         These run over the shipped assemblies rather than over the catalog on disk. Regenerating an unchanged catalog and
    ///         finding no diff already proves the sources are what the catalog produces; what it cannot prove is that
    ///         what the template produces is well formed. A defect written into the template is emitted uniformly,
    ///         survives the round trip, and is invisible in a diff spanning two hundred files — these assertions are
    ///         the ones that would catch it, once, whatever the size of the catalog.
    ///     </para>
    ///     <para>
    ///         Each is a claim made somewhere in the ADR base that nothing else checks.
    ///     </para>
    /// </remarks>
    public sealed class CatalogConventionTests {

        // One assembly per catalogued work since ADR-0027, so the whole vocabulary is the union of them. The
        // assembly holding the base marker is not among them: it ships no pattern.
        private static readonly Type[] Catalogued = Repository.CatalogueAssemblies
                                                             .SelectMany(assembly => assembly.GetTypes())
                                                             .Where(type => typeof(DesignPatternAttribute).IsAssignableFrom(type))
                                                             .Where(type => type != typeof(DesignPatternAttribute))
                                                             .ToArray();

        private static readonly Type[] Roles = Catalogued.Where(type => !type.IsAbstract).ToArray();

        private static readonly Type[] RoleBases = Catalogued.Where(type => type.IsAbstract).ToArray();

        #region Statics members declarations

        public static TheoryData<Type> EveryRole() {
            TheoryData<Type> data = [];
            foreach (Type role in Roles) { data.Add(role); }

            return data;
        }

        public static TheoryData<Type> EveryPattern() {
            TheoryData<Type> data = [];
            foreach (Type container in Roles.Select(role => role.DeclaringType).OfType<Type>().Distinct()) {
                data.Add(container);
            }

            return data;
        }

        private static HashSet<string> ExternalLinksOf(Type role) {
            string path = Path.Combine(Repository.Root, "catalog", PatternInfo.CatalogOf(role), PatternInfo.PatternNameOf(role) + ".json");
            string name = role.Name[..^"Attribute".Length];

            using JsonDocument entry = JsonDocument.Parse(File.ReadAllText(path));
            JsonElement declared = entry.RootElement.GetProperty("roles").EnumerateArray()
                                        .Single(candidate => candidate.GetProperty("name").GetString() == name);

            return declared.TryGetProperty("externalLinks", out JsonElement links)
                ? links.EnumerateArray().Select(link => link.GetProperty("name").GetString()!).ToHashSet()
                : new HashSet<string>();
        }

        #endregion

        [Fact]
        public void The_catalog_is_not_empty() {
            // Every assertion below is a "for all" and would pass over nothing at all.
            Assert.True(Roles.Length > 90, $"only {Roles.Length} role attributes found");
        }

        [Theory]
        [MemberData(nameof(EveryRole))]
        public void A_role_is_an_attribute_that_a_generic_reader_can_find(Type role) {
            // ADR-0004: a consumer reads the whole catalog through the base attribute alone. One generated file not
            // deriving from it is invisible to every reader ever written, and nothing else says so.
            Assert.True(typeof(Attribute).IsAssignableFrom(role));
            Assert.EndsWith("Attribute", role.Name, StringComparison.Ordinal);
        }

        [Theory]
        [MemberData(nameof(EveryRole))]
        public void A_role_declares_what_it_can_be_applied_to(Type role) {
            // ADR-0009. Omitting AttributeUsage is not a compilation error: it silently means "anything, anywhere",
            // which is what four of the first hand-written entries said by accident. Inherited on purpose here — a
            // declension takes its counterpart's declaration rather than restating it (ADR-0019).
            AttributeUsageAttribute? usage = role.GetCustomAttribute<AttributeUsageAttribute>(true);

            Assert.NotNull(usage);
            Assert.NotEqual(AttributeTargets.All, usage.ValidOn);
        }

        [Theory]
        [MemberData(nameof(EveryPattern))]
        public void Every_role_of_one_pattern_answers_one_identity(Type container) {
            // ADR-0019, which supersedes ADR-0005 on exactly this sentence, and the reason a consumer may group by
            // identity at all: a pattern spread over seven attributes
            // must not be counted as seven patterns.
            Type[] identities = container.GetNestedTypes()
                                         .Where(type => typeof(DesignPatternAttribute).IsAssignableFrom(type))
                                         .Where(type => !type.IsAbstract)
                                         .Select(PatternInfo.IdentityOf)
                                         .Distinct()
                                         .ToArray();

            Assert.Single(identities);
        }

        [Theory]
        [MemberData(nameof(EveryRole))]
        public void A_role_is_sealed_unless_something_derives_from_it(Type role) {
            // Exactly the attributes that are derived from are left unsealed, and the difference is explained by the
            // catalog rather than readable in the file. An unsealed attribute nothing derives from is a template slip,
            // and the only place it shows is here. Since ADR-0027 the search stays inside the role's own assembly:
            // nothing in another catalogue can derive from it, which is the point of the split.
            if (role.IsSealed) { return; }

            Assert.Contains(role.Assembly.GetTypes(), other => other != role && role.IsAssignableFrom(other));
        }

        [Theory]
        [MemberData(nameof(EveryRole))]
        public void A_link_is_a_type_naming_a_role_of_the_same_pattern_or_declared_as_external(Type role) {
            // ADR-0008: a link binds participants of one occurrence, and it is a Type precisely so that it cannot
            // point at something that does not exist. Nothing checks that it points WITHIN the pattern — except
            // here. ADR-0043 adds the one exception: a link to a type that is no role, which the catalog must
            // declare as an external link, so that a property cannot appear in a generated attribute without the
            // data having said it should.
            HashSet<string> external = ExternalLinksOf(role);

            foreach (PropertyInfo link in role.GetProperties(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly)) {
                Assert.Equal(typeof(Type), link.PropertyType);

                if (external.Contains(link.Name)) { continue; }

                Type? container = role.DeclaringType;
                Assert.NotNull(container);
                Assert.Contains(container.GetNestedTypes(), sibling => sibling.Name == link.Name + "Attribute");
            }
        }

        [Theory]
        [MemberData(nameof(EveryRole))]
        public void A_role_is_read_back_into_the_catalog_it_was_written_in(Type role) {
            // ADR-0004's first rule, and the one it calls a trap: the catalog is the FIRST namespace segment below the
            // root, so a consumer taking the last one gets a plausible wrong answer the day a catalog gains a
            // sub-namespace.
            string catalog = PatternInfo.CatalogOf(role);

            Assert.NotEmpty(catalog);
            Assert.DoesNotContain('.', catalog);
            Assert.StartsWith($"DesignPatternCatalog.{catalog}", role.Namespace, StringComparison.Ordinal);
        }

        [Theory]
        [MemberData(nameof(EveryRole))]
        public void A_pattern_name_is_a_pattern_name_and_not_an_attribute_name(Type role) {
            string pattern = PatternInfo.PatternNameOf(role);

            Assert.NotEmpty(pattern);
            Assert.DoesNotContain("Attribute", pattern, StringComparison.Ordinal);
        }

        [Fact]
        public void A_role_base_gathers_roles_and_nothing_else() {
            // The abstract base is what makes the identity of a multi-role pattern a single type. One emitted outside
            // a container, or holding a member, would change what every role of that pattern answers.
            foreach (Type roleBase in RoleBases) {
                Assert.Equal("Role", roleBase.Name);
                Assert.NotNull(roleBase.DeclaringType);
                Assert.Empty(roleBase.GetProperties(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly));
            }
        }

        [Fact]
        public void Every_catalogue_publishes_the_vocabulary_and_nothing_else() {
            // ADR-0004: a catalogue is a vocabulary and nothing else. Anything public that is neither an attribute nor
            // a pattern container is surface a consumer can take a dependency on. Run over each shipped assembly, so
            // one catalogue cannot smuggle a stray type in under cover of another's diff.
            IEnumerable<Type> strays = Repository.CatalogueAssemblies
                                                 .SelectMany(assembly => assembly.GetExportedTypes())
                                                 .Where(type => !typeof(Attribute).IsAssignableFrom(type))
                                                 .Where(type => !(type.IsAbstract && type.IsSealed));

            Assert.Empty(strays);
        }

        [Fact]
        public void Every_catalogue_in_the_data_ships_as_a_package() {
            // ADR-0027: one package per catalogued work. A catalogue that exists as JSON and not as an assembly would
            // be a directory nobody can annotate with, and loading them by name is what makes that fail here.
            Assert.Equal(Repository.Catalogues.Length, Repository.CatalogueAssemblies.Length);
            Assert.NotEmpty(Repository.Catalogues);
        }

    }

}
