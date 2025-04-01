# Install Flux

```
curl -s https://fluxcd.io/install.sh | sudo bash

```

# Initialize Flux in EKS Cluster

```
flux bootstrap github \
  --owner=AlvaradoA \
  --repository=Employee-Application \
  --branch=main \
  --path=./app \
  --personal
```

# Create Kustomization resource

Tell Flux to check repo every 1 minute. Apply changes found in ./app

```
kubectl apply -f flux.yaml
```

