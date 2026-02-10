import boto3
from botocore.exceptions import ClientError, BotoCoreError

def fetch_s3_buckets():
    try:
        s3 = boto3.client("s3")
        response = s3.list_buckets()

        buckets = []

        for bucket in response.get("Buckets", []):
            name = bucket.get("Name")

            public = False
            versioning = False
            encryption = False

            try:
                acl = s3.get_bucket_acl(Bucket=name)
                public = any(
                    grant.get("Grantee", {}).get("URI", "").endswith("AllUsers")
                    for grant in acl.get("Grants", [])
                )
            except ClientError:
                pass

            try:
                ver = s3.get_bucket_versioning(Bucket=name)
                versioning = ver.get("Status") == "Enabled"
            except ClientError:
                pass

            try:
                enc = s3.get_bucket_encryption(Bucket=name)
                encryption = "ServerSideEncryptionConfiguration" in enc
            except ClientError:
                pass

            try:
                pab = s3.get_public_access_block(Bucket=name)
                block = pab["PublicAccessBlockConfiguration"]
                if not all(block.values()):
                    public = True
            except ClientError:
                pass

            buckets.append(
                {
                    "name": name,
                    "public": public,
                    "versioning": versioning,
                    "encryption": encryption,
                }
            )

        return buckets

    except (ClientError, BotoCoreError) as error:
        print(f"S3 fetch error: {error}")
        return []