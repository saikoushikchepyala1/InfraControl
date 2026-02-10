import boto3
from botocore.exceptions import ClientError, BotoCoreError

def fetch_lambda_functions(region: str):
    try:
        client = boto3.client("lambda", region_name=region)
        paginator = client.get_paginator("list_functions")

        results = []

        for page in paginator.paginate():
            for fn in page.get("Functions", []):
                results.append({
                    "name": fn["FunctionName"],
                    "region": region,
                    "runtime": fn.get("Runtime"),
                    "timeout": fn.get("Timeout"),
                })

        return results

    except (ClientError, BotoCoreError) as e:
        print(f"Lambda error {region}: {e}")
        return []