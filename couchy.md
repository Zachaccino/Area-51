# Adding the volumes to the hosts
On the master hosts as root:
```
mkfs.ext4 /dev/vdb
mkdir /mnt/couch
mount -t auto -v /dev/vdb /mnt/couch
```

