ebs-backup
==========

AWS EBS Backup Script

ebs_snapshot.py will help you with your backup needs in the EBS land. 
The file creates an ebs snapshot of the volume specified. 
It tells you how long it took for the whole backup process. 
And in the end it cleans up all the old EBS snapshots you might have leaving only the number you specified.

Usage: 
	python ebs_snapshot.py volume_id number_of_snapshots_to_keep description
	volume id and number of snapshots to keep are required. description is optional
	create .boto file with AWS Credentials as a Prerequisite
