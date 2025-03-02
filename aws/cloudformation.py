import boto3
from botocore import exceptions

from models import CloudFormationParameter


def _check_exist_stack(cfn, stack_name: str) -> bool:
    try:
        _ = cfn.describe_stacks(StackName=stack_name)
        return True
    except exceptions.ClientError as e:
        code = e.response["Error"]["Code"]
        msg = e.response["Error"]["Message"]
        if code == "ValidationError" and msg == f"Stack with id {stack_name} does not exist":
            return False
        raise e


def deploy_stack(
    stack_name: str,
    template_s3_key: str,
    parameters: list[CloudFormationParameter],
    bucket_name: str,
    wait_complete: bool = True,
    use_localstack: bool = False,
) -> str:
    cfn = boto3.client("cloudformation")

    if use_localstack:
        template_url = f"https://localhost.localstack.cloud:4566/{bucket_name}/{template_s3_key}"
    else:
        template_url = f"https://{bucket_name}.s3.amazonaws.com/{template_s3_key}"

    exist_stack = _check_exist_stack(cfn, stack_name)

    if exist_stack:
        res = cfn.update_stack(
            StackName=stack_name,
            TemplateURL=template_url,
            Parameters=[param.to_dict() for param in parameters],
            Capabilities=["CAPABILITY_IAM"],
            DisableRollback=True,
            RetainExceptOnCreate=True,
        )
    else:
        res = cfn.create_stack(
            StackName=stack_name,
            TemplateURL=template_url,
            Parameters=[param.to_dict() for param in parameters],
            DisableRollback=False,
            TimeoutInMinutes=20,
            Capabilities=["CAPABILITY_IAM"],
        )

    if not wait_complete:
        return res["StackId"]

    waiter_name = "stack_update_complete" if exist_stack else "stack_create_complete"
    print("Waiting for stack to be created or updated...")
    wait_complete_stack(stack_name=stack_name, waiter_name=waiter_name)

    return res["StackId"]


def wait_complete_stack(stack_name: str, waiter_name: str) -> None:
    cfn = boto3.client("cloudformation")

    waiter = cfn.get_waiter("stack_create_complete")
    waiter.wait(
        StackName=stack_name,
        WaiterConfig={
            "Delay": 10,
            "MaxAttempts": 15,
        },
    )
