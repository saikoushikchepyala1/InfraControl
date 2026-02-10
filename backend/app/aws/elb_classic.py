import boto3

def fetch_classic_elbs(region):
    """
    Fetch Classic ELBs in a region.
    """
    try:
        client = boto3.client("elb", region_name=region)
        response = client.describe_load_balancers()

        return response.get("LoadBalancerDescriptions", [])
    except Exception as e:
        print(f"Classic ELB error {region}: {e}")
        return []