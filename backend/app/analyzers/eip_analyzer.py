def analyze_eips(eips):
    issues = []

    for e in eips:
        issues.append({
            "service": "EC2",
            "resource": e["public_ip"],
            "region": e["region"],
            "severity": "HIGH",
            "issue": "Unattached Elastic IP",
            "why": "AWS charges for Elastic IPs not attached to instances.",
            "suggested_fix": "Release the Elastic IP if unused."
        })

    return issues