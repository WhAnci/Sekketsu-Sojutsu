# MySQL with Lambda [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/README.md)
## [SQL Generator](https://whanci.github.io/sql-generator/)
## [Layer](https://github.com/WhAnci/Sekketsu-Sojutsu/tree/main/Ketsujin/2026/Nikyu/module4/Layer)

## API Gateway
### [기본 연동 (REST API + Lambda Proxy)](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module4/APIGateway_basic.md)
### [Cognito Authorizer](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module4/APIGateway_cognito.md)

## Function
### [function 1](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module4/lambda_function_1.py)
- `GET /item` 전체 조회
- `GET /item?id=<id>` 단일 조회

### [function 2](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module4/lambda_function_2.py)
- function 1 + `POST /item` 생성 (UUID 자동 발급, created_at 자동 저장)

### [function 3](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module4/lambda_function_3.py)
- function 2 + `PUT /item?id=<id>` 수정 (id, created_at 불변)
- `PATCH /item?id=<id>` 부분 수정

### [function 4](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module4/lambda_function_4.py)
- function 3 + `updated_at` 자동 저장 (생성 시 기록, 수정 시 자동 갱신)

### [function 5](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module4/lambda_function_5.py)
- function 3 + Filter(`category`, `price_lt`, `price_gt`) + Pagination(`limit`, `offset`)

### [function 6](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module4/lambda_function_6.py)
- function 5 + `DELETE /item?id=<id>` 삭제 → CRUD 완성
