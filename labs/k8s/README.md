# Lab09: Minikube

## Task 1-3

- [deployment.yaml](./deployment.yaml) (replicas 3)
- [service.yaml](./service.yaml)

Usage:

```sh
kubectl apply -f labs/k8s/deployment.yaml
kubectl get deployment python-info-service
kubectl describe deployment python-info-service
kubectl get pods -l app=python-info-service
```

```sh
kubectl get deployment python-info-service
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
python-info-service   3/3     3            3           11m

kubectl describe deployment python-info-service
Name:                   python-info-service
Namespace:              default
CreationTimestamp:      Thu, 26 Mar 2026 21:33:30 +0300
Labels:                 app=python-info-service
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=python-info-service
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  0 max unavailable, 1 max surge
Pod Template:
  Labels:  app=python-info-service
  Containers:
   python-info-service:
    Image:      projacktor/python-info-service:latest
    Port:       8080/TCP
    Host Port:  0/TCP
    Limits:
      cpu:     200m
      memory:  256Mi
    Requests:
      cpu:         100m
      memory:      128Mi
    Liveness:      tcp-socket :8080 delay=15s timeout=2s period=10s #success=1 #failure=3
    Readiness:     tcp-socket :8080 delay=5s timeout=2s period=5s #success=1 #failure=3
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   python-info-service-85d87fc579 (3/3 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  11m   deployment-controller  Scaled up replica set python-info-service-85d87fc579 from 0 to 3

kubectl get pods -l app=python-info-service
NAME                                   READY   STATUS    RESTARTS   AGE
python-info-service-85d87fc579-rjbx8   1/1     Running   0          11m
python-info-service-85d87fc579-sxbp5   1/1     Running   0          11m
python-info-service-85d87fc579-zq7gd   1/1     Running   0          11m
```

```sh
projacktor@projacktorLaptop ~/P/e/DevOps-Core-Course (lab9)> kubectl apply -f labs/k8s/service.yaml
service/python-info-service created
projacktor@projacktorLaptop ~/P/e/DevOps-Core-Course (lab9)> kubectl get svc -n default
NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes            ClusterIP   10.96.0.1       <none>        443/TCP          23h
python-info-service   NodePort    10.104.130.60   <none>        8080:30080/TCP   6s
projacktor@projacktorLaptop ~/P/e/DevOps-Core-Course (lab9)> kubectl get svc python-info-service -n default
NAME                  TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
python-info-service   NodePort   10.104.130.60   <none>        8080:30080/TCP   16s
projacktor@projacktorLaptop ~/P/e/DevOps-Core-Course (lab9)> minikube service python-info-service --url
http://192.168.49.2:30080
projacktor@projacktorLaptop ~/P/e/DevOps-Core-Course (lab9)> kubectl get services
NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes            ClusterIP   10.96.0.1       <none>        443/TCP          23h
python-info-service   NodePort    10.104.130.60   <none>        8080:30080/TCP   68s
projacktor@projacktorLaptop ~/P/e/DevOps-Core-Course (lab9)> kubectl get services python-info-service 
NAME                  TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
python-info-service   NodePort   10.104.130.60   <none>        8080:30080/TCP   79s
projacktor@projacktorLaptop ~/P/e/DevOps-Core-Course (lab9)> kubectl get endpoints
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME                  ENDPOINTS                                         AGE
kubernetes            192.168.49.2:8443                                 23h
python-info-service   10.244.0.4:8080,10.244.0.5:8080,10.244.0.6:8080   85s
```

## Task 4

Increase replicas:

```sh
kubectl scale deployment/python-info-service --replicas=5

deployment.apps/python-info-service scaled

kubectl get pods -w
NAME                                   READY   STATUS    RESTARTS   AGE
python-info-service-85d87fc579-c8z74   1/1     Running   0          33s
python-info-service-85d87fc579-nqxrh   1/1     Running   0          33s
python-info-service-85d87fc579-rjbx8   1/1     Running   0          16m
python-info-service-85d87fc579-sxbp5   1/1     Running   0          16m
python-info-service-85d87fc579-zq7gd   1/1     Running   0          16m


^C⏎ 

kubectl rollout status deployment/python-info-service
deployment "python-info-service" successfully rolled out
```

## Task 5

### Architecture Overview

- Cluster: minikube (single-node local Kubernetes)
- Workload: Deployment/python-info-service
- Replicas: 3 (scaled to 5 in Task 4)
- Networking: Service/python-info-service type NodePort (8080 -> 30080)
- Traffic flow: Client -> NodeIP:30080 -> Service -> Pod:8080
- Resources per Pod:
  - requests: 100m CPU, 128Mi RAM
  - limits: 200m CPU, 256Mi RAM

### Manifest Files

- deployment.yaml
  - replicas: 3
  - RollingUpdate strategy (maxSurge: 1, maxUnavailable: 0)
  - livenessProbe/readinessProbe via TCP 8080
  - resources.requests/limits set for predictable scheduling
- service.yaml
  - type: NodePort
  - selector app: python-info-service
  - port: 8080, targetPort: 8080, nodePort: 30080

