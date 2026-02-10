def analyze_lambda_functions(functions):
    issues = []

    for fn in functions:
        if fn.get("timeout", 0) > 30:
            issues.append({
                "service": "Lambda",
                "resource": fn["name"],
                "region": fn["region"],
                "severity": "LOW",
                "issue": "Lambda timeout unusually high",
                "why": "High timeout may indicate inefficient execution.",
                "suggested_fix": "Review function performance and reduce timeout.",
            })

    return issues