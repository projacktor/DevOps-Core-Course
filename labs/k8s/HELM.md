# Lab 10 - Helm Package Manager

## 1. Chart Overview

Implemented chart path:
- labs/k8s/python-info-service

Chart structure:
- Chart.yaml: chart metadata, versioning, maintainers
- values.yaml: default configuration for all environments
- values-dev.yaml: development overrides
- values-prod.yaml: production overrides
- templates/_helpers.tpl: reusable naming and label helpers
- templates/deployment.yaml: templated Deployment
- templates/service.yaml: templated Service
- templates/hooks/pre-install-job.yaml: pre-install hook Job
- templates/hooks/post-install-job.yaml: post-install hook Job
- templates/NOTES.txt: post-install usage hints

Template strategy:
- Reused labels and names via helper templates to avoid duplication.
- Kept health checks enabled and configurable through values.
- Preserved rollout strategy and resource controls from Lab 9 manifests.

## 2. Configuration Guide

Important values in values.yaml:
- replicaCount: number of pods
- image.repository, image.tag, image.pullPolicy
- service.type, service.port, service.targetPort, service.nodePort
- resources.requests, resources.limits
- strategy.type, strategy.rollingUpdate.*
- livenessProbe.* and readinessProbe.*
- hooks.enabled, hooks.image.*, hooks.preInstall.*, hooks.postInstall.*

Environment files:
- values-dev.yaml:
  - replicaCount: 1
  - lower CPU and memory requests/limits
  - NodePort service
  - image tag latest
- values-prod.yaml:
  - replicaCount: 5
  - stronger CPU and memory requests/limits
  - LoadBalancer service
  - pinned image tag 1.0.0

Example installs:

```bash
helm install python-dev labs/k8s/python-info-service -f labs/k8s/python-info-service/values-dev.yaml
helm install python-prod labs/k8s/python-info-service -f labs/k8s/python-info-service/values-prod.yaml
```

```sh
helm version
version.BuildInfo{Version:"v4.0.0", GitCommit:"99cd1964357c793351be481d55abbe21c6b2f4ec", GitTreeState:"clean", GoVersion:"go1.25.3", KubeClientVersion:"v1.34"}
```

Upgrade dev release to prod profile:

```bash
helm upgrade python-dev labs/k8s/python-info-service -f labs/k8s/python-info-service/values-prod.yaml
```

## 3. Hook Implementation

Implemented hooks:
- Pre-install hook Job:
  - file: templates/hooks/pre-install-job.yaml
  - annotation helm.sh/hook: pre-install
  - default weight: -5
  - purpose: run validation-style task before resource install
- Post-install hook Job:
  - file: templates/hooks/post-install-job.yaml
  - annotation helm.sh/hook: post-install
  - default weight: 5
  - purpose: run smoke-check style task after install

Deletion policy:
- Both hooks use:
  - helm.sh/hook-delete-policy: hook-succeeded
- Additionally set:
  - ttlSecondsAfterFinished: 30

Execution order:
- Hook weight controls order.
- Pre-install weight -5 runs before default-weight hooks.
- Post-install weight 5 runs after lower-weight post-install hooks.

## 4. Installation Evidence

Current local tool status:

```bash
# Local install (without sudo)
mkdir -p $HOME/.local/bin
cd /tmp
curl -fsSL -o helm.tar.gz https://get.helm.sh/helm-v4.0.0-linux-amd64.tar.gz
tar -xzf helm.tar.gz
cp linux-amd64/helm helm
chmod +x helm

helm version
# version.BuildInfo{Version:"v4.0.0", ...}
```

Validation results collected for this chart:

