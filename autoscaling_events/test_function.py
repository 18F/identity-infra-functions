from unittest import TestCase, mock
from function import *
import os

test_cpu_scaling_event = {
    {"Records": 
    [
        {"EventSource": "aws:sns", 
            "EventVersion": "1.0", 
            "EventSubscriptionArn": "arn:aws:sns:us-west-2:894947205914:dev_autoscaling_test:8d985b5b-655b-42f9-a1a4-572805e2c0cc", 
            "Sns": {
                "Type": "Notification", 
                "MessageId": "c19f52f3-7369-517c-b0a4-0a53bfd81132", 
                "TopicArn": "arn:aws:sns:us-west-2:894947205914:dev_autoscaling_test", 
                "Subject": "Auto Scaling: launch for group 'dev-idp'", 
                "Message": "{\"Progress\":50,\"AccountId\":\"894947205914\",\"Description\":\"Launching a new EC2 instance: i-06e5a36f44cf8a51c\",\"RequestId\":\"e595de5d-f9db-02f0-e912-8f9116d8bb58\",\"EndTime\":\"2021-02-12T18:35:29.642Z\",\"AutoScalingGroupARN\":\"arn:aws:autoscaling:us-west-2:894947205914:autoScalingGroup:906a4909-c850-4a0d-b3c6-7bc6150271c1:autoScalingGroupName/dev-idp\",\"ActivityId\":\"e595de5d-f9db-02f0-e912-8f9116d8bb58\",\"StartTime\":\"2021-02-12T18:26:23.552Z\",\"Service\":\"AWS Auto Scaling\",\"Time\":\"2021-02-12T18:35:29.642Z\",\"EC2InstanceId\":\"i-06e5a36f44cf8a51c\",\"StatusCode\":\"InProgress\",\"StatusMessage\":\"\",\"Details\":{\"Subnet ID\":\"subnet-8fff48c7\",\"Availability Zone\":\"us-west-2a\",\"InvokingAlarms\":[{\"AlarmArn\":\"arn:aws:cloudwatch:us-west-2:894947205914:alarm:TargetTracking-dev-idp-AlarmHigh-409e8972-e301-4241-87d0-8629ffd20ec7\",\"Trigger\":{\"MetricName\":\"CPUUtilization\",\"EvaluateLowSampleCountPercentile\":\"\",\"ComparisonOperator\":\"GreaterThanThreshold\",\"TreatMissingData\":\"\",\"Statistic\":\"AVERAGE\",\"StatisticType\":\"Statistic\",\"Period\":60,\"EvaluationPeriods\":3,\"Unit\":null,\"Namespace\":\"AWS/EC2\",\"Threshold\":2},\"AlarmName\":\"TargetTracking-dev-idp-AlarmHigh-409e8972-e301-4241-87d0-8629ffd20ec7\",\"AlarmDescription\":\"DO NOT EDIT OR DELETE. For TargetTrackingScaling policy arn:aws:autoscaling:us-west-2:894947205914:scalingPolicy:60220277-e0ba-4cde-940f-5af0b5ddb911:autoScalingGroupName/dev-idp:policyName/cpu-scaling.\",\"AWSAccountId\":\"894947205914\",\"OldStateValue\":\"ALARM\",\"Region\":\"US West (Oregon)\",\"NewStateValue\":\"ALARM\",\"StateChangeTime\":1613154306643}]},\"AutoScalingGroupName\":\"dev-idp\",\"Cause\":\"At 2021-02-12T18:26:06Z a monitor alarm TargetTracking-dev-idp-AlarmHigh-409e8972-e301-4241-87d0-8629ffd20ec7 in state ALARM triggered policy cpu-scaling changing the desired capacity from 2 to 3.  At 2021-02-12T18:26:21Z an instance was started in response to a difference between desired and actual capacity, increasing the capacity from 2 to 3.\",\"Event\":\"autoscaling:EC2_INSTANCE_LAUNCH\"}",
                "Timestamp": "2021-02-12T18:35:29.685Z", 
                "SignatureVersion": "1", 
                "Signature": "fHNdtJd66sCz6fpxkcQGXBjXvqJDCnuZmueV/kQhFnMfPk9akIyflmcf5TQzOL1uXlrhWi9EM5u1TBW5LQa/AdyNG7zZ3vCVbbEJP3A/cVokcIDFkldYSMZQmKppBgkXHfBVxsKQgMs43/z0UfyEp7OpoxFbtpMwljql6YKPHxTcUcLJkiyWmMZ/vUCYIrjtvnEfdeFoQLzU1WVqjRTgcdAh/Zfw9odDoGJZ0k6Lgnsk/AChY8OU6rQEvaPUDyIWVvOG7YILAu0QCILfnZ7MDoaqTK2KTutaLyb7mLjnVnrIT7Lsyo478gu+MMSE6IOFOK11ol5W68264Te4oJZvFg==", 
                "SigningCertUrl": "https://sns.us-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem", 
                "UnsubscribeUrl": "https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:894947205914:dev_autoscaling_test:8d985b5b-655b-42f9-a1a4-572805e2c0cc", 
                "MessageAttributes": {}
            }
        }
    ]
    }   
}

