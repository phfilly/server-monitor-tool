import boto3
import datetime
import env
import time
from datetime import timedelta
from functools import reduce


def cpu(name, instanceID, instanceType):
    cw = boto3.client('cloudwatch',
                      region_name='eu-west-1',
                      aws_access_key_id=env.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY)
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
                      region_name='eu-west-1',
                      aws_access_key_id=env.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY)
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
                      region_name='eu-west-1',
                      aws_access_key_id=env.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY)
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
                      region_name='eu-west-1',
                      aws_access_key_id=env.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY)
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
        data.append([points['Timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                     points['Average'] if 'Average' in points else points['Sum']
                     ])

    average = reduce(lambda x, y: x + y, (avg[1] for avg in data))/len(data)

    data = sorted(data, key=lambda x: x[0])
    return [data, average]


def dataPipeline(pipelineID):
    try:
        cw = boto3.client('datapipeline',
                          region_name='eu-west-1',
                          aws_access_key_id=env.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY)
        pipelines = cw.list_pipelines()
        pipe_data = []
        for pipeline in pipelines['pipelineIdList']:
            pipe_data.append(pipeline['id'])

        response = cw.describe_pipelines(pipelineIds=pipe_data)
    except Exception as e:
        print('Pipeline Error', e)
        response = {'pipelineDescriptionList': [{'name': 'Something went wrong /"-.-"\ '}]}

    return response


def read_logs():
    client = boto3.client('logs',
                          region_name='eu-west-1',
                          aws_access_key_id=env.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY)

    group_name = 'docker-container-status'
    stream = 'Scrapers'
    result = {}
    logs_batch = client.get_log_events(logGroupName=group_name, logStreamName=stream)

    for event in logs_batch['events']:
        tmp = event['message'][1:-1].split(',')
        char = [char.replace('"', '') for char in tmp]
        char.append(event['timestamp'])

        """ THIS NEEDS TO BE CLEANED UP """

        if char[0] not in result:
            result.update({char[0]: [{'name': char[0],
                                      'status': char[1],
                                      'server': char[2],
                                      'ram': char[3],
                                      'time': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(char[-1]/1000.0))}]})
        else:
            result[char[0]][0]['status'] = char[1]
            result[char[0]][0]['server'] = char[2]
            result[char[0]][0]['ram'] = char[3]
            result[char[0]][0]['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(char[-1]/1000.0))

    return result


def retrieve_scraper_data(scraper):
    cw = boto3.client('cloudwatch',
                      region_name='eu-west-1',
                      aws_access_key_id=env.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY)
    tmp = datetime.datetime.utcnow()-timedelta(days=1)
    view = cw.get_metric_statistics(
        Period=3600,
        StartTime=tmp.strftime('%Y-%m-%d %H:%M:%S'),
        EndTime=datetime.datetime.utcnow(),
        MetricName='ScraperStatus',
        Namespace='DockerScrapers',
        Statistics=['Sum'],
        Dimensions=[{'Name': 'Scraper', 'Value': scraper}]
    )
    view['InstanceName'] = scraper
    view['InstanceType'] = ''
    data = graphData(view)
    return [view, data]
