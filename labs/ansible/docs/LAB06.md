# Lab 5: Ansible Fundamentals

> by Arsen Galiev B23 CBS-01

## Task 1

```sh
$ ansible-playbook playbooks/provision.yaml --tags "doc
ker" --ask-vault-pass
Vault password:

PLAY [Provision web servers] *********************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Install required system packages] *************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Create directory for Docker GPG key] **********************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Add Docker's official GPG key] ****************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Add Docker repository] ************************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Install Docker packages] **********************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Install python3-docker] ***********************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Add users to docker group] ********************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-54-146-54-202.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-3-89-229-132.compute-1.amazonaws.com] => (item=ubuntu)

TASK [docker : Ensure Docker service is running and enabled] *************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
fatal: [ec2-3-89-229-132.compute-1.amazonaws.com]: FAILED! => {"changed": false, "msg": "Unable to start service docker: Job for docker.service failed because the control process exited with error code.\nSee \"systemctl status docker.service\" and \"journalctl -xeu docker.service\" for details.\n"}
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

PLAY RECAP ***************************************************************************************************************
ec2-100-27-222-39.compute-1.amazonaws.com : ok=9    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-3-89-229-132.compute-1.amazonaws.com : ok=8    changed=4    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
ec2-54-146-54-202.compute-1.amazonaws.com : ok=9    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

$ ansible-playbook playbooks/provision.yaml --skip-tags
"common"

PLAY [Provision web servers] *********************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [common : Update apt cache] *****************************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [common : Install essential packages] *******************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [common : Log package installation] *********************************************************************************
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [common : User creation] ********************************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com] => {
    "msg": "User creation tasks would be placed here."
}
ok: [ec2-54-146-54-202.compute-1.amazonaws.com] => {
    "msg": "User creation tasks would be placed here."
}
ok: [ec2-3-89-229-132.compute-1.amazonaws.com] => {
    "msg": "User creation tasks would be placed here."
}

TASK [common : Set timezone] *********************************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Install required system packages] *************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Create directory for Docker GPG key] **********************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Add Docker's official GPG key] ****************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Add Docker repository] ************************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Install Docker packages] **********************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Install python3-docker] ***********************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Add users to docker group] ********************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-100-27-222-39.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-3-89-229-132.compute-1.amazonaws.com] => (item=ubuntu)

TASK [docker : Ensure Docker service is running and enabled] *************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]

PLAY RECAP ***************************************************************************************************************
ec2-100-27-222-39.compute-1.amazonaws.com : ok=14   changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-3-89-229-132.compute-1.amazonaws.com : ok=14   changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-54-146-54-202.compute-1.amazonaws.com : ok=14   changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

$ ansible-playbook playbooks/provision.yaml --tags "pack
ages"

PLAY [Provision web servers] *********************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [common : Update apt cache] *****************************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [common : Install essential packages] *******************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [common : Log package installation] *********************************************************************************
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]

PLAY RECAP ***************************************************************************************************************
ec2-100-27-222-39.compute-1.amazonaws.com : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-3-89-229-132.compute-1.amazonaws.com : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-54-146-54-202.compute-1.amazonaws.com : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

$ ansible-playbook playbooks/provision.yaml --tags "dock
er" --check

PLAY [Provision web servers] *********************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Install required system packages] *************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Create directory for Docker GPG key] **********************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Add Docker's official GPG key] ****************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Add Docker repository] ************************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Install Docker packages] **********************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Install python3-docker] ***********************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Add users to docker group] ********************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-100-27-222-39.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-54-146-54-202.compute-1.amazonaws.com] => (item=ubuntu)

TASK [docker : Ensure Docker service is running and enabled] *************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

PLAY RECAP ***************************************************************************************************************
ec2-100-27-222-39.compute-1.amazonaws.com : ok=9    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-3-89-229-132.compute-1.amazonaws.com : ok=9    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-54-146-54-202.compute-1.amazonaws.com : ok=9    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

$ ansible-playbook playbooks/provision.yaml --tags "dock
er_install"

PLAY [Provision web servers] *********************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Install required system packages] *************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Create directory for Docker GPG key] **********************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Add Docker's official GPG key] ****************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Add Docker repository] ************************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Install Docker packages] **********************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Install python3-docker] ***********************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

PLAY RECAP ***************************************************************************************************************
ec2-100-27-222-39.compute-1.amazonaws.com : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-3-89-229-132.compute-1.amazonaws.com : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-54-146-54-202.compute-1.amazonaws.com : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Tags list

```sh
ansible-playbook playbooks/provision.yaml --list-tags

