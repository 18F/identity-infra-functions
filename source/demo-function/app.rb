require 'json'
require 'aws-sdk-sns'
require 'aws-xray-sdk/lambda'

def lambda_handler(event:, context:)
    # TODO implement
    { statusCode: 200, body: JSON.generate('Hello from Lambda!') }
end
