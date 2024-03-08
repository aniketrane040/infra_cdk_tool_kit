#!/usr/bin/env python3
import os
import aws_cdk as cdk
from union_infra.union_infra_stack import UnionInfraStack

app = cdk.App()

acc_no = os.environ.get('AWS_ACCOUNT_NO')

UnionInfraStack(app, "UnionInfraStack",
    env=cdk.Environment(account=acc_no, region='us-east-1'),
    )

app.synth()
