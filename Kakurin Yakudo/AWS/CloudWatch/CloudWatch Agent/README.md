# CloudWatch Agent
## on EC2
```bash
sudo dnf install -y amazon-cloudwatch-agent

sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime # TZ 서울로 설정
cat <<'EOF' > /home/ec2-user/cwagent-config.json
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "<LOG_DIR>",
            "log_group_name": "<LOG_Group>",
            "log_stream_name": "{instance_id}",
            "timezone": "LOCAL"
          }
        ]
      }
    }
  }
}
EOF

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -c file:/home/ec2-user/cwagent-config.json \
  -s

# 동작 확인
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a status

systemctl enable amazon-cloudwatch-agent
```
