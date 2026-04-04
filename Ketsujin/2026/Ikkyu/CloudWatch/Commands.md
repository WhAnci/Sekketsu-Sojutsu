# Commands [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Ikkyu/CloudWatch/README.md)

## 설치

```bash
# Amazon Linux 2 / AL2023
sudo yum install -y amazon-cloudwatch-agent

# Ubuntu
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb
```

## 설정 적용 및 시작

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json \
  -s
```

## 상태 확인 / 로그

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a status
tail -f /opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log
```

## IAM 권한

EC2 Instance Profile에 `CloudWatchAgentServerPolicy` 관리형 정책 연결로 충분.

> SSM Parameter Store에 설정 저장 시 `ssm:GetParameter` 권한 추가 필요
