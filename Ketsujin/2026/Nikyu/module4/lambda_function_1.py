import json
import pymysql
import os

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
# Filter 허용 컬럼 목록
# GET /item?category=food&price_lt=5000 처럼 사용
# 요구사항에 따라 자유롭게 추가 / 삭제 / 변경하세요.
#
# FILTER_FIELDS      : 동등(=) 조건으로 필터링할 컬럼
# FILTER_RANGE_FIELDS: 범위 조건(<, >) 필터링할 컬럼
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
                    # 단일 조회 — id가 있으면 Filter/Pagination 무시
                    cursor.execute("SELECT * FROM item WHERE id = %s", (item_id,))
                    result = cursor.fetchone()
                    if not result:
                        return _response(404, {"message": "Item not found"})
                else:
                    # Pagination
                    limit  = int(params.get("limit", DEFAULT_LIMIT))
                    offset = int(params.get("offset", 0))

                    # Filter
                    where, filter_values = build_filter_clause(params)

                    sql    = f"SELECT * FROM item {where} LIMIT %s OFFSET %s"
                    values = filter_values + [limit, offset]

                    cursor.execute(sql, values)
                    result = cursor.fetchall()

                    # 전체 건수 조회 (페이지네이션 메타)
                    cursor.execute(f"SELECT COUNT(*) AS total FROM item {where}", filter_values)
                    total = cursor.fetchone()["total"]

                    result = {
                        "total": total,
                        "limit": limit,
                        "offset": offset,
                        "items": result,
                    }
            conn.close()
            return _response(200, result)
        except Exception as e:
            return _response(500, {"message": str(e)})

    return _response(405, {"message": "Method Not Allowed"})


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=str),
    }
