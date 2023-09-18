import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    #Get the s3 address from the Step Function event input (You may also check lambda test)
    key = event['s3_key']                               ## TODO: fill in
    bucket = event['s3_bucket']                         ## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    boto3.resource('s3').Bucket(bucket).download_file(key, "/tmp/image.png")
    # s3.download_file(bucket, key, "/tmp/image.png")   #Alternatively
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "s3_bucket": bucket,
            "s3_key": key,
            "image_data": image_data,
            "inferences": []
        }
    }
    

# Test Event Used
#{
#  "s3_bucket": "sagemaker-studio-gertjzq23es",
#  "s3_key": "test/bicycle_s_000513.png",
# "image_data": ""
#}
