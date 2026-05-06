# StatefulSet Implementation

## StatefulSet Overview

This lab migrates the application from a stateless controller to a `StatefulSet` because the service now needs per-pod persistent storage and stable pod identity.

Why `StatefulSet` is a better fit here:

- Each pod gets a stable name such as `python-info-service-python-info-service-0`, `-1`, and `-2`.
- Each pod gets its own `PersistentVolumeClaim` created from `volumeClaimTemplates`.
- Pod DNS names stay predictable through the headless service.
- Storage is preserved when an individual pod is deleted and recreated.

Key differences from `Deployment`:

| Feature | Deployment | StatefulSet |
|---|---|---|
| Pod identity | Ephemeral | Stable ordinal names |
| Storage | Shared or manually attached PVC | One PVC per pod via `volumeClaimTemplates` |
| Network identity | Service load-balances to any pod | Direct pod-to-pod DNS through a headless service |
| Scaling behavior | No ordering guarantees | Ordered creation and termination by default |

Implementation summary:

- `service.yaml` provides external access to the application.
- `service-headless.yaml` provides `clusterIP: None` for pod DNS discovery.
- `statefulset.yaml` defines stable replicas and per-pod storage with `volumeClaimTemplates`.

## Resource Verification

Relevant application resources from `kubectl get po,sts,svc,pvc`:

```bash
NAME                                            READY   STATUS    RESTARTS   AGE
pod/python-info-service-python-info-service-0   1/1     Running   0          2m55s
pod/python-info-service-python-info-service-1   1/1     Running   0          23m
pod/python-info-service-python-info-service-2   1/1     Running   0          23m

NAME                                                       READY   AGE
statefulset.apps/python-info-service-python-info-service   3/3     23m

NAME                                                       TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/python-info-service-python-info-service            NodePort    10.97.124.60   <none>        8080:30080/TCP 6m40s
service/python-info-service-python-info-service-headless   ClusterIP   None            <none>        8080/TCP       23m

NAME                                                                   STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/data-python-info-service-python-info-service-0   Bound    pvc-c1a5c9c5-6a23-4ab9-84b0-4c372139a342   100Mi      RWO            standard       23m
persistentvolumeclaim/data-python-info-service-python-info-service-1   Bound    pvc-80eb040a-e66e-4622-988d-7f81fe7598c8   100Mi      RWO            standard       23m
persistentvolumeclaim/data-python-info-service-python-info-service-2   Bound    pvc-4dabc27b-9d5f-405f-9d2d-4dbc2d0dde57   100Mi      RWO            standard       23m
```

Verification notes:

- The StatefulSet is healthy with `3/3` ready replicas.
- Pod names use ordinal suffixes as expected.
- The headless service exists and has `CLUSTER-IP: None`.
- Three separate PVCs were created, one for each replica.

## Network Identity

StatefulSet pods can resolve each other directly by DNS through the headless service.

Command:

```bash
kubectl exec -it python-info-service-python-info-service-0 -- \
  getent hosts python-info-service-python-info-service-1.python-info-service-python-info-service-headless
```

Output:

```bash
10.244.0.181  python-info-service-python-info-service-1.python-info-service-python-info-service-headless.default.svc.cluster.local
```

DNS naming pattern:

```text
<pod-name>.<headless-service-name>.<namespace>.svc.cluster.local
```

Example in this lab:

```text
python-info-service-python-info-service-1.python-info-service-python-info-service-headless.default.svc.cluster.local
```

## Per-Pod Storage Evidence

Each pod stores its own visit counter in its own mounted volume, so the visit counts differ between replicas.

Commands used:

```bash
kubectl port-forward pod/python-info-service-python-info-service-0 8080:8080
kubectl port-forward pod/python-info-service-python-info-service-1 8081:8080
curl localhost:8080/visit
curl localhost:8081/visit
```

Observed output:

```json
{"total":4,"all":[{"datetime":"2026-05-06T22:18:57.171916","IP":"127.0.0.1"},{"datetime":"2026-05-06T22:19:32.793909","IP":"127.0.0.1"},{"datetime":"2026-05-06T22:19:47.565205","IP":"127.0.0.1"},{"datetime":"2026-05-06T22:24:36.939964","IP":"127.0.0.1"}]}
{"total":2,"all":[{"datetime":"2026-05-06T22:19:32.805844","IP":"127.0.0.1"},{"datetime":"2026-05-06T22:19:47.605275","IP":"127.0.0.1"}]}
```

Interpretation:

- Pod `-0` reported `total: 4`.
- Pod `-1` reported `total: 2`.
- Different totals confirm storage isolation per pod.

Current implementation note:

- The application currently exposes `GET /visit`, not `GET /visits`.
- To match the lab wording exactly, the endpoint should be renamed from `/visit` to `/visits`.

## Persistence Test

The visit counter survived deletion of pod `-0`, which confirms that the data lives on the pod-specific PVC rather than inside the ephemeral container filesystem.

Before deletion:

```bash
kubectl exec -it python-info-service-python-info-service-0 -- cat /app/data/visits.json
```

```json
{"visits": [{"datetime": "2026-05-06T22:18:57.171916", "IP": "127.0.0.1"}, {"datetime": "2026-05-06T22:19:32.793909", "IP": "127.0.0.1"}, {"datetime": "2026-05-06T22:19:47.565205", "IP": "127.0.0.1"}, {"datetime": "2026-05-06T22:24:36.939964", "IP": "127.0.0.1"}], "total": 4}
```

Delete the pod:

```bash
kubectl delete pod python-info-service-python-info-service-0
```

After the pod was recreated:

```bash
kubectl exec -it python-info-service-python-info-service-0 -- cat /app/data/visits.json
```

```json
{"visits": [{"datetime": "2026-05-06T22:18:57.171916", "IP": "127.0.0.1"}, {"datetime": "2026-05-06T22:19:32.793909", "IP": "127.0.0.1"}, {"datetime": "2026-05-06T22:19:47.565205", "IP": "127.0.0.1"}, {"datetime": "2026-05-06T22:24:36.939964", "IP": "127.0.0.1"}], "total": 4}
```

Result:

- The recreated pod kept the same counter data.
- This confirms that the PVC for pod `-0` was reattached successfully.

## Current Gaps

The StatefulSet implementation itself is working, but two details should still be aligned with the lab requirements:

1. The lab asks for a `/visits` endpoint, while the current application exposes `/visit`.
2. The lab examples use `/data/visits`, while the current application writes to `/app/data/visits.json` because the container `WORKDIR` is `/app` and the volume is mounted at `/app/data`.

These are small application-level differences and do not change the StatefulSet behavior, but updating them would make the implementation match the lab instructions exactly.
