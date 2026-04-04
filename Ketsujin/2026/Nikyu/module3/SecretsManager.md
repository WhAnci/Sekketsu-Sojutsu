# Secrets Manager Fine-grained IAM Policy [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module3/README.md)

### 특정 시크릿만 읽기
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": "arn:aws:secretsmanager:{region}:{account-id}:secret:{secret-name}-*"
    }
  ]
}
```
> 시크릿 이름 뒤에 `-*` 붙이는 이유: AWS가 자동으로 6자리 접미사 붙임

---

### 특정 Prefix의 시크릿만 접근 (환경별 분리)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["secretsmanager:GetSecretValue"],
      "Resource": "arn:aws:secretsmanager:{region}:{account-id}:secret:{env}/{app}/*"
    }
  ]
}
```
> 예) `prod/myapp/*` → prod 환경의 myapp 시크릿만 허용
