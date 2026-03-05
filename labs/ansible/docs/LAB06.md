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