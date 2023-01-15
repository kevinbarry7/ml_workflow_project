import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event['s3_key']
    bucket = event['s3_bucket']
    #print(key)
    #print(bucket)
    
    # Download the data from s3 to /tmp/image.png
    s3.download_file(bucket, key, '/tmp/image.png')
    
        # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }



import json
#import sagemaker
import base64
import boto3
#from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2023-01-14-19-27-59-756'
runtime = boto3.Session().client('sagemaker-runtime')

def lambda_handler(event, context):
    #print(event)
    
    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])
    
    # Instantiate a Predictor
    #predictor = sagemaker.predictor.Predictor(endpoint, sagemaker_session=sagemaker.Session())
    
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT, 
        ContentType = 'image/png',
        Body = image)
        
    
    # We return the data back to the Step Function

    event['inferences'] = json.loads(response['Body'].read().decode('utf-8'))
    
    return{
        'statusCode': 200,
        'body':event
    }




import json

THRESHOLD = .88


def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event['body']['inferences']
    #inferences = json.loads(event['body']['inferences']) if type(event['body']['inferences']) == str else event['body']['inferences']
    print(inferences)
    meets_threshold = (max(inferences)> THRESHOLD)
    
    # If our threshold is met, pass our data back out of the

    # Step Function, else, end the Step Function with an error

    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': event
}