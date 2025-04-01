# Install Flux

```
curl -s https://fluxcd.io/install.sh | sudo bash

```

# Create var for Github PAT

Flux bootstrap uses PAT to authenticate Github repo, then push Flux manifests to the GitHub repository and configures Flux to update itself from Git 
```
export GITHUB_TOKEN=<your-github-pat>
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

