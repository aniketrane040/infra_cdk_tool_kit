from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2
)
from constructs import Construct

class UnionInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, 
                    'union_vpc',
                    cidr='0.0.0.0/16',
                    max_azs=2)

        alb_sg = ec2.SecurityGroup(self,
                                'alb_security_group',
                                vpc=vpc)

        lb = elbv2.ApplicationLoadBalancer(self, 
                                        id='application_load_balancer',
                                        load_balancer_name='union_load_balancer',
                                        security_group=alb_sg,
                                        vpc=vpc)

        tg = elbv2.ApplicationTargetGroup(self,
                                        'union_tg',
                                        port=80,
                                        protocol=elbv2.ApplicationProtocol.HTTP,
                                        target_group_name='union_target_group')

        
