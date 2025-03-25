# Deploy AKS Cluster

```
kubectl apply -f eks_config.yaml
```
# Create secret to authenticate ECR

```
kubectl create secret docker-registry ecr-secret \
  --docker-server=[awsid].dkr.ecr.[region].amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region [region]) \
  --namespace final
```

# Provision EBS

```
aws ec2 create-volume --volume-type gp2 --size 20 --availability-zone us-east-1a
```

# Install container storage interface (CSI) driver

```
eksctl create addon --name aws-ebs-csi-driver --cluster [name] --service-account-role-arn arn:aws:iam::[awsid]:role/LabRole –force
```