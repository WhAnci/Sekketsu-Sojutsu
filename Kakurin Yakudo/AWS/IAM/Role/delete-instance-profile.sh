#!/bin/bash
=========================================================================================================
ROLE_NAME=KarpenterNodeRole-cluster
=========================================================================================================
aws iam remove-role-from-instance-profile \
--instance-profile-name $(aws iam list-instance-profiles-for-role --role-name $ROLE_NAME --query 'InstanceProfiles[].InstanceProfileName' \
--output json | jq -r '.[]') \
--role-name $ROLE_NAME
