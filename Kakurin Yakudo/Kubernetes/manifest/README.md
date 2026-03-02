# Kubernetes Manifest 템플릿 가이드

이 디렉토리에는 Kubernetes를 운영할 때 자주 사용되는 YAML 파일 템플릿들이 포함되어 있습니다.
각 파일은 주석이 많이 포함되어 있어 프로젝트에 맞게 수정해서 사용할 수 있습니다.

## 파일 설명

### 1. **deployment.yaml**
- Kubernetes Deployment 템플릿
- 애플리케이션 배포의 기본 단위
- 리소스 제한, 헬스 체크, 롤링 업데이트 등 설정 포함

**사용 예:**
```bash
kubectl apply -f deployment.yaml
kubectl rollout status deployment/app-deployment
```

### 2. **service.yaml**
- ClusterIP, LoadBalancer, NodePort 세 가지 Service 타입
- 애플리케이션을 네트워크로 노출시키는 방법 제공

**사용 예:**
```bash
kubectl apply -f service.yaml -n default
kubectl get svc
```

### 3. **configmap-secret.yaml**
- ConfigMap: 비밀이 아닌 설정 데이터 저장
- Secret: 민감한 정보(비밀번호, API 키) 저장
- 파일 및 키-값 형태 모두 지원

**사용 예:**
```bash
# ConfigMap 생성
kubectl create configmap app-config --from-file=nginx.conf

# Secret 생성
kubectl create secret generic app-secrets --from-literal=password=mypassword
```

### 4. **ingress.yaml**
- Kubernetes Ingress 리소스
- 외부 트래픽을 클러스터 내 Service로 라우팅
- Nginx, AWS ALB 등 다양한 인그레스 컨트롤러 지원

**사용 예:**
```bash
# Nginx Ingress Controller 설치 (필수)
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install my-ingress ingress-nginx/ingress-nginx

kubectl apply -f ingress.yaml
kubectl get ingress
```

### 5. **statefulset-daemonset.yaml**
- **StatefulSet**: 상태가 있는 애플리케이션 (DB, 캐시 등)
- **DaemonSet**: 모든 노드에서 하나씩 실행 (로깅, 모니터링 등)

**사용 예:**
```bash
kubectl apply -f statefulset-daemonset.yaml
kubectl get statefulset
kubectl get daemonset
```

### 6. **job-cronjob.yaml**
- **Job**: 한 번 실행되고 완료되는 작업
- **CronJob**: 주기적으로 반복되는 작업

**사용 예:**
```bash
kubectl apply -f job-cronjob.yaml
kubectl get job
kubectl get cronjob
kubectl logs job/backup-job
```

### 7. **storage.yaml**
- **StorageClass**: 스토리지 프로비저닝 정책
- **PersistentVolume**: 클러스터 레벨 스토리지 리소스
- **PersistentVolumeClaim**: Pod에서 스토리지 요청

**사용 예:**
```bash
kubectl apply -f storage.yaml
kubectl get pv
kubectl get pvc
```

### 8. **network-autoscale.yaml**
- **NetworkPolicy**: 네트워크 트래픽 제어
- **HorizontalPodAutoscaler (HPA)**: CPU/메모리 기반 자동 스케일링
- **VerticalPodAutoscaler (VPA)**: 리소스 사용량 기반 권고

**사용 예:**
```bash
# HPA 적용
kubectl apply -f network-autoscale.yaml

# HPA 상태 확인
kubectl get hpa
kubectl describe hpa app-hpa

# Metrics Server 필요 (메트릭 수집)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### 9. **rbac-quota.yaml**
- **ServiceAccount**: Kubernetes 사용자 계정
- **Role/RoleBinding**: 네임스페이스 수준 권한 관리
- **ClusterRole/ClusterRoleBinding**: 클러스터 수준 권한 관리
- **ResourceQuota**: 네임스페이스별 리소스 할당량
- **LimitRange**: 리소스 최소/최대 제한

**사용 예:**
```bash
kubectl apply -f rbac-quota.yaml

# 권한 확인
kubectl auth can-i get pods --as=system:serviceaccount:default:app-serviceaccount

# ResourceQuota 확인
kubectl get resourcequota
kubectl describe resourcequota compute-quota
```

### 10. **pod-advanced.yaml**
- 다양한 고급 Pod 설정 예제
- InitContainer, 여러 컨테이너, Probe, Affinity, Security Context 등

**사용 예:**
```bash
kubectl apply -f pod-advanced.yaml
kubectl get pods
kubectl logs pod/pod-with-probes
```

## 빠른 시작 가이드

### 1. 필수 설정 수정
각 파일에서 다음을 수정해야 합니다:

```yaml
# 이미지 변경
image: "당신의-이미지:태그"

# 포트 번호
containerPort: 8080

# 리소스 제한
resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

# 환경 변수
env:
- name: DATABASE_URL
  value: "postgres://host:5432/db"
```

### 2. 리소스 생성
```bash
# 단일 파일 생성
kubectl apply -f deployment.yaml

# 여러 파일 한 번에 생성
kubectl apply -f .

# 특정 네임스페이스에 생성
kubectl apply -f deployment.yaml -n production
```

### 3. 상태 확인
```bash
kubectl get pods
kubectl get deployment
kubectl get svc
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs <pod-name> -c <container-name>  # 여러 컨테이너인 경우
```

### 4. 문제 해결
```bash
# Pod 상세 정보 확인
kubectl describe pod <pod-name>

# 로그 확인
kubectl logs <pod-name> --tail=100  # 최근 100줄
kubectl logs <pod-name> -f          # 실시간 스트리밍

# 이벤트 확인
kubectl get events --sort-by='.lastTimestamp'

# 리소스 사용량 확인
kubectl top nodes
kubectl top pods
```

## 네임스페이스 관리

```bash
# 네임스페이스 생성
kubectl create namespace production

# 네임스페이스 조회
kubectl get namespaces

# 특정 네임스페이스의 리소스 조회
kubectl get pods -n production

# 모든 네임스페이스의 리소스 조회
kubectl get pods --all-namespaces
# 또는
kubectl get pods -A
```

## 유용한 명령어

```bash
# 리소스 삭제
kubectl delete -f deployment.yaml
kubectl delete deployment app-deployment

# 리소스 업데이트
kubectl apply -f deployment.yaml

# 롤링 업데이트
kubectl set image deployment/app-deployment app=myapp:v2

# 업데이트 상태 확인
kubectl rollout status deployment/app-deployment

# 업데이트 이력 확인
kubectl rollout history deployment/app-deployment

# 이전 버전으로 롤백
kubectl rollout undo deployment/app-deployment

# Pod 셸 접속
kubectl exec -it <pod-name> -- /bin/bash

# 포트 포워딩
kubectl port-forward svc/app-service-clusterip 8080:80
```

## 주의사항

1. **이미지 선택**: 최신 버전의 이미지 사용을 권장합니다
2. **리소스 제한**: CPU/메모리 제한을 적절히 설정해야 합니다
3. **프로브 설정**: 헬스 체크 패턴을 애플리케이션에 맞게 수정합니다
4. **보안**: Secret에는 실제 비밀번호를 넣지 않고, 배포 전에 교체하세요
5. **테스트**: 프로덕션 배포 전에 staging 환경에서 충분히 테스트하세요

## 참고 자료

- [Kubernetes 공식 문서](https://kubernetes.io/docs/)
- [Kubectl 치트 시트](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Best Practices](https://kubernetes.io/docs/concepts/best-practices/)
