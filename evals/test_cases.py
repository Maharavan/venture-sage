"""Golden mock outputs used for offline structural and guardrail evals.

These are hand-crafted representative outputs — not real LLM runs — so evals
can execute without API calls.  Two profiles are provided: a strong startup
(high scores, rich fields) and a weak startup (low scores, thin fields).
"""

from agents.market_agent import MarketAnalysis
from agents.competitor_agent import CompetitionAnalysis
from agents.founder_agent import FounderAnalysis
from agents.financial_agent import FinanceAnalysis, FundingRound
from agents.risk_agent import RiskAnalysis
from agents.investment_agent import InvestmentAnalysis, ScoreCategory, InvestmentRecommendation
from agents.memo_agent import MemoReport

# ---------------------------------------------------------------------------
# Strong startup (payments infrastructure, Series B, strong founding team)
# ---------------------------------------------------------------------------

STRONG_MARKET = MarketAnalysis(
    industry="Fintech / Payments Infrastructure",
    market_size="$2.5 trillion global payments market",
    growth_rate="14% CAGR through 2030",
    market_stage="Growth",
    customer_segments=["SaaS companies", "E-commerce platforms", "Marketplaces", "B2B platforms"],
    key_trends=["API-first payments", "Embedded finance", "Cross-border expansion", "Real-time payments"],
    opportunities=["Underserved SMB segment", "Emerging markets", "B2B accounts payable automation"],
    risks=["Regulatory changes in key markets", "Big tech competition (Apple Pay, Google Pay)"],
    market_score=8.5,
    summary="Large and growing payments market with strong tailwinds for developer-first API platforms.",
)

STRONG_COMPETITION = CompetitionAnalysis(
    competitors=["Stripe", "Adyen", "Braintree", "Square"],
    market_leader="Stripe",
    competitive_advantages=[
        "Simpler onboarding than incumbents",
        "Deeper vertical-specific features",
        "Lower transaction fees for SMBs",
    ],
    competitive_disadvantages=[
        "Smaller brand recognition",
        "Narrower global coverage than Adyen",
    ],
    barriers_to_entry=[
        "Payment network relationships",
        "Regulatory licensing across jurisdictions",
        "Trust and compliance certifications",
    ],
    competition_intensity="High",
    competition_score=6.5,
    summary="Competitive but addressable market with strong differentiation on developer experience and SMB focus.",
)

STRONG_FOUNDER = FounderAnalysis(
    founders=["Jane Smith", "Alex Chen"],
    education=["MIT Computer Science (Jane)", "Stanford MBA (Alex)"],
    professional_experience=[
        "Jane: 8 years at PayPal, led payments API team",
        "Alex: 6 years at Goldman Sachs fintech division",
    ],
    domain_expertise=["Payment processing", "Financial compliance", "Developer tooling"],
    technical_expertise=["Distributed systems", "PCI-DSS compliance", "API design"],
    previous_startups=["Jane co-founded PayKit (acquired by PayPal 2018)"],
    previous_exits=["PayKit — acquired by PayPal for $45M (2018)"],
    strengths=[
        "Deep domain expertise in payments",
        "Prior successful exit",
        "Complementary technical and business skill sets",
    ],
    risks=["First time as CEO for Jane", "Small founding team of two"],
    founder_market_fit="Exceptional — founders built payments infrastructure at scale",
    execution_capability="High — prior exit and industry relationships",
    founder_score=8.8,
    summary="Highly credible founding team with direct payments domain expertise and a prior exit.",
)

