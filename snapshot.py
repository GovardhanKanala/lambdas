import boto3
import os
from datetime import datetime, timezone

# Initialize the Boto3 client for EC2
ec2_client = boto3.client('ec2')

# Get the environment variable for snapshot deletion
snapshotdelete = os.getenv('snapshotdelete', 'false').lower() == 'true'

def get_old_snapshots():
    # Get the current time
    now = datetime.now(timezone.utc)
    
    # Get the snapshots
    snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])['Snapshots']
    
    old_snapshots = []
    
    for snapshot in snapshots:
        # Parse the snapshot creation time
        create_time = snapshot['StartTime']
        
        # Check if the snapshot is older than one year
        if (now - create_time).days > 365:
            old_snapshots.append(snapshot)
    
    return old_snapshots

def main():
    old_snapshots = get_old_snapshots()
    
    if not old_snapshots:
        print("No snapshots older than one year.")
        return
    
    if snapshotdelete:
        # Print details of old snapshots
        print(f"Found {len(old_snapshots)} snapshots older than one year:")
        for snapshot in old_snapshots:
            print(f"Snapshot ID: {snapshot['SnapshotId']}")
            print(f"Creation Time: {snapshot['StartTime']}")
            print(f"Size (GiB): {snapshot['VolumeSize']}")
            print('-' * 40)
        
        # Delete snapshots
        deleted_snapshots = []
        for snapshot in old_snapshots:
            ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            deleted_snapshots.append(snapshot['SnapshotId'])
        
        print("Deleted Snapshots:")
        for snapshot_id in deleted_snapshots:
            print(snapshot_id)
    
    else:
        print("Snapshot deletion is not enabled.")
        print("Available snapshots ready to delete (older than one year):")
        for snapshot in old_snapshots:
            print(f"Snapshot ID: {snapshot['SnapshotId']}")
            print(f"Creation Time: {snapshot['StartTime']}")
            print(f"Size (GiB): {snapshot['VolumeSize']}")
            print('-' * 40)

if __name__ == "__main__":
    main()
