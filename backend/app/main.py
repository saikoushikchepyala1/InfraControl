from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.aws.ec2 import fetch_ec2_instances
from backend.app.aws.s3 import fetch_s3_buckets
from backend.app.aws.iam import fetch_iam_users

from backend.app.analyzers.ec2_analyzer import analyze_ec2_instances
from backend.app.analyzers.s3_analyzer import analyze_s3_buckets
from backend.app.analyzers.iam_analyzer import analyze_iam_users

from backend.app.core.orchestrator import scan_account

app = FastAPI(
    title="InfraControl",
    description="Cloud Infrastructure Visibility and Control Platform",
    version="1.0.0"
)


app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)


@app.get("/health")
def health():
    return {"status": "InfraControl backend running"}


@app.get("/analyze/ec2")
def analyze_ec2(region: str = "us-east-1"):
    instances = fetch_ec2_instances(region)
    issues = analyze_ec2_instances(instances)

    return {
        "service": "EC2",
        "region": region,
        "issues_found": len(issues),
        "issues": issues
    }


@app.get("/analyze/s3")
def analyze_s3():
    buckets = fetch_s3_buckets()
    issues = analyze_s3_buckets(buckets)

    return {
        "service": "S3",
        "issues_found": len(issues),
        "issues": issues
    }


@app.get("/analyze/iam")
def analyze_iam():
    users = fetch_iam_users()
    issues = analyze_iam_users(users)

    return {
        "service": "IAM",
        "issues_found": len(issues),
        "issues": issues
    }


@app.get("/scan/account")
def scan_full_account():
    return scan_account()


@app.get("/")
def serve_dashboard():
    return FileResponse("frontend/index.html")