```bash
helm lint labs/k8s/python-info-service
==> Linting labs/k8s/python-info-service
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed

helm install --dry-run --debug test-release labs/k8s/python-info-service -f labs/k8s/python-info-service/values-dev.yaml
level=WARN msg="--dry-run is deprecated and should be replaced with '--dry-run=client'"
level=DEBUG msg="Original chart version" version=""
level=DEBUG msg="Chart path" path=/home/projacktor/Projects/edu/DevOps-Core-Course/labs/k8s/python-info-service
level=DEBUG msg="number of dependencies in the chart" dependencies=0
NAME: test-release
LAST DEPLOYED: Thu Apr  2 23:11:45 2026
NAMESPACE: default
STATUS: pending-install
REVISION: 1
DESCRIPTION: Dry run complete
TEST SUITE: None
USER-SUPPLIED VALUES:
image:
  tag: latest
livenessProbe:
  initialDelaySeconds: 5
  periodSeconds: 10
readinessProbe:
  initialDelaySeconds: 3
  periodSeconds: 5
replicaCount: 1
resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 50m
    memory: 64Mi
service:
  nodePort: 30080
  type: NodePort

COMPUTED VALUES:
fullnameOverride: ""
hooks:
  enabled: true
  image:
    pullPolicy: IfNotPresent
    repository: busybox
    tag: "1.36"
  postInstall:
    command:
    - sh
    - -c
    - echo Post-install smoke test started && sleep 5 && echo Post-install smoke test
      finished
    enabled: true
    weight: "5"
  preInstall:
    command:
    - sh
    - -c
    - echo Pre-install validation started && sleep 5 && echo Pre-install validation
      finished
    enabled: true
    weight: "-5"
image:
  pullPolicy: IfNotPresent
  repository: projacktor/python-info-service
  tag: latest
livenessProbe:
  failureThreshold: 3
  initialDelaySeconds: 5
  periodSeconds: 10
  tcpSocket:
    port: 8080
  timeoutSeconds: 2
nameOverride: ""
readinessProbe:
  failureThreshold: 3
  initialDelaySeconds: 3
  periodSeconds: 5
  tcpSocket:
    port: 8080
  timeoutSeconds: 2
replicaCount: 1
resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 50m
    memory: 64Mi
service:
  nodePort: 30080
  port: 8080
  targetPort: 8080
  type: NodePort
strategy:
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
  type: RollingUpdate

HOOKS:
---
# Source: python-info-service/templates/hooks/post-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: test-release-python-info-service-post-install
  labels:
    helm.sh/chart: python-info-service-0.1.0
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": post-install
    "helm.sh/hook-weight": "5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  ttlSecondsAfterFinished: 30
  template:
    metadata:
      labels:
        app.kubernetes.io/name: python-info-service
        app.kubernetes.io/instance: test-release
        app: python-info-service
    spec:
      restartPolicy: Never
      containers:
        - name: post-install-job
          image: "busybox:1.36"
          imagePullPolicy: IfNotPresent
          command:
            - sh
            - -c
            - echo Post-install smoke test started && sleep 5 && echo Post-install smoke test
              finished
---
# Source: python-info-service/templates/hooks/pre-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: test-release-python-info-service-pre-install
  labels:
    helm.sh/chart: python-info-service-0.1.0
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  ttlSecondsAfterFinished: 30
  template:
    metadata:
      labels:
        app.kubernetes.io/name: python-info-service
        app.kubernetes.io/instance: test-release
        app: python-info-service
    spec:
      restartPolicy: Never
      containers:
        - name: pre-install-job
          image: "busybox:1.36"
          imagePullPolicy: IfNotPresent
          command:
            - sh
            - -c
            - echo Pre-install validation started && sleep 5 && echo Pre-install validation finished
MANIFEST:
---
# Source: python-info-service/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: test-release-python-info-service
  labels:
    helm.sh/chart: python-info-service-0.1.0
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 8080
      nodePort: 30080
---
# Source: python-info-service/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-release-python-info-service
  labels:
    helm.sh/chart: python-info-service-0.1.0
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 1
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: python-info-service
      app.kubernetes.io/instance: test-release
      app: python-info-service
  template:
    metadata:
      labels:
        app.kubernetes.io/name: python-info-service
        app.kubernetes.io/instance: test-release
        app: python-info-service
    spec:
      containers:
        - name: python-info-service
          image: "projacktor/python-info-service:latest"
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          resources:
            limits:
              cpu: 100m
              memory: 128Mi
            requests:
              cpu: 50m
              memory: 64Mi
          livenessProbe:
            failureThreshold: 3
            initialDelaySeconds: 5
            periodSeconds: 10
            tcpSocket:
              port: 8080
            timeoutSeconds: 2
          readinessProbe:
            failureThreshold: 3
            initialDelaySeconds: 3
            periodSeconds: 5
            tcpSocket:
              port: 8080
            timeoutSeconds: 2

NOTES:
1. Get the application URL:
  export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services test-release-python-info-service)
  export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
```

Production override rendering check:

```bash
helm template prod-release labs/k8s/python-info-service -f labs/k8s/python-info-service/values-prod.yaml | grep -nE "replicas:|type: LoadBalancer|nodePort:|image:"

15:  type: LoadBalancer
39:  replicas: 5
59:          image: "projacktor/python-info-service:1.0.0"
115:          image: "busybox:1.36"
151:          image: "busybox:1.36"
```

Commands to collect cluster evidence:

```bash
# Chart validation and render
helm lint labs/k8s/python-info-service
helm template test-release labs/k8s/python-info-service
helm install --dry-run --debug test-release labs/k8s/python-info-service

# Dev deployment
helm install python-dev labs/k8s/python-info-service -f labs/k8s/python-info-service/values-dev.yaml
helm list
kubectl get all
kubectl get jobs
kubectl describe job python-dev-python-info-service-pre-install
kubectl describe job python-dev-python-info-service-post-install

# Prod-style upgrade
helm upgrade python-dev labs/k8s/python-info-service -f labs/k8s/python-info-service/values-prod.yaml
kubectl get deployment,svc,pods
```