playbook: playbooks/provision.yaml

  play #1 (webservers): Provision web servers   TAGS: []
      TASK TAGS: [docker, docker_config, docker_install, packages, users]

```

## Task 2: Docker Compose

### Research Questions

- **Q: What's the difference between \`restart: always\` and \`restart: unless-stopped\`?**
  - **A:** \`restart: always\` will restart the container indefinitely regardless of the exit code, even if it was manually stopped (it will restart on daemon restart). \`restart: unless-stopped\` behaves similarly (restarts on failure or exit), but if the container is explicitly stopped (e.g., \`docker stop\`), it will **not** restart automatically when the daemon/host restarts. This is generally preferred for maintenance.

- **Q: How do Docker Compose networks differ from Docker bridge networks?**
  - **A:** By default, Docker Compose creates a **user-defined bridge network** for the project (named \`project_default\`). This allows containers to communicate by service name (DNS resolution), which the default legacy \`bridge\` network does not support (it requires --link). Compose networks also provide better isolation.

- **Q: Can you reference Ansible Vault variables in the template?**
  - **A:** Yes. Since the template is processed by the Ansible \`template\` module (using Jinja2) **before** being deployed to the target, any variable available to the playbook (including Vault-encrypted vars in \`group_vars\`) can be injected. For example: \`password: {{ vault_db_password }}\` will render the decrypted value into the file.

### 2.4

```sh
ansible-playbook playbooks/deploy.yaml

PLAY [Deploy application] ************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
fatal: [ec2-54-146-54-202.compute-1.amazonaws.com]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: Connection timed out during banner exchange\r\nConnection to 54.146.54.202 port 22 timed out", "unreachable": true}

TASK [docker : Install required system packages] *************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Create directory for Docker GPG key] **********************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Add Docker's official GPG key] ****************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Add Docker repository] ************************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Install Docker packages] **********************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Install python3-docker] ***********************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Add users to docker group] ********************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-3-89-229-132.compute-1.amazonaws.com] => (item=ubuntu)

TASK [docker : Ensure Docker service is running and enabled] *************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Log in to Docker Hub] ************************************************************************************
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Pull Docker image] ***************************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Remove existing container] *******************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Run application container] *******************************************************************************
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Wait for application to be ready] ************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Verify health endpoint] **********************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

PLAY RECAP ***************************************************************************************************************
ec2-100-27-222-39.compute-1.amazonaws.com : ok=15   changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-3-89-229-132.compute-1.amazonaws.com : ok=15   changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-54-146-54-202.compute-1.amazonaws.com : ok=0    changed=0    unreachable=1    failed=0    skipped=0    rescued=0    ignored=0
```

### 2.7 Testing

```sh
$ ansible-playbook playbooks/deploy.yaml

PLAY [Deploy application] ************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Install required system packages] *************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Create directory for Docker GPG key] **********************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Add Docker's official GPG key] ****************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Add Docker repository] ************************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Install Docker packages] **********************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Install python3-docker] ***********************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Add users to docker group] ********************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-100-27-222-39.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-54-146-54-202.compute-1.amazonaws.com] => (item=ubuntu)

TASK [docker : Ensure Docker service is running and enabled] *************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Log in to Docker Hub] ************************************************************************************
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [web_app : Create app directory] ************************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Template docker-compose file] ****************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [web_app : Ensure legacy container is removed (migration)] **********************************************************
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [web_app : Deploy with docker-compose] ******************************************************************************
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [web_app : Wait for application to be ready] ************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Verify health endpoint] **********************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

PLAY RECAP ***************************************************************************************************************
ec2-100-27-222-39.compute-1.amazonaws.com : ok=16   changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-3-89-229-132.compute-1.amazonaws.com : ok=16   changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-54-146-54-202.compute-1.amazonaws.com : ok=16   changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Idempotency Check
`$ ansible-playbook playbooks/deploy.yaml && ansible-playbook playbooks/deploy.yaml`
Went successfully

Connection

