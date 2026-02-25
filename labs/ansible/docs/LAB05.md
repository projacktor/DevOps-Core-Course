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
