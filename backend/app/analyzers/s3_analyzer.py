def analyze_s3_buckets(buckets):
    issues = []

    for b in buckets:
        if b["public"]:
            issues.append(
                {
                    "service": "S3",
                    "resource": b["name"],
                    "region": "global",
                    "severity": "HIGH",
                    "issue": "S3 bucket is publicly accessible",
                    "why": "Public buckets can expose sensitive data.",
                    "suggested_fix": "Disable public access and review bucket policy.",
                }
            )

        if not b["encryption"]:
            issues.append(
                {
                    "service": "S3",
                    "resource": b["name"],
                    "region": "global",
                    "severity": "MEDIUM",
                    "issue": "S3 bucket encryption not enabled",
                    "why": "Data at rest should be encrypted for security compliance.",
                    "suggested_fix": "Enable default encryption (SSE-S3 or SSE-KMS).",
                }
            )

        if not b["versioning"]:
            issues.append(
                {
                    "service": "S3",
                    "resource": b["name"],
                    "region": "global",
                    "severity": "LOW",
                    "issue": "S3 bucket versioning disabled",
                    "why": "Versioning protects against accidental deletion or overwrite.",
                    "suggested_fix": "Enable bucket versioning.",
                }
            )

    return issues