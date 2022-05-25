from aws_cdk import (
    aws_codepipeline,
    aws_codepipeline_actions,
    aws_ssm,
    aws_codebuild,
    App, CfnOutput,SecretValue, Stack
)
from constructs import Construct

class AwsPythonPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        pipeline = aws_codepipeline.Pipeline(self, "Pipeline",pipeline_name="AWSPythonPipeline")
        cdk_source_output = aws_codepipeline.Artifact("CDK_GitHub_Source_Artifact")
        cdk_source_action = aws_codepipeline_actions.GitHubSourceAction(
                            action_name="CDK_GitHub_Source",
                            owner="Ruby1209",
                            repo="aws-python-cdk-pipeline",
                            oauth_token=SecretValue.secrets_manager("git_pip_token"),
                            branch="master",
                            output=cdk_source_output,
                            trigger = aws_codepipeline_actions.GitHubTrigger.POLL
            )
        pipeline.add_stage(
                        stage_name="Source",
                        actions=[cdk_source_action]
            )
        project = aws_codebuild.PipelineProject(self, "AWSPythonPipelineProject",
                            build_spec = aws_codebuild.BuildSpec.from_source_filename(
                                 "/cdk_buildspec.yml"
                        )
            )
        cdk_build_output = aws_codepipeline.Artifact()
        cdk_build_action = aws_codepipeline_actions.CodeBuildAction(
                            action_name="CDK_CodeBuild",
                            project=project,
                            input=cdk_source_output,
                            environment_variables={
                                "COMMIT_URL": aws_codebuild.BuildEnvironmentVariable(
                                    value=cdk_source_action.variables.commit_url
                                )
                            },
                            outputs = [cdk_build_output]
            )
        pipeline.add_stage(
                        stage_name="Build",
                        actions=[cdk_build_action] 
            )      
