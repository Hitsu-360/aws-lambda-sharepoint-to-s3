# aws-lambda-sharepoint-to-s3
AWS Lambda function that consumes from Microsoft Sharepoint and load data to S3 Bucket. 

This AWS Lambda function is capable of generally retrieve CSVs and Excel files via Microsoft Sharepoint API by specifying sites, folders, regex expressions representing multiple sources.

## Installing dependencies
Considering you have Python installed in your machine and you are able to use pip, run the following command:

`pip3 install -r requirements.txt`


## Setting .env file

The .env file will contain your environment variables, keys and variables needed to access Microsoft Sharepoint, AWS Lambda and also AWS S3 Bucket.

Define your keys and variables like the following `.env` content: 
```
#SHAREPOINT CREDENTIALS

SHAREPOINT_URL=<sharepoint_url>
SHAREPOINT_CLIENT_ID=<sharepoint_client_id>
SHAREPOINT_SECRET=<sharepoint_secret>
SHAREPOINT_DOMAIN=<sharepoint_domain>
SHAREPOINT_REDIRECT=<sharepoint_redirect>

#AWS CREDENTIALS

AWS_REGION=<aws_region>
BUCKET=<dev_bucket>
BUCKET_AWS_ACCESS_KEY_ID=<bucket_aws_access_key_id>
BUCKET_AWS_SECRET_ACCESS_KEY=<bucket_aws_secret_access_key>
```