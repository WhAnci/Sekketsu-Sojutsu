#!/bin/bash

echo "apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: default
spec:
  amiFamily: Bottlerocket
  role: "KarpenterNodeRole-cluster"
  amiSelectorTerms:
    - alias: bottlerocket@latest
  subnetSelectorTerms:
    - id: $(aws ec2 describe-subnets --filters "Name=availability-zone,Values=ap-northeast-2a" --query 'Subnets[0].SubnetId' --output text)
    - id: $(aws ec2 describe-subnets --filters "Name=availability-zone,Values=ap-northeast-2b" --query 'Subnets[0].SubnetId' --output text)
    - id: $(aws ec2 describe-subnets --filters "Name=availability-zone,Values=ap-northeast-2c" --query 'Subnets[0].SubnetId' --output text)
  securityGroupSelectorTerms:
    - id: $(aws ec2 describe-security-groups --filters "Name=tag:aws:eks:cluster-name,Values=$CLUSTER_NAME" --query 'SecurityGroups[0].GroupId' --output text)
    " | kubectl apply -f -

echo "apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: default
spec:
  template:
    spec:
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
      requirements:
      - key: node.kubernetes.io/instance-type
        operator: In
        values: ["t3.medium"]
        " | kubectl apply -f -