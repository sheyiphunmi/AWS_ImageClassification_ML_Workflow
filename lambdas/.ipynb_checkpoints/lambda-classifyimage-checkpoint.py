import json
import sagemaker
import base64
import boto3

# To invoke endpoint
runtime = boto3.client('sagemaker-runtime')                   


# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2023-09-17-20-47-50-590" ##  Trained image classification model name

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])     ## Decoding the encoded 'Base64' image-data and class remains'bytes'

    # Instantiate a Predictor 
    # Invoke the endpoint using boto3 runtime via SageMaker Runtime 
    response = runtime.invoke_endpoint(
                                        EndpointName=ENDPOINT,    # Endpoint Name
                                        Body=image,               # Decoded Image Data as Input (class:'Bytes') 
                                        ContentType='image/png'   # using content type eliminates the need for serializer
                                    )
     
    ## Read and decode predictions/inference
         
    event['body']['inferences'] = json.loads(response['Body'].read().decode('utf-8'))   
    
    ## Return data back to Step Function
    return {
        "image_data": event["body"]['image_data'],
        "s3_bucket": event["body"]['s3_bucket'],
        "s3_key": event["body"]['s3_key'],
        "inferences": event['body']['inferences']
        
        ## or return just event
    }

# Test Event
# {
#   "statusCode": 200,
#   "body": {
#     "s3_bucket": "sagemaker-studio-gertjzq23es",
#     "s3_key": "test/bicycle_s_000513.png",
#     "image_data": "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",
#     "inferences": []
#   }
# }


    


    


