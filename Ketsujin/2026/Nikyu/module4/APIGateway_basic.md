# API Gateway — 기본 연동 (REST API + Lambda Proxy) [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module4/README.md)

## 1. REST API 생성

콘솔 → API Gateway → **Create API** → REST API → Build

| 항목 | 값 |
|------|----|
| API name | 요구사항에 맞게 |
| Endpoint Type | Regional |

---

## 2. 리소스 생성

**Actions → Create Resource**

| 항목 | 값 |
|------|----|
| Resource Path | `/item` |
| Enable API Gateway CORS | ✅ 체크 (CORS 요구 시) |

> 경로 파라미터 방식(`ID_SOURCE = "path"`) 요구 시 `/item/{id}` 리소스도 추가 생성

---

## 3. 메서드 연결

`/item` 선택 → **Actions → Create Method** → `ANY` (또는 GET, POST, PUT, DELETE 개별)

| 항목 | 값 |
|------|----|
| Integration type | Lambda Function |
| Use Lambda Proxy integration | ✅ **반드시 체크** |
| Lambda Function | 연결할 함수 이름 입력 |

> ⚠️ **Lambda Proxy integration 미체크 시** `httpMethod`, `path` 등이 event에 전달되지 않아 함수가 동작하지 않음

---

## 4. CORS 헤더 추가 (Lambda 코드)

Lambda Proxy 방식에서는 **Lambda 응답에 직접 CORS 헤더를 넣어야** 함.

```python
def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,PATCH,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Api-Key",
        },
        "body": json.dumps(body, default=str),
    }
```

> CORS 요구사항이 없으면 `Content-Type`만 있어도 무방

---

## 5. API 배포

**Actions → Deploy API**

| 항목 | 값 |
|------|----|
| Deployment stage | [New Stage] |
| Stage name | `prod` (요구사항에 맞게) |

배포 후 Invoke URL:
```
https://{api-id}.execute-api.ap-northeast-2.amazonaws.com/prod/item
```

---

## 6. 동작 확인

```bash
# 전체 조회
curl https://{invoke-url}/prod/item

# 단일 조회 (query 방식)
curl https://{invoke-url}/prod/item?id=<uuid>

# 단일 조회 (path 방식)
curl https://{invoke-url}/prod/item/<uuid>

# 생성
curl -X POST https://{invoke-url}/prod/item \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "category": "food", "price": 1000}'

# 삭제
curl -X DELETE https://{invoke-url}/prod/item?id=<uuid>
```

---

## 7. Lambda 환경변수 설정

Lambda 함수 → Configuration → Environment variables

| Key | Value |
|-----|-------|
| `RDS_HOST` | RDS 엔드포인트 |
| `RDS_PORT` | `3306` |
| `RDS_USER` | DB 사용자명 |
| `RDS_PASSWORD` | DB 비밀번호 |
| `RDS_DB` | DB 이름 |

> Secrets Manager 연동 방식은 [EC2 가이드](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Ikkyu/EC2/README.md) 참고

---

## 8. VPC Lambda (RDS 접근 시)

Lambda → Configuration → VPC

- RDS와 **동일한 VPC + Private Subnet** 선택
- Lambda용 Security Group → RDS Security Group의 **3306 포트 인바운드 허용**
- RDS Security Group 인바운드: Lambda SG에서 3306 허용
