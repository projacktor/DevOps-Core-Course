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

* **Q: What's the difference between \`restart: always\` and \`restart: unless-stopped\`?**
  * **A:** \`restart: always\` will restart the container indefinitely regardless of the exit code, even if it was manually stopped (it will restart on daemon restart). \`restart: unless-stopped\` behaves similarly (restarts on failure or exit), but if the container is explicitly stopped (e.g., \`docker stop\`), it will **not** restart automatically when the daemon/host restarts. This is generally preferred for maintenance.

* **Q: How do Docker Compose networks differ from Docker bridge networks?**
  * **A:** By default, Docker Compose creates a **user-defined bridge network** for the project (named \`project_default\`). This allows containers to communicate by service name (DNS resolution), which the default legacy \`bridge\` network does not support (it requires --link). Compose networks also provide better isolation.

* **Q: Can you reference Ansible Vault variables in the template?**
  * **A:** Yes. Since the template is processed by the Ansible \`template\` module (using Jinja2) **before** being deployed to the target, any variable available to the playbook (including Vault-encrypted vars in \`group_vars\`) can be injected. For example: \`password: {{ vault_db_password }}\` will render the decrypted value into the file.

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
```$ ansible-playbook playbooks/deploy.yaml && ansible-playbook playbooks/deploy.yaml```
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