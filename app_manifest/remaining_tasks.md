# Remaining tasks
1. Create Dockerfile, docker image and test the application locally in your Cloud9 environment.
- Rony will do it

2. Store your application in GitHub and create a GitHub Action that builds and tests your application. Upon successful unit test, GitHub Action publishes your image to Amazon ECR.
- Rony will do it

3 - · Create serviceaccount named “clo835” with IRSA (IAM Roles for Serviceaccounts) permissions to 
access your S3 private bucket storing the background image
- I'm stuck because setup requires OpenID Connect (OIDC) provider which we do not have
Source: https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html

4 - Bonus: add deployment automation with Flux.

- I'm working on it


