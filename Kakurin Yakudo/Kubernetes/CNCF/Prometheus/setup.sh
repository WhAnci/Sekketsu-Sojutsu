#!/bin/bash

kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
parameters:
  type: gp3
  fsType: ext4
provisioner: ebs.csi.aws.com
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
EOF

kubectl create ns prometheus --dry-run=client -o yaml | kubectl apply -f -
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade -i prometheus prometheus-community/prometheus \
    --namespace prometheus

DEFAULT_PORT="190190"
echo ""
while true; do
    read -p "▶ Enter Port Number for Port-Forwarding [$DEFAULT_PORT]: " CUSTOM_PORT
    CUSTOM_PORT=${CUSTOM_PORT:-$DEFAULT_PORT}
            8[]
    if lsof -Pi :$CUSTOM_PORT -sTCP:LISTEN -t >/dev/null ; then
        echo "!! Error: Port $CUSTOM_PORT is already in use by another process."
        echo "   Please enter a different port number."
    else
        break
    fi
done

echo "◈ Waiting for Prometheus server pod to be ready..."

kubectl wait --namespace prometheus \
    --for=condition=ready pod \
    -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=prometheus" \
    --timeout=300s

export POD_NAME=$(kubectl get pods --namespace prometheus -l "app.kubernetes.io/name=prometheus,app.kubernetes.io/instance=prometheus" -o jsonpath="{.items[0].metadata.name}")

PRIVATE_IP=$(hostname -I | awk '{print $1}')
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)

echo "-------------------------------------------------------"
echo "                      (～￣▽￣)～"
echo "◈ Prometheus Server is running!"
echo "   - Local Access:      http://localhost:${CUSTOM_PORT}"
echo "   - Private Network:   http://${PRIVATE_IP}:${CUSTOM_PORT}"
echo "   - Public Access:     http://${PUBLIC_IP}:${CUSTOM_PORT}"
echo "-------------------------------------------------------"
echo "◈ Note: Ensure Security Group allows Inbound TCP:${CUSTOM_PORT}"
echo "◈ Internal DNS: http://prometheus-server.prometheus.svc.cluster.local:80"
echo "-------------------------------------------------------"

kubectl --namespace prometheus port-forward $POD_NAME ${CUSTOM_PORT}:9090 --address 0.0.0.0 > /dev/null 2>&1 &

echo "[✔] Port-forwarding started on port ${CUSTOM_PORT} in the background."
