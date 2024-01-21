from aws_cdk import (
    Stack,
)
from constructs import Construct

class UnionInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # queue = sqs.Queue(
        #     self, "InfraCodeToolKitQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
