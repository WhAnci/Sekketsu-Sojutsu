# Shared Network Storage
## EFS
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
sudo dnf install python3-pip amazon-efs-utils -y
sudo pip3 install botocore
sudo mkdir $D
cat <<EOF >> /etc/fstab
$FSID:/  $DIR  efs  _netdev,noresvport,tls,accesspoint=$APID  0  0
EOF
sudo mount -t efs -o tls,accesspoint=$APID $FSID:/ $DIR
```
