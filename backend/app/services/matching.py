from dataclasses import dataclass

@dataclass
class EligibilityMatchResult:
    sector_match: bool
    dpiit_match: bool
    overall_aligned: bool
    sector_message: str
    dpiit_message: str
    guidance: str

def check_informational_eligibility(
    startup_sector: str,
    challenge_sector: str,
    startup_dpiit: bool,
    challenge_dpiit_required: bool
) -> EligibilityMatchResult:
    """
    Deterministic informational eligibility comparison.
    NEVER blocks application submission.
    """
    sector_match = startup_sector.strip().lower() == challenge_sector.strip().lower()
    
    # If challenge does not require DPIIT, it's always satisfied.
    # If challenge requires DPIIT, startup must be DPIIT recognized.
    if challenge_dpiit_required:
        dpiit_match = bool(startup_dpiit)
    else:
        dpiit_match = True

    overall_aligned = sector_match and dpiit_match

    sector_message = "Sector Match" if sector_match else "Sector Mismatch"
    dpiit_message = "DPIIT Status Match" if dpiit_match else "DPIIT Requirement Mismatch"
    
    guidance = (
        "Fully aligned with challenge requirements."
        if overall_aligned
        else "Informational notice: Some criteria differ from preferred specifications, but all startups may apply."
    )

    return EligibilityMatchResult(
        sector_match=sector_match,
        dpiit_match=dpiit_match,
        overall_aligned=overall_aligned,
        sector_message=sector_message,
        dpiit_message=dpiit_message,
        guidance=guidance
    )