### Deployment Evidence
```sh
kubectl get all
kubectl get all
NAME                                       READY   STATUS    RESTARTS   AGE
pod/python-info-service-85d87fc579-c8z74   1/1     Running   0          5m34s
pod/python-info-service-85d87fc579-nqxrh   1/1     Running   0          5m34s
pod/python-info-service-85d87fc579-rjbx8   1/1     Running   0          21m
pod/python-info-service-85d87fc579-sxbp5   1/1     Running   0          21m
pod/python-info-service-85d87fc579-zq7gd   1/1     Running   0          21m

NAME                          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/kubernetes            ClusterIP   10.96.0.1       <none>        443/TCP          23h
service/python-info-service   NodePort    10.104.130.60   <none>        8080:30080/TCP   14m

NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/python-info-service   5/5     5            5           21m

NAME                                             DESIRED   CURRENT   READY   AGE
replicaset.apps/python-info-service-85d87fc579   5         5         5       21m
```

```sh
kubectl get pods,svc -o wide
NAME                                       READY   STATUS    RESTARTS   AGE     IP           NODE       NOMINATED NODE   READINESS GATES
pod/python-info-service-85d87fc579-c8z74   1/1     Running   0          5m56s   10.244.0.8   minikube   <none>           <none>
pod/python-info-service-85d87fc579-nqxrh   1/1     Running   0          5m56s   10.244.0.7   minikube   <none>           <none>
pod/python-info-service-85d87fc579-rjbx8   1/1     Running   0          22m     10.244.0.4   minikube   <none>           <none>
pod/python-info-service-85d87fc579-sxbp5   1/1     Running   0          22m     10.244.0.6   minikube   <none>           <none>
pod/python-info-service-85d87fc579-zq7gd   1/1     Running   0          22m     10.244.0.5   minikube   <none>           <none>

NAME                          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE   SELECTOR
service/kubernetes            ClusterIP   10.96.0.1       <none>        443/TCP          23h   <none>
service/python-info-service   NodePort    10.104.130.60   <none>        8080:30080/TCP   14m   app=python-info-service
```
```sh
kubectl describe deployment python-info-service
Name:                   python-info-service
Namespace:              default
CreationTimestamp:      Thu, 26 Mar 2026 21:33:30 +0300
Labels:                 app=python-info-service
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=python-info-service
Replicas:               5 desired | 5 updated | 5 total | 5 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  0 max unavailable, 1 max surge
Pod Template:
  Labels:  app=python-info-service
  Containers:
   python-info-service:
    Image:      projacktor/python-info-service:latest
    Port:       8080/TCP
    Host Port:  0/TCP
    Limits:
      cpu:     200m
      memory:  256Mi
    Requests:
      cpu:         100m
      memory:      128Mi
    Liveness:      tcp-socket :8080 delay=15s timeout=2s period=10s #success=1 #failure=3
    Readiness:     tcp-socket :8080 delay=5s timeout=2s period=5s #success=1 #failure=3
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
OldReplicaSets:  <none>
NewReplicaSet:   python-info-service-85d87fc579 (5/5 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  22m    deployment-controller  Scaled up replica set python-info-service-85d87fc579 from 0 to 3
  Normal  ScalingReplicaSet  6m26s  deployment-controller  Scaled up replica set python-info-service-85d87fc579 from 3 to 5
```

#### App accessibility check
```sh
curl http://192.168.49.2:30080/
{"service":{"name":"devops-info-service","version":"1.0.0","description":"DevOps course info service","framework":"FastAPI"},"system":{"hostname":"python-info-service-85d87fc579-nqxrh","platform":"Linux","platform_version":"#37~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Nov 20 10:25:38 UTC 2","architecture":"x86_64","cpu_count":16,"python_version":"3.12.13"},"runtime":{"uptime_seconds":428,"uptime_human":"0 hours, 7 minutes","current_time":"2026-03-26T18:56:57.746777","timezone":"UTC"},"request":{"client_ip":"10.244.0.1","user_agent":"curl/8.5.0","method":"GET","path":"/"},"endpoints":[{"path":"/","method":"GET","description":"Service information"},{"path":"/health","method":"GET","description":"Health check"}]}⏎ 
```


### Operations Performed

#### Deploy
- ```kubectl apply -f labs/k8s/deployment.yaml```
- ```kubectl apply -f labs/k8s/service.yaml```

#### Scale
- ```kubectl scale deployment/python-info-service --replicas=5```
- ```kubectl rollout status deployment/python-info-service```

#### Rolling update
- Performed by changing runtime config:
  - ```kubectl set env deployment/python-info-service RELEASE=lab09-update```
- Verified:
  - ```kubectl rollout status deployment/python-info-service```
  - ```kubectl rollout history deployment/python-info-service```

#### Rollback
- ```kubectl rollout undo deployment/python-info-service```
- Verified:
  - ```kubectl rollout status deployment/python-info-service```
  - ```kubectl rollout history deployment/python-info-service```

### Production Considerations

- Health checks:
  - readiness probe prevents routing traffic to not-ready Pods
  - liveness probe restarts hung container
- Resource limits:
  - protect node from noisy-neighbor effect
  - guarantee minimum CPU/memory via requests
- Production improvements:
  - use fixed image tags (not latest)
  - add startupProbe for slow starts
  - add HPA + metrics-server
  - central logging/monitoring (Prometheus + Grafana, Loki/ELK)

### Challenges & Solutions

- Issue: Service not found in minikube
  - Cause: wrong kubectl context/namespace
  - Fix: kubectl config use-context minikube, then re-apply manifests
- Issue: Deployment initially showed 0/3 available
  - Cause: probes and startup delay
  - Fix: waited for readiness and checked with kubectl rollout status
- Learning:
  - Kubernetes is declarative; actual state converges asynchronously
  - Labels/selectors are critical for Service-to-Pod routing