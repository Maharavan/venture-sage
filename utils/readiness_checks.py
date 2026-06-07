import os
import boto3
from utils.console import print_error
from botocore.exceptions import NoCredentialsError,ClientError
def check_aws_credentials() -> bool:
    """AWS tool checks for credentials and required environment variables."""
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials is None:
            print_error("AWS credentials not found. Please configure your AWS credentials.")
            return False
        else:
            return True
    except NoCredentialsError as e:
        print_error(f"No AWS credentials found: {e}")
        return False
    except ClientError as e:
        print_error(f"Error checking AWS credentials: {e}")
        return False
    except Exception as e:
        print_error(f"An unexpected error occurred while checking AWS credentials: {e}")
        return False

def check_tool_environments() -> bool:
    """Verify that all required API keys are present in the environment."""
    env_keys = [
        'EXA_API_KEY',
        'TAVILY_API_KEY',
        'NEWSAPI_KEY',
        'SERPAPI_API_KEY',
        'FIRECRAWL_API_KEY'
    ]

    missing_keys = [ key for key in env_keys if not os.getenv(key)]

    if missing_keys:
        print_error(f"Missing API keys: {', '.join(missing_keys)}")
        return False
    return True