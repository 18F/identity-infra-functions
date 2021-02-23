import boto3
import botocore
import json
import logging
import os

from botocore.exceptions import ClientError

region = os.environ["AWS_REGION"]
events_channel = os.environ["EVENTS_CHANNEL"].split(",")
logger = logging.getLogger()
#logger.setLevel(logging.INFO)

ssm = boto3.client("ssm", region_name=region)
slack_events_param = ssm.get_parameter(
    Name=f'/account/{region}/alert/sns/arn_slack_events',
    WithDecryption=False
)

slack_other_events_param = ssm.get_parameter(
    Name=f'/account/{region}/alert/sns/arn_slack_otherevents',
    WithDecryption=False
)

slack_events_topic = slack_events_param["Parameter"]["Value"]
slack_other_events_topic = slack_other_events_param["Parameter"]["Value"]

def get_sns_client():
    sns = boto3.client("sns", region_name=region)
    return sns
    
def send_sns_message(sns_topic_arn, sns_message):
    sns = get_sns_client()
    try:
        response = sns.publish(
                    TargetArn=sns_topic_arn,
                    Message=sns_message)
    except botocore.exceptions.ClientError as error:
        logger.exception(error)
    
def get_message(record):
    message_json = record["Sns"]["Message"]
    message = json.loads(message_json)
    return message

def get_subject(record):
    subject = record["Sns"]["Subject"]
    return subject

def parse_record(record):
    message = get_message(record)
    details = message["Details"]
    parsed_message = {}
    parsed_message["cause"] = message["Cause"]
    parsed_message["asg_name"] = message["AutoScalingGroupName"]
    asg_name_parts = parsed_message["asg_name"].split("-")
    parsed_message["environment"] = asg_name_parts[0]

    alarm = details["InvokingAlarms"][0]
    parsed_message["alarm_name"] = alarm["AlarmName"] 
    
    trigger = details["InvokingAlarms"][0]["Trigger"]
    parsed_message["metric_name"] = trigger["MetricName"]

    return parsed_message

def get_sns_topic(environment):
    if environment in events_channel:
        sns_topic_arn = slack_events_topic
    else:
        sns_topic_arn = slack_other_events_topic
    return sns_topic_arn

def lambda_handler(event, context):
    for index, record in enumerate(event["Records"]):
        logger.info(json.dumps(record))
        subject = get_subject(record)
        message_details = parse_record(record)
        
        if message_details["metric_name"] == "CPUUtilization":
            console_url = f'https://{region}.console.aws.amazon.com/ec2autoscaling/home?region={region}#/details/{message_details["asg_name"]}?view=activity'
            alarm_url = f'https://{region}.console.aws.amazon.com/cloudwatch/home?region={region}#alarmsV2:alarm/{message_details["alarm_name"]}'
            sns_message = f'*Subject: {subject}*\n*Message:* {message_details["cause"]}\n*ASG Console url:* {console_url}\n*CW Alarm url:* {alarm_url}\n*EOM*'
            sns_topic_arn = get_sns_topic(message_details["environment"])

            response = send_sns_message(
                sns_topic_arn = sns_topic_arn,
                sns_message = sns_message)
            logger.info(f"Processed record {index} succesfully")
            logger.info(json.dumps(response))
        else:
            log_message = f'Launch event was not for CPUUtilization. Record:{json.dumps(record)}'
            logger.warning(log_message)
    return {
        "status": "Complete"
    }