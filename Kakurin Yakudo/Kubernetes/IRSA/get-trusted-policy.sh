#!/bin/bash
ACCOUNT_ID=586639730662
CLUSTER_NAME=demo
REGION=ap-northeast-2

SA_NS=external-secrets
SA_NAME=external-secrets

ISSUER=$(aws eks describe-cluster --name "$CLUSTER_NAME" --region "$REGION" \
  --query "cluster.identity.oidc.issuer" --output text)

ISSUER_HOSTPATH=${ISSUER#https://}

cat > trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::${ACCOUNT_ID}:oidc-provider/${ISSUER_HOSTPATH}"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "${ISSUER_HOSTPATH}:aud": "sts.amazonaws.com",
          "${ISSUER_HOSTPATH}:sub": "system:serviceaccount:${SA_NS}:${SA_NAME}"
        }
      }
    }
  ]
}
EOF
