# Fine-grained IAM Policy [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/README.md)

## Services
- [[DynamoDB]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module3/DynamoDB.md)
- [[Secrets Manager]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module3/SecretsManager.md)
- [[S3]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module3/S3.md)
- [[SSM Parameter Store]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module3/SSM.md)

## 공통 팁

| 서비스 | Resource ARN 패턴 | 주의사항 |
|--------|-----------------|----------|
| DynamoDB | `arn:aws:dynamodb:{region}:{account-id}:table/{name}` | 인덱스는 `.../index/*` 추가 |
| Secrets Manager | `arn:aws:secretsmanager:{region}:{account-id}:secret:{name}-*` | 접미사 `-*` 필수 |
| S3 GetObject | `arn:aws:s3:::{bucket}/{prefix}/*` | ListBucket은 버킷 ARN 따로 |
| SSM Parameter | `arn:aws:ssm:{region}:{account-id}:parameter/{path}/*` | SecureString은 KMS Decrypt 함께 |
