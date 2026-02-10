import boto3
import traceback
from backend.app.core.config import AWS_REGION

from backend.app.aws.ec2 import fetch_ec2_instances
from backend.app.aws.s3 import fetch_s3_buckets
from backend.app.aws.iam import fetch_iam_users
from backend.app.aws.ebs import fetch_unattached_ebs
from backend.app.aws.eip import fetch_unattached_eips
from backend.app.aws.elbv2 import fetch_idle_load_balancers
from backend.app.aws.elb_classic import fetch_classic_elbs
from backend.app.aws.dynamodb import fetch_dynamodb_tables
from backend.app.aws.lambda_service import fetch_lambda_functions
from backend.app.aws.rds import fetch_rds_instances
from backend.app.aws.vpc import fetch_vpcs

from backend.app.analyzers.ec2_analyzer import analyze_ec2_instances
from backend.app.analyzers.s3_analyzer import analyze_s3_buckets
from backend.app.analyzers.iam_analyzer import analyze_iam_users
from backend.app.analyzers.dynamodb_analyzer import analyze_dynamodb_tables
from backend.app.analyzers.lambda_analyzer import analyze_lambda_functions
from backend.app.analyzers.rds_analyzer import analyze_rds_instances
from backend.app.analyzers.vpc_analyzer import analyze_vpcs
from backend.app.analyzers.ebs_analyzer import analyze_ebs_volumes
from backend.app.analyzers.eip_analyzer import analyze_eips
from backend.app.analyzers.elbv2_analyzer import analyze_load_balancers


def get_all_regions():
    ec2 = boto3.client("ec2", region_name=AWS_REGION)

    regions = ec2.describe_regions(AllRegions=True)["Regions"]

    enabled = [
        r["RegionName"]
        for r in regions
        if r["OptInStatus"] in ("opt-in-not-required", "opted-in")
    ]

    return enabled


def safe_fetch(fetch_fn, *args, **kwargs):
    try:
        return fetch_fn(*args, **kwargs)
    except Exception as e:
        print(f"[fetch error] {fetch_fn.__name__} {args} -> {e}")
        traceback.print_exc()
        return []


def scan_account():
    regions = get_all_regions()

    all_issues = []
    inventory = {}

    summary = {
        "EC2": 0,
        "S3": 0,
        "IAM": 0,
        "DynamoDB": 0,
        "Lambda": 0,
        "RDS": 0,
        "VPC": 0,
        "EBS": 0,
        "EIP": 0,
        "ELB": 0,
        "InfraUsage": 0,
    }

    for region in regions:
        ec2_instances = safe_fetch(fetch_ec2_instances, region)
        dynamo_tables = safe_fetch(fetch_dynamodb_tables, region)
        lambda_functions = safe_fetch(fetch_lambda_functions, region)
        rds_instances = safe_fetch(fetch_rds_instances, region)
        vpcs = safe_fetch(fetch_vpcs, region)
        load_balancers = safe_fetch(fetch_idle_load_balancers, region)
        classic_elbs = safe_fetch(fetch_classic_elbs, region)
        ebs_volumes = safe_fetch(fetch_unattached_ebs, region)
        eip_addresses = safe_fetch(fetch_unattached_eips, region)
        has_workload = bool(ec2_instances or rds_instances or lambda_functions or dynamo_tables)

        if has_workload:
            for v in vpcs:
                v["has_resources"] = True
        if any([
            ec2_instances,
            dynamo_tables,
            lambda_functions,
            rds_instances,
            vpcs,
            ebs_volumes,
            eip_addresses,
            load_balancers,
            classic_elbs,
        ]):
            inventory[region] = {
                "EC2": len(ec2_instances),
                "DynamoDB": len(dynamo_tables),
                "Lambda": len(lambda_functions),
                "RDS": len(rds_instances),
                "VPC": len([
                    v for v in vpcs
                    if not (v.get("is_default", False) and not v.get("has_resources", False))
                ]),
                "EBS": len(ebs_volumes),
                "EIP": len(eip_addresses),
                "ELB": len(load_balancers) + len(classic_elbs),
            }

        ec2_issues = analyze_ec2_instances(ec2_instances)
        dynamo_issues = analyze_dynamodb_tables(dynamo_tables)
        lambda_issues = analyze_lambda_functions(lambda_functions)
        rds_issues = analyze_rds_instances(rds_instances)
        vpc_issues = analyze_vpcs(vpcs)
        ebs_issues = analyze_ebs_volumes(ebs_volumes)
        eip_issues = analyze_eips(eip_addresses)
        elb_issues = analyze_load_balancers(load_balancers)

        for group in [
            ec2_issues,
            dynamo_issues,
            lambda_issues,
            rds_issues,
            vpc_issues,
            ebs_issues,
            eip_issues,
            elb_issues,
        ]:
            for issue in group:
                issue["region"] = issue.get("region", region)

        all_issues.extend(
            ec2_issues
            + dynamo_issues
            + lambda_issues
            + rds_issues
            + vpc_issues
            + ebs_issues
            + eip_issues
            + elb_issues
        )

        summary["EC2"] += len(ec2_issues)
        summary["DynamoDB"] += len(dynamo_issues)
        summary["Lambda"] += len(lambda_issues)
        summary["RDS"] += len(rds_issues)
        summary["VPC"] += len(vpc_issues)
        summary["EBS"] += len(ebs_issues)
        summary["EIP"] += len(eip_issues)
        summary["ELB"] += len(elb_issues) + len(classic_elbs)

    s3_buckets = safe_fetch(fetch_s3_buckets)
    iam_users = safe_fetch(fetch_iam_users)

    s3_issues = analyze_s3_buckets(s3_buckets)
    iam_issues = analyze_iam_users(iam_users)

    for issue in s3_issues + iam_issues:
        issue["region"] = issue.get("region", "global")

    all_issues.extend(s3_issues + iam_issues)

    summary["S3"] = len(s3_issues)
    summary["IAM"] = len(iam_issues)

    return {
        "regions_scanned": regions,
        "inventory": {r: v for r, v in inventory.items() if any(v.values())},
        "summary": {
            "total_issues": len(all_issues),
            "by_service": summary,
        },
        "issues": all_issues,
    }