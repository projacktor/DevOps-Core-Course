# ArgoCD assgnement

## Task 1 installation

1) Installing ArgoCD into Helm:

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

kubectl create namespace argocd
helm install argocd argo/argo-cd --namespace argocd

kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=argocd-server -n argocd --timeout=120s
```

2) Getting to the ArgoCD web

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
# new terminal
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

![alt](assets/argo-web.png)

3) CLI install

Go to https://argo-cd.readthedocs.io/en/stable/cli_installation/

```bash
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64

argocd login localhost:8080 --insecure
```

## Task 2 ArgoCD deployment

1) ArgoCD deployment at [application.yaml](./argocd/application.yaml)

lab12 set as a `targetRevision`

2) Application of manifest:

```bash
kubectl apply -f k8s/argocd/application.yaml

application.argoproj.io/python-app configured

argocd app sync python-app
TIMESTAMP                  GROUP        KIND              NAMESPACE                  NAME                     STATUS    HEALTH        HOOK  MESSAGE
2026-04-23T22:34:01+03:00          ConfigMap                default  python-app-python-info-service-env       Synced                        
2026-04-23T22:34:01+03:00         PersistentVolumeClaim     default  python-app-python-info-service-data      Synced   Healthy              
2026-04-23T22:34:01+03:00             Secret                default       app-credentials                     Synced                        
2026-04-23T22:34:01+03:00            Service                default  python-app-python-info-service         OutOfSync  Missing              
2026-04-23T22:34:01+03:00   apps  Deployment                default  python-app-python-info-service           Synced   Healthy              
2026-04-23T22:34:01+03:00          ConfigMap                default  python-app-python-info-service-config    Synced                        
2026-04-23T22:34:02+03:00  batch         Job     default  python-app-python-info-service-pre-install            Progressing              
2026-04-23T22:34:04+03:00  batch         Job     default  python-app-python-info-service-pre-install   Running   Synced     PreSync  job.batch/python-app-python-info-service-pre-install created
2026-04-23T22:34:11+03:00            Service     default  python-app-python-info-service    Synced  Healthy              
2026-04-23T22:34:13+03:00         PersistentVolumeClaim     default  python-app-python-info-service-data           Synced   Healthy              persistentvolumeclaim/python-app-python-info-service-data unchanged
2026-04-23T22:34:13+03:00            Service                default  python-app-python-info-service                Synced   Healthy              service/python-app-python-info-service created
2026-04-23T22:34:13+03:00   apps  Deployment                default  python-app-python-info-service                Synced   Healthy              deployment.apps/python-app-python-info-service unchanged
2026-04-23T22:34:13+03:00  batch         Job                default  python-app-python-info-service-pre-install  Succeeded   Synced     PreSync  Reached expected number of succeeded pods
2026-04-23T22:34:13+03:00             Secret                default       app-credentials                          Synced                        secret/app-credentials unchanged
2026-04-23T22:34:13+03:00          ConfigMap                default  python-app-python-info-service-config         Synced                        configmap/python-app-python-info-service-config unchanged
2026-04-23T22:34:13+03:00          ConfigMap                default  python-app-python-info-service-env            Synced                        configmap/python-app-python-info-service-env unchanged
2026-04-23T22:34:13+03:00  batch         Job     default  python-app-python-info-service-post-install   Running   Synced    PostSync  job.batch/python-app-python-info-service-post-install created
2026-04-23T22:34:22+03:00  batch         Job     default  python-app-python-info-service-post-install  Succeeded   Synced    PostSync  Reached expected number of succeeded pods

Name:               argocd/python-app
Project:            default
Server:             https://kubernetes.default.svc
Namespace:          default
URL:                https://argocd.example.com/applications/python-app
Source:
- Repo:             https://github.com/projacktor/DevOps-Core-Course.git
  Target:           lab12
  Path:             labs/k8s/python-info-service
  Helm Values:      values.yaml
SyncWindow:         Sync Allowed
Sync Policy:        Manual
Sync Status:        Synced to lab12 (ef91d1e)
Health Status:      Healthy

Operation:          Sync
Sync Revision:      ef91d1e0362a0dc618222a397e5ca3829b43f317
Phase:              Succeeded
Start:              2026-04-23 22:34:02 +0300 MSK
Finished:           2026-04-23 22:34:22 +0300 MSK
Duration:           20s
Message:            successfully synced (no more tasks)

GROUP  KIND                   NAMESPACE  NAME                                         STATUS     HEALTH   HOOK      MESSAGE
batch  Job                    default    python-app-python-info-service-pre-install   Succeeded           PreSync   Reached expected number of succeeded pods
       Secret                 default    app-credentials                              Synced                        secret/app-credentials unchanged
       ConfigMap              default    python-app-python-info-service-config        Synced                        configmap/python-app-python-info-service-config unchanged
       ConfigMap              default    python-app-python-info-service-env           Synced                        configmap/python-app-python-info-service-env unchanged
       PersistentVolumeClaim  default    python-app-python-info-service-data          Synced     Healthy            persistentvolumeclaim/python-app-python-info-service-data unchanged
       Service                default    python-app-python-info-service               Synced     Healthy            service/python-app-python-info-service created
