"""Structural evals: verify Pydantic model constraints and score coherence offline.

These tests run without any LLM calls by using the golden mock data from
test_cases.py.  They validate:
  - Schema constraints (ge/le ranges, Literal values)
  - Score-to-category coherence
  - Field completeness (no empty required lists, no trivially short strings)
  - Cross-agent consistency (e.g. investment score aligns with risk score)
"""

from __future__ import annotations

import traceback
from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, ValidationError

from agents.investment_agent import InvestmentAnalysis, ScoreCategory, InvestmentRecommendation
from agents.risk_agent import RiskAnalysis
from agents.financial_agent import FinanceAnalysis
from guardrails.output_guardrails import validate_output_quality


@dataclass
class EvalResult:
    name: str
    passed: bool
    detail: str = ""
    warnings: list[str] = field(default_factory=list)


def _run(name: str, fn) -> EvalResult:
    try:
        result = fn()
        if isinstance(result, EvalResult):
            return result
        return EvalResult(name=name, passed=True)
    except AssertionError as e:
        return EvalResult(name=name, passed=False, detail=str(e))
    except Exception:
        return EvalResult(name=name, passed=False, detail=traceback.format_exc())


# ---------------------------------------------------------------------------
# Schema constraint evals
# ---------------------------------------------------------------------------

def eval_investment_score_bounds() -> EvalResult:
    """investment_score must be rejected outside 0–10."""
    try:
        InvestmentAnalysis(
            investment_score=11.0,
            score_category="Strong",
            score_rationale="test",
            recommendation="INVEST",
            investment_thesis="test thesis",
            executive_summary="test summary that is long enough",
        )
        return EvalResult("investment_score_bounds", False, "score=11.0 was accepted — ge/le not enforced")
    except ValidationError:
        return EvalResult("investment_score_bounds", True)


def eval_investment_score_category_literal() -> EvalResult:
    """score_category must reject values outside the Enum."""
    try:
        InvestmentAnalysis(
            investment_score=7.0,
            score_category="Amazing",  # type: ignore[arg-type]
            score_rationale="test rationale that is long enough",
            recommendation="INVEST",
            investment_thesis="test thesis that is long enough",
            executive_summary="test executive summary that is long enough",
        )
        return EvalResult("investment_score_category_literal", False, "'Amazing' was accepted as score_category")
    except (ValidationError, ValueError):
        return EvalResult("investment_score_category_literal", True)


def eval_investment_recommendation_literal() -> EvalResult:
    """recommendation must reject values outside the Enum."""
    try:
        InvestmentAnalysis(
            investment_score=7.0,
            score_category="Strong",
            score_rationale="test rationale that is long enough",
            recommendation="Buy Now",  # type: ignore[arg-type]
            investment_thesis="test thesis that is long enough",
            executive_summary="test executive summary that is long enough",
        )
        return EvalResult("investment_recommendation_literal", False, "'Buy Now' was accepted as recommendation")
    except (ValidationError, ValueError):
        return EvalResult("investment_recommendation_literal", True)


def eval_risk_score_category_literal() -> EvalResult:
    """RiskAnalysis.score_category must reject values outside its Literal."""
    try:
        RiskAnalysis(
            risk_score=5.0,
            score_category="Medium",  # type: ignore[arg-type]
            score_rationale="test",
            recommendation="Proceed",
            summary="test summary that is long enough",
        )
        return EvalResult("risk_score_category_literal", False, "'Medium' was accepted as score_category")
    except (ValidationError, ValueError):
        return EvalResult("risk_score_category_literal", True)


def eval_risk_recommendation_literal() -> EvalResult:
    """RiskAnalysis.recommendation must reject values outside its Literal."""
    try:
        RiskAnalysis(
            risk_score=5.0,
            score_category="Moderate Risk",
            score_rationale="test rationale",
            recommendation="Maybe",  # type: ignore[arg-type]
            summary="test summary that is long enough",
        )
        return EvalResult("risk_recommendation_literal", False, "'Maybe' was accepted as recommendation")
    except (ValidationError, ValueError):
        return EvalResult("risk_recommendation_literal", True)


def eval_finance_score_category_literal() -> EvalResult:
    """FinanceAnalysis.score_category must reject values outside its Literal."""
    try:
        FinanceAnalysis(
            finance_score=5.0,
            score_category="OK",  # type: ignore[arg-type]
            score_rationale="test",
            investment_recommendation="Invest",
            funding_summary="test summary that is long enough",
        )
        return EvalResult("finance_score_category_literal", False, "'OK' was accepted as score_category")
    except (ValidationError, ValueError):
        return EvalResult("finance_score_category_literal", True)


def eval_finance_investment_recommendation_literal() -> EvalResult:
    """FinanceAnalysis.investment_recommendation must reject values outside its Literal."""
    try:
        FinanceAnalysis(
            finance_score=5.0,
            score_category="Moderate",
            score_rationale="test",
            investment_recommendation="Hold",  # type: ignore[arg-type]
            funding_summary="test summary that is long enough",
        )
        return EvalResult("finance_investment_recommendation_literal", False, "'Hold' was accepted as investment_recommendation")
    except (ValidationError, ValueError):
        return EvalResult("finance_investment_recommendation_literal", True)


