import boto3
from botocore.exceptions import ClientError, BotoCoreError


def fetch_iam_users():
    """
    Fetch AWS IAM users and evaluate their MFA configuration.
    IAM is a global AWS service and is not region-specific.
    """
    try:
        iam = boto3.client("iam")
        paginator = iam.get_paginator("list_users")

        users = []

        for page in paginator.paginate():
            for user in page.get("Users", []):
                username = user.get("UserName")

                try:
                    mfa_devices = iam.list_mfa_devices(UserName=username)
                    mfa_enabled = len(mfa_devices.get("MFADevices", [])) > 0
                
                except ClientError:
                    mfa_enabled = False

                users.append(
                    {
                        "username": username,
                        "mfa_enabled": mfa_enabled,
                    }
                )

        return users

    except (ClientError, BotoCoreError) as error:
        print(f"IAM fetch error: {error}")
        return []