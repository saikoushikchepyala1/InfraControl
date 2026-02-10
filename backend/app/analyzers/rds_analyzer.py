def analyze_rds_instances(instances):
    issues = []

    for db in instances:
        if db["public"]:
            issues.append({
                "service": "RDS",
                "resource": db["id"],
                "region": db["region"],
                "severity": "HIGH",
                "issue": "RDS instance publicly accessible",
                "why": "Public databases expose sensitive data.",
                "suggested_fix": "Disable public accessibility and use private subnets.",
            })

        if not db["encrypted"]:
            issues.append({
                "service": "RDS",
                "resource": db["id"],
                "region": db["region"],
                "severity": "MEDIUM",
                "issue": "RDS storage not encrypted",
                "why": "Encryption is required for compliance and security.",
                "suggested_fix": "Enable storage encryption.",
            })

    return issues