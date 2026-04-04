# Athena Table [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module2/README.md)

## Hive Format
S3 경로가 `key=value` 형태로 파티션된 경우 사용
```
s3://{bucket}/{prefix}/year=2024/month=01/day=15/
```

```sql
CREATE EXTERNAL TABLE {table_name} (
  {col1} {type1},
  {col2} {type2}
)
PARTITIONED BY (
  {partition_col1} {type},
  {partition_col2} {type}
)
STORED AS {format}  -- PARQUET / ORC / JSON / CSV
LOCATION 's3://{bucket}/{prefix}/';
```

> 파티션 콜럼은 데이터 콜럼에 포함하지 않음

파티션 등록 (테이블 생성 후 실행)
```sql
-- 수동 등록
ALTER TABLE {table_name}
ADD PARTITION ({partition_col1}='{value1}', {partition_col2}='{value2}')
LOCATION 's3://{bucket}/{prefix}/{partition_col1}={value1}/{partition_col2}={value2}/';

-- 자동 인식 (MSCK)
MSCK REPAIR TABLE {table_name};
```

---

## Non-Hive Format
S3 경로가 `key=value` 형태가 아닌 일반 경로인 경우 사용
```
s3://{bucket}/{prefix}/2024/01/15/
```

```sql
CREATE EXTERNAL TABLE {table_name} (
  {col1} {type1},
  {col2} {type2}
)
PARTITIONED BY (
  {partition_col1} {type},
  {partition_col2} {type}
)
STORED AS {format}
LOCATION 's3://{bucket}/{prefix}/';
```

파티션 등록 (경로를 직접 지정해야 함)
```sql
ALTER TABLE {table_name}
ADD PARTITION ({partition_col1}='{value1}', {partition_col2}='{value2}')
LOCATION 's3://{bucket}/{prefix}/{value1}/{value2}/';
```

> Hive Format과 달리 MSCK REPAIR 사용 불가 → 파티션은 반드시 수동 등록

---

## Partition Projection
S3에 데이터가 추가될 때마다 파티션을 등록하지 않아도 Athena가 범위를 자동 계산

```sql
CREATE EXTERNAL TABLE {table_name} (
  {col1} {type1},
  {col2} {type2}
)
PARTITIONED BY (
  {partition_col} {type}  -- ex) dt string
)
STORED AS {format}
LOCATION 's3://{bucket}/{prefix}/'
TBLPROPERTIES (
  'projection.enabled' = 'true',

  -- 정수형 범위
  'projection.{partition_col}.type'          = 'integer',
  'projection.{partition_col}.range'         = '{min},{max}',  -- ex) 2020,2030
  'projection.{partition_col}.interval'      = '1',

  -- 날짜형 범위
  -- 'projection.{partition_col}.type'       = 'date',
  -- 'projection.{partition_col}.range'      = '2024-01-01,NOW',
  -- 'projection.{partition_col}.format'     = 'yyyy-MM-dd',
  -- 'projection.{partition_col}.interval'   = '1',
  -- 'projection.{partition_col}.interval.unit' = 'DAYS',

  -- 열거형 (고정 값 목록)
  -- 'projection.{partition_col}.type'       = 'enum',
  -- 'projection.{partition_col}.values'     = '{value1},{value2},{value3}',

  'storage.location.template' = 's3://{bucket}/{prefix}/${' || '{partition_col}}'
);
```

> `MSCK REPAIR` 나 `ALTER TABLE ADD PARTITION` 불필요
> 실제 S3에 해당 경로만 있으면 작동함
