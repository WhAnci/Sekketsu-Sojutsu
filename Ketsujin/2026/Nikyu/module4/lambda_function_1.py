import json
import pymysql
import os

# ===========================================================
# ★ 수정 포인트 ★  — 아래 설정만 바꾸면 됩니다.
# ===========================================================

# RDS 연결 정보 (Lambda 환경 변수로 주입)
RDS_HOST     = os.getenv("RDS_HOST")
RDS_PORT     = int(os.getenv("RDS_PORT", 3306))
RDS_USER     = os.getenv("RDS_USER")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_DB       = os.getenv("RDS_DB")

# 조회 대상 테이블 이름
TABLE_NAME = "item"

# ===========================================================
# 내부 유틸
# ===========================================================

def _get_connection():
    return pymysql.connect(
        host=RDS_HOST, port=RDS_PORT,
        user=RDS_USER, password=RDS_PASSWORD,
        database=RDS_DB,
        cursorclass=pymysql.cursors.DictCursor,
    )


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=str),
    }


# ===========================================================
# 핸들러 — GET 단건 / 전체 조회
# ===========================================================
# 지원 엔드포인트
#   GET /item           → 전체 조회
#   GET /item?id=<id>   → 단건 조회
# -----------
# Path Parameter 방식으로 바꾸려면?
#   아래 주석 블록을 해제하고 Query Parameter 블록을 주석 처리하세요.
# -----------
# [Path Parameter 방식 — 해제하면 사용 가능]
# path_parts = path.strip("/").split("/")
# if http_method == "GET" and len(path_parts) == 2 and path_parts[0] == TABLE_NAME:
#     item_id = path_parts[1]
#     ...  (단건 조회 로직)
# ===========================================================

def lambda_handler(event, context):
    http_method = event.get("httpMethod", "")
    path        = event.get("path", "")
    params      = event.get("queryStringParameters") or {}

    if http_method == "GET" and path == f"/{TABLE_NAME}":
        return _handle_get(params)

    return _response(405, {"message": "Method Not Allowed"})


# ===========================================================
# GET 처리
# ===========================================================

def _handle_get(params):
    item_id = params.get("id")
    try:
        conn = _get_connection()
        with conn.cursor() as cur:
            if item_id:
                cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = %s", (item_id,))
                result = cur.fetchone()
                if not result:
                    conn.close()
                    return _response(404, {"message": "Item not found"})
            else:
                cur.execute(f"SELECT * FROM {TABLE_NAME}")
                result = cur.fetchall()
        conn.close()
        return _response(200, result)
    except Exception as e:
        return _response(500, {"message": str(e)})
