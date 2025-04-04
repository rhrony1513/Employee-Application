# Deploy EKS Cluster

```
eksctl create cluster -f eks_config.yaml
```

# Create EKS namespace

```
kubectl create ns final
```

# Create secret to authenticate ECR

```
kubectl create secret docker-registry ecr-secret \
  --docker-server=[awsid].dkr.ecr.[region].amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region [region]) \
  --namespace final
```
# Deploy storageClass & pvc
## Provision EBS

```
aws ec2 create-volume --volume-type gp2 --size 20 --availability-zone us-east-1a
```

## Install container storage interface (CSI) driver

```
eksctl create addon --name aws-ebs-csi-driver --cluster [name] --service-account-role-arn arn:aws:iam::[awsid]:role/LabRole –force
```
## Provision pvc

```
kubectl apply -f app_pvc.yaml
```

#  Deploy configmap, secrets, services

```
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml
kubectl apply -f services.yaml
```

# Deploy app

```
kubectl apply -f db.yaml
kubectl apply -f app.yaml
```
# HPA, autoscaling
## Deploy Metric Server for HPA

```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.7.2/components.yaml

```

## Deploy HPA

K8s will add more pod to myapp deployment when pod's cpu utilization surpass 50%. Max number of pod added is 10 

```
kubectl autoscale deployment myapp --cpu-percent=50 --min=1 --max=10 -n final
```

## Generate load

```
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://[lb]:81; done"
```

## Monitor HPA

```
kubectl get hpa myapp -n final --watch 
kubectl get pod -n final --watch 
```

# Create ClusterRole & ClusterRolebinding

```
kubectl apply -f service_account_role_role_binding.yaml
```

## Test service account to create namespace

```
kubectl auth can-i create namespaces --as=system:serviceaccount:final:clo835
kubectl auth can-i get namespaces --as=system:serviceaccount:final:clo835
```
