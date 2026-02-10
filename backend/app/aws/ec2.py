import boto3
from botocore.exceptions import ClientError, BotoCoreError

def fetch_ec2_instances(region: str):
    try:
        ec2 = boto3.client("ec2", region_name=region)
        paginator = ec2.get_paginator("describe_instances")

        results = []

        for page in paginator.paginate():
            for reservation in page.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    results.append({
                        "instance_id": instance.get("InstanceId"),
                        "instance_type": instance.get("InstanceType"),
                        "state": instance.get("State", {}).get("Name"),
                        "availability_zone": instance.get("Placement", {}).get("AvailabilityZone"),
                        "region": region,
                    })

        return results

    except (ClientError, BotoCoreError) as error:
        print(f"EC2 fetch error {region}: {error}")
        return []