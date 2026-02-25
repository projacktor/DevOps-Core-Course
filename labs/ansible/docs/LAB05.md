# Lab 5

> by Arsen Galiev B23 CBS-01

## Task 1: Ansible Setup & Role Structure

### 1.1 & 1.2 Structure and Installation

We set up a role-based Ansible project structure to ensure modularity and reusability. The project is organized as follows:

```
ansible/
├── inventory/
│   └── hosts.ini              # Static inventory
├── roles/
│   ├── common/                # System basics (packages, timezone)
├── ansible.cfg                # Main configuration
└── docs/                      # Documentation
```

### 1.3 Inventory Configuration

We configured a static inventory in `inventory/hosts.ini` pointing to our cloud VM. We used specific SSH parameters to handle key authentication correctly:

```ini
[webservers]
ubuntu ansible_host=52.87.175.129 ansible_user=ubuntu ansible_ssh_private_key_file=/home/projacktor/Projects/edu/DevOps-Core-Course/labs/terraform/labsuser.pem ansible_ssh_common_args='-o IdentitiesOnly=yes'
```

### 1.4 Ansible Configuration

We created `ansible.cfg` with secure defaults, including `host_key_checking = True` to prevent MITM attacks, and privilege escalation enabled by default for tasks requiring sudo.

### 1.5 Connectivity Test

We verified connectivity to the target VM using the `ping` module and ran a raw command to check the kernel version.

**Output:**

```sh
ansible all -m ping
ubuntu | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

```sh
ansible webservers -a "uname -a"
ubuntu | CHANGED | rc=0 >>
Linux ip-172-31-20-49 6.17.0-1007-aws #7~24.04.1-Ubuntu SMP Thu Jan 22 21:04:49 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
```

---

## Task 2: System Provisioning Roles

### 2.1 Common Role

We created the `common` role to handle basic system setup tasks. This role ensures that the package cache is updated, essential tools are installed, and the timezone is set.

**Role Structure:**

- `defaults/main.yaml`: Defines variables for packages and timezone.
- `tasks/main.yaml`: Implements the logic using `apt` and `timezone` modules.

#### Implementation Decisions & Q&A

**1. What does `cache_valid_time` do?**
In our task `Update apt cache`, we used `cache_valid_time: 3600`.
This parameter tells Ansible to update the apt cache **only if** the cache is older than the specified time (in seconds). In our case, 3600 seconds (1 hour).

- **Why?** It speeds up repeated playbook runs significantly. Without it, every run would trigger `apt-get update`, which is slow and unnecessary if done frequently.

**2. How do you define a list of packages in defaults?**
We defined the list in `roles/common/defaults/main.yaml` using standard YAML list syntax:

```yaml
common_packages:
  - python3-pip
  - curl
  - git
  - vim
  - htop
```

In the task, we referenced this variable specifically: `name: "{{ common_packages }}"`. This allows future users of the role to override the list (e.g., add or remove tools) without modifying the task code itself.

**3. Should you use `state: present` or `state: latest`?**
We chose **`state: present`**.

- **`state: present`**: Ensures the package is installed. If it's already there (even an older version), Ansible does nothing. This is **safer** for production because it prevents unexpected upgrades that might break applications.
- **`state: latest`**: Always updates the package to the newest version available. This can be dangerous as it might introduce breaking changes uncontrollably.

### 2.2 Docker Role

We created the `docker` role to handle the installation and configuration of the Docker engine.

**Role Structure:**

- `defaults/main.yaml`: Defines variables for Docker packages (`docker-ce`, `docker-ce-cli`, etc.) and the user to be added to the docker group.
- `handlers/main.yaml`: Contains the `restart docker` handler.
- `tasks/main.yaml`: Implements the installation steps: adding GPG key, repository, installing packages, and starting the service.

#### Implementation Details

We followed the official Docker installation guide but translated it into Ansible tasks:

1.  **GPG Key**: Downloaded using `get_url` to `/etc/apt/keyrings`.
2.  **Repository**: Added using `apt_repository`. We used Ansible facts to dynamically determine the architecture (`amd64`) and OS release (`noble` for Ubuntu 24.04), making the role adaptable.
3.  **Service**: We use the `service` module to ensure Docker is running and enabled on boot.
4.  **User Group**: The `user` module adds `ubuntu` to the `docker` group, allowing non-root container management.

---

### 2.3 & 2.4 Provisioning Playbook & Idempotency

We created `playbooks/provision.yml` to apply both `common` and `docker` roles to our `webservers`.

```yaml
---
- name: Provision web servers
  hosts: webservers
  become: yes

  roles:
    - common
    - docker
