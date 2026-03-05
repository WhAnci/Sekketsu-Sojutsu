# KEDA
## Setup [(Official Guide)](https://keda.sh/docs/2.19/deploy/)
### Add helm repo
```bash
helm repo add kedacore https://kedacore.github.io/charts  
helm repo update
```
### Install KEDA
```bash
helm install keda kedacore/keda --namespace keda --create-namespace
```
### Apply CRD
```
k create -f https://github.com/kedacore/keda/releases/download/v2.19.0/keda-2.19.0-crds.yaml
```
### Verify
```bash
watch kubectl get pods -n keda
```
### Expected Output
```bash
Every 2.0s: kubectl get pods -n keda                                                                 ip-10-0-5-51.ap-northeast-2.compute.internal: Thu Mar  5 14:21:27 2026

NAME                                               READY   STATUS    RESTARTS        AGE
keda-admission-webhooks-7b48797dc8-pncsp           1/1     Running   0               6m52s
keda-operator-55db59458d-j8kgg                     1/1     Running   1 (6m33s ago)   6m52s
keda-operator-metrics-apiserver-5c648889d4-vj2dc   1/1     Running   0               6m52s
```
