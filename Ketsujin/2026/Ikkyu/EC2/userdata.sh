#!/bin/bash

# Boto3 Python 3.9 버전부터 지원안함 이슈
dnf install python3.11 python3.11-pip amazon-cloudwatch-agent -y

cat <<EOF > requirements.txt
Flask>=2.0
SQLAlchemy>=1.4
PyMySQL>=1.0
gunicorn>=20.0
python-dotenv>=1.0
boto3>=1.26
EOF

pip3.11 install -r requirements.txt --no-cache-dir
rm requirements.txt

curl -L <Application URL> -o /home/ec2-user/app.py
# pastebin 사용하셈

mkdir -p /var/log/worldpay
chmod 777 /var/log/worldpay 
# 로그 디렉토리 생성하고 권한 부여

cat <<EOF > /etc/systemd/system/worldpay.service
[Unit]
Description=Worldpay Flask Service
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user
ExecStart=/usr/bin/python3.11 -m gunicorn --bind 0.0.0.0:80 app:application
# fastapi uvicorn main:app --host 0.0.0.0 --port 8000 --reload
Restart=on-failure

AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now worldpay.service

sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
cat <<'EOF' > /home/ec2-user/cwagent-config.json
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/worldpay/app.log",
            "log_group_name": "/wsc2026/worldpay/log",
            "log_stream_name": "{instance_id}",
            "timezone": "LOCAL"
          }
        ]
      }
    }
  }
}
EOF

/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -c file:/home/ec2-user/cwagent-config.json \
  -s

systemctl enable amazon-cloudwatch-agent
