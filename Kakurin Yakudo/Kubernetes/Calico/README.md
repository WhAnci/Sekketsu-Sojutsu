# Calico
## Setup [(Official Guide)](https://docs.tigera.io/calico/latest/getting-started/kubernetes/helm)
### Download the Helm chart
```bash
helm repo add projectcalico https://docs.tigera.io/calico/charts
```
### Customize the Helm chart
```bash
echo '{ installation: {kubernetesProvider: EKS }}' > values.yaml
```
### Install Calico
```bash
kubectl create namespace tigera-operator
helm install calico projectcalico/tigera-operator --version v3.31.4 -f values.yaml --namespace tigera-operator
```
### Verify
```bash
watch kubectl get pods -n calico-system
```
### Expected Output
```bash
Every 2.0s: kubectl get pods -n calico-system                                                    ip-10-0-4-169.ap-northeast-2.compute.internal: Mon Mar  2 12:40:37 2026

NAME                                       READY   STATUS    RESTARTS   AGE
calico-apiserver-7689df8d6f-jlpng          1/1     Running   0          48m
calico-apiserver-7689df8d6f-ljfxp          1/1     Running   0          48m
calico-kube-controllers-748b7c7dd9-8v4qm   1/1     Running   0          48m
calico-node-fdc7q                          1/1     Running   0          48m
calico-node-vq5ss                          1/1     Running   0          48m
calico-typha-d459b4c85-8twzz               1/1     Running   0          48m
goldmane-58f96f7c58-h8bxn                  1/1     Running   0          48m
whisker-84b9469dc4-mqr9b                   2/2     Running   0          47m
```