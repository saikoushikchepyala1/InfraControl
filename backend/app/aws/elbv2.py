import boto3
from botocore.exceptions import ClientError, BotoCoreError


def fetch_idle_load_balancers(region: str):
    try:
        elb = boto3.client("elbv2", region_name=region)
        paginator = elb.get_paginator("describe_load_balancers")

        idle = []

        for page in paginator.paginate():
            for lb in page.get("LoadBalancers", []):

                try:
                    tg = elb.describe_target_groups(LoadBalancerArn=lb["LoadBalancerArn"])
                except ClientError:
                    continue

                target_groups = tg.get("TargetGroups", [])

                has_targets = False

                for g in target_groups:
                    try:
                        th = elb.describe_target_health(TargetGroupArn=g["TargetGroupArn"])
                        if th.get("TargetHealthDescriptions"):
                            has_targets = True
                            break
                    except ClientError:
                        continue

                if not has_targets:
                    idle.append({
                        "name": lb["LoadBalancerName"],
                        "arn": lb["LoadBalancerArn"],
                        "region": region
                    })

        return idle

    except (ClientError, BotoCoreError) as e:
        print(f"ELB error {region}: {e}")
        return []