```sh
ssh -i ../terraform/labsuser.pem -o IdentitiesOnl
y=yes ubuntu@3.89.229.132
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.17.0-1007-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Thu Mar  5 18:31:52 UTC 2026

  System load:  0.06               Temperature:           -273.1 C
  Usage of /:   66.6% of 14.46GB   Processes:             122
  Memory usage: 38%                Users logged in:       0
  Swap usage:   0%                 IPv4 address for ens5: 172.31.38.197


Expanded Security Maintenance for Applications is not enabled.

4 updates can be applied immediately.
1 of these updates is a standard security update.
To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


Last login: Thu Mar  5 18:29:38 2026 from 141.105.143.51
ubuntu@ip-172-31-38-197:~$ docker ps
CONTAINER ID   IMAGE                                   COMMAND           CREATED         STATUS         PORTS                                         NAMES
8732292affe1   projacktor/python-info-service:latest   "python app.py"   2 minutes ago   Up 2 minutes   0.0.0.0:5000->8080/tcp, [::]:5000->8080/tcp   python-info-service

docker compose -f /opt/python-info-service/compose.yaml ps
NAME                  IMAGE                                   COMMAND           SERVICE               CREATED         STATUS         PORTS
python-info-service   projacktor/python-info-service:latest   "python app.py"   python-info-service   3 minutes ago   Up 3 minutes   0.0.0.0:5000->8080/tcp, [::]:5000->8080/tcp
ubuntu@ip-172-31-38-197:~$ cat /opt/python-info-service/compose.yaml
services:
  python-info-service:
    image: projacktor/python-info-service:latest
    container_name: python-info-service
    ports:
      - "5000:8080"
    environment:
          restart: unless-stopped
```

## Task 3: Wiping

Test run w/o wipe

```sh
$ ansible-playbook playbooks/deploy.yaml

PLAY [Deploy application] ************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Install required system packages] *************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Create directory for Docker GPG key] **********************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Add Docker's official GPG key] ****************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [docker : Add Docker repository] ************************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Install Docker packages] **********************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Install python3-docker] ***********************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Add users to docker group] ********************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-54-146-54-202.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-100-27-222-39.compute-1.amazonaws.com] => (item=ubuntu)

TASK [docker : Ensure Docker service is running and enabled] *************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Include wipe tasks] **************************************************************************************
included: /home/projacktor/Projects/edu/DevOps-Core-Course/labs/ansible/roles/web_app/tasks/wipe.yaml for ec2-100-27-222-39.compute-1.amazonaws.com, ec2-54-146-54-202.compute-1.amazonaws.com, ec2-3-89-229-132.compute-1.amazonaws.com

TASK [web_app : Stop and remove containers (Compose down)] ***************************************************************
skipping: [ec2-100-27-222-39.compute-1.amazonaws.com]
skipping: [ec2-54-146-54-202.compute-1.amazonaws.com]
skipping: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Remove application directory] ****************************************************************************
skipping: [ec2-100-27-222-39.compute-1.amazonaws.com]
skipping: [ec2-54-146-54-202.compute-1.amazonaws.com]
skipping: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Remove Docker image (optional cleanup)] ******************************************************************
skipping: [ec2-100-27-222-39.compute-1.amazonaws.com]
skipping: [ec2-54-146-54-202.compute-1.amazonaws.com]
skipping: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Log wipe completion] *************************************************************************************
skipping: [ec2-100-27-222-39.compute-1.amazonaws.com]
skipping: [ec2-54-146-54-202.compute-1.amazonaws.com]
skipping: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Log in to Docker Hub] ************************************************************************************
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [web_app : Create app directory] ************************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Template docker-compose file] ****************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Ensure legacy container is removed (migration)] **********************************************************
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Deploy with docker-compose] ******************************************************************************
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Wait for application to be ready] ************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Verify health endpoint] **********************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

PLAY RECAP ***************************************************************************************************************
ec2-100-27-222-39.compute-1.amazonaws.com : ok=17   changed=3    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
ec2-3-89-229-132.compute-1.amazonaws.com : ok=17   changed=3    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
ec2-54-146-54-202.compute-1.amazonaws.com : ok=17   changed=3    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0

$ ssh -i ../terraform/labsuser.pem -o IdentitiesOnly=yes ubunt
u@3.89.229.132
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.17.0-1007-aws x86_64)
ubuntu@ip-172-31-38-197:~$ docker ps
CONTAINER ID   IMAGE                                   COMMAND           CREATED              STATUS              PORTS                                         NAMES
1d1eb57a418d   projacktor/python-info-service:latest   "python app.py"   About a minute ago   Up About a minute   0.0.0.0:5000->8080/tcp, [::]:5000->8080/tcp   python-info-service
ubuntu@ip-172-31-38-197:~$
logout
Connection to 3.89.229.132 closed.
```

