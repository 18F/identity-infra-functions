import boto3
import json
import datetime
import pprint
import os

WEB_ACL_ID = os.environ["WEB_ACL_ID"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
WAF_API = os.environ["WAF_API"]
REQUEST_PERIOD_INT = int(os.environ["SAMPLE_REQUEST_PERIOD_MIN"])

def lambda_handler(event, context):
  result = {}

  try:
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(minutes=REQUEST_PERIOD_INT)
    result['start_time'] = start_time.strftime("%Y-%m-%d %H:%M:%S")
    result['end_time'] = end_time.strftime("%Y-%m-%d %H:%M:%S")
    result['events'] = []

    # -----------------------------------------------------------------------------------
    # Get Rules
    # -----------------------------------------------------------------------------------
    waf_client = boto3.client(WAF_API)
    response = waf_client.get_web_acl(WebACLId=WEB_ACL_ID)

    # -----------------------------------------------------------------------------------
    # Get Events
    # -----------------------------------------------------------------------------------
    events = {}
    for rule in response['WebACL']['Rules']:
      rule_type = rule['Type']
      rule_action = rule['Action']['Type']
      rule_id = rule['RuleId']
      rule_name = ""

      events[rule_id] = {}

      # Get Rule Name
      if rule_type == "RATE_BASED":
        response = waf_client.get_rate_based_rule(RuleId=rule_id)
        rule_name = response['Rule']['Name']
      else:
        response = waf_client.get_rule(RuleId=rule_id)
        rule_name = response['Rule']['Name']

      events[rule_id]['name'] = rule_name
      events[rule_id]['rule_action'] = rule_action
      events[rule_id]['events'] = {}


      response = waf_client.get_sampled_requests(
        WebAclId=WEB_ACL_ID,
        RuleId=rule_id,
        TimeWindow={
          'StartTime': start_time,
          'EndTime': end_time
        },
        MaxItems=500
      )

      if len(response['SampledRequests']) > 0:
        for e in response['SampledRequests']:
          client_ip = e['Request']['ClientIP']
          print "this is client ip "  +client_ip
          #if client_ip == "184.73.170.150":
           # print "client ip found"
            #continue
          if client_ip in events[rule_id]['events']:
            events[rule_id]['events'][client_ip] += 1
          else:
            events[rule_id]['events'][client_ip] = 1

    for r in events:
      for k in events[r]['events']:
        line = ""
        if events[r]['events'][k] > 1:
          line = "%s where %s by rule %s (%s) %d times"%(k, events[r]['rule_action'], r, events[r]['name'], events[r]['events'][k])
         #line = "%s where %s by rule %s (%s) %d times"%(k, rule_action, r, events[r]['name'], events[r]['events'][k])
        else:
          line = "%s where %s by rule %s (%s)"%(k, events[r]['rule_action'], r, events[r]['name'])
         #line = "%s where %s by rule %s (%s)"%(k, rule_action, r, events[r]['name'])
        result['events'].append(line)


    # ---------
    # Publish to an SNS topic
    # ---------
    if len(result['events']) > 0:
      sns_client = boto3.client('sns')
      response = sns_client.publish(
          TopicArn=SNS_TOPIC_ARN,
          Subject='[WAF Alert]',
          Message=json.dumps(result)
      )

  except Exception as e:
    print e
  return result
