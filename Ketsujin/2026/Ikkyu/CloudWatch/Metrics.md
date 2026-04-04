# Metrics [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Ikkyu/CloudWatch/README.md)

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

## 팁

- `totalcpu: true` → 코어별 + 전체 평균 동시 수집
- `drop_original_metrics` → 집계 메트릭만 남기고 원본 제거 (비용 절감)
- `aggregation_dimensions` → ASG 단위 집계 메트릭 생성 가능
