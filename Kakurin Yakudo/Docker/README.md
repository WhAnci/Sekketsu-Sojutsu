#  most-widely-used Dockerfile
## RUN Golang Binary
<details>
<summary>Dockerfile</summary>
  
  ```Dockerfile
  FROM golang:alpine
  RUN apk add --no-cache curl libc6-compat
  WORKDIR /app
  COPY app .
  RUN chmod +x app
  CMD ["./app"]
  ```
</details>

## RUN Python File(.py)
### most-widely-used
<details>
<summary>Dockerfile</summary>

  ```Dockerfile
  FROM python:alpine
  WORKDIR /app
  
  ### [ Use Requirements.txt ] ###
  # COPY requirements.txt .
  # RUN pip install --no-cache-dir -r requirements.txt
  
  COPY <application>.py .
  EXPOSE <port>
  
  # Run the application
  CMD ["python3", "<application>.py"]
  ```
  
</details>

### RUN with gunicorn
<details>
<summary>Dockerfile</summary>
  
  ```Dockerfile
  FROM python:alpine
  WORKDIR /app
  
  ### [ Use Requirements.txt ] ###
  # COPY requirements.txt .
  # RUN pip install --no-cache-dir -r requirements.txt
  
  COPY <application.py> .
  EXPOSE <port>
  
  # Run the application with gunicorn
  CMD ["gunicorn", "-b", "0.0.0.0:<port>", "<application>:app"]
  ```
</details>
