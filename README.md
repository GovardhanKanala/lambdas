# lambdas

```
import boto3

def lambda_handler(event, context):
    # Initialize EC2 client
    ec2_client = boto3.client('ec2')

    # Get all volumes
    volumes = ec2_client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])

    unused_volumes = []

    # Loop through volumes and find unused (available) ones
    for volume in volumes['Volumes']:
        if not volume['Attachments']:  # If there are no attachments, the volume is unused
            unused_volumes.append(volume['VolumeId'])

    if unused_volumes:
        print(f"Unused volumes: {unused_volumes}")
    else:
        print("No unused volumes found.")

    return {
        'statusCode': 200,
        'body': unused_volumes
    }
```
