def analyze_dynamodb_tables(tables):
    issues = []

    for t in tables:
        if not t["encrypted"]:
            issues.append(
                {
                    "service": "DynamoDB",
                    "resource": t["name"],
                    "region": t["region"],
                    "severity": "MEDIUM",
                    "issue": "DynamoDB table not encrypted",
                    "why": "Encryption at rest is required for data protection.",
                    "suggested_fix": "Enable server-side encryption.",
                }
            )

    return issues