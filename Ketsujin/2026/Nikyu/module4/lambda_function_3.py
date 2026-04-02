import json
import pymysql
import os
import uuid
from datetime import datetime

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
# POST /item 허용 필드 — 요구사항에 따라 자유롭게 수정하세요.
# -----------------------------------------------------------
CREATE_ALLOWED_FIELDS = ["name", "category", "price"]

# -----------------------------------------------------------
# PUT /item 허용 필드 — id, created_at 은 수정 불가입니다.
# 요구사항에 따라 자유롭게 수정하세요.
# -----------------------------------------------------------
UPDATE_ALLOWED_FIELDS = ["name", "category", "price"]
IMMUTABLE_FIELDS      = {"id", "created_at"}


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
    #   자동 추가 필드: id (UUID), created_at (현재 타임스탬프)
    # -------------------------------------------------------
    if http_method == "POST" and path == "/item":
        try:
            body = json.loads(event.get("body") or "{}")

            data = {k: body[k] for k in CREATE_ALLOWED_FIELDS if k in body}
            if not data:
                return _response(400, {"message": f"Request body must contain at least one of: {CREATE_ALLOWED_FIELDS}"})

            data["id"]         = str(uuid.uuid4())
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

    # -------------------------------------------------------
    # PUT /item?id=<id> → 아이템 수정
    #   id, created_at 은 수정 불가
    # -------------------------------------------------------
    # [주석 처리] Path Parameter 방식
    # PUT /item/<id>  → 아이템 수정
    # path_parts = path.strip("/").split("/")
    # if http_method == "PUT" and len(path_parts) == 2 and path_parts[0] == "item":
    #     item_id = path_parts[1]
    #     ...
    # -------------------------------------------------------

    if http_method == "PUT" and path == "/item":
        item_id = params.get("id")
        if not item_id:
            return _response(400, {"message": "Query parameter 'id' is required"})
        try:
            body = json.loads(event.get("body") or "{}")

            # 불변 필드 제거 후 허용 필드만 필터링
            data = {
                k: body[k]
                for k in UPDATE_ALLOWED_FIELDS
                if k in body and k not in IMMUTABLE_FIELDS
            }
            if not data:
                return _response(400, {"message": f"Request body must contain at least one of: {UPDATE_ALLOWED_FIELDS}"})

            set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
            values     = list(data.values()) + [item_id]

            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    f"UPDATE item SET {set_clause} WHERE id = %s",
                    values,
                )
                if cursor.rowcount == 0:
                    conn.close()
                    return _response(404, {"message": "Item not found"})
            conn.commit()
            conn.close()
            return _response(200, {"message": "Item updated", "id": item_id})
        except Exception as e:
            return _response(500, {"message": str(e)})

    return _response(405, {"message": "Method Not Allowed"})


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=str),
    }
