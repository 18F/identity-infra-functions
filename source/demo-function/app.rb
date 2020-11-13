require 'json'
require 'aws-sdk-lambda'
require 'aws-sdk-sns'
require 'aws-xray-sdk'

$lambda = Aws::Lambda::Client.new()
$lambda.get_account_settings()
$sns = Aws::SNS::Resource.new()

config = {
  name: 'my app',
  patch: %I[net_http aws_sdk]
}

XRay.recorder.configure(config)

def lambda_handler(event:, context:)
    topic = $sns.topic('arn:aws:sns:us-west-2:894947205914:slack-otherevents')
    topic.publish({message: 'Testing please ignoe'})

    { statusCode: 200, body: JSON.generate('Hello from Lambda!') }
end
