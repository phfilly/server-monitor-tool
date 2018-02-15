import boto3
from boto3.session import Session
import datetime


def metrics(name, instanceID):
    cw = boto3.client('cloudwatch', region_name='eu-west-1')
    view = cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=1200),
        EndTime=datetime.datetime.utcnow(),
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name': 'InstanceId', 'Value': instanceID}]
    )
    view['InstanceName'] = name
    dates = []
    values = []
    for points in view['Datapoints']:
        dates.append(points['Timestamp'])
        values.append(points['Average'])

    return [view, [dates, values]]


def memory(name, imageID):
    cw = boto3.client('cloudwatch', region_name='eu-west-1')
    view = cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=1200),
        EndTime=datetime.datetime.utcnow(),
        MetricName='MemoryUtilization',
        Namespace='System/Linux',
        Statistics=['Average'],
        Dimensions=[{'Name': 'ImageId', 'Value': imageID}]
    )
    view['InstanceName'] = name
    dates = []
    values = []
    for points in view['Datapoints']:
        dates.append(points['Timestamp'])
        values.append(points['Average'])

    return [view, [dates, values]]


def databaseMemory(name, db):
    cw = boto3.client('cloudwatch', region_name='eu-west-1')
    view = cw.get_metric_statistics(
        Period=300,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=1200),
        EndTime=datetime.datetime.utcnow(),
        MetricName='CPUUtilization',
        Namespace='AWS/RDS',
        Statistics=['Average'],
        Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': db}]
    )

    view['InstanceName'] = name
    dates = []
    values = []
    for points in view['Datapoints']:
        dates.append(points['Timestamp'])
        values.append(points['Average'])

    return [view, [dates, values]]
