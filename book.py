"""Per-novel settings shared by the drafting, revision, and evaluation tools."""

TITLE = "The Unfinished Name"
SERIES = "The Omni Chronicles, Book One"
GENRE = "near-future supernatural investigative thriller"

POV_RULE = (
    "Close third person, past tense, locked to ONE viewpoint character per "
    "chapter: Dr. Elias Cade by default, Sister Miriam Halevi where the outline "
    "says so. The narrator never knows more than that character."
)

# Book-specific drafting rules, appended to every draft/revision prompt.
DRAFT_RULES = """\
BOOK RULES (The Unfinished Name):
- The narrator NEVER certifies a disputed event as divine, demonic, or
  mechanical. Attribute interpretations to characters.
- First meaning must work in the scene; any biblical echo deepens it
  without solving the mystery. Two or three prominent echoes max; often none.
- Never decode an echo inside the scene. No "this represented..." lines.
- Conceal causes, not observations. Never invent an earlier clue the prose
  didn't show.
- Keep the three deceptions distinct (Name / WordS / OMNI Problem). Do not
  reveal SINTAX, Ellis's nature, or the Book of AbyssOS attribution before
  the outline says so.
- Keep human explanations (prior access, shared documents, rehearsal,
  compromised records, technical failure) plausible where evidence allows.
- Every discovery changes access, trust, responsibility, or a next action,
  and costs someone something. Don't end on another withheld file.
- Respect the clock ledger: day, time, travel (60-90 min between sites),
  meals, and sleep. Drafted chapters and canon override the outline.
- Cade's public correction stays outstanding until the outline resolves it.
- Human worth is never earned by usefulness, speech, or performance.
- Metaphors come from records, handwriting, equipment, labs, archives,
  recovery meetings, liturgy -- never from a thesaurus.
- Target 2,200-3,200 words. Short chapters with consequences.
"""
