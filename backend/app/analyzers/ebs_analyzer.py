def analyze_ebs_volumes(volumes):
    issues = []

    for v in volumes:
        issues.append({
            "service": "EBS",
            "resource": v["volume_id"],
            "region": v["region"],
            "severity": "MEDIUM",
            "issue": "Unattached EBS volume",
            "why": "Unattached EBS volumes are billed even when not used.",
            "suggested_fix": "Delete the volume if not required."
        })

    return issues