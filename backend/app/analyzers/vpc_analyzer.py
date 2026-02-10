def analyze_vpcs(vpcs):
    issues = []

    for vpc in vpcs:
        is_default = vpc.get("is_default", False)
        has_resources = vpc.get("has_resources", False)
        flow_logs_enabled = vpc.get("flow_logs_enabled", False)

        if is_default and not has_resources:
            continue

        if is_default:
            issues.append({
                "service": "VPC",
                "resource": vpc["id"],
                "region": vpc["region"],
                "issue": "Default VPC in use",
                "severity": "LOW",
                "why": "Default VPCs often contain permissive security settings.",
                "suggested_fix": "Create and use a custom VPC with restricted rules."
            })

        if not flow_logs_enabled:
            issues.append({
                "service": "VPC",
                "resource": vpc["id"],
                "region": vpc["region"],
                "issue": "VPC Flow Logs not enabled",
                "severity": "MEDIUM",
                "why": "Flow logs are required for network monitoring and auditing.",
                "suggested_fix": "Enable VPC Flow Logs for security visibility."
            })

    return issues