# External Secrets Operator
## Setup
### Install from chart repository
```bash
helm repo add external-secrets https://charts.external-secrets.io

helm install external-secrets \
   external-secrets/external-secrets \
    -n external-secrets \
    --create-namespace \
    --set installCRDs=true
```
### OIDC
```bash
CLUSTER=
OIDC_URL=$(aws eks describe-cluster --name $CLUSTER --query "cluster.identity.oidc.issuer" --output text)

OIDC_ID=$(echo $OIDC_URL | sed 's|https://oidc.eks.ap-northeast-2.amazonaws.com/id/||')
echo "OIDC ID: $OIDC_ID"

aws iam create-open-id-connect-provider \
  --url $OIDC_URL \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 9e99a48a9960b14926bb7f3b02e22da2b0ab7280
```
### IRSA
#### [Trusted Policy](https://github.com/WhAnci/Sekketsu-Sojutsu/blob/main/Kakurin%20Yakudo/Kubernetes/IRSA/get-trusted-policy.sh)
#### Service Account
```bash
SA_NAME=
SA_NS=
kubectl patch sa $SA_NAME -n $SA_NS \
  -p '{"metadata":{"annotations":{"eks.amazonaws.com/role-arn":"arn:aws:iam::586639730662:role/gjmstSecretsRole"}}}'
```
