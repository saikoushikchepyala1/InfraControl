import boto3
from botocore.exceptions import ClientError, BotoCoreError


def fetch_dynamodb_tables(region: str):
    try:
        client = boto3.client("dynamodb", region_name=region)
        paginator = client.get_paginator("list_tables")

        results = []

        for page in paginator.paginate():
            for name in page.get("TableNames", []):
                desc = client.describe_table(TableName=name)["Table"]

                sse = desc.get("SSEDescription")
                encrypted = bool(sse and sse.get("Status") == "ENABLED")

                results.append(
                    {
                        "name": name,
                        "region": region,
                        "status": desc.get("TableStatus"),
                        "encrypted": encrypted,
                    }
                )

        return results

    except (ClientError, BotoCoreError) as e:
        print(f"DynamoDB error {region}: {e}")
        return []