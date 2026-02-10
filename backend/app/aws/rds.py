import boto3
from botocore.exceptions import ClientError, BotoCoreError

def fetch_rds_instances(region: str):
    try:
        client = boto3.client("rds", region_name=region)
        paginator = client.get_paginator("describe_db_instances")

        results = []

        for page in paginator.paginate():
            for db in page.get("DBInstances", []):
                results.append({
                    "id": db["DBInstanceIdentifier"],
                    "region": region,
                    "public": db.get("PubliclyAccessible"),
                    "encrypted": db.get("StorageEncrypted"),
                    "status": db.get("DBInstanceStatus"),
                })

        return results

    except (ClientError, BotoCoreError) as e:
        print(f"RDS error {region}: {e}")
        return []