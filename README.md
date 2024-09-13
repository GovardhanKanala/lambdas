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

```
import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    # Initialize EC2 client
    ec2_client = boto3.client('ec2')

    # Get all available volumes
    volumes = ec2_client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])

    # Calculate the time threshold for 1 week ago
    one_week_ago = datetime.now(timezone.utc) - timedelta(weeks=1)

    unused_volumes = []

    # Loop through volumes and find those unused for more than one week
    for volume in volumes['Volumes']:
        # Get the volume's creation date
        creation_date = volume['CreateTime']

        # Check if the volume has been unused for more than 1 week
        if not volume['Attachments'] and creation_date < one_week_ago:
            # Get the volume's ID, size, and name (if it has a tag named 'Name')
            volume_id = volume['VolumeId']
            size = volume['Size']
            name = 'Unnamed'
            
            # Get volume name from tags
            if 'Tags' in volume:
                for tag in volume['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                        break
            
            # Add the volume details to the unused_volumes list
            unused_volumes.append({
                'VolumeId': volume_id,
                'Name': name,
                'CreationDate': creation_date.strftime('%Y-%m-%d %H:%M:%S'),
                'Size': size
            })

    # Print the details of unused volumes older than 1 week
    if unused_volumes:
        for vol in unused_volumes:
            print(f"VolumeId: {vol['VolumeId']}, Name: {vol['Name']}, CreationDate: {vol['CreationDate']}, Size: {vol['Size']} GiB")
    else:
        print("No unused volumes older than one week found.")

    return {
        'statusCode': 200,
        'body': unused_volumes
    }
```
