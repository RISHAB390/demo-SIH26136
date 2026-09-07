from dataclasses import dataclass

@dataclass
class DecisionSupportResult:
    pilot_id: int
    total_kpis: int
    approved_kpis: int
    achievement_ratio: float
    recommendation: str
    explanation: str

def compute_decision_support(pilot_id: int, total_kpis: int, approved_kpis: int) -> DecisionSupportResult:
    """
    Pure, deterministic calculation of pilot decision support recommendations.
    Independent of AI/ML, zero external calls, and guarded against division by zero.
    """
    if total_kpis == 0:
        return DecisionSupportResult(
            pilot_id=pilot_id,
            total_kpis=0,
            approved_kpis=0,
            achievement_ratio=0.0,
            recommendation="Insufficient Data",
            explanation="No KPIs have been established for this pilot."
        )

    ratio = approved_kpis / total_kpis
    # Round ratio to 2 decimal places for clean reporting
    achievement_ratio = round(ratio, 2)

    if ratio >= 0.70:
        recommendation = "Recommend Scale"
    elif ratio >= 0.40:
        recommendation = "Extend Pilot"
    else:
        recommendation = "Discontinue"

    explanation = f"{approved_kpis} of {total_kpis} KPIs have approved evidence ({round(ratio * 100, 1)}% achieved)."

    return DecisionSupportResult(
        pilot_id=pilot_id,
        total_kpis=total_kpis,
        approved_kpis=approved_kpis,
        achievement_ratio=achievement_ratio,
        recommendation=recommendation,
        explanation=explanation
    )
