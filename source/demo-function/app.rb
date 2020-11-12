require 'json'
require 'aws-sdk-sns'
require 'aws-sdk-xray'

def lambda_handler(event:, context:)
    sns = Aws::SNS::Resource.new()
    topic = sns.topic('arn:aws:sns:us-west-2:894947205914:slack-otherevents')
    topic.publish({message: 'Testing please ignoe'})
    # TODO implement
    { statusCode: 200, body: JSON.generate('Hello from Lambda!') }
end
