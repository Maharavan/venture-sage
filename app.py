from __future__ import annotations
from workflow.due_dilegence_workflow import due_dil_workflow
from utils.console import print_success, print_banner
from utils.readiness_checks import check_aws_credentials,check_tool_environments
from cli.chat import ChatTerminal

if __name__ == "__main__":
    if not check_aws_credentials():
        exit(1)
    print_success("AWS credentials check passed.")
    if not check_tool_environments():
        exit(1)
    print_success("Tool environments check passed.")
    print_banner()
    ChatTerminal().chat_ui()