test_cpu_scaling_record = {
    {"EventSource": "aws:sns", 
            "EventVersion": "1.0", 
            "EventSubscriptionArn": "arn:aws:sns:us-west-2:894947205914:dev_autoscaling_test:8d985b5b-655b-42f9-a1a4-572805e2c0cc", 
            "Sns": {
                "Type": "Notification", 
                "MessageId": "c19f52f3-7369-517c-b0a4-0a53bfd81132", 
                "TopicArn": "arn:aws:sns:us-west-2:894947205914:dev_autoscaling_test", 
                "Subject": "Auto Scaling: launch for group 'dev-idp'", 
                "Message": "{\"Progress\":50,\"AccountId\":\"894947205914\",\"Description\":\"Launching a new EC2 instance: i-06e5a36f44cf8a51c\",\"RequestId\":\"e595de5d-f9db-02f0-e912-8f9116d8bb58\",\"EndTime\":\"2021-02-12T18:35:29.642Z\",\"AutoScalingGroupARN\":\"arn:aws:autoscaling:us-west-2:894947205914:autoScalingGroup:906a4909-c850-4a0d-b3c6-7bc6150271c1:autoScalingGroupName/dev-idp\",\"ActivityId\":\"e595de5d-f9db-02f0-e912-8f9116d8bb58\",\"StartTime\":\"2021-02-12T18:26:23.552Z\",\"Service\":\"AWS Auto Scaling\",\"Time\":\"2021-02-12T18:35:29.642Z\",\"EC2InstanceId\":\"i-06e5a36f44cf8a51c\",\"StatusCode\":\"InProgress\",\"StatusMessage\":\"\",\"Details\":{\"Subnet ID\":\"subnet-8fff48c7\",\"Availability Zone\":\"us-west-2a\",\"InvokingAlarms\":[{\"AlarmArn\":\"arn:aws:cloudwatch:us-west-2:894947205914:alarm:TargetTracking-dev-idp-AlarmHigh-409e8972-e301-4241-87d0-8629ffd20ec7\",\"Trigger\":{\"MetricName\":\"CPUUtilization\",\"EvaluateLowSampleCountPercentile\":\"\",\"ComparisonOperator\":\"GreaterThanThreshold\",\"TreatMissingData\":\"\",\"Statistic\":\"AVERAGE\",\"StatisticType\":\"Statistic\",\"Period\":60,\"EvaluationPeriods\":3,\"Unit\":null,\"Namespace\":\"AWS/EC2\",\"Threshold\":2},\"AlarmName\":\"TargetTracking-dev-idp-AlarmHigh-409e8972-e301-4241-87d0-8629ffd20ec7\",\"AlarmDescription\":\"DO NOT EDIT OR DELETE. For TargetTrackingScaling policy arn:aws:autoscaling:us-west-2:894947205914:scalingPolicy:60220277-e0ba-4cde-940f-5af0b5ddb911:autoScalingGroupName/dev-idp:policyName/cpu-scaling.\",\"AWSAccountId\":\"894947205914\",\"OldStateValue\":\"ALARM\",\"Region\":\"US West (Oregon)\",\"NewStateValue\":\"ALARM\",\"StateChangeTime\":1613154306643}]},\"AutoScalingGroupName\":\"dev-idp\",\"Cause\":\"At 2021-02-12T18:26:06Z a monitor alarm TargetTracking-dev-idp-AlarmHigh-409e8972-e301-4241-87d0-8629ffd20ec7 in state ALARM triggered policy cpu-scaling changing the desired capacity from 2 to 3.  At 2021-02-12T18:26:21Z an instance was started in response to a difference between desired and actual capacity, increasing the capacity from 2 to 3.\",\"Event\":\"autoscaling:EC2_INSTANCE_LAUNCH\"}",
                "Timestamp": "2021-02-12T18:35:29.685Z", 
                "SignatureVersion": "1", 
                "Signature": "fHNdtJd66sCz6fpxkcQGXBjXvqJDCnuZmueV/kQhFnMfPk9akIyflmcf5TQzOL1uXlrhWi9EM5u1TBW5LQa/AdyNG7zZ3vCVbbEJP3A/cVokcIDFkldYSMZQmKppBgkXHfBVxsKQgMs43/z0UfyEp7OpoxFbtpMwljql6YKPHxTcUcLJkiyWmMZ/vUCYIrjtvnEfdeFoQLzU1WVqjRTgcdAh/Zfw9odDoGJZ0k6Lgnsk/AChY8OU6rQEvaPUDyIWVvOG7YILAu0QCILfnZ7MDoaqTK2KTutaLyb7mLjnVnrIT7Lsyo478gu+MMSE6IOFOK11ol5W68264Te4oJZvFg==", 
                "SigningCertUrl": "https://sns.us-west-2.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem", 
                "UnsubscribeUrl": "https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:894947205914:dev_autoscaling_test:8d985b5b-655b-42f9-a1a4-572805e2c0cc", 
                "MessageAttributes": {}
            }
        }
}

@mock.patch.dict(os.environ, {"AWS_REGION": "us-west-2"})
class TestFunction(TestCase):
    def test_get_message(self):
        record = test_cpu_scaling_record
        self.assertEqual(message, 'foobar')

if __name__ == '__main__':
    unittest.main()

