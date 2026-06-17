"""Output guardrails: validate agent structured outputs before they propagate downstream."""

from dataclasses import dataclass, field
from pydantic import BaseModel

_MIN_STRING_LENGTH = 15

# Fields that are legitimately short (category labels, single-word descriptors).
_SHORT_BY_DESIGN: frozenset[str] = frozenset({
    "score_category", "market_stage", "competition_intensity",
    "round_name", "date", "founder_market_fit", "execution_capability",
    "recommendation", "investment_recommendation",
    "market_leader", "industry", "growth_rate", "total_funding", "valuation",
})

# Maps score field name → (low_threshold, high_threshold, direction)
# direction "higher_better": high score → positive category
# direction "higher_worse":  high score → negative category (e.g. risk_score)
_SCORE_COHERENCE: dict[str, tuple[dict[float, list[str]], str]] = {
    "investment_score": (
        {8.5: ["exceptional"], 7.0: ["strong"], 5.0: ["moderate"], 3.0: ["weak"]},
        "higher_better",
    ),
    "market_score": (
        {8.5: ["exceptional", "strong"], 7.0: ["strong", "moderate"]},
        "higher_better",
    ),
    "founder_score": (
        {8.5: ["exceptional", "strong"], 7.0: ["strong", "moderate"]},
        "higher_better",
    ),
    "finance_score": (
        {8.5: ["exceptional"], 7.0: ["strong"], 5.0: ["moderate"], 3.0: ["weak"]},
        "higher_better",
    ),
    "competition_score": (
        {8.5: ["exceptional", "strong"], 2.0: ["weak", "high risk"]},
        "higher_better",
    ),
    "risk_score": (
        {8.0: ["critical risk"], 6.0: ["high risk"], 4.0: ["elevated risk"], 2.0: ["moderate risk"]},
        "higher_worse",
    ),
}


@dataclass
class OutputQualityResult:
    passed: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _check_score_coherence(
    score_field: str,
    score: float,
    category: str,
    agent_name: str,
    warnings: list[str],
) -> None:
    """Warn when a score value and its category label contradict each other."""
    spec = _SCORE_COHERENCE.get(score_field)
    if spec is None:
        return
    thresholds, direction = spec
    cat_lower = category.lower()

    if direction == "higher_better":
        if score >= 8.5 and not any(w in cat_lower for w in ["exceptional", "strong"]):
            warnings.append(
                f"[{agent_name}] {score_field}={score:.1f} is very high "
                f"but score_category='{category}' looks inconsistent."
            )
        elif score <= 2.5 and any(w in cat_lower for w in ["exceptional", "strong"]):
            warnings.append(
                f"[{agent_name}] {score_field}={score:.1f} is very low "
                f"but score_category='{category}' looks inconsistent."
            )
    elif direction == "higher_worse":
        if score >= 8.0 and "critical" not in cat_lower:
            warnings.append(
                f"[{agent_name}] {score_field}={score:.1f} signals critical risk "
                f"but score_category='{category}' does not reflect that."
            )
        elif score <= 2.0 and any(w in cat_lower for w in ["high", "critical", "elevated"]):
            warnings.append(
                f"[{agent_name}] {score_field}={score:.1f} is very low risk "
                f"but score_category='{category}' looks inconsistent."
            )


def validate_output_quality(model: BaseModel, agent_name: str) -> OutputQualityResult:
    """Check an agent's structured output for completeness and internal coherence.

    Warnings are non-blocking; errors will cause the workflow to treat the
    agent as failed.
    """
    warnings: list[str] = []
    errors: list[str] = []

    data = model.model_dump()

    for fname, fvalue in data.items():
        if isinstance(fvalue, str):
            if fname not in _SHORT_BY_DESIGN and len(fvalue.strip()) < _MIN_STRING_LENGTH:
                warnings.append(
                    f"[{agent_name}] '{fname}' is suspiciously short: {repr(fvalue)}"
                )
        elif isinstance(fvalue, list):
            if len(fvalue) == 0:
                warnings.append(f"[{agent_name}] '{fname}' is empty — agent may not have gathered data.")
            else:
                for i, item in enumerate(fvalue):
                    if isinstance(item, str) and len(item.strip()) < 3:
                        warnings.append(
                            f"[{agent_name}] '{fname}[{i}]' appears trivial: {repr(item)}"
                        )

    # Score coherence
    for score_field, score_value in data.items():
        if score_field.endswith("_score") and isinstance(score_value, (int, float)):
            category = data.get("score_category")
            if category:
                _check_score_coherence(score_field, float(score_value), category, agent_name, warnings)

    return OutputQualityResult(passed=len(errors) == 0, warnings=warnings, errors=errors)
