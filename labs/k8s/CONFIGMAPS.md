# ConfigMaps and Persistent Volumes

## Application Changes

### Visits Counter Implementation

From Task 1 commits:

- Added visit counting in `labs/app_python/app.py` via `count_visit(client_ip)`.
- Counter state is stored in `data/visits.json` as:
  - `visits`: list of visit records (`datetime`, `IP`)
  - `total`: aggregated counter
- File is initialized on first request if missing.
- Docker image was updated to guarantee data directory existence: `mkdir -p /app/data` and ownership setup.

### New Endpoint Documentation

Lab requirement asks for `/visits`. In current state, the service still exposes `GET /` and `GET /health`; `/visit` or `/visits` is not implemented yet (confirmed by runtime `404`).

`labs/app_python/Dockerfile` creates `/app/data`.

app writes counter to `data/visits.json`; test data artifacts were added (`labs/app_python/data/visits.json`, `.keep`).

## ConfigMap Implementation

### ConfigMap Template Structure

1. File-backed ConfigMap:
- `labs/k8s/python-info-service/templates/ConfigMap.yaml`
- Uses `.Files.Get "files/config.json"`.

2. Env-backed ConfigMap:
- `labs/k8s/python-info-service/templates/configmap-env.yaml`
- Exposes `APP_*` keys from `values.yaml`.

### `config.json` Content

Located at `labs/k8s/python-info-service/files/config.json`:

```json
{
  "applicationName": "python-info-service",
  "environment": "dev",
  "featureFlags": {
    "debug": true,
    "metrics": true,
    "newUI": false
  }
}
```

### How ConfigMap Is Mounted as File

In `templates/deployment.yaml`:

- Volume `app-config` references `...-config` ConfigMap.
- `volumeMounts` mounts `config.json` using `subPath` to:
  - `/config/config.json`

### How ConfigMap Provides Environment Variables

In `templates/deployment.yaml`:

- `envFrom` includes:
  - `configMapRef: <release>-python-info-service-env`
- This injects all `APP_*` keys from `templates/configmap-env.yaml`.

### Verification Outputs

#### `kubectl get configmap,pvc`

```bash
kubectl get configmap,pvc -n default
NAME                                                       DATA   AGE
configmap/kube-root-ca.crt                                 1      13d
configmap/python-info-service-python-info-service-config   1      25m
configmap/python-info-service-python-info-service-env      5      19m

NAME                                                                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/python-info-service-python-info-service-data   Bound    pvc-4de13677-c5f1-4947-937f-13877286847e   100Mi      RWO            standard       <unset>                 13m
```

#### File content inside Pod

```bash
kubectl exec -n default python-info-service-python-info-service-78c59457b4-bx657 -c python-info-service -- cat /config/config.json
{
  "applicationName": "python-info-service",
  "environment": "dev",
  "featureFlags": {
    "debug": true,
    "metrics": true,
    "newUI": false
  }
}
```

#### Environment variables in Pod

```bash
kubectl exec -n default python-info-service-python-info-service-78c59457b4-bx657 -c python-info-service -- printenv | grep APP_ | sort
APP_ENV=dev
APP_FEATURE_DEBUG=true
APP_FEATURE_METRICS=true
APP_FEATURE_NEW_UI=false
APP_NAME=python-info-service
```

## Persistent Volume

### PVC Configuration Explanation

PVC template (`templates/pvc.yaml`):

- Kind: `PersistentVolumeClaim`
- Name: `<release>-python-info-service-data`
- Access mode: `ReadWriteOnce`
- Size from values: `.Values.persistence.size` (currently `100Mi`)
- Optional storage class: `.Values.persistence.storageClass`
- Wrapped with condition: only rendered if `.Values.persistence.enabled=true`

### Access Modes and Storage Class

- `ReadWriteOnce` means volume is mounted as read-write by one node.
- In Minikube, `standard` (`k8s.io/minikube-hostpath`) dynamically provisions the PV.
- Current PVC is `Bound` to dynamic PV `pvc-4de13677-c5f1-4947-937f-13877286847e`.

### Volume Mount Configuration

In `templates/deployment.yaml`:

- `volumes` includes `data-volume` -> `persistentVolumeClaim.claimName: <release>-python-info-service-data`
- `volumeMounts` mounts `data-volume` to `/app/data`

### Persistence Test Evidence

#### Counter before pod deletion

```bash
kubectl exec -n default python-info-service-python-info-service-78c59457b4-6xhfd -c python-info-service -- cat /app/data/visits.json
{"visits": [{"datetime": "2026-04-16T19:50:52.411821", "IP": "127.0.0.1"}], "total": 1}
```

#### Pod deletion command

```bash
kubectl delete pod -n default python-info-service-python-info-service-78c59457b4-6xhfd
```

#### Counter after new pod starts

```bash
kubectl exec -n default python-info-service-python-info-service-78c59457b4-bx657 -c python-info-service -- cat /app/data/visits.json
{"visits": [{"datetime": "2026-04-16T19:50:52.411821", "IP": "127.0.0.1"}], "total": 1}
```

Result: counter value persisted across pod recreation.

## ConfigMap vs Secret

### When to Use ConfigMap

Use ConfigMap for non-sensitive configuration:

- app name
- environment (`dev`/`prod`)
- feature flags
- general runtime settings

### When to Use Secret

Use Secret for sensitive data:

- passwords
- API tokens
- DB credentials
- private keys/certificates

### Key Differences

- Sensitivity: ConfigMap is plain-text config; Secret is intended for confidential values.
- Encoding: Secret values are base64-encoded (not encrypted by default).
- Access control: Secrets usually require stricter RBAC and handling policies.
- Operational usage: both can be mounted as files or injected as env vars.