With wipe

```sh
ansible-playbook playbooks/deploy.yaml \
                                                                    -e "web_app_wipe=true" \
                                                                    --tags web_app_wipe

PLAY [Deploy application] ************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Include wipe tasks] **************************************************************************************
included: /home/projacktor/Projects/edu/DevOps-Core-Course/labs/ansible/roles/web_app/tasks/wipe.yaml for ec2-100-27-222-39.compute-1.amazonaws.com, ec2-54-146-54-202.compute-1.amazonaws.com, ec2-3-89-229-132.compute-1.amazonaws.com

TASK [web_app : Stop and remove containers (Compose down)] ***************************************************************
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Remove application directory] ****************************************************************************
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Remove Docker image (optional cleanup)] ******************************************************************
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Log wipe completion] *************************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com] => {
    "msg": "Application python-info-service wiped successfully"
}
ok: [ec2-54-146-54-202.compute-1.amazonaws.com] => {
    "msg": "Application python-info-service wiped successfully"
}
ok: [ec2-3-89-229-132.compute-1.amazonaws.com] => {
    "msg": "Application python-info-service wiped successfully"
}

PLAY RECAP ***************************************************************************************************************
ec2-100-27-222-39.compute-1.amazonaws.com : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-3-89-229-132.compute-1.amazonaws.com : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-54-146-54-202.compute-1.amazonaws.com : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

$ ssh -i ../terraform/labsuser.pem -o IdentitiesOnly=yes ubunt
u@3.89.229.132 "docker ps"
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
$ ssh -i ../terraform/labsuser.pem -o IdentitiesOnly=yes ubunt
u@3.89.229.132 "ls /opt"
containerd
```

Only default `containerd` found, works

Clean installation

```sh
ansible-playbook playbooks/deploy.yaml \
                                                                    -e "web_app_wipe=true"

PLAY [Deploy application] ************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Install required system packages] *************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Create directory for Docker GPG key] **********************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Add Docker's official GPG key] ****************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [docker : Add Docker repository] ************************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Install Docker packages] **********************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Install python3-docker] ***********************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [docker : Add users to docker group] ********************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-3-89-229-132.compute-1.amazonaws.com] => (item=ubuntu)
ok: [ec2-100-27-222-39.compute-1.amazonaws.com] => (item=ubuntu)

TASK [docker : Ensure Docker service is running and enabled] *************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Include wipe tasks] **************************************************************************************
included: /home/projacktor/Projects/edu/DevOps-Core-Course/labs/ansible/roles/web_app/tasks/wipe.yaml for ec2-100-27-222-39.compute-1.amazonaws.com, ec2-54-146-54-202.compute-1.amazonaws.com, ec2-3-89-229-132.compute-1.amazonaws.com

TASK [web_app : Stop and remove containers (Compose down)] ***************************************************************
fatal: [ec2-54-146-54-202.compute-1.amazonaws.com]: FAILED! => {"changed": false, "msg": "\"/opt/python-info-service\" is not a directory"}
...ignoring
fatal: [ec2-100-27-222-39.compute-1.amazonaws.com]: FAILED! => {"changed": false, "msg": "\"/opt/python-info-service\" is not a directory"}
...ignoring
fatal: [ec2-3-89-229-132.compute-1.amazonaws.com]: FAILED! => {"changed": false, "msg": "\"/opt/python-info-service\" is not a directory"}
...ignoring

TASK [web_app : Remove application directory] ****************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [web_app : Remove Docker image (optional cleanup)] ******************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Log wipe completion] *************************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com] => {
    "msg": "Application python-info-service wiped successfully"
}
ok: [ec2-54-146-54-202.compute-1.amazonaws.com] => {
    "msg": "Application python-info-service wiped successfully"
}
ok: [ec2-3-89-229-132.compute-1.amazonaws.com] => {
    "msg": "Application python-info-service wiped successfully"
}

TASK [web_app : Log in to Docker Hub] ************************************************************************************
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [web_app : Create app directory] ************************************************************************************
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Template docker-compose file] ****************************************************************************
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [web_app : Ensure legacy container is removed (migration)] **********************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Deploy with docker-compose] ******************************************************************************
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Wait for application to be ready] ************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Verify health endpoint] **********************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

PLAY RECAP ***************************************************************************************************************
ec2-100-27-222-39.compute-1.amazonaws.com : ok=21   changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=1
ec2-3-89-229-132.compute-1.amazonaws.com : ok=21   changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=1
ec2-54-146-54-202.compute-1.amazonaws.com : ok=21   changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=1

(.venv) projacktor@projacktorLaptop ~/P/e/D/l/ansible (lab6)> ssh -i ../terraform/labsuser.pem -o IdentitiesOnly=yes ubunt
u@3.89.229.132 "docker ps"
CONTAINER ID   IMAGE                                   COMMAND           CREATED          STATUS          PORTS                                         NAMES
8d046daf0baa   projacktor/python-info-service:latest   "python app.py"   43 seconds ago   Up 42 seconds   0.0.0.0:5000->8080/tcp, [::]:5000->8080/tcp   python-info-service
```

