# EC2 [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Ikkyu/README.md)

## 환경 세팅

```bash
sudo apt update
sudo apt install -y python3 python3-pip jq
```

## Secrets Manager 환경변수 설정

```bash
# 시크릿 값 전체 가져오기
SECRET_JSON=$(aws secretsmanager get-secret-value --secret-id "설정한 SecretName" --query "SecretString" --output text)

# 환경변수로 설정 - 시크릿매니저에 등록한 key이름과 동일해야 함
export DB_HOST=$(echo $SECRET_JSON | jq -r '.DB_HOST')
export DB_PORT=$(echo $SECRET_JSON | jq -r '.DB_PORT')
export DB_USERNAME=$(echo $SECRET_JSON | jq -r '.DB_USERNAME')
export DB_PASSWORD=$(echo $SECRET_JSON | jq -r '.DB_PASSWORD')
export DB_NAME=$(echo $SECRET_JSON | jq -r '.DB_NAME')
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
User=ubuntu
WorkingDirectory=/home/ubuntu/app
ExecStart=/usr/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
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
