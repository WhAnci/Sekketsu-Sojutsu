# Logs [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Ikkyu/CloudWatch/README.md)

| 항목 | 설명 |
|------|------|
| `file_path` | 수집할 로그 파일 경로 |
| `log_group_name` | CloudWatch Log Group 이름 |
| `log_stream_name` | `{instance_id}` 등으로 인스턴스 구분 |
| `retention_in_days` | 로그 보존 기간 |
| `multi_line_start_pattern` | Java 스택트레이스 등 멀티라인 처리 |

> SSM Parameter Store에 설정 저장하면 Auto Scaling 그룹 전체에 자동 적용
