import boto3
import datetime
import pytz

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get current time and calculate one week ago
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    one_week_ago = now - datetime.timedelta(weeks=1)
    
    # Describe volumes
    response = ec2.describe_volumes(
        Filters=[
            {'Name': 'status', 'Values': ['available']},
        ]
    )
    
    volumes = response.get('Volumes', [])
    
    # Filter volumes that have been available for more than one week
    old_volumes = []
    for volume in volumes:
        create_time = volume.get('CreateTime')
        if create_time and create_time < one_week_ago:
            volume_id = volume.get('VolumeId')
            size = volume.get('Size')
            tags = volume.get('Tags', [])
            name = None
            
            # Extract the Name tag if it exists
            for tag in tags:
                if tag['Key'] == 'Name':
                    name = tag['Value']
                    break
            
            old_volumes.append({
                'VolumeId': volume_id,
                'Size': size,
                'Name': name if name else 'N/A',
                'Created': create_time
            })
    
    # Print or log the old volumes
    for volume in old_volumes:
        print(f"Volume ID: {volume['VolumeId']}, Size: {volume['Size']} GiB, Name: {volume['Name']}, Created: {volume['Created']}")
    
    return {
        'statusCode': 200,
        'body': f"Found {len(old_volumes)} volumes older than one week."
    }
