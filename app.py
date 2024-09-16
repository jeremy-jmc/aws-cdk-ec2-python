#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import DefaultStackSynthesizer

from project.project_stack import ProjectStack


app = cdk.App()
ProjectStack(app, "ProjectStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.
    synthesizer = DefaultStackSynthesizer(
        bootstrap_stack_version_ssm_parameter="/cdk-bootstrap/${Qualifier}/version",
        bucket_prefix="",
        
        cloud_formation_execution_role="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/LabRole",
        
        deploy_role_arn="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/LabRole",
        deploy_role_external_id="",
        
        generate_bootstrap_version_rule=True,
        
        file_asset_publishing_role_arn="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/LabRole",
        file_asset_publishing_external_id="",
        file_assets_bucket_name="cdk-${Qualifier}-assets-${AWS::AccountId}-${AWS::Region}",
        
        image_asset_publishing_role_arn="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/LabRole",
        image_asset_publishing_external_id="",
        image_assets_repository_name="cdk-${Qualifier}-container-assets-${AWS::AccountId}-${AWS::Region}",

        lookup_role_arn="arn:${AWS::Partition}:iam::${AWS::AccountId}:role/LabRole",
        lookup_role_external_id="",
    ),
    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
