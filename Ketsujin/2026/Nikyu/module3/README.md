# Fine-grained IAM Policy [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/README.md)

## DynamoDB

### 특정 테이블만 읽기/쓰기
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": "arn:aws:dynamodb:{region}:{account-id}:table/{table-name}"
    }
  ]
}
```
> 인덱스에도 접근하려면 Resource에 `".../index/*"` 추가

---

### 특정 파티션 키 기준 행 수준 접근 (Leading Key 조건)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:{region}:{account-id}:table/{table-name}",
      "Condition": {
        "ForAllValues:StringEquals": {
          "dynamodb:LeadingKeys": ["${aws:PrincipalTag/{tag-key}}"]
        }
      }
    }
  ]
}
```
> 예) IAM 태그 `userId`와 DynamoDB PK가 일치하는 행만 접근 가능

---

### 특정 콜럼만 허용 (Attributes 필터)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["dynamodb:GetItem", "dynamodb:Query"],
      "Resource": "arn:aws:dynamodb:{region}:{account-id}:table/{table-name}",
      "Condition": {
        "ForAllValues:StringEquals": {
          "dynamodb:Attributes": ["{col1}", "{col2}", "{col3}"]
        },
        "StringEqualsIfExists": {
          "dynamodb:Select": "SPECIFIC_ATTRIBUTES"
        }
      }
    }
  ]
}
```
> 지정한 콜럼 외에는 읽기 불가

---

## Secrets Manager

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

### 특정 Prefix의 시크릿만 접근 (ex. 환경별 분리)
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

---

## S3

### 특정 버킷의 특정 프리픽스만 읽기
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::{bucket-name}/{prefix}/*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::{bucket-name}",
      "Condition": {
        "StringLike": {
          "s3:prefix": ["{prefix}/*"]
        }
      }
    }
  ]
}
```
> `ListBucket`은 버킷 ARN, `GetObject`는 객체 ARN에 각각 적용

---

### 데이터 업로드는 허용하지만 삭제는 차단
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::{bucket-name}/{prefix}/*"
    },
    {
      "Effect": "Deny",
      "Action": ["s3:DeleteObject"],
      "Resource": "arn:aws:s3:::{bucket-name}/{prefix}/*"
    }
  ]
}
```

---

## SSM Parameter Store

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

---

## 공통 팅

| 천사 | Resource ARN 패턴 | 주의사항 |
|------|-----------------|----------|
| DynamoDB | `...table/{name}` | 인덱스는 `.../index/*` 대시 추가 |
| Secrets Manager | `...secret:{name}-*` | 접미사 `-*` 필수 |
| S3 GetObject | `...{bucket}/{prefix}/*` | ListBucket은 버킷 ARN 따로 |
| SSM Parameter | `...parameter/{path}/*` | SecureString은 KMS Decrypt 함께 |
