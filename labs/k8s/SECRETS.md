## Task 1

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

## Task 2

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

## Task 3

HashiCorp Vault deployment:

```bash
kubectl get pods
NAME                                                       READY   STATUS    RESTARTS      AGE
python-info-service-python-info-service-8654bfdbb6-ntgwk   1/1     Running   1 (19m ago)   33m
python-info-service-python-info-service-8654bfdbb6-vvp4n   1/1     Running   1 (19m ago)   33m
python-info-service-python-info-service-8654bfdbb6-wltkh   1/1     Running   1 (19m ago)   33m
vault-0                                                    1/1     Running   0             29m
vault-agent-injector-848dd747d7-dkf66                      1/1     Running   1 (19m ago)   29m
(.venv) projacktor@projacktorLaptop ~/P/e/D/l/k8s (lab11)> kubectl exec -it vault
-0 -- /bin/sh
```

vault work

```sh
/ $ export VAULT_ADDR=http://127.0.0.1:8200
/ $ vault status
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         1.21.2
Build Date      2026-01-06T08:33:05Z
Storage Type    inmem
Cluster Name    vault-cluster-956efc88
Cluster ID      8e8fe3e0-4f1f-8863-5c5a-36cff09c17c6
HA Enabled      false
/ $ vault login root
Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                  Value
---                  -----
token                root
token_accessor       TBPUXazHkRbNCf0hiXqzD4MY
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
/ $ vault secrets enable -path=secret kv-v2
Error enabling: Error making API request.

URL: POST http://127.0.0.1:8200/v1/sys/mounts/secret
Code: 400. Errors:

* path is already in use at secret/
/ $ vault kv put secret/python-info-service
Must supply data
/ $ vault kv put secret/python-info-service username=change-me password=change-me
========= Secret Path =========
secret/data/python-info-service

======= Metadata =======
Key                Value
---                -----
created_time       2026-04-09T20:13:53.908958525Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1
/ $ vault kv get secret/python-info-service
========= Secret Path =========
secret/data/python-info-service

======= Metadata =======
Key                Value
---                -----
created_time       2026-04-09T20:13:53.908958525Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1

====== Data ======
Key         Value
---         -----
password    change-me
username    change-me
/ $ vault auth enable kubernetes
Success! Enabled kubernetes auth method at: kubernetes/
/ $ export K8S_HOST=htts://kubernetes.default.svc:443
/ $ export K8S_CA_CERT=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
/ $ export TOKEN_REVIEW_JWT=$(cat /var/run/secrets/kubernetes.io/serviceaccount/t
oken)
/ $ export K8S_HOST=https://kubernetes.default.svc:443
/ $ vault write auth/kubernetes/role/python-info-service bound_service_account_na
mes=default bound_service_account_namespaces=default policies=python-info-service
 ttl=24h
WARNING! The following warnings were returned from Vault:

  * Role python-info-service does not have an audience configured. While
  audiences are not required, consider specifying one if your use case would
  benefit from additional JWT claim verification.

/ $ vault read auth/kubernetes/role/python-info-service
Key                                         Value
---                                         -----
alias_name_source                           serviceaccount_uid
bound_service_account_names                 [default]
bound_service_account_namespace_selector    n/a
bound_service_account_namespaces            [default]
policies                                    [python-info-service]
token_bound_cidrs                           []
token_explicit_max_ttl                      0s
token_max_ttl                               0s
token_no_default_policy                     false
token_num_uses                              0
token_period                                0s
token_policies                              [python-info-service]
token_ttl                                   24h
token_type                                  default
ttl                                         24h
/ $ vault write auth/kubernetes/config \
>   token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
>   kubernetes_host="https://kubernetes.default.svc:443" \
>   kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
Success! Data written to: auth/kubernetes/config
/ $ vault policy write python-info-service - <<'EOF'
> path "secret/data/python-info-service" {
>   capabilities = ["read"]
> }
> EOF
Success! Uploaded policy: python-info-service
/ $ vault write auth/kubernetes/role/python-info-service \
>   bound_service_account_names=default \
>   bound_service_account_namespaces=default \
>   policies=python-info-service \
>   ttl=24h
WARNING! The following warnings were returned from Vault:

  * Role python-info-service does not have an audience configured. While
  audiences are not required, consider specifying one if your use case would
  benefit from additional JWT claim verification.

/ $ vault read auth/kubernetes/config
Key                                  Value
---                                  -----
disable_iss_validation               true
disable_local_ca_jwt                 false
issuer                               n/a
kubernetes_ca_cert                   -----BEGIN CERTIFICATE-----
                        # my cert hidden :))
-----END CERTIFICATE-----
kubernetes_host                      https://kubernetes.default.svc:443
pem_keys                             []
token_reviewer_jwt_set               true
use_annotations_as_alias_metadata    false
/ $ vault policy read python-info-service
path "secret/data/python-info-service" {
  capabilities = ["read"]
}
/ $ vault read auth/kubernetes/role/python-info-service
Key                                         Value
---                                         -----
alias_name_source                           serviceaccount_uid
bound_service_account_names                 [default]
bound_service_account_namespace_selector    n/a
bound_service_account_namespaces            [default]
policies                                    [python-info-service]
token_bound_cidrs                           []
token_explicit_max_ttl                      0s
token_max_ttl                               0s
token_no_default_policy                     false
token_num_uses                              0
token_period                                0s
token_policies                              [python-info-service]
token_ttl                                   24h
token_type                                  default
ttl                                         24h
/ $ vault kv get secret/python-info-service
========= Secret Path =========
secret/data/python-info-service

======= Metadata =======
Key                Value
---                -----
created_time       2026-04-09T20:13:53.908958525Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1

====== Data ======
Key         Value
---         -----
password    change-me
username    change-me
```

