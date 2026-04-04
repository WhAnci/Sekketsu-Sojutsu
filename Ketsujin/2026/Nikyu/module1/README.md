# Shared Network Storage

## Elastic File System

## EFS Access Point


## EFS on EC2
### Dependency
botocore, amazon-efs-utils
```bash
sudo dnf install python3-pip amazon-efs-utils -y
sudo pip3 install botocore
```
### Userdata
```bash
#!/bin/bash
FSID=
APID=
DIR=
dnf install python3-pip amazon-efs-utils -y
pip3 install botocore
mkdir $D
cat <<EOF >> /etc/fstab
$FSID:/  $DIR  efs  _netdev,noresvport,tls,accesspoint=$APID  0  0
#                                      ^ iam 옵션 추가가능
EOF
mount -t efs -o tls,accesspoint=$APID $FSID:/ $DIR
#                  ^ iam 옵션 추가가능
```
