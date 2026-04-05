# Shared Network Storage [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/README.md)

## Elastic File System
마운트 타겟에 IP 지정할 수 있음
### Security Group
TCP 2049 Port </br>
요구사항에 따라 알잘딱

## [EFS Access Point](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module1/Access%20Point.md)

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
mkdir $Dㅑㄲ
cat <<EOF >> /etc/fstab
$FSID:/  $DIR  efs  _netdev,noresvport,tls,accesspoint=$APID  0  0
#                                      ^ iam 옵션 추가가능
EOF
mount -t efs -o tls,accesspoint=$APID $FSID:/ $DIR
#                  ^ iam 옵션 추가가능
```
