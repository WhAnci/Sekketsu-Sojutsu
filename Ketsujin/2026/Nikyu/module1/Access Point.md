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