# ---------------------------------------------------------------------------
# Score coherence evals using golden data
# ---------------------------------------------------------------------------

def eval_strong_startup_output_quality() -> EvalResult:
    """Strong startup golden outputs should pass quality checks with no errors."""
    from evals.test_cases import (
        STRONG_MARKET, STRONG_COMPETITION, STRONG_FOUNDER,
        STRONG_FINANCE, STRONG_RISK, STRONG_INVESTMENT,
    )
    models: list[tuple[str, BaseModel]] = [
        ("market_agent", STRONG_MARKET),
        ("competition_agent", STRONG_COMPETITION),
        ("founder_agent", STRONG_FOUNDER),
        ("finance_agent", STRONG_FINANCE),
        ("risk_agent", STRONG_RISK),
        ("investment_agent", STRONG_INVESTMENT),
    ]
    all_warnings: list[str] = []
    all_errors: list[str] = []
    for agent_name, model in models:
        result = validate_output_quality(model, agent_name)
        all_warnings.extend(result.warnings)
        all_errors.extend(result.errors)

    if all_errors:
        return EvalResult("strong_startup_output_quality", False, "; ".join(all_errors))
    return EvalResult("strong_startup_output_quality", True, warnings=all_warnings)


def eval_weak_startup_output_quality() -> EvalResult:
    """Weak startup golden outputs should pass structurally (no errors, some warnings expected)."""
    from evals.test_cases import (
        WEAK_MARKET, WEAK_COMPETITION, WEAK_FOUNDER,
        WEAK_FINANCE, WEAK_RISK, WEAK_INVESTMENT,
    )
    models: list[tuple[str, BaseModel]] = [
        ("market_agent", WEAK_MARKET),
        ("competition_agent", WEAK_COMPETITION),
        ("founder_agent", WEAK_FOUNDER),
        ("finance_agent", WEAK_FINANCE),
        ("risk_agent", WEAK_RISK),
        ("investment_agent", WEAK_INVESTMENT),
    ]
    all_errors: list[str] = []
    all_warnings: list[str] = []
    for agent_name, model in models:
        result = validate_output_quality(model, agent_name)
        all_errors.extend(result.errors)
        all_warnings.extend(result.warnings)

    if all_errors:
        return EvalResult("weak_startup_output_quality", False, "; ".join(all_errors))
    return EvalResult("weak_startup_output_quality", True, warnings=all_warnings)


def eval_strong_investment_score_range() -> EvalResult:
    """Strong startup investment score must be >= 7.0."""
    from evals.test_cases import STRONG_INVESTMENT
    score = STRONG_INVESTMENT.investment_score
    if score < 7.0:
        return EvalResult(
            "strong_investment_score_range", False,
            f"Expected score >= 7.0 for strong startup, got {score}"
        )
    return EvalResult("strong_investment_score_range", True)


def eval_weak_investment_score_range() -> EvalResult:
    """Weak startup investment score must be <= 4.0."""
    from evals.test_cases import WEAK_INVESTMENT
    score = WEAK_INVESTMENT.investment_score
    if score > 4.0:
        return EvalResult(
            "weak_investment_score_range", False,
            f"Expected score <= 4.0 for weak startup, got {score}"
        )
    return EvalResult("weak_investment_score_range", True)


def eval_cross_agent_consistency() -> EvalResult:
    """High risk score should correlate with low investment score."""
    from evals.test_cases import STRONG_RISK, STRONG_INVESTMENT, WEAK_RISK, WEAK_INVESTMENT

    issues: list[str] = []

    if STRONG_RISK.risk_score >= 7.0 and STRONG_INVESTMENT.investment_score >= 7.0:
        issues.append(
            f"Strong profile: risk_score={STRONG_RISK.risk_score} is high "
            f"but investment_score={STRONG_INVESTMENT.investment_score} is also high — incoherent."
        )

    if WEAK_RISK.risk_score <= 3.0 and WEAK_INVESTMENT.investment_score >= 7.0:
        issues.append(
            f"Weak profile: risk_score={WEAK_RISK.risk_score} is low "
            f"but investment_score={WEAK_INVESTMENT.investment_score} is high — incoherent."
        )

    if issues:
        return EvalResult("cross_agent_consistency", False, "; ".join(issues))
    return EvalResult("cross_agent_consistency", True)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

STRUCTURAL_EVALS = [
    ("investment_score_bounds", eval_investment_score_bounds),
    ("investment_score_category_literal", eval_investment_score_category_literal),
    ("investment_recommendation_literal", eval_investment_recommendation_literal),
    ("risk_score_category_literal", eval_risk_score_category_literal),
    ("risk_recommendation_literal", eval_risk_recommendation_literal),
    ("finance_score_category_literal", eval_finance_score_category_literal),
    ("finance_investment_recommendation_literal", eval_finance_investment_recommendation_literal),
    ("strong_startup_output_quality", eval_strong_startup_output_quality),
    ("weak_startup_output_quality", eval_weak_startup_output_quality),
    ("strong_investment_score_range", eval_strong_investment_score_range),
    ("weak_investment_score_range", eval_weak_investment_score_range),
    ("cross_agent_consistency", eval_cross_agent_consistency),
]


def run_structural_evals() -> list[EvalResult]:
    return [_run(name, fn) for name, fn in STRUCTURAL_EVALS]
