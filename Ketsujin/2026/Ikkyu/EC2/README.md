# EC2 [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Ikkyu/README.md)

## 환경 세팅

```bash
# 파이썬 및 pip 설치
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate
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
ExecStart=/home/ubuntu/app/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
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
