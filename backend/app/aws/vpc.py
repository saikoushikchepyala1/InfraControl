import boto3
from botocore.exceptions import ClientError, BotoCoreError

def fetch_vpcs(region: str):
    try:
        ec2 = boto3.client("ec2", region_name=region)

        vpcs = ec2.describe_vpcs()["Vpcs"]

        paginator = ec2.get_paginator("describe_flow_logs")
        flow_log_vpc_ids = set()

        for page in paginator.paginate():
            for fl in page.get("FlowLogs", []):
                flow_log_vpc_ids.add(fl["ResourceId"])

        results = []

        for v in vpcs:
            vpc_id = v["VpcId"]

            results.append({
                "id": vpc_id,
                "region": region,
                "is_default": v.get("IsDefault", False),
                "flow_logs_enabled": vpc_id in flow_log_vpc_ids,
                "has_resources": False
            })

        return results

    except (ClientError, BotoCoreError) as e:
        print(f"VPC error {region}: {e}")
        return []