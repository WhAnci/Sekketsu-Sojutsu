# SSM Parameter Store Fine-grained IAM Policy [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module3/README.md)

### 특정 경로의 파라미터만 읽기
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter",
        "ssm:GetParameters",
        "ssm:GetParametersByPath"
      ],
      "Resource": "arn:aws:ssm:{region}:{account-id}:parameter/{path}/*"
    }
  ]
}
```
> 예) `/{env}/{app}/*` → 환경/앱 단위로 권한 분리

---

### SecureString 복호화 추가 허용 (KMS)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter",
        "ssm:GetParametersByPath"
      ],
      "Resource": "arn:aws:ssm:{region}:{account-id}:parameter/{path}/*"
    },
    {
      "Effect": "Allow",
      "Action": ["kms:Decrypt"],
      "Resource": "arn:aws:kms:{region}:{account-id}:key/{kms-key-id}"
    }
  ]
}
```
> `WithDecryption=true` 옵션 사용 시 KMS Decrypt 권한 필요
