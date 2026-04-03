import json
import pymysql
import os
import uuid
from datetime import datetime  # created_at 미사용 시 이 줄도 제거 가능

# -----------------------------------------------------------
# Lambda Environment Variables (Lambda 콘솔에서 설정)
#   RDS_HOST     : RDS 엔드포인트
#   RDS_PORT     : 포트 (기본 3306)
#   RDS_USER     : DB 사용자명
#   RDS_PASSWORD : DB 비밀번호
#   RDS_DB       : 데이터베이스 이름
# -----------------------------------------------------------

RDS_HOST     = os.getenv("RDS_HOST")
RDS_PORT     = int(os.getenv("RDS_PORT", 3306))
RDS_USER     = os.getenv("RDS_USER")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_DB       = os.getenv("RDS_DB")

# -----------------------------------------------------------
# POST /item 요청 시 허용할 필드 목록
# 요구사항에 따라 자유롭게 추가 / 삭제 / 변경하세요.
# -----------------------------------------------------------
ALLOWED_FIELDS = ["name", "category", "price"]


def get_connection():
    return pymysql.connect(
        host=RDS_HOST,
        port=RDS_PORT,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB,
        cursorclass=pymysql.cursors.DictCursor,
    )


def lambda_handler(event, context):
    http_method = event.get("httpMethod", "")
    path        = event.get("path", "")
    params      = event.get("queryStringParameters") or {}

    # -------------------------------------------------------
    # GET /item           → 아이템 전체 조회
    # GET /item?id=<id>   → 단일 아이템 조회
    # -------------------------------------------------------
    # [주석 처리] Path Parameter 방식
    # GET /item/<id>  → 단일 아이템 조회
    # path_parts = path.strip("/").split("/")
    # if len(path_parts) == 2 and path_parts[0] == "item":
    #     item_id = path_parts[1]
    #     ...
    # -------------------------------------------------------

    if http_method == "GET" and path == "/item":
        item_id = params.get("id")
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                if item_id:
                    cursor.execute("SELECT * FROM item WHERE id = %s", (item_id,))
                    result = cursor.fetchone()
                    if not result:
                        return _response(404, {"message": "Item not found"})
                else:
                    cursor.execute("SELECT * FROM item")
                    result = cursor.fetchall()
            conn.close()
            return _response(200, result)
        except Exception as e:
            return _response(500, {"message": str(e)})

    # -------------------------------------------------------
    # POST /item → 아이템 생성
    # -------------------------------------------------------
    if http_method == "POST" and path == "/item":
        try:
            body = json.loads(event.get("body") or "{}")

            data = {k: body[k] for k in ALLOWED_FIELDS if k in body}
            if not data:
                return _response(400, {"message": f"Request body must contain at least one of: {ALLOWED_FIELDS}"})

            # -------------------------------------------------------
            # 자동 생성 필드: id (UUID)
            # -------------------------------------------------------
            data["id"] = str(uuid.uuid4())

            # -------------------------------------------------------
            # 자동 생성 필드: created_at (현재 타임스탬프)
            # 테이블에 created_at 커럼이 없으면 아래 줄을 주석 처리하세요.
            # -------------------------------------------------------
            data["created_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

            columns      = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            values       = list(data.values())

            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO item ({columns}) VALUES ({placeholders})",
                    values,
                )
            conn.commit()
            conn.close()
            return _response(201, {"message": "Item created", "id": data["id"]})
        except Exception as e:
            return _response(500, {"message": str(e)})

    return _response(405, {"message": "Method Not Allowed"})


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=str),
    }