Clean new web installed, works.

Safety check:

```sh
$ ansible-playbook playbooks/deploy.yaml --tags web_app_
wipe

PLAY [Deploy application] ************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Include wipe tasks] **************************************************************************************
included: /home/projacktor/Projects/edu/DevOps-Core-Course/labs/ansible/roles/web_app/tasks/wipe.yaml for ec2-100-27-222-39.compute-1.amazonaws.com, ec2-54-146-54-202.compute-1.amazonaws.com, ec2-3-89-229-132.compute-1.amazonaws.com

TASK [web_app : Stop and remove containers (Compose down)] ***************************************************************
skipping: [ec2-100-27-222-39.compute-1.amazonaws.com]
skipping: [ec2-54-146-54-202.compute-1.amazonaws.com]
skipping: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Remove application directory] ****************************************************************************
skipping: [ec2-100-27-222-39.compute-1.amazonaws.com]
skipping: [ec2-54-146-54-202.compute-1.amazonaws.com]
skipping: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Remove Docker image (optional cleanup)] ******************************************************************
skipping: [ec2-100-27-222-39.compute-1.amazonaws.com]
skipping: [ec2-54-146-54-202.compute-1.amazonaws.com]
skipping: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Log wipe completion] *************************************************************************************
skipping: [ec2-100-27-222-39.compute-1.amazonaws.com]
skipping: [ec2-54-146-54-202.compute-1.amazonaws.com]
skipping: [ec2-3-89-229-132.compute-1.amazonaws.com]

PLAY RECAP ***************************************************************************************************************
ec2-100-27-222-39.compute-1.amazonaws.com : ok=2    changed=0    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
ec2-3-89-229-132.compute-1.amazonaws.com : ok=2    changed=0    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
ec2-54-146-54-202.compute-1.amazonaws.com : ok=2    changed=0    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
```

Wipe tasks skipped, nice

