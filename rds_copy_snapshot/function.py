import boto3
import datetime as dt
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

region = os.environ["AWS_REGION"]
destination_region = os.environ["DESTINATION_REGION"]
destination_kms_alias = os.environ["DESTINATION_KMS_ALIAS"]

# rds copy snapshot call is made from the destination region
rds_destination = boto3.client("rds", region_name=destination_region)

def get_message(record):
    message_json = record["Sns"]["Message"]
    message = json.loads(message_json)
    return message
    
def is_automated_backup_complete(message):
    # rds event documentation https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Events.html
    # this event is automated snapshot completion
    if "RDS-EVENT-0091" in message["Event ID"]:
        return True
    else:
        return False
        
def parse_message(message):
    logger.info(message)
    parsed_message = {}
    parsed_message["source_arn"] = message["Source ARN"]
    parsed_message["source_id"] = message["Source ID"]
    return parsed_message
    
def copy_snapshot(source_arn, source_region, target_name):
    response = rds_destination.copy_db_snapshot(
        SourceDBSnapshotIdentifier = source_arn,
        TargetDBSnapshotIdentifier = target_name,
        KmsKeyId = destination_kms_alias,
        Tags=[
            {
                'Key': 'Source',
                'Value': region
            },
        ],
        CopyTags=True,
        SourceRegion = source_region
    )
    
    # confirming that the snapshot copy started successfully
    # copy is async so we don't hang around and wait for completion
    if response['DBSnapshot']['Status'] != "pending" and response['DBSnapshot']['Status'] != "available":
        raise Exception("Copy operation for " + copy_name + " failed!")
        print("Copied " + target_name)

def lambda_handler(event, context):
    print(json.dumps(event))
    for index, record in enumerate(event["Records"]):
        message = get_message(record)
        if is_automated_backup_complete(message):
            logger.info("Automated backup complete")
            parsed_message = parse_message(message)
        else:
            continue
            
    target_name = f'{parsed_message["source_id"].strip("rds:")}-copy'
    copy_snapshot(parsed_message["source_arn"], region, target_name)
    
    return {}
    
