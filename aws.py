import boto3
import env
from boto3.session import Session
import datetime


def metrics(name, instanceID):
    cw = boto3.client('cloudwatch', region_name='eu-west-1')
    view = cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name': 'InstanceId', 'Value': instanceID}]
    )
    view['InstanceName'] = name

    return view


def memory(name, imageID):
    cw = boto3.client('cloudwatch', region_name='eu-west-1')
    view = cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='MemoryUtilization',
        Namespace='System/Linux',
        Statistics=['Average'],
        Dimensions=[{'Name': 'ImageId', 'Value': imageID}]
    )
    view['InstanceName'] = name

    return view
