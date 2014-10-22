#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 and Beyond
#
# This file created by Leonid Khudisman
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from boto.ec2.connection import EC2Connection
import boto.ec2
from datetime import datetime
import sys
import time

if len(sys.argv) < 3:
    print "Usage: python ebs_snapshot.py volume_id number_of_snapshots_to_keep description"
    print "volume id and number of snapshots to keep are required. description is optional"
    print "create .boto file with AWS Credentials as a Prerequisite"
    sys.exit(1)


vol_id = sys.argv[1]
keep = int(sys.argv[2])

regions = boto.ec2.regions()
east = regions[0]

conn = EC2Connection(region=east)

volumes = conn.get_all_volumes([vol_id])
volume = volumes[0]
description = 'Created by ebs-snapshot.py at ' + datetime.today().isoformat(' ')

Begin = datetime.now()

if len(sys.argv) > 3:
    description = sys.argv[3]

if volume.create_snapshot(description):
    print 'Snapshot created with description: ' + description

snapshots = volume.snapshots()
snapshot = snapshots[0]

a = str(snapshot).rsplit(":", 1)[1]
print "Snapshot ID is " + str(a)

snap = conn.get_all_snapshots(snapshot_ids=a)[0]

while snap.status == 'pending':
        time.sleep(2)
        snap.update()
  
print "Snapshot created"
    

End = datetime.now()
Total = End - Begin
print "Time took for snapshot: " + str(Total)

def date_compare(snap1, snap2):
    if snap1.start_time < snap2.start_time:
        return -1
    elif snap1.start_time == snap2.start_time:
        return 0
    return 1

snapshots.sort(date_compare)
delta = len(snapshots) - keep
for i in range(delta):
    print 'Deleting snapshot ' + snapshots[i].description
    snapshots[i].delete()
