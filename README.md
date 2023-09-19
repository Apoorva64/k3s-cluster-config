<div style="text-align: center;
   align-content: center;
   align-items: center;">
    <h1><b>Flux Config</b></h1>
    <img src='readme-assets/flux-logo.png' width='250'  alt="flux-logo"/>
    <p> GitOps for Kubernetes </p>
</div>

## Getting started

### What is GitOps?

GitOps is an operational framework that takes DevOps best practices used for application development such as version
control, collaboration, compliance, and CI/CD, and applies them to infrastructure automation.GitOps is an operational
framework that takes DevOps best practices used for application development such as version control, collaboration,
compliance, and CI/CD, and applies them to infrastructure automation.

### What is Flux?

Flux CD is a Continuous Delivery tool to help keep Kubernetes clusters in sync with configuration sources such as Git
repositories and automate configuration updates when available

### Repositories Structure

#### Infrastructure Repository (This repository)

This repository contains the configuration for the flux cluster. It contains the configuration for the infrastructure
components and links to the repositories for the applications deployed in the cluster.

#### Application Repositories

The application repositories contain the configuration for the applications deployed in the cluster.
Each application repository contains a manifests folder which contains the yaml configuration resources for the
application.

#### Linking Application Repositories

The application repositories are linked to the infrastructure repository by adding a folder in
the [apps/base folder](./apps/base)
containing the following files:

- kustomization.yaml - This file contains the configuration for aggregating the
  manifests
- repository.yaml - This file contains the configuration for the repository containing the application configuration.(
  This is used by flux to sync the cluster state with the git repository)
- kustomize.yaml - This file contains the configuration to deploy the application manifests in the cluster using
  kustomize(kustomization.yaml).

Those files can then be `kuztomize`d in the [dev overlay](./apps/dev) or [prod overlay](./apps/prod).
This setup can be used to create different environments for the application.

For example, you can create a dev
environment and a prod environment for the application. The dev environment can be used for testing and the prod
environment can be used for production.
The dev will for example be at [https://dev.example.com](https://dev.example.com) and the prod will be at
[https://example.com](https://example.com).

### How does it work?

The flux operator is installed in the cluster. The flux operator monitors the git repository for changes. When a change
is detected, the flux operator updates the cluster state to match the git repository.
Using this setup, you can use git as a single source of truth for the cluster state.

### Prerequisites

1. Get a Kubernetes cluster
   You can use any Kubernetes cluster you have access to. If you don't have one, you can create a cluster locally
   using [kind](https://kind.sigs.k8s.io/).
2. Install flux cli
   see [flux cli](https://fluxcd.io/flux/installation/) for installation instructions.
3. Bootstrap flux
   see [flux bootstrap](https://fluxcd.io/docs/get-started/#bootstrapping-flux) for instructions.
   Bootstrapping flux will install flux in your cluster and sync the cluster state with the git repository.

   Before you bootstrap flux, you need to create PAT(Personal Access Token), which will be used by flux to access the
   git
   repository.
   You can create a PAT by following the
   instructions [here](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#creating-a-personal-access-token).

   Then, you need to export the PAT as an environment variable.

    ```shell
    export GITLAB_TOKEN=<your-gitlab-token>
    export GITLAB_USER=<your-gitlab-username> #devops573026/flux-gitops
    ```
   You also need to set the KUBECONFIG environment variable to point to the kubeconfig file for the cluster.

    ```shell
    export KUBECONFIG=<path-to-kubeconfig-file>
    ```

And then bootstrap flux using the following command.

    ```shell
    flux bootstrap gitlab \
      --owner=$GITLAB_USER \
      --repository=flux-config \  
      --branch=main \
      --path=clusters/arm-cluster \
      --deploy-token-auth \
      --components-extra=image-reflector-controller,image-automation-controller 

    ```

## Infrastructure

### [Cert Manager](./infrastructure/controllers/cert-manager.yaml)

Cert manager is used to manage certificates in the cluster. It is deployed in the cert-manager namespace.
It is deployed using the helm chart [cert-manager](https://cert-manager.io/docs/installation/helm/).

#### [Cluster Issuers](./infrastructure/configs)

There are two cluster issuers deployed in the cluster. One for the staging environment and one for the production.
The staging issuer is used to issue certificates for the staging environment and the production issuer is used to issue
certificates for the production environment.

### [Sealed Secrets](./infrastructure/controllers/sealed-secrets.yaml)

The sealed secrets controller is used to manage secrets in the cluster. It is deployed in the sealed-secrets namespace.
It is deployed using the helm chart [sealed-secrets](https://bitnami-labs.github.io/sealed-secrets)

### [Auth](./infrastructure/auth)

The auth folder contains the configuration for the auth provider. The auth provider used is keycloak. The auth provider
is deployed in the auth namespace. It is deployed using the helm
chart [keycloak](https://github.com/codecentric/helm-charts/tree/master/charts/keycloakx).

### [Monitoring](./infrastructure/monitoring)

1. [Prometheus+Grafana](./infrastructure/monitoring/kube-prometheus-stack)
   The kube prometheus stack is used for monitoring metrics in the cluster. It is deployed in the monitoring namespace.
   It is
   deployed
   using the helm chart [kube-prometheus-stack](https://prometheus-community.github.io/helm-charts).

2. [Loki](./infrastructure/monitoring/loki)
   Loki is used for log aggregation. Loki is deployed in the monitoring
   namespace.
   It is deployed using the helm chart [loki-stack](https://grafana.github.io/loki/charts).
3. [Promtail](./infrastructure/monitoring/promtail)
   Promtail is used to scrape logs from the cluster and send them to Loki. Promtail is deployed in the monitoring
   namespace.
   It is deployed using the helm chart [promtail](https://grafana.github.io/loki/charts).

### [Storage](./infrastructure/storage)

Minio is used for object storage. It is deployed in the storage namespace. It is deployed using the helm chart
[minio](./infrastructure/storage/minio.yaml).

### [Sealed Secrets](./infrastructure/controllers/sealed-secrets.yaml)

Sealed secrets is used to manage secrets in the cluster.
It is used to encrypt the secrets and store them in the git repository.
They are then decrypted and stored in the cluster as secrets.
You need to set the environment variable SEALED_SECRETS_CONTROLLER_NAMESPACE to the namespace where the sealed secrets
controller is deployed.
You also need to set the environment variable KUBECONFIG to point to the kubeconfig file for the cluster.

```shell
export SEALED_SECRETS_CONTROLLER_NAMESPACE=flux-system
```

#### Encryption workflow

- Create a secret and then export it to a yaml file.
  ```shell
   kubectl create secret generic <secret_name> --from-literal=<key>=<value> --dry-run=client -o yaml > <secret_name>.yaml
  ```

- Encrypt the secret using kubeseal don't forget to load the environment variables (SEALED_SECRETS_CONTROLLER_NAMESPACE,
  KUBECONFIG).

  ```shell
  kubeseal --format=yaml < <secret_name>.yaml > <secret_name>-sealed.yaml
  ```

- add an example of the secret.
- Commit the sealed secret to the git repository.
