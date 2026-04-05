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
# POST /item 허용 필드 — 요구사항에 따라 자유롭게 수정하세요.
# -----------------------------------------------------------
CREATE_ALLOWED_FIELDS = ["name", "category", "price"]

# -----------------------------------------------------------
# PUT /item 허용 필드 — id, created_at 은 수정 불가입니다.
# 요구사항에 따라 자유롭게 수정하세요.
# -----------------------------------------------------------
UPDATE_ALLOWED_FIELDS = ["name", "category", "price"]
IMMUTABLE_FIELDS      = {"id", "created_at"}

# -----------------------------------------------------------
# Filter 허용 컨럼 목록
# GET /item?category=food&price_lt=5000 처럼 사용
# 요구사항에 따라 자유롭게 추가 / 삭제 / 변경하세요.
#
# FILTER_FIELDS      : 동등(=) 조건으로 필터링할 컨럼
# FILTER_RANGE_FIELDS: 범위 조건(<, >) 필터링할 컨럼
#   예) price_lt → price < %s  /  price_gt → price > %s
# -----------------------------------------------------------
FILTER_FIELDS       = ["category"]
FILTER_RANGE_FIELDS = ["price"]   # price_lt / price_gt 파라미터 자동 지원

# 페이지당 기본 조회 건수
DEFAULT_LIMIT = 20


def get_connection():
    return pymysql.connect(
        host=RDS_HOST,
        port=RDS_PORT,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB,
        cursorclass=pymysql.cursors.DictCursor,
    )


def build_filter_clause(params):
    """Query Parameter로부터 WHERE 절과 바인딩 값을 동적으로 생성합니다."""
    conditions = []
    values     = []

    for col in FILTER_FIELDS:
        if col in params:
            conditions.append(f"{col} = %s")
            values.append(params[col])

    for col in FILTER_RANGE_FIELDS:
        if f"{col}_lt" in params:
            conditions.append(f"{col} < %s")
            values.append(params[f"{col}_lt"])
        if f"{col}_gt" in params:
            conditions.append(f"{col} > %s")
            values.append(params[f"{col}_gt"])

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    return where, values


def lambda_handler(event, context):
    http_method = event.get("httpMethod", "")
    path        = event.get("path", "")
    params      = event.get("queryStringParameters") or {}

    # -------------------------------------------------------
    # GET /item                          → 전체 조회 (Filter + Pagination)
    # GET /item?id=<id>                  → 단일 아이템 조회
    # GET /item?category=food            → 필터 조회
    # GET /item?price_lt=5000            → 범위 필터 조회
    # GET /item?limit=10&offset=0        → 페이지네이션
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
                    limit  = int(params.get("limit", DEFAULT_LIMIT))
                    offset = int(params.get("offset", 0))

                    where, filter_values = build_filter_clause(params)

                    sql    = f"SELECT * FROM item {where} LIMIT %s OFFSET %s"
                    values = filter_values + [limit, offset]

                    cursor.execute(sql, values)
                    items = cursor.fetchall()

                    cursor.execute(f"SELECT COUNT(*) AS total FROM item {where}", filter_values)
                    total = cursor.fetchone()["total"]

                    result = {
                        "total": total,
                        "limit": limit,
                        "offset": offset,
                        "items": items,
                    }
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
    if http_method == "PUT" and path == "/item":
        item_id = params.get("id")
        if not item_id:
            return _response(400, {"message": "Query parameter 'id' is required"})
        try:
            body = json.loads(event.get("body") or "{}")

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

    # -------------------------------------------------------
    # DELETE /item?id=<id> → 아이템 삭제
    # -------------------------------------------------------
    if http_method == "DELETE" and path == "/item":
        item_id = params.get("id")
        if not item_id:
            return _response(400, {"message": "Query parameter 'id' is required"})
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM item WHERE id = %s", (item_id,))
                if cursor.rowcount == 0:
                    conn.close()
                    return _response(404, {"message": "Item not found"})
            conn.commit()
            conn.close()
            return _response(200, {"message": "Item deleted", "id": item_id})
        except Exception as e:
            return _response(500, {"message": str(e)})

    return _response(405, {"message": "Method Not Allowed"})


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=str),
    }
