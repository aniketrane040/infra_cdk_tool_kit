from aws_cdk import (
    Stack,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2
)
from constructs import Construct

class UnionInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, 
                    'union_vpc',
                    ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
                    max_azs=2)
        
        union_sg = ec2.SecurityGroup(self,
                                'app_security_group',
                                vpc=vpc)

        union_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP traffic")
        union_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(3000), "Allow HTTP traffic")

        # union_backend_ecr = ecr.Repository.from_repository_name(self,'union_backend_repo','union-backend-app')

        union_task_def = ecs.FargateTaskDefinition(self,'app_task',
                                                cpu=1024,
                                                memory_limit_mib=2048)
                                                
        union_task_def.add_container('union_backend_container',
                                    # image=ecs.ContainerImage.from_ecr_repository(union_backend_ecr),
                                    image=ecs.ContainerImage.from_registry('public.ecr.aws/m7p9x7q8/union-backend-app:latest'),
                                    cpu=512,
                                    memory_limit_mib=512,
                                    port_mappings=[ecs.PortMapping(container_port=3000)])

        union_task_def.add_container('mongo_container',
                                    image=ecs.ContainerImage.from_registry('mongo'),
                                    cpu=512,
                                    memory_limit_mib=512,
                                    port_mappings=[ecs.PortMapping(container_port=27017)],
                                    environment={
                                        'MONGO_INITDB_ROOT_USERNAME': 'mongoadmin',
                                        'MONGO_INITDB_ROOT_PASSWORD': 'secret'
                                    })

        cluster = ecs.Cluster(self,'union_cluster',vpc=vpc)

        union_service = ecs.FargateService(self, 'fargate_union_service',
                        cluster=cluster,
                        task_definition=union_task_def,
                        security_groups=[union_sg])

        # Add auto scaling group to cluster

        lb = elbv2.ApplicationLoadBalancer(self, 
                                        id='application_load_balancer',
                                        load_balancer_name='union-load-balancer',
                                        security_group=union_sg,
                                        internet_facing=True,
                                        vpc=vpc)
        
        tg = elbv2.ApplicationTargetGroup(self,
                                        'union_tg',
                                        port=3000,
                                        protocol=elbv2.ApplicationProtocol.HTTP,
                                        target_group_name='union-target-group',
                                        target_type=elbv2.TargetType.IP,
                                        vpc=vpc)
        
        tg.add_target(union_service)
        
        listener = lb.add_listener("Listener",
                                port=80,
                                open=True)
        listener.add_target_groups("TargetGroup", target_groups=[tg])

        

        
