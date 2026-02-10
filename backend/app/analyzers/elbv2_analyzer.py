def analyze_load_balancers(load_balancers):
    issues = []

    for lb in load_balancers:
        issues.append({
            "service": "ELB",
            "resource": lb["name"],
            "region": lb["region"],
            "severity": "MEDIUM",
            "issue": "Idle load balancer (no targets)",
            "why": "Load balancers without traffic still incur cost.",
            "suggested_fix": "Delete the load balancer if unused."
        })

    return issues