# Prometheus
## Install
### Create default storageclass
```bash
kubectl apply -f - <<'EOF'
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  fsType: ext4
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
EOF
```
#### OR use Github Raw File
```bash
kubectl apply -f https://raw.githubusercontent.com/WhAnci/Sen-ketsu/refs/heads/main/Kakurin%20Yakudo/Kubernetes/Prometheus/gp3.yaml
```
### Use Helm
```bash
kubectl create namespace prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm upgrade -i prometheus prometheus-community/prometheus \
    --namespace prometheus

```
## Access Prometheus
### Port-Forwarding
```bash
kubectl --namespace=prometheus port-forward deploy/prometheus-server  19090:9090 &
```
### Use setup.sh
```
curl -fsSL https://raw.githubusercontent.com/WhAnci/Sen-ketsu/refs/heads/main/Kakurin%20Yakudo/Kubernetes/Prometheus/setup.sh | bash
```
## Information
```bash
"-------------------------------------------------------"
"                       (～￣▽￣)～"
"Prometheus server is running!"
"Local Access:      http://localhost:19090"
"Private Network:   http://${PRIVATE_IP}:19090"
"Public Access:     http://${PUBLIC_IP}:19090"
"Target Pod:        $POD_NAME"
"-------------------------------------------------------"
```
