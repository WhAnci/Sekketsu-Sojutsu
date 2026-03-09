CLUSTER=cluster
ACCOUNT_ID=586639730662
aws eks create-access-entry --cluster-name $CLUSTER --principal-arn arn:aws:iam::$ACCOUND_ID:role/KarpenterNodeRole-$CLUSTER --type EC2_LINUX
aws iam create-role \
  --role-name KarpenterControllerRole-$CLUSTER \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "pods.eks.amazonaws.com"
        },
        "Action": [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
      }
    ]
  }'
for POLICY in \
KarpenterControllerEKSIntegrationPolicy-cluster \
KarpenterControllerIAMIntegrationPolicy-cluster \
KarpenterControllerInterruptionPolicy-cluster \
KarpenterControllerNodeLifecyclePolicy-cluster \
KarpenterControllerResourceDiscoveryPolicy-cluster
do
  aws iam attach-role-policy \
    --role-name KarpenterControllerRole-$CLUSTER \
    --policy-arn arn:aws:iam::$ACCOUND_ID:policy/$POLICY
done
aws eks create-pod-identity-association \
  --cluster-name $CLUSTER \
  --namespace kube-system \
  --service-account karpenter \
  --role-arn arn:aws:iam::$ACCOUNT_ID:role/KarpenterControllerRole-$CLUSTER