apps   Deployment             default    python-app-python-info-service               Synced     Healthy            deployment.apps/python-app-python-info-service unchanged
batch  Job                    default    python-app-python-info-service-post-install  Succeeded           PostSync  Reached expected number of succeeded pods
```

Verify

```bash
argocd app sync python-app
TIMESTAMP                  GROUP        KIND              NAMESPACE                  NAME                     STATUS    HEALTH        HOOK  MESSAGE
2026-04-23T22:34:01+03:00          ConfigMap                default  python-app-python-info-service-env       Synced                        
2026-04-23T22:34:01+03:00         PersistentVolumeClaim     default  python-app-python-info-service-data      Synced   Healthy              
2026-04-23T22:34:01+03:00             Secret                default       app-credentials                     Synced                        
2026-04-23T22:34:01+03:00            Service                default  python-app-python-info-service         OutOfSync  Missing              
2026-04-23T22:34:01+03:00   apps  Deployment                default  python-app-python-info-service           Synced   Healthy              
2026-04-23T22:34:01+03:00          ConfigMap                default  python-app-python-info-service-config    Synced                        
2026-04-23T22:34:02+03:00  batch         Job     default  python-app-python-info-service-pre-install            Progressing              
2026-04-23T22:34:04+03:00  batch         Job     default  python-app-python-info-service-pre-install   Running   Synced     PreSync  job.batch/python-app-python-info-service-pre-install created
2026-04-23T22:34:11+03:00            Service     default  python-app-python-info-service    Synced  Healthy              
2026-04-23T22:34:13+03:00         PersistentVolumeClaim     default  python-app-python-info-service-data           Synced   Healthy              persistentvolumeclaim/python-app-python-info-service-data unchanged
2026-04-23T22:34:13+03:00            Service                default  python-app-python-info-service                Synced   Healthy              service/python-app-python-info-service created
2026-04-23T22:34:13+03:00   apps  Deployment                default  python-app-python-info-service                Synced   Healthy              deployment.apps/python-app-python-info-service unchanged
2026-04-23T22:34:13+03:00  batch         Job                default  python-app-python-info-service-pre-install  Succeeded   Synced     PreSync  Reached expected number of succeeded pods
2026-04-23T22:34:13+03:00             Secret                default       app-credentials                          Synced                        secret/app-credentials unchanged
2026-04-23T22:34:13+03:00          ConfigMap                default  python-app-python-info-service-config         Synced                        configmap/python-app-python-info-service-config unchanged
2026-04-23T22:34:13+03:00          ConfigMap                default  python-app-python-info-service-env            Synced                        configmap/python-app-python-info-service-env unchanged
2026-04-23T22:34:13+03:00  batch         Job     default  python-app-python-info-service-post-install   Running   Synced    PostSync  job.batch/python-app-python-info-service-post-install created
2026-04-23T22:34:22+03:00  batch         Job     default  python-app-python-info-service-post-install  Succeeded   Synced    PostSync  Reached expected number of succeeded pods

Name:               argocd/python-app
Project:            default
Server:             https://kubernetes.default.svc
Namespace:          default
URL:                https://argocd.example.com/applications/python-app
Source:
- Repo:             https://github.com/projacktor/DevOps-Core-Course.git
  Target:           lab12
  Path:             labs/k8s/python-info-service
  Helm Values:      values.yaml
SyncWindow:         Sync Allowed
Sync Policy:        Manual
Sync Status:        Synced to lab12 (ef91d1e)
Health Status:      Healthy

Operation:          Sync
Sync Revision:      ef91d1e0362a0dc618222a397e5ca3829b43f317
Phase:              Succeeded
Start:              2026-04-23 22:34:02 +0300 MSK
Finished:           2026-04-23 22:34:22 +0300 MSK
Duration:           20s
Message:            successfully synced (no more tasks)

GROUP  KIND                   NAMESPACE  NAME                                         STATUS     HEALTH   HOOK      MESSAGE
batch  Job                    default    python-app-python-info-service-pre-install   Succeeded           PreSync   Reached expected number of succeeded pods
       Secret                 default    app-credentials                              Synced                        secret/app-credentials unchanged
       ConfigMap              default    python-app-python-info-service-config        Synced                        configmap/python-app-python-info-service-config unchanged
       ConfigMap              default    python-app-python-info-service-env           Synced                        configmap/python-app-python-info-service-env unchanged
       PersistentVolumeClaim  default    python-app-python-info-service-data          Synced     Healthy            persistentvolumeclaim/python-app-python-info-service-data unchanged
       Service                default    python-app-python-info-service               Synced     Healthy            service/python-app-python-info-service created
apps   Deployment             default    python-app-python-info-service               Synced     Healthy            deployment.apps/python-app-python-info-service unchanged
batch  Job                    default    python-app-python-info-service-post-install  Succeeded           PostSync  Reached expected number of succeeded pods
```