```sh
ansible-playbook playbooks/deploy.yaml \
                                                                    -e "web_app_wipe=true" \
                                                                    --tags web_app_wipe

PLAY [Deploy application] ************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [ec2-54-146-54-202.compute-1.amazonaws.com]
ok: [ec2-100-27-222-39.compute-1.amazonaws.com]
ok: [ec2-3-89-229-132.compute-1.amazonaws.com]

TASK [web_app : Include wipe tasks] **************************************************************************************
included: /home/projacktor/Projects/edu/DevOps-Core-Course/labs/ansible/roles/web_app/tasks/wipe.yaml for ec2-100-27-222-39.compute-1.amazonaws.com, ec2-54-146-54-202.compute-1.amazonaws.com, ec2-3-89-229-132.compute-1.amazonaws.com

TASK [web_app : Stop and remove containers (Compose down)] ***************************************************************
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Remove application directory] ****************************************************************************
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]

TASK [web_app : Remove Docker image (optional cleanup)] ******************************************************************
changed: [ec2-3-89-229-132.compute-1.amazonaws.com]
changed: [ec2-100-27-222-39.compute-1.amazonaws.com]
changed: [ec2-54-146-54-202.compute-1.amazonaws.com]

TASK [web_app : Log wipe completion] *************************************************************************************
ok: [ec2-100-27-222-39.compute-1.amazonaws.com] => {
    "msg": "Application python-info-service wiped successfully"
}
ok: [ec2-54-146-54-202.compute-1.amazonaws.com] => {
    "msg": "Application python-info-service wiped successfully"
}
ok: [ec2-3-89-229-132.compute-1.amazonaws.com] => {
    "msg": "Application python-info-service wiped successfully"
}

PLAY RECAP ***************************************************************************************************************
ec2-100-27-222-39.compute-1.amazonaws.com : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-3-89-229-132.compute-1.amazonaws.com : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
ec2-54-146-54-202.compute-1.amazonaws.com : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Wipe done, all good.

### Research Questions

- **Q: Why use both variable AND tag? (Double safety mechanism)**
  - **A:** The dual-gate approach provides defense-in-depth:
    - **Variable condition** (`when: web_app_wipe | default(false) | bool`): Acts as the primary gatekeeper. Without explicitly setting `-e "web_app_wipe=true"`, wipe tasks never execute, even if tags are specified.
    - **Tag filter** (`--tags web_app_wipe`): Provides secondary filtering. If only the tag is used without the variable, wipe is still prevented by the `when` condition.
    - **Combined effect**: Both conditions must be satisfied for wipe to execute. This prevents accidental wipes from a single mistyped command. A user must consciously add both the variable AND the specific tag.

- **Q: What's the difference between `never` tag and this approach?**
  - **A:**
    - **`never` tag**: Tasks with `tags: never` never run unless explicitly included with `--tags never`. It's a hardcoded "always skip unless specifically requested" mechanism.
    - **Double-gate approach (variable + tag)**: Provides flexibility. Wipe tasks can run: (1) normally during full playbook runs if variable is set, or (2) only on-demand with the tag. The `never` tag forces you to always add it to the command, while our approach allows wipe during normal execution if the variable is true.
    - **This approach is better** because it enables clean reinstall scenarios where you want wipe → deploy in one playbook run without specifying tags (just use `-e "web_app_wipe=true"`).

- **Q: Why must wipe logic come BEFORE deployment in main.yml? (Clean reinstall scenario)**
  - **A:** The execution order enables the critical clean-install workflow:
    1. **Wipe Phase**: If `web_app_wipe=true`, containers/directories/images are removed first.
    2. **Deployment Phase**: Regardless of wipe outcome, deployment tasks run and install fresh.
    3. **Result**: A complete clean reinstall in a single playbook run.
    - If wipe came after deployment, you'd have the old deployment still running, then try to wipe it (order conflict).
    - This order naturally supports the use case: `ansible-playbook deploy.yaml -e "web_app_wipe=true"` = clean install.

- **Q: When would you want clean reinstallation vs. rolling update?**
  - **A:**
    - **Clean reinstallation** (`-e "web_app_wipe=true"`): Needed when:
      - Major version upgrade with incompatible configs
      - Database schema changes requiring reset
      - Testing from vanilla state
      - Decommissioning and redeploying
      - Debugging issues from a clean slate
    - **Rolling update** (normal run without wipe): Used when:
      - Patch/minor version updates (backward compatible)
      - Configuration tweaks without breaking changes
      - Regular deployments (idempotent updates)
      - Preserving application state/data between versions
    - **Choice**: Use the wipe variable to let operators decide on a per-deployment basis.

- **Q: How would you extend this to wipe Docker images and volumes too?**
  - **A:** The current implementation already removes images with `community.docker.docker_image` module. To extend further with volumes:

    ```yaml
    - name: Remove Docker volumes
      community.docker.docker_volume:
        name: "{{ web_app_container_name }}_data"
        state: absent
      ignore_errors: yes

    - name: Prune unused volumes
      community.docker.docker_volume_info:
        volumes: "{{ web_app_container_name }}"
      register: volumes
      ignore_errors: yes

    - name: List dangling volumes for manual inspection
      debug:
        msg: "Review volumes: docker volume ls -f dangling=true"
    ```

    - Note: Be cautious with volume removal—data loss is permanent.
    - Alternative: Keep volumes by default, add a separate wipe variable like `web_app_wipe_volumes` (more granular control).
    - Consider: Using named volumes in docker-compose.yml for explicit management vs. anonymous volumes.


## Task 4: CI/CD

Evidence:
- Ansible lint went well^
```sh

Run cd labs/ansible
  cd labs/ansible
  ansible-lint playbooks/*.yaml
  shell: /usr/bin/bash -e {0}
  env:
    pythonLocation: /opt/hostedtoolcache/Python/3.12.12/x64
    PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.12/x64/lib/pkgconfig
    Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.12/x64
    Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.12/x64
    Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.12/x64
    LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.12/x64/lib

Passed: 0 failure(s), 0 warning(s) in 13 files processed of 13 encountered. Last profile that met the validation criteria was 'production'.
```