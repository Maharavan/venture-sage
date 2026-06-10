from __future__ import annotations
import boto3
from botocore.exceptions import NoCredentialsError,ClientError
from workflow.due_dilegence_workflow import due_diligence_workflow
import asyncio

def check_aws_credentials():
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials is None:
            print("AWS credentials not found. Please configure your AWS credentials.")
            return False
        else:
            print("AWS credentials are configured correctly.")
            return True
    except NoCredentialsError as e:
        print(f"No AWS credentials found: {e}")
        return False
    except ClientError as e:
        print(f"Error checking AWS credentials: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while checking AWS credentials: {e}")
        return False
    
    
if __name__ == "__main__":
    if not check_aws_credentials():
        exit(1)
    print("AWS credentials check passed. You can proceed with running the application.")
    asyncio.run(due_diligence_workflow(startup_description="Analyze Cursor AI a startup that provides a code search tool for developers. The tool uses AI to help developers find relevant code snippets and documentation quickly, improving their productivity and efficiency so that I can invest."))
