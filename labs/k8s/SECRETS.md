# Task 1

Create secrets via:

```sh
kubectl create secret generic app-credentials --from-literal=key=value
secret/app-credentials created
```
Get in YAML:

```sh
kubectl get secret app-credentials -o yaml
```
```yaml
apiVersion: v1
data:
  key: dmFsdWU=
kind: Secret
metadata:
  creationTimestamp: "2026-04-09T18:52:20Z"
  name: app-credentials
  namespace: default
  resourceVersion: "1618"
  uid: a70d861e-0ec4-415c-821b-d38f4016f341
type: Opaque
```

I used [cyberchef](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)&input=ZG1Gc2RXVT0) to decode ```key: dmFsdWU=```

![alt](./assets/image.png)

# Task 2

See git diffs how values.yaml and deployment.yaml was changed. [secrets.yaml](./service.yaml) created

Commands used:

```bash
helm upgrade --install pyt
hon-info-service ./python-info-service/
Release "python-info-service" does not exist. Installing it now.
NAME: python-info-service
LAST DEPLOYED: Thu Apr  9 22:32:41 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None
NOTES:
1. Get the application URL:
  export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services python-info-service-python-info-service)
  export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT

kubectl get secret app-credent
ials -o yaml
apiVersion: v1
data:
  password: Y2hhbmdlLW1l
  username: Y2hhbmdlLW1l
kind: Secret
metadata:
  annotations:
    meta.helm.sh/release-name: python-info-service
    meta.helm.sh/release-namespace: default
  creationTimestamp: "2026-04-09T19:32:50Z"
  labels:
    app: python-info-service
    app.kubernetes.io/instance: python-info-service
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: python-info-service
    app.kubernetes.io/version: 1.0.0
    helm.sh/chart: python-info-service-0.1.0
  name: app-credentials
  namespace: default
  resourceVersion: "3573"
  uid: 38b3fd7b-1fdb-420e-80fe-883c969854a2
type: Opaque

kubectl get pods
NAME                                                       READY   STATUS    RESTARTS   AGE
python-info-service-python-info-service-7f8959cf57-2ntjg   1/1     Running   0          112s
python-info-service-python-info-service-7f8959cf57-5dsvk   1/1     Running   0          112s
python-info-service-python-info-service-7f8959cf57-jwj8x   1/1     Running   0          112s

kubectl exec -it python-info-service-python-i
nfo-service-8654bfdbb6-ntgwk -- printenv | grep -E 'usename|password|APP_'
password=change-me
```