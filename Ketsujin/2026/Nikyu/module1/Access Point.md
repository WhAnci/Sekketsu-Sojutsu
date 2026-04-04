# EFS Access Point [[돌아가기]](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Ketsujin/2026/Nikyu/module1/README.md)

## Details
### Root Directory Path
- EFS 파일 시스템 내의 특정 디렉토리를 루트(/)처럼 보이게 만듦
- 예: /data/app1을 Root Directory로 설정하면, 애플리케이션은 /data/app1을 /로 인식
- 경로가 존재하지 않으면 자동 생성 (아래 creation permissions 참조)
- 애플리케이션의 파일 시스템 접근 범위를 제한

## POSIX User
### User ID
- 파일 시스템 작업(읽기/쓰기)을 수행하는 사용자 ID
- 이 UID가 파일 소유자로 기록됨
- 예: 1000 (일반적으로 애플리케이션 전용 사용자)

### Group ID
- 파일 시스템 작업 시 사용하는 주 그룹 ID
- 파일 생성 시 이 GID가 기본 그룹으로 설정
- 예: 1000

### Secondary Group IDs
- 기본 Group ID 외에 추가로 적용할 보조 그룹 ID 목록
- 여러 그룹에 걸친 파일 접근 권한이 필요할 때 사용
- 예: [2000, 3000] → 해당 GID를 가진 파일에도 그룹 권한으로 접근 가능
- 최대 16개까지 지정 가능

## Root Directory Creation Permissions
### Owner User ID
- Root Directory Path가 존재하지 않을 때 자동 생성되는 디렉토리의 소유자 UID
- POSIX User의 User ID와 다르게 설정 가능
- 예: 1000

### Owner Group ID
- 자동 생성되는 디렉토리의 소유 그룹 GID
- POSIX User의 Group ID와 다르게 설정 가능
- 예: 1000

### Access point Permissions
- 자동 생성되는 디렉토리에 적용할 Unix 퍼미션 (8진수)
- 클라이언트가 디렉토리에 진입하려면 실행(x) 비트가 필요
- 예: 0755 → 소유자는 rwx, 그룹/기타는 r-x

### Permissions 표

| 권한값 | 심볼 | 소유자 | 그룹 | 기타 | 사용 사례 |
|--------|--------|--------|------|------|----------|
| 0755 | rwxr-xr-x | rwx | r-x | r-x | 일반적인 디렉토리, 모두 읽기/진입 가능, 쓰기는 소유자만 |
| 0750 | rwxr-x--- | rwx | r-x | --- | 그룹만 읽기/진입 가능, 외부 접근 차단 |
| 0700 | rwx------ | rwx | --- | --- | 소유자만 접근, 높은 보안이 필요한 디렉토리 |
| 0777 | rwxrwxrwx | rwx | rwx | rwx | 모두 읽기/쓰기/진입 가능, 테스트용 외 비권장 |
| 0644 | rw-r--r-- | rw- | r-- | r-- | 파일에 주로 사용, 디렉토리에 활용 불가 (x 없음) |
| 0600 | rw------- | rw- | --- | --- | 소유자만 읽기/쓰기, 완전 비공개 파일 |
