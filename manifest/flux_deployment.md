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
## Create Kustomization resource

Tell Flux to check repo every 1 minute. Apply changes found in ./app

```
kubectl apply -f flux.yaml
```

## Automate image updates to Git

### Install Flux with the image automation components:

```
flux bootstrap github \
  --components-extra=image-reflector-controller,image-automation-controller \
  --owner=AlvaradoA \
  --repository=Employee-Application \
  --branch=main \
  --path=./manifest/apps \
  --read-write-key \
  --personal
```

### Create an ImageRepository to tell Flux which container registry to scan for new tags:

```
kubectl apply -f ImageRepo.yaml
```

### Create an ImagePolicy to tell Flux which semver range to use when filtering tags:

image format shoule be image:1.x

```
kubectl apply -f ImagePolicy.yaml
```

### Create an ImageUpdateAutomation to tell Flux which Git repository to write image updates to:

```
kubectl apply -f ImageUpdate.yaml
```

### Wait for Flux to apply the latest commit on the cluster and verify that podinfo was updated

```
watch "kubectl get deployment/myapp -oyaml | grep 'image:'"
```