Check if applied

```bash
command terminated with exit code 130
(.venv) projacktor@projacktorLaptop ~/P/e/D/l/k8s (lab11) [0|SIGINT]> helm upgrade --install pyth
on-info-service ./python-info-service --set vault.enabled=true
Release "python-info-service" has been upgraded. Happy Helming!
NAME: python-info-service
LAST DEPLOYED: Thu Apr  9 23:28:05 2026
NAMESPACE: default
STATUS: deployed
REVISION: 3
DESCRIPTION: Upgrade complete
TEST SUITE: None
NOTES:
1. Get the application URL:
  export NODE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].nodePort}" services python-info-service-python-info-service)
  export NODE_IP=$(kubectl get nodes --namespace default -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
(.venv) projacktor@projacktorLaptop ~/P/e/D/l/k8s (lab11)> kubectl get pods
NAME                                                       READY   STATUS    RESTARTS      AGE
python-info-service-python-info-service-8654bfdbb6-ntgwk   1/1     Running   1 (36m ago)   49m
python-info-service-python-info-service-8654bfdbb6-vvp4n   1/1     Running   1 (36m ago)   49m
python-info-service-python-info-service-8654bfdbb6-wltkh   1/1     Running   1 (36m ago)   49m
python-info-service-python-info-service-d8cb78fc7-4jssc    1/2     Running   0             5s
vault-0                                                    1/1     Running   0             45m
vault-agent-injector-848dd747d7-dkf66                      1/1     Running   1 (36m ago)   45m

kubectl describe pod python-info-servi
ce-python-info-service-d8cb78fc7-4jssc | grep vault.hashicorp.com
Annotations:      vault.hashicorp.com/agent-inject: true
                  vault.hashicorp.com/agent-inject-secret-app.env: secret/data/python-info-service
                  vault.hashicorp.com/agent-inject-status: injected
                  vault.hashicorp.com/agent-inject-template-app.env:
                  vault.hashicorp.com/role: python-info-service

 kubectl exec -it python-info-service-p
ython-info-service-d8cb78fc7-4jssc -- ls /vault/secrets
Defaulted container "python-info-service" out of: python-info-service, vault-agent, vault-agent-init (init)
app.env
(.venv) projacktor@projacktorLaptop ~/P/e/D/l/k8s (lab11)> kubectl exec -it python-info-service-p
ython-info-service-d8cb78fc7-4jssc -- cat /vault/secrets/app.env
Defaulted container "python-info-service" out of: python-info-service, vault-agent, vault-agent-init (init)
export APP_USERNAME="change-me"
export APP_PASSWORD="change-me"
```

## K8s Secrets vs Vault

#### Kubernetes Secrets:

- Easy to implement and quick to configure.
- Natively integrated with Deployment/StatefulSet.
- Well suited for basic scenarios and small projects.
- Stored in etcd (encryption at rest recommended).
- Limited rotation and dynamic secrets capabilities without additional tools.

#### Vault:

- Centralized secret management and auditing.
- Flexible access policies (fine-grained ACLs).
- Support for dynamic secrets and rotation.
- Pod injection without storing secrets in Git/values ​​as plain values.
- More complex operationally: requires configuring auth, policy, role, Vault accessibility, and lifecycle tokens.


### When to Use Each Approach

#### Use Kubernetes Secrets when:

- You need a quick start and simple operation.
- You have a small number of secrets and infrequent rotation.
- Your environment doesn't require advanced auditing/compliance.

#### Use Vault when:

- You need strict access policies and auditing.
- You need rotation and dynamic/temporary credentials.
- Multiple applications/teams use a common secrets platform.
- You have production-level security requirements.

### Production Recommendations

- Don't store real secrets in Git or in regular values.yaml.
- For Kubernetes Secrets, enable encryption at rest in etcd and strict RBAC.
- For Vault, don't use dev mode/inmem storage.
- For Vault, use HA + persistent storage (e.g., Raft), backup, and auto-unseal (KMS/HSM).
- For Vault roles, set the audience and minimum required policy.
- For applications, use a separate ServiceAccount instead of the default.
- Enable monitoring and auditing:
    - Kubernetes events,
    - Vault audit logs,
    - injector/server unavailability alerts.
    - Regularly rotate secrets and test failover.
- Post-deploy checks:
    - pod annotations for Vault injection,
    - presence of the ```/vault/secrets/...``` file,
    - no secret leaks in ```kubectl describe```.