Expected evidence to capture:
- helm list output with release status
- kubectl get all showing deployment, rs, pods, service
- kubectl get jobs and job describe/logs for hook execution
- deployment/service differences before and after prod upgrade

## 5. Operations

Install:

```bash
helm install python-dev labs/k8s/python-info-service -f labs/k8s/python-info-service/values-dev.yaml

NAME: python-dev
LAST DEPLOYED: Thu Apr  2 23:22:45 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None
NOTES:
1. Get the application URL:
  export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services python-dev-python-info-service)
  export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
```

Upgrade:

```bash
helm upgrade python-dev labs/k8s/python-info-service -f labs/k8s/python-info-service/values-prod.yaml
Release "python-dev" has been upgraded. Happy Helming!
NAME: python-dev
LAST DEPLOYED: Thu Apr  2 23:23:25 2026
NAMESPACE: default
STATUS: deployed
REVISION: 2
DESCRIPTION: Upgrade complete
TEST SUITE: None
NOTES:
1. Get the application URL:
  NOTE: It may take a few minutes for the LoadBalancer external IP to become available.
  kubectl get svc --namespace default python-dev-python-info-service -w
```

Rollback:

```bash
helm history python-dev

REVISION        UPDATED                         STATUS          CHART                           APP VERSION     DESCRIPTION     
1               Thu Apr  2 23:22:45 2026        superseded      python-info-service-0.1.0       1.0.0           Install complete
2               Thu Apr  2 23:23:25 2026        deployed        python-info-service-0.1.0       1.0.0           Upgrade complete


helm rollback python-dev 1

Rollback was a success! Happy Helming!
```

Uninstall:

```bash
helm uninstall python-dev
release "python-dev" uninstalled
```

## 6. Testing and Validation

Validation sequence:

