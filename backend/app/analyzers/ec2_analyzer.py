def analyze_ec2_instances(instances):
    issues = []

    for instance in instances:
        instance_id = instance.get("instance_id")
        state = instance.get("state")

        if state == "running":
            issues.append({
                "service": "EC2",
                "resource": instance_id,
                "region": instance.get("region"),
                "severity": "MEDIUM",
                "issue": "Running EC2 instance detected",
                "why": "Running instances incur compute cost.",
                "suggested_fix": "Stop or terminate if not required."
            })

    return issues