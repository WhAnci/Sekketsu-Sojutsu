#!/bin/bash

trap 'echo ""; exit 1' INT

echo "======================================================"
echo "      ◆ External Secrets Setup (Pod Identity)"
echo "======================================================"

# 1. 입력 받기 (Cluster Name & Namespace)
while true; do
    read -p "▶ CLUSTER_NAME: " CLUSTER_NAME
    if [[ -n "$CLUSTER_NAME" ]]; then break; fi
    echo "[!] Error: CLUSTER_NAME is required."
done

read -p "▶ TARGET_NAMESPACE (default: external-secrets): " TARGET_NS
TARGET_NS=${TARGET_NS:-"external-secrets"}

read -p "▶ SERVICE_ACCOUNT_NAME (default: external-secrets): " SA_NAME
SA_NAME=${SA_NAME:-"external-secrets"}

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=$(aws configure get region)
REGION=${REGION:-"ap-northeast-2"}
ROLE_NAME="ESO-Pod-Identity-Role-${CLUSTER_NAME}"

# 2. IAM Role 생성
echo "◈ Creating IAM Role for Pod Identity..."
cat <<EOF > trust-policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": { "Service": "pods.eks.amazonaws.com" },
            "Action": ["sts:AssumeRole", "sts:TagSession"]
        }
    ]
}
EOF

aws iam create-role --role-name $ROLE_NAME --assume-role-policy-document file://trust-policy.json > /dev/null 2>&1
aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite

# 3. 네임스페이스 및 ServiceAccount 준비
echo "◈ Preparing Namespace and ServiceAccount..."
kubectl create namespace $TARGET_NS --dry-run=client -o yaml | kubectl apply -f -

# 해당 네임스페이스에 SA가 없으면 생성
if ! kubectl get sa $SA_NAME -n $TARGET_NS > /dev/null 2>&1; then
    kubectl create serviceaccount $SA_NAME -n $TARGET_NS
    echo "[+] Created ServiceAccount: $SA_NAME in $TARGET_NS"
fi

# 4. Pod Identity Association 설정
echo "◈ Associating Pod Identity with EKS Cluster..."
aws eks create-pod-identity-association \
    --cluster-name $CLUSTER_NAME \
    --role-arn arn:aws:iam::${AWS_ACCOUNT_ID}:role/$ROLE_NAME \
    --namespace $TARGET_NS \
    --service-account $SA_NAME

# 5. Helm 설치 (이미 설치된 경우 업그레이드)
echo "◈ Installing External Secrets Operator via Helm..."
helm repo add external-secrets https://charts.external-secrets.io > /dev/null 2>&1
helm repo update

# 주의: Operator 자체는 external-secrets 네임스페이스에 설치하는 것이 일반적입니다.
# 하지만 사용자가 지정한 SA를 사용하게 하려면 설정을 맞춰야 합니다.
helm upgrade -i external-secrets external-secrets/external-secrets \
    --namespace external-secrets \
    --create-namespace \
    --set installCRDs=true

echo "◈ Waiting for pods..."
kubectl wait --namespace external-secrets \
    --for=condition=ready pod \
    -l "app.kubernetes.io/instance=external-secrets" \
    --timeout=300s

echo "-------------------------------------------------------"
echo "               (～￣▽￣)～"
echo "◈ Setup Complete!"
echo "   - IAM Role: $ROLE_NAME"
echo "   - Target Namespace: $TARGET_NS"
echo "   - ServiceAccount: $SA_NAME"
echo "-------------------------------------------------------"