```bash
helm lint labs/k8s/python-info-service
==> Linting labs/k8s/python-info-service
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed


helm template test-release labs/k8s/python-info-service


---
# Source: python-info-service/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: test-release-python-info-service
  labels:
    helm.sh/chart: python-info-service-0.1.0
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 8080
      nodePort: 30080
---
# Source: python-info-service/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-release-python-info-service
  labels:
    helm.sh/chart: python-info-service-0.1.0
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: python-info-service
      app.kubernetes.io/instance: test-release
      app: python-info-service
  template:
    metadata:
      labels:
        app.kubernetes.io/name: python-info-service
        app.kubernetes.io/instance: test-release
        app: python-info-service
    spec:
      containers:
        - name: python-info-service
          image: "projacktor/python-info-service:latest"
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          resources:
            limits:
              cpu: 200m
              memory: 256Mi
            requests:
              cpu: 100m
              memory: 128Mi
          livenessProbe:
            failureThreshold: 3
            initialDelaySeconds: 15
            periodSeconds: 10
            tcpSocket:
              port: 8080
            timeoutSeconds: 2
          readinessProbe:
            failureThreshold: 3
            initialDelaySeconds: 5
            periodSeconds: 5
            tcpSocket:
              port: 8080
            timeoutSeconds: 2
---
# Source: python-info-service/templates/hooks/post-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: test-release-python-info-service-post-install
  labels:
    helm.sh/chart: python-info-service-0.1.0
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": post-install
    "helm.sh/hook-weight": "5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  ttlSecondsAfterFinished: 30
  template:
    metadata:
      labels:
        app.kubernetes.io/name: python-info-service
        app.kubernetes.io/instance: test-release
        app: python-info-service
    spec:
      restartPolicy: Never
      containers:
        - name: post-install-job
          image: "busybox:1.36"
          imagePullPolicy: IfNotPresent
          command:
            - sh
            - -c
            - echo Post-install smoke test started && sleep 5 && echo Post-install smoke test
              finished
---
# Source: python-info-service/templates/hooks/pre-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: test-release-python-info-service-pre-install
  labels:
    helm.sh/chart: python-info-service-0.1.0
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  ttlSecondsAfterFinished: 30
  template:
    metadata:
      labels:
        app.kubernetes.io/name: python-info-service
        app.kubernetes.io/instance: test-release
        app: python-info-service
    spec:
      restartPolicy: Never
      containers:
        - name: pre-install-job
          image: "busybox:1.36"
          imagePullPolicy: IfNotPresent
          command:
            - sh
            - -c


helm install --dry-run --debug test-release labs/k8s/python-info-service

level=WARN msg="--dry-run is deprecated and should be replaced with '--dry-run=client'"
level=DEBUG msg="Original chart version" version=""
level=DEBUG msg="Chart path" path=/home/projacktor/Projects/edu/DevOps-Core-Course/labs/k8s/python-info-service
level=DEBUG msg="number of dependencies in the chart" dependencies=0
NAME: test-release
LAST DEPLOYED: Thu Apr  2 23:24:58 2026
NAMESPACE: default
STATUS: pending-install
REVISION: 1
DESCRIPTION: Dry run complete
TEST SUITE: None
USER-SUPPLIED VALUES:
{}

COMPUTED VALUES:
fullnameOverride: ""
hooks:
  enabled: true
  image:
    pullPolicy: IfNotPresent
    repository: busybox
    tag: "1.36"
  postInstall:
    command:
    - sh
    - -c
    - echo Post-install smoke test started && sleep 5 && echo Post-install smoke test
      finished
    enabled: true
    weight: "5"
  preInstall:
    command:
    - sh
    - -c
    - echo Pre-install validation started && sleep 5 && echo Pre-install validation
      finished
    enabled: true
    weight: "-5"
image:
  pullPolicy: IfNotPresent
  repository: projacktor/python-info-service
  tag: latest
livenessProbe:
  failureThreshold: 3
  initialDelaySeconds: 15
  periodSeconds: 10
  tcpSocket:
    port: 8080
  timeoutSeconds: 2
nameOverride: ""
readinessProbe:
  failureThreshold: 3
  initialDelaySeconds: 5
  periodSeconds: 5
  tcpSocket:
    port: 8080
  timeoutSeconds: 2
replicaCount: 3
resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi
service:
  nodePort: 30080
  port: 8080
  targetPort: 8080
  type: NodePort
strategy:
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
  type: RollingUpdate

HOOKS:
---
# Source: python-info-service/templates/hooks/post-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: test-release-python-info-service-post-install
  labels:
    helm.sh/chart: python-info-service-0.1.0
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": post-install
    "helm.sh/hook-weight": "5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  ttlSecondsAfterFinished: 30
  template:
    metadata:
      labels:
        app.kubernetes.io/name: python-info-service
        app.kubernetes.io/instance: test-release
        app: python-info-service
    spec:
      restartPolicy: Never
      containers:
        - name: post-install-job
          image: "busybox:1.36"
          imagePullPolicy: IfNotPresent
          command:
            - sh
            - -c
            - echo Post-install smoke test started && sleep 5 && echo Post-install smoke test
              finished
---
# Source: python-info-service/templates/hooks/pre-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: test-release-python-info-service-pre-install
  labels:
    helm.sh/chart: python-info-service-0.1.0
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  ttlSecondsAfterFinished: 30
  template:
    metadata:
      labels:
        app.kubernetes.io/name: python-info-service
        app.kubernetes.io/instance: test-release
        app: python-info-service
    spec:
      restartPolicy: Never
      containers:
        - name: pre-install-job
          image: "busybox:1.36"
          imagePullPolicy: IfNotPresent
          command:
            - sh
            - -c
            - echo Pre-install validation started && sleep 5 && echo Pre-install validation finished
MANIFEST:
---
# Source: python-info-service/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: test-release-python-info-service
  labels:
    helm.sh/chart: python-info-service-0.1.0
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 8080
      nodePort: 30080
---
# Source: python-info-service/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-release-python-info-service
  labels:
    helm.sh/chart: python-info-service-0.1.0
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/instance: test-release
    app: python-info-service
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: python-info-service
      app.kubernetes.io/instance: test-release
      app: python-info-service
  template:
    metadata:
      labels:
        app.kubernetes.io/name: python-info-service
        app.kubernetes.io/instance: test-release
        app: python-info-service
    spec:
      containers:
        - name: python-info-service
          image: "projacktor/python-info-service:latest"
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          resources:
            limits:
              cpu: 200m
              memory: 256Mi
            requests:
              cpu: 100m
              memory: 128Mi
          livenessProbe:
            failureThreshold: 3
            initialDelaySeconds: 15
            periodSeconds: 10
            tcpSocket:
              port: 8080
            timeoutSeconds: 2
          readinessProbe:
            failureThreshold: 3
            initialDelaySeconds: 5
            periodSeconds: 5
            tcpSocket:
              port: 8080
            timeoutSeconds: 2

NOTES:
1. Get the application URL:
  export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services test-release-python-info-service)
  export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
```

Runtime verification:

```bash
kubectl get pods -l app.kubernetes.io/name=python-info-service
kubectl get svc
kubectl get jobs

                                                             kubectl get jobs
No resources found in default namespace.
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   5m9s
No resources found in default namespace.
```

Application accessibility checks:

```bash
# NodePort profile (dev)
minikube service python-dev-python-info-service --url

# Or port-forward
kubectl port-forward service/python-dev-python-info-service 8080:8080
curl http://127.0.0.1:8080/
```

## Notes

- This implementation keeps health probes active and configurable.
- Chart defaults mirror existing Lab 9 behavior.
- Final graded evidence should be collected after Helm installation on the target machine.
