import boto3
from boto3.session import Session
import datetime


def cpu(name, instanceID, instanceType):
    cw = boto3.client('cloudwatch',
                      region_name='eu-west-1')
    view = cw.get_metric_statistics(
        Period=60,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistics=['Average'],
        Dimensions=[{'Name': 'InstanceId', 'Value': instanceID}]
    )
    view['InstanceName'] = name
    view['InstanceType'] = instanceType
    data = graphData(view)
    return [view, data]


def memory(name, imageID, instanceType):
    cw = boto3.client('cloudwatch',
                      region_name='eu-west-1')
    view = cw.get_metric_statistics(
        Period=60,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='MemoryUtilization',
        Namespace='System/Linux',
        Statistics=['Average'],
        Dimensions=[{'Name': 'ImageId', 'Value': imageID}]
    )
    view['InstanceName'] = name
    view['InstanceType'] = instanceType
    data = graphData(view)
    return [view, data]


def databaseMemory(name, db, instanceType):
    cw = boto3.client('cloudwatch',
                      region_name='eu-west-1')
    view = cw.get_metric_statistics(
        Period=60,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='CPUUtilization',
        Namespace='AWS/RDS',
        Statistics=['Average'],
        Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': db}]
    )

    view['InstanceName'] = name
    view['InstanceType'] = instanceType
    data = graphData(view)
    return [view, data]


def redshift(name, db, instanceType):
    cw = boto3.client('cloudwatch',
                      region_name='eu-west-1')
    view = cw.get_metric_statistics(
        Period=60,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=3600),
        EndTime=datetime.datetime.utcnow(),
        MetricName='CPUUtilization',
        Namespace='AWS/Redshift',
        Statistics=['Average'],
        Dimensions=[{'Name': 'ClusterIdentifier',
                     'Value': db}, {'Name': 'NodeID', 'Value': 'Leader'}]
    )
    view['InstanceName'] = name
    view['InstanceType'] = instanceType
    data = graphData(view)
    return [view, data]


def graphData(view):
    data = []
    for points in view['Datapoints']:
        data.append([points['Timestamp'].strftime('%Y-%m-%d %H:%M:%S'), points['Average']])

    data = sorted(data, key=lambda x: x[0])
    return data


def dataPipeline(pipelineID):
    cw = boto3.client('datapipeline',
                      region_name='eu-west-1')
    response = cw.describe_pipelines(pipelineIds=[pipelineID])
    return response
