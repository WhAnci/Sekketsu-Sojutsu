# DynamoDB Fine-grained IAM Policy [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module3/README.md)

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

### 특정 컬럼만 허용 (Attributes 필터)
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
> 지정한 컬럼 외에는 읽기 불가
