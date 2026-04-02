# EFS IAM Policy

> AWS EFS(Elastic File System) 접근 제어를 위한 IAM Policy 정의입니다.  
> 최소 권한 원칙에 따라 역할별로 필요한 액션만 부여합니다.

---

## Role 목록

| Role 이름 | 용도 |
|---|---|
| `efs-readonly-role` | 읽기 전용 마운트 |
| `efs-readwrite-role` | 읽기/쓰기 마운트 |
| `efs-root-role` | 루트(UID 0) 접근 |

---

## 1. efs-readonly-role

EFS 파일 시스템을 **읽기 전용**으로 마운트합니다.  
`ClientWrite`, `ClientRootAccess` 는 부여하지 않습니다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EFSReadOnly",
      "Effect": "Allow",
      "Action": [
        "elasticfilesystem:ClientMount",
        "elasticfilesystem:DescribeFileSystems",
        "elasticfilesystem:DescribeMountTargets"
      ],
      "Resource": "arn:aws:elasticfilesystem:<region>:<account-id>:file-system/*"
    }
  ]
}
```

---

## 2. efs-readwrite-role

EFS 파일 시스템에 **읽기 및 쓰기** 작업이 가능합니다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EFSReadWrite",
      "Effect": "Allow",
      "Action": [
        "elasticfilesystem:ClientMount",
        "elasticfilesystem:ClientWrite",
        "elasticfilesystem:DescribeFileSystems",
        "elasticfilesystem:DescribeMountTargets"
      ],
      "Resource": "arn:aws:elasticfilesystem:<region>:<account-id>:file-system/*"
    }
  ]
}
```

---

## 3. efs-root-role

EFS Access Point를 통해 **UID 0(root) 권한**으로 접근합니다.  
시스템 운영 목적으로만 사용하며, 최소한의 대상에게만 부여하세요.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EFSRootAccess",
      "Effect": "Allow",
      "Action": [
        "elasticfilesystem:ClientMount",
        "elasticfilesystem:ClientWrite",
        "elasticfilesystem:ClientRootAccess",
        "elasticfilesystem:DescribeFileSystems",
        "elasticfilesystem:DescribeMountTargets"
      ],
      "Resource": "arn:aws:elasticfilesystem:<region>:<account-id>:file-system/*"
    }
  ]
}
```

---

## Trust Policy (공통)

세 Role 모두 동일한 Trust Policy를 사용합니다.

### EC2

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### EKS IRSA

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<account-id>:oidc-provider/oidc.eks.<region>.amazonaws.com/id/<OIDC_ID>"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.<region>.amazonaws.com/id/<OIDC_ID>:sub": "system:serviceaccount:<namespace>:<serviceaccount-name>"
        }
      }
    }
  ]
}
```

---

## 권한 비교

| Action | efs-readonly-role | efs-readwrite-role | efs-root-role |
|---|:---:|:---:|:---:|
| `ClientMount` | ✅ | ✅ | ✅ |
| `ClientWrite` | ❌ | ✅ | ✅ |
| `ClientRootAccess` | ❌ | ❌ | ✅ |
| `DescribeFileSystems` | ✅ | ✅ | ✅ |
| `DescribeMountTargets` | ✅ | ✅ | ✅ |

---

## 주의사항

- `Resource`는 `*` 대신 **특정 EFS ARN**으로 제한하는 것을 강력히 권장합니다
- EFS **File System Policy**(리소스 기반)와 IAM Policy **모두 Allow** 되어야 최종 접근이 가능합니다 (명시적 Deny 우선)
- Access Point 사용 시 `elasticfilesystem:AccessPointArn` Condition으로 접근 범위를 추가 제한하세요
- Kubernetes 환경에서는 **IRSA**와 연동하여 Pod 단위 권한 제어를 권장합니다
