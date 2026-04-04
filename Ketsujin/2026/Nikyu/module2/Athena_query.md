# Athena Query Templates [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module2/README.md)

### 특정 값 순서대로 정렬 조회 (CASE WHEN 정렬)
```sql
SELECT *
FROM {table}
ORDER BY
  CASE {column}
    WHEN '{value1}' THEN 1
    WHEN '{value2}' THEN 2
    WHEN '{value3}' THEN 3
    ELSE 4
  END;
```
> 예) `{column}` = `region`, `{value1~3}` = `Seoul`, `Busan`, `Daegu`

---

### 오름차순 / 내림차순 정렬 조회
```sql
-- 오름차순 (ASC)
SELECT *
FROM {table}
ORDER BY {column} ASC;

-- 내림차순 (DESC)
SELECT *
FROM {table}
ORDER BY {column} DESC;
```
> 예) `{column}` = `salary`, `age`, `score`

---

### 특정 값 이상 / 이하 / 초과 / 미만 필터
```sql
SELECT *
FROM {table}
WHERE {column} >= {value};
-- >= 이상 / <= 이하 / > 초과 / < 미만
```
> 예) `{column}` = `hire_date`, `{value}` = `DATE '2023-03-14'`

---

### 날짜 범위 필터 (BETWEEN)
```sql
SELECT *
FROM {table}
WHERE {date_column} BETWEEN DATE '{start_date}' AND DATE '{end_date}';
```
> 예) `{date_column}` = `created_at`, `{start_date}` = `2024-01-01`, `{end_date}` = `2024-12-31`

---

### 특정 값 목록에 포함되는 데이터 조회 (IN)
```sql
SELECT *
FROM {table}
WHERE {column} IN ('{value1}', '{value2}', '{value3}');
```
> 예) `{column}` = `department`, `{value1~3}` = `'HR'`, `'Dev'`, `'Sales'`

---

### 특정 문자열이 포함된 데이터 조회 (LIKE)
```sql
SELECT *
FROM {table}
WHERE {column} LIKE '%{keyword}%';
-- 접두사 검색: '{keyword}%' / 접미사 검색: '%{keyword}'
```
> 예) `{column}` = `name`, `{keyword}` = `김`

---

### 그룹별 집계 (GROUP BY)
```sql
SELECT {group_column}, COUNT(*) AS count, AVG({agg_column}) AS avg_value
FROM {table}
GROUP BY {group_column}
ORDER BY count DESC;
-- 집계 함수: COUNT / SUM / AVG / MAX / MIN
```
> 예) `{group_column}` = `region`, `{agg_column}` = `salary`

---

### 그룹별 집계 결과 필터 (HAVING)
```sql
SELECT {group_column}, COUNT(*) AS count
FROM {table}
GROUP BY {group_column}
HAVING COUNT(*) >= {min_count};
```
> 예) 직원 수가 {min_count}명 이상인 부서만 출력

---

### 상위 N개 데이터 조회 (LIMIT)
```sql
SELECT *
FROM {table}
ORDER BY {column} DESC
LIMIT {n};
```
> 예) 연봉 상위 10명: `{column}` = `salary`, `{n}` = `10`

---

### NULL 포함 / 제외 조회
```sql
-- NULL인 데이터
SELECT *
FROM {table}
WHERE {column} IS NULL;

-- NULL이 아닌 데이터
SELECT *
FROM {table}
WHERE {column} IS NOT NULL;
```
> 예) `{column}` = `phone_number`, `email`

---

### 여러 조건 복합 (AND / OR)
```sql
SELECT *
FROM {table}
WHERE {column1} = '{value1}'
  AND {column2} >= {value2}
  AND ({column3} = '{value3a}' OR {column3} = '{value3b}');
```
> 예) 지역이 서울이고 연봉이 5000만 이상이며 부서가 Dev 또는 HR