STRONG_FINANCE = FinanceAnalysis(
    funding_rounds=[
        FundingRound(
            round_name="Seed",
            amount_raised="$3M",
            date="2022-06",
            lead_investors=["First Round Capital"],
            participating_investors=["Angel investors"],
        ),
        FundingRound(
            round_name="Series A",
            amount_raised="$18M",
            date="2023-09",
            lead_investors=["Andreessen Horowitz"],
            participating_investors=["First Round Capital", "Stripe"],
        ),
    ],
    total_funding="$21M",
    valuation="$120M post-money (Series A)",
    revenue_signals=[
        "$2.5M ARR growing 15% MoM",
        "150 paying enterprise customers",
        "Net revenue retention of 125%",
    ],
    burn_rate_signals=[
        "18-month runway at current burn",
        "Burn multiple of 1.2x (efficient)",
    ],
    financial_strengths=[
        "Strong NRR indicates product-market fit",
        "Tier-1 lead investors add credibility",
        "Efficient burn relative to growth",
    ],
    financial_risks=[
        "Pre-profitability",
        "Fundraising market may tighten before Series B",
    ],
    finance_score=8.0,
    score_category="Strong",
    score_rationale="Strong revenue growth, tier-1 backers, efficient burn, and healthy NRR.",
    investment_recommendation="Invest",
    funding_summary="Well-funded with $21M raised, strong growth metrics, and tier-1 backing.",
)

STRONG_RISK = RiskAnalysis(
    technology_risks=["Payment gateway dependencies", "PCI-DSS scope expansion risk"],
    market_risks=["Big tech players bundling payments", "Macro slowdown reducing SMB spend"],
    regulatory_risks=["PSD2 compliance in Europe", "Evolving AML regulations"],
    operational_risks=["Scaling customer support with growth", "Key-person dependency on Jane"],
    execution_risks=["Hiring senior engineering talent in competitive market"],
    risk_mitigations=[
        "PCI-DSS Level 1 certification already obtained",
        "Legal counsel retained for EU expansion",
        "Series A funding provides 18-month runway",
    ],
    risk_score=3.5,
    score_category="Moderate Risk",
    score_rationale="Manageable risks for a payments infrastructure startup at this stage.",
    key_risks=["Regulatory compliance costs", "Key-person dependency", "Big tech competitive pressure"],
    recommendation="Proceed with Caution",
    summary="Risk profile is moderate and manageable. Key risks are addressable with proper planning.",
)

STRONG_INVESTMENT = InvestmentAnalysis(
    investment_strengths=[
        "Exceptional founding team with prior exit",
        "Large and growing TAM",
        "Strong NRR of 125% signals product-market fit",
        "Tier-1 investor backing",
    ],
    investment_weaknesses=[
        "Pre-profitability with 18-month runway",
        "Small team in a competitive market",
    ],
    opportunities=[
        "Expand into LATAM and SEA payments",
        "Launch B2B invoice financing product",
    ],
    threats=[
        "Stripe expanding downmarket to SMBs",
        "Regulatory changes in key EU markets",
    ],
    investment_score=8.2,
    score_category="Strong",
    score_rationale="Strong team, proven traction, large market, manageable risk — compelling Series A investment.",
    recommendation="INVEST",
    investment_thesis="API-first payments platform targeting underserved SMBs with superior developer experience.",
    executive_summary="Compelling Series A investment with strong fundamentals, experienced founders, and clear path to $10M ARR.",
)

STRONG_MEMO = MemoReport(
    executive_summary="PayFlow is a high-conviction investment opportunity at Series A, combining exceptional founders with strong early traction in a $2.5T market.",
    market_analysis="The global payments market is $2.5T and growing at 14% CAGR, with strong tailwinds for API-first infrastructure providers targeting SMBs.",
    competition_analysis="Stripe dominates but leaves SMB and emerging market segments underserved. PayFlow's pricing and developer experience differentiate meaningfully.",
    founder_analysis="Jane Smith (PayPal) and Alex Chen (Goldman) bring rare domain depth and a prior exit, significantly de-risking execution.",
    financial_analysis="$21M raised, $2.5M ARR growing 15% MoM, 125% NRR. Efficient burn with 18-month runway.",
    risk_analysis="Moderate risk profile. PCI-DSS certified. Key risks are regulatory complexity and key-person dependency — both manageable.",
    key_strengths=["Prior exit", "125% NRR", "Tier-1 backers", "PCI certified"],
    key_concerns=["Pre-profitability", "Small team", "Big tech competition"],
    investment_thesis="API-first payments infrastructure for underserved SMBs with clear path to market leadership.",
    recommendation="Invest",
    next_steps=["Reference check Jane's PayPal leadership", "Validate EU licensing timeline", "Review Series B fundraising plan"],
    conclusion="PayFlow represents a strong investment with a credible team, proven traction, and a large addressable market.",
)

