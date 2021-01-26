# aws-lambda-sharepoint-to-s3
AWS Lambda function that consumes from Microsoft Sharepoint and load data to S3 Bucket. 

This AWS Lambda function is capable of generally retrieve CSVs and Excel files via Microsoft Sharepoint API by specifying sites, folders, regex expressions representing multiple sources.

## Installing dependencies
Considering you have Python installed in your machine and you are able to use pip, run the following command:

`pip3 install -r requirements.txt`


## Setting .env file

The `.env` file will contain your environment variables, keys and variables needed to access Microsoft Sharepoint, AWS Lambda and also AWS S3 Bucket.

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

## Setting sharepoint_sources.json file

The `sharepoint_sources.json` file have a custom json structure where the developer can specify multiples sources to retrieve multiple files. In a source you can specify the site, folder, file regex expression, number of lines to skip in the beginning of the files and sheet name, if you want to load a specific sheet from a Excel file.

The parameters __site__, __folder__ and __regex__ are __required__. The parameter __skip_lines__ and __sheet__ are option (by default lines are not skipped and the first tab from a Excel file is loaded).

Here is a example of how your `sharepoint_sources.json` file should be defined with ficticional files definition:
```
{
    "sources": {
        "tables": {
            "invoices": {
                "site": "Invoices",
                "folder": "Shared Documents/All Invoices",
                "regex": "Invoice_([0-9]{2})-([0-9]{2})-([0-9]{4}).xlsx",
                "skip_lines": 3,
                "sheet": "Invoice" 
            },
            "receipts": {
                "site": "Receipts",
                "folder": "Shared Documents",
                "regex": "Receipts_([0-9]{4}.csv",
                "skip_lines": 0
            }
        }
    }
}
```

On your S3 Bucket, it will be created a folder called __invoices__ and another with the name __receipts__ with all respective files in it.