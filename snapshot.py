import boto3
import os
from datetime import datetime, timezone, timedelta
import json

def lambda_handler(event, context):
    # Initialize the Boto3 client for EC2
    ec2_client = boto3.client('ec2')

    # Get the environment variable for snapshot deletion
    snapshotdelete = os.getenv('snapshotdelete', 'false').lower() == 'true'
    
    # Calculate the time threshold for one year ago
    one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)
    
    # Get the snapshots
    snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])['Snapshots']
    
    old_snapshots = []

    # Loop through snapshots and find those older than one year
    for snapshot in snapshots:
        # Get the snapshot's creation date
        creation_date = snapshot['StartTime']

        # Check if the snapshot is older than one year
        if creation_date < one_year_ago:
            old_snapshots.append({
                'SnapshotId': snapshot['SnapshotId'],
                'Name': 'Unnamed',  # Name is not available, so default to 'Unnamed'
                'Size': snapshot['VolumeSize']
            })

    count_of_old_snapshots = len(old_snapshots)
    
    if snapshotdelete:
        # Print the details of old snapshots
        if count_of_old_snapshots > 0:
            for snap in old_snapshots:
                print(f"SnapshotId: {snap['SnapshotId']}, Name: {snap['Name']}, Size: {snap['Size']} GiB")
            print(f"Total snapshots deleted: {count_of_old_snapshots}")

        # Delete snapshots
        deleted_snapshots = []
        for snapshot in old_snapshots:
            ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            deleted_snapshots.append(snapshot['SnapshotId'])

        result = {
            'count_of_deleted_snapshots': len(deleted_snapshots),
            'deleted_snapshots': deleted_snapshots
        }
    
    else:
        # Print the details of old snapshots ready to delete
        if count_of_old_snapshots > 0:
            for snap in old_snapshots:
                print(f"SnapshotId: {snap['SnapshotId']}, Name: {snap['Name']}, Size: {snap['Size']} GiB")
        else:
            print("No snapshots older than one year found.")
        
        result = {
            'count_of_old_snapshots': count_of_old_snapshots,
            'old_snapshots': old_snapshots
        }

    # Return results as JSON
    return {
        'statusCode': 200,
        'body': json.dumps(result, indent=4)
    }