# ---------------------------------------------------------------------------
# Weak startup (vague social app, no traction, unknown founders)
# ---------------------------------------------------------------------------

WEAK_MARKET = MarketAnalysis(
    industry="Social Media",
    market_size="Unclear, possibly $50B adjacent",
    growth_rate="Flat to declining in core segments",
    market_stage="Saturated",
    customer_segments=["Gen Z"],
    key_trends=["Short-form video saturation", "Platform fatigue"],
    opportunities=[],
    risks=["TikTok dominance", "Meta copying features", "Regulatory pressure", "User acquisition costs"],
    market_score=2.0,
    summary="Highly saturated social media market with no clear differentiation identified.",
)

WEAK_COMPETITION = CompetitionAnalysis(
    competitors=["TikTok", "Instagram", "BeReal", "Snapchat"],
    market_leader="TikTok",
    competitive_advantages=["Unclear"],
    competitive_disadvantages=["No brand recognition", "No network effects", "No differentiation"],
    barriers_to_entry=["None identified — low barrier means easy to copy"],
    competition_intensity="Extreme",
    competition_score=1.5,
    summary="Extreme competition from well-funded incumbents with no clear moat identified.",
)

WEAK_FOUNDER = FounderAnalysis(
    founders=["Unknown Founder"],
    education=["Unverified"],
    professional_experience=["No relevant experience found"],
    domain_expertise=[],
    technical_expertise=[],
    previous_startups=[],
    previous_exits=[],
    strengths=["Passion for the product"],
    risks=["No domain expertise", "No prior startup experience", "No network in industry"],
    founder_market_fit="Weak — no evidence of relevant experience",
    execution_capability="Unknown",
    founder_score=2.0,
    summary="Founding team lacks verifiable experience, domain expertise, or prior startup track record.",
)

WEAK_FINANCE = FinanceAnalysis(
    funding_rounds=[],
    total_funding=None,
    valuation=None,
    revenue_signals=["No revenue signals found"],
    burn_rate_signals=["Unknown burn rate"],
    financial_strengths=[],
    financial_risks=["No funding", "No revenue", "Unknown burn", "No investor validation"],
    finance_score=1.5,
    score_category="High Risk",
    score_rationale="No funding, no revenue, and no investor validation at any stage.",
    investment_recommendation="Pass",
    funding_summary="No funding history found. Pre-revenue with no evidence of investor interest.",
)

WEAK_RISK = RiskAnalysis(
    technology_risks=["No technical differentiation"],
    market_risks=["Saturated market", "Platform fatigue"],
    regulatory_risks=["GDPR and COPPA exposure for youth audience"],
    operational_risks=["No team depth", "No advisors identified"],
    execution_risks=["High likelihood of pivoting without clear strategy"],
    risk_mitigations=[],
    risk_score=8.5,
    score_category="Critical Risk",
    score_rationale="Combination of weak team, saturated market, no traction, and no funding creates critical risk.",
    key_risks=["No differentiation", "No funding", "Unknown team", "Extreme competition"],
    recommendation="Avoid",
    summary="Critical risk profile. No mitigating factors identified.",
)

WEAK_INVESTMENT = InvestmentAnalysis(
    investment_strengths=["Early stage — upside exists theoretically"],
    investment_weaknesses=[
        "Saturated market",
        "Unknown founding team",
        "No traction",
        "No funding",
        "No differentiation",
    ],
    opportunities=["Niche community focus could reduce competition"],
    threats=["TikTok", "Instagram Reels", "Snapchat", "Meta"],
    investment_score=1.8,
    score_category="High Risk",
    score_rationale="Weak team, saturated market, no traction, and critical risk profile make this uninvestable at this stage.",
    recommendation="PASS",
    investment_thesis="No compelling thesis identified. Generic social app in a saturated market.",
    executive_summary="Pass. No differentiation, unknown team, no traction, and extreme competition with well-funded incumbents.",
)
