"""The skill catalog: known skills, their categories, and the other names they go by.

Matching is only as good as this list. Add a skill (or alias) here when a posting uses a
term the analyzer misses, together with a test that covers it.
"""

import re
from collections.abc import Iterable

from gap_analyzer.models import Skill, SkillCategory

L = SkillCategory.LANGUAGE
F = SkillCategory.FRAMEWORK
D = SkillCategory.DATABASE
T = SkillCategory.TOOL
C = SkillCategory.CLOUD
P = SkillCategory.PRACTICE

# Aliases that are also ordinary English words or letters ("Go big", "Grade C"). They only
# match with exactly this capitalization, and only when another skill is mentioned in the
# same text ("Go and Python", "C/C++").
AMBIGUOUS_ALIASES = frozenset({"Go", "C"})

DEFAULT_SKILLS: tuple[Skill, ...] = (
    # Languages
    Skill(name="Python", category=L),
    Skill(name="Java", category=L),
    Skill(name="JavaScript", category=L, aliases=("JS", "ECMAScript", "ES6")),
    Skill(name="TypeScript", category=L, aliases=("TS",)),
    Skill(name="C", category=L),
    Skill(name="C++", category=L, aliases=("CPP",)),
    Skill(name="C#", category=L, aliases=("C Sharp", "CSharp")),
    Skill(name="Go", category=L, aliases=("Golang",)),
    Skill(name="Rust", category=L),
    Skill(name="Kotlin", category=L),
    Skill(name="Swift", category=L),
    Skill(name="Ruby", category=L),
    Skill(name="PHP", category=L),
    Skill(name="Scala", category=L),
    Skill(name="SQL", category=L),
    Skill(name="HTML", category=L, aliases=("HTML5",)),
    Skill(name="CSS", category=L, aliases=("CSS3",)),
    Skill(name="Bash", category=L, aliases=("Shell scripting",)),
    # Frameworks and libraries
    Skill(name="React", category=F, aliases=("React.js", "ReactJS")),
    Skill(name="React Native", category=F),
    Skill(name="Angular", category=F, aliases=("AngularJS",)),
    Skill(name="Vue", category=F, aliases=("Vue.js", "VueJS")),
    Skill(name="Next.js", category=F, aliases=("NextJS",)),
    Skill(name="Node.js", category=F, aliases=("Node", "NodeJS")),
    Skill(name="Express", category=F, aliases=("Express.js", "ExpressJS")),
    Skill(name="Django", category=F),
    Skill(name="Flask", category=F),
    Skill(name="FastAPI", category=F),
    Skill(name="Spring", category=F, aliases=("Spring Boot",)),
    Skill(name=".NET", category=F, aliases=("ASP.NET", "dotnet", ".NET Core")),
    Skill(name="Pandas", category=F),
    Skill(name="NumPy", category=F),
    Skill(name="PyTorch", category=F),
    Skill(name="TensorFlow", category=F),
    Skill(name="scikit-learn", category=F, aliases=("sklearn",)),
    # Databases
    Skill(name="PostgreSQL", category=D, aliases=("Postgres",)),
    Skill(name="MySQL", category=D),
    Skill(name="SQLite", category=D),
    Skill(name="MongoDB", category=D, aliases=("Mongo",)),
    Skill(name="Redis", category=D),
    Skill(name="NoSQL", category=D),
    # Tools
    Skill(name="Git", category=T),
    Skill(name="GitHub", category=T),
    Skill(name="Docker", category=T),
    Skill(name="Kubernetes", category=T, aliases=("K8s",)),
    Skill(name="Linux", category=T, aliases=("Unix",)),
    Skill(name="Jira", category=T),
    # Cloud
    Skill(name="AWS", category=C, aliases=("Amazon Web Services",)),
    Skill(name="Azure", category=C, aliases=("Microsoft Azure",)),
    Skill(name="Google Cloud", category=C, aliases=("GCP", "Google Cloud Platform")),
    # Practices
    Skill(name="REST APIs", category=P, aliases=("REST", "RESTful", "RESTful APIs", "REST API")),
    Skill(name="GraphQL", category=P),
    Skill(
        name="Automated testing",
        category=P,
        aliases=("unit testing", "unit tests", "integration testing", "test automation"),
    ),
    Skill(name="CI/CD", category=P, aliases=("continuous integration", "continuous delivery")),
    Skill(name="Agile", category=P, aliases=("Scrum",)),
    Skill(name="Data structures", category=P, aliases=("data structures and algorithms", "DSA")),
    Skill(name="Algorithms", category=P),
    Skill(name="Object-oriented programming", category=P, aliases=("OOP", "object oriented")),
    Skill(name="Machine learning", category=P, aliases=("ML",)),
)


def _alias_pattern(alias: str) -> re.Pattern[str]:
    # Plain \b does not work for names like "C++", ".NET" or "Node.js", so define the
    # boundaries explicitly: no word character (or ".") directly before the alias, and no
    # word character, "+", "#" or ".x" directly after it.
    flags = 0 if alias in AMBIGUOUS_ALIASES else re.IGNORECASE
    escaped = r"\s+".join(re.escape(part) for part in alias.split())
    return re.compile(rf"(?<![\w.]){escaped}(?![\w+#])(?!\.\w)", flags)


class SkillCatalog:
    def __init__(self, skills: Iterable[Skill] = DEFAULT_SKILLS):
        self.skills: dict[str, Skill] = {}
        self._by_alias: dict[str, Skill] = {}
        self._patterns: list[tuple[re.Pattern[str], Skill, bool]] = []

        for skill in skills:
            if skill.name in self.skills:
                raise ValueError(f"duplicate skill in catalog: {skill.name!r}")
            self.skills[skill.name] = skill
            for alias in (skill.name, *skill.aliases):
                key = alias.casefold()
                if self._by_alias.get(key, skill) is not skill:
                    raise ValueError(f"alias {alias!r} is used by more than one skill")
                self._by_alias[key] = skill
                ambiguous = alias in AMBIGUOUS_ALIASES
                self._patterns.append((_alias_pattern(alias), skill, ambiguous))

    def lookup(self, name: str) -> Skill | None:
        """Find the skill a name or alias refers to, ignoring case and surrounding spaces."""
        return self._by_alias.get(" ".join(name.split()).casefold())

    def find_in_text(self, text: str) -> list[tuple[int, int, Skill]]:
        """Return (start, end, skill) for each skill mentioned in `text`, in reading order.

        When mentions overlap, the longest wins, so "React Native" is not also read as
        "React", and "Node.js" is not also read as "JS". Ambiguous aliases only count when
        another skill is mentioned too (see AMBIGUOUS_ALIASES).
        """
        candidates = [
            (match.start(), match.end(), skill, ambiguous)
            for pattern, skill, ambiguous in self._patterns
            for match in pattern.finditer(text)
        ]
        candidates.sort(key=lambda c: (-(c[1] - c[0]), c[0]))

        taken: list[tuple[int, int]] = []
        found: list[tuple[int, int, Skill, bool]] = []
        for start, end, skill, ambiguous in candidates:
            if any(start < t_end and t_start < end for t_start, t_end in taken):
                continue
            taken.append((start, end))
            found.append((start, end, skill, ambiguous))

        has_clear_mention = any(not ambiguous for *_, ambiguous in found)
        return sorted(
            (
                (start, end, skill)
                for start, end, skill, ambiguous in found
                if has_clear_mention or not ambiguous
            ),
            key=lambda f: f[0],
        )
