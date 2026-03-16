#!/bin/bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

kubectl create ns grafana
helm install grafana grafana/grafana -n grafana

export POD_NAME=$(kubectl get pods --namespace grafana -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")

PRIVATE_IP=$(hostname -I | awk '{print $1}')
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)

echo "-------------------------------------------------------"
echo "                       (～￣▽￣)～"
echo "Grafanna Dashboard is running!"
echo "Local Access:      http://localhost:13000"
echo "Private Network:   http://${PRIVATE_IP}:13000"
echo "Public Access:     http://${PUBLIC_IP}:13000"
echo "Target Pod:        $POD_NAME"
echo "-------------------------------------------------------"

kubectl --namespace grafana port-forward $POD_NAME 13000:3000 --address 0.0.0.0 > /dev/null 2>&1 &

echo "  ✅ Port-forwarding is running in the background."
