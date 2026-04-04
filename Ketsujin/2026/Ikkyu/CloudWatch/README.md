# CloudWatch Agent [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Ikkyu/README.md)

EC2에서 CloudWatch Agent로 기본 제공되지 않는 메트릭(메모리, 디스크 등)을 수집.

## 수집 메트릭

| 카테고리 | 주요 메트릭 | 비고 |
|---------|------------|------|
| CPU | `usage_active`, `usage_iowait`, `usage_user`, `usage_system` | `iowait` 높으면 EBS 병목 의심 |
| Memory | `used_percent`, `available_percent`, `used` | EC2 기본 메트릭에 없어서 필수 |
| Disk | `used_percent`, `inodes_free` | inode 소진 시 파일 생성 불가 |
| Disk I/O | `reads`, `writes`, `read_bytes`, `write_bytes`, `io_time` | |
| Network | `bytes_sent`, `bytes_recv`, `packets_sent`, `packets_recv` | |
| Netstat | `tcp_established`, `tcp_time_wait`, `udp_socket` | |
| Processes | `running`, `sleeping`, `total`, `zombies` | zombie 증가 시 코드 버그 의심 |
| Swap | `used_percent` | |

## Logs 수집 항목

| 항목 | 설명 |
|------|------|
| `file_path` | 수집할 로그 파일 경로 |
| `log_group_name` | CloudWatch Log Group 이름 |
| `log_stream_name` | `{instance_id}` 등으로 인스턴스 구분 |
| `retention_in_days` | 로그 보존 기간 |
| `multi_line_start_pattern` | Java 스택트레이스 등 멀티라인 처리 |

## 설정 파일

[[cwagent-config.json]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Ikkyu/CloudWatch/cwagent-config.json) — `__PLACEHOLDER__` 값만 교체해서 사용

## 주요 명령어

```bash
# 설치 (Amazon Linux 2 / AL2023)
sudo yum install -y amazon-cloudwatch-agent

# 설정 적용 및 시작
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json \
  -s

# 상태 확인
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -m ec2 -a status
```

## IAM 권한

EC2 Instance Profile에 `CloudWatchAgentServerPolicy` 관리형 정책 연결로 충분.

> SSM Parameter Store에 설정 저장 시 `ssm:GetParameter` 권한 추가 필요

## 팁

- `totalcpu: true` → 코어별 + 전체 평균 동시 수집
- `drop_original_metrics` → 집계 메트릭만 남기고 원본 제거 (비용 절감)
- `aggregation_dimensions` → ASG 단위 집계 메트릭 생성 가능
- SSM Parameter Store에 설정 저장하면 Auto Scaling 그룹 전체에 자동 적용
