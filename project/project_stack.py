import aws_cdk as core
from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct

class ProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        
        instance_name = self.node.try_get_context("InstanceName") or "MV Reemplazar"
        ami_id = self.node.try_get_context("AMI") or "ami-0aa28dab1f2852040"
        role = self.format_arn(service='iam', region='', account=self.account, resource='role/LabRole')
        
        # Security Group
        security_group = ec2.SecurityGroup(
            self, "InstanceSecurityGroup",
            vpc=ec2.Vpc.from_lookup(self, "MyDefaultVPC", is_default=True),
            description="Permitir trafico SSH y HTTP desde cualquier lugar",
            allow_all_outbound=True
        )

        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Permitir SSH"
        )

        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Permitir HTTP"
        )

        # EC2 Instance
        instance = ec2.Instance(
            self, "EC2Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.generic_linux({
                "us-east-1": ami_id
            }),
            vpc=ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True),
            security_group=security_group,
            key_name="vockey",  # Asegúrate de tener esta llave en tu cuenta de AWS
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(20)
                )
            ],
            role=iam.Role.from_role_arn(self, "InstanceRole", role)
        )

        instance.add_user_data(
            "#!/bin/bash",
            "cd /var/www/html/",
            "git clone https://github.com/utec-cc-2024-2-test/websimple.git",
            "git clone https://github.com/utec-cc-2024-2-test/webplantilla.git",
            "ls -l"
        )

        # Outputs
        core.CfnOutput(
            self, "InstanceId",
            value=instance.instance_id,
            description="ID de la instancia EC2"
        )

        core.CfnOutput(
            self, "InstancePublicIP",
            value=instance.instance_public_ip,
            description="IP pública de la instancia"
        )

        core.CfnOutput(
            self, "websimpleURL",
            value=f"http://{instance.instance_public_ip}/websimple",
            description="URL de websimple"
        )

        core.CfnOutput(
            self, "webplantillaURL",
            value=f"http://{instance.instance_public_ip}/webplantilla",
            description="URL de webplantilla"
        )
