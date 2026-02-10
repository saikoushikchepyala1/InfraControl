import boto3
from botocore.exceptions import ClientError, BotoCoreError


def fetch_unattached_eips(region: str):
    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = ec2.describe_addresses()

        eips = []

        for addr in response.get("Addresses", []):
            if "InstanceId" not in addr and "NetworkInterfaceId" not in addr:
                eips.append({
                    "allocation_id": addr.get("AllocationId"),
                    "public_ip": addr.get("PublicIp"),
                    "region": region
                })

        return eips

    except (ClientError, BotoCoreError) as e:
        print(f"EIP error {region}: {e}")
        return []