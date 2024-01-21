import aws_cdk as core
import aws_cdk.assertions as assertions

from infra_code_tool_kit.infra_code_tool_kit_stack import InfraCodeToolKitStack

# example tests. To run these tests, uncomment this file along with the example
# resource in infra_code_tool_kit/infra_code_tool_kit_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = InfraCodeToolKitStack(app, "infra-code-tool-kit")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
