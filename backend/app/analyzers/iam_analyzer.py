from typing import List, Dict


def analyze_iam_users(users: List[Dict]) -> List[Dict]:
    """
    Analyze IAM users for security risks.

    """

    issues: List[Dict] = []

    for user in users:
        username = user.get("username")
        mfa_enabled = user.get("mfa_enabled")

        if not mfa_enabled:
            issues.append(
                {
                    "service": "IAM",
                    "resource": username,
                    "region": "global",  
                    "severity": "HIGH",
                    "issue": "IAM user does not have MFA enabled",
                    "why": "MFA is required to prevent unauthorized account access.",
                    "suggested_fix": "Enable MFA for this IAM user in AWS Console.",
                }
            )

    return issues