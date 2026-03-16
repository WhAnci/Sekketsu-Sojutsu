# Grafana
## Install Grafana
### Add the Grafana repository
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```
### Deploy the grafana helm charts
```bash
kubectl create namespace grafana
helm install my-grafana grafana/grafana --namespace grafana
```
## Access Grafana
### View Grafana Notes
```bash
helm get notes my-grafana -n grafana
```
### Get Admin Password
```bash
kubectl get secret --namespace monitoring my-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```
### Port forwarding Grafana
```bash
export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=my-grafana" -o jsonpath="{.items[0].metadata.name}")
kubectl --namespace monitoring port-forward $POD_NAME 23000:3000 & # 백그라운드로 실행
```
## Use setup.sh
```bash
curl -fsSL https://raw.githubusercontent.com/WhAnci/Sen-ketsu/refs/heads/main/Kakurin%20Yakudo/Kubernetes/Grafana/setup.sh | bash
```