```

#### Idempotency Demonstration

We executed the playbook twice to demonstrate Ansible's idempotency.

**First Run Output:**

```sh
ansible-playbook playbooks/provision.yaml

PLAY [Provision web servers] *************************************************************************

TASK [Gathering Facts] *******************************************************************************
ok: [ubuntu]

TASK [common : Update apt cache] *********************************************************************
ok: [ubuntu]

TASK [common : Install essential packages] ***********************************************************
ok: [ubuntu]

TASK [common : Set timezone] *************************************************************************
changed: [ubuntu]

TASK [docker : Install required system packages] *****************************************************
ok: [ubuntu]

TASK [docker : Create directory for Docker GPG key] **************************************************
ok: [ubuntu]

TASK [docker : Add Docker's official GPG key] ********************************************************
changed: [ubuntu]

TASK [docker : Add Docker repository] ****************************************************************
changed: [ubuntu]

TASK [docker : Install Docker packages] **************************************************************
changed: [ubuntu]

TASK [docker : Install python3-docker] ***************************************************************
changed: [ubuntu]

TASK [docker : Ensure Docker service is running and enabled] *****************************************
ok: [ubuntu]

TASK [docker : Add users to docker group] ************************************************************
changed: [ubuntu] => (item=ubuntu)

RUNNING HANDLER [docker : restart docker] ************************************************************
changed: [ubuntu]

PLAY RECAP *******************************************************************************************
ubuntu                     : ok=13   changed=7    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

**Second Run Output:**

```sh
ansible-playbook playbooks/provision.yaml

PLAY [Provision web servers] *************************************************************************

TASK [Gathering Facts] *******************************************************************************
ok: [ubuntu]

TASK [common : Update apt cache] *********************************************************************
ok: [ubuntu]

TASK [common : Install essential packages] ***********************************************************
ok: [ubuntu]

TASK [common : Set timezone] *************************************************************************
ok: [ubuntu]

TASK [docker : Install required system packages] *****************************************************
ok: [ubuntu]

TASK [docker : Create directory for Docker GPG key] **************************************************
ok: [ubuntu]

TASK [docker : Add Docker's official GPG key] ********************************************************
ok: [ubuntu]

TASK [docker : Add Docker repository] ****************************************************************
ok: [ubuntu]

TASK [docker : Install Docker packages] **************************************************************
ok: [ubuntu]

TASK [docker : Install python3-docker] ***************************************************************
ok: [ubuntu]

TASK [docker : Ensure Docker service is running and enabled] *****************************************
ok: [ubuntu]

TASK [docker : Add users to docker group] ************************************************************
ok: [ubuntu] => (item=ubuntu)

PLAY RECAP *******************************************************************************************
ubuntu                     : ok=12   changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

#### Analysis

**First Run Analysis:**

- **Changed Tasks**: `Set timezone`, `Add Docker's official GPG key`, `Add Docker repository`, `Install Docker packages`, `Install python3-docker`, `Add users to docker group`.
- **Why**: This was a fresh installation. Ansible detected that these configurations or packages were missing on the target system and applied them to reach the desired state.
- **Handler**: The `restart docker` handler ran because the installation tasks notified it.

**Second Run Analysis:**

- **Changed Tasks**: None (`changed=0`).
- **Why**: Ansible checked the state of every resource. It found that the timezone was correct, packages were already installed, the GPG key existed, and the user was already in the group. Since the **actual state** matched the **desired state**, no actions were performed.

**Conclusion:** This demonstrates **idempotency**. We can run this playbook 100 times, and it will not break the system or duplicate configurations; it ensures the system stays in the defined valid state.
