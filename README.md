# identity-infra-functions
Infrastructure Lambda Functions for login.gov


CircleCI account needs iam:ListPolicies

S3 Bucket policy needs to allow access from serverlessrepo
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service":  "serverlessrepo.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<your-bucket-name>/*"
        }
    ]
}

CircleCI acccount needs rights to publish application
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "serverlessrepo:UpdateApplication",
                "serverlessrepo:CreateApplicationVersion"
            ],
            "Resource": "arn:aws:serverlessrepo:us-west-2:894947205914:applications/*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "serverlessrepo:CreateApplication",
            "Resource": "*"
        }
    ]
}