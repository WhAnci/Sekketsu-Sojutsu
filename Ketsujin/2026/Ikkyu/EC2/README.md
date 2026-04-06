# EC2 [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Ikkyu/README.md)

## 환경 세팅

```bash
sudo dnf update
sudo dnf install -y python3 python3-pip jq
```

## Secrets Manager 환경변수 설정

```bash
# 시크릿 값 전체 가져오기
SECRET_JSON=$(aws secretsmanager get-secret-value --secret-id "설정한 SecretName" --query "SecretString" --output text)

# 환경변수 파일로 저장 - systemd EnvironmentFile에서 가져옴
cat <<EOF | sudo tee /etc/app.env
DB_HOST=$(echo $SECRET_JSON | jq -r '.DB_HOST')
DB_PORT=$(echo $SECRET_JSON | jq -r '.DB_PORT')
DB_USERNAME=$(echo $SECRET_JSON | jq -r '.DB_USERNAME')
DB_PASSWORD=$(echo $SECRET_JSON | jq -r '.DB_PASSWORD')
DB_NAME=$(echo $SECRET_JSON | jq -r '.DB_NAME')
EOF

sudo chmod 600 /etc/app.env
```

## FastAPI + Gunicorn

```bash
pip install fastapi gunicorn uvicorn[standard]

# 실행
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## Flask + Gunicorn

```bash
pip install flask gunicorn

# 실행
gunicorn main:app -w 4 -b 0.0.0.0:8000
```

## systemd 서비스 등록

```bash
sudo vim /etc/systemd/system/app.service
```

```ini
[Unit]
Description=App Service
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/app
EnvironmentFile=/etc/app.env
ExecStart=/usr/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
# fastapi uvicorn main:app --host 0.0.0.0 --port 8000 --reload
StandardOutput=append:/home/ec2-user/worldpay.log
StandardError=append:/home/ec2-user/worldpay.log
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 서비스 시작
sudo systemctl daemon-reload
sudo systemctl enable app
sudo systemctl start app
sudo systemctl status app
```
