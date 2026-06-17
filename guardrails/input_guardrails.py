"""Input guardrails for startup descriptions entering the due diligence pipeline."""

import re
from dataclasses import dataclass

_MIN_LENGTH = 20
_MAX_LENGTH = 5000

# Patterns that suggest prompt injection attempts
_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?", re.IGNORECASE),
    re.compile(r"disregard\s+(all\s+)?(previous|prior|above)", re.IGNORECASE),
    re.compile(r"forget\s+(all\s+)?(previous|prior|above)\s+instructions?", re.IGNORECASE),
    re.compile(r"new\s+instructions?:", re.IGNORECASE),
    re.compile(r"\bsystem\s+prompt\b", re.IGNORECASE),
    re.compile(r"\byou\s+are\s+now\s+", re.IGNORECASE),
    re.compile(r"\bact\s+as\s+(a\s+)?(new|different|another)", re.IGNORECASE),
    re.compile(r"\bpretend\s+(to\s+be|you\s+are)\b", re.IGNORECASE),
    re.compile(r"<\s*(system|user|assistant)\s*>", re.IGNORECASE),
    re.compile(r"\[INST\]", re.IGNORECASE),
    re.compile(r"###\s*Instruction", re.IGNORECASE),
    re.compile(r"always\s+(score|rate|give)\s+(this\s+)?(a\s+)?10", re.IGNORECASE),
]

# Descriptions that are clearly not startup pitches
_GIBBERISH_PATTERN = re.compile(r"^[^a-zA-Z]*$")


@dataclass
class GuardrailResult:
    passed: bool
    reason: str | None = None


def validate_startup_description(description: str) -> GuardrailResult:
    """Validate a startup description before it enters the agent pipeline.

    Checks length bounds and prompt injection patterns.
    Returns a GuardrailResult with passed=True if safe, False with a reason otherwise.
    """
    if not description or not description.strip():
        return GuardrailResult(False, "Startup description cannot be empty.")

    desc = description.strip()

    if len(desc) < _MIN_LENGTH:
        return GuardrailResult(
            False,
            f"Description too short ({len(desc)} chars). Provide at least {_MIN_LENGTH} characters.",
        )

    if len(desc) > _MAX_LENGTH:
        return GuardrailResult(
            False,
            f"Description too long ({len(desc)} chars). Keep it under {_MAX_LENGTH} characters.",
        )

    if _GIBBERISH_PATTERN.match(desc):
        return GuardrailResult(False, "Description contains no readable text.")

    for pattern in _INJECTION_PATTERNS:
        if pattern.search(desc):
            return GuardrailResult(False, "Description contains disallowed content.")

    return GuardrailResult(True)
