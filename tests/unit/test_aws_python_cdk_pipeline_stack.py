import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_python_cdk_pipeline.aws_python_cdk_pipeline_stack import AwsPythonCdkPipelineStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_python_cdk_pipeline/aws_python_cdk_pipeline_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsPythonCdkPipelineStack(app, "aws-python-cdk-pipeline")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
