import boto3
from botocore.exceptions import ClientError, BotoCoreError


def fetch_unattached_ebs(region: str):
    try:
        ec2 = boto3.client("ec2", region_name=region)
        paginator = ec2.get_paginator("describe_volumes")

        volumes = []

        for page in paginator.paginate(
            Filters=[{"Name": "status", "Values": ["available"]}]
        ):
            for vol in page.get("Volumes", []):
                volumes.append({
                    "volume_id": vol["VolumeId"],
                    "size": vol["Size"],
                    "region": region
                })

        return volumes

    except (ClientError, BotoCoreError) as e:
        print(f"EBS error {region}: {e}")
        return []