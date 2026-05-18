## Lab 04: IaC
> by Arsen Galiev CBS-01 B23


## Task 1 Terraform

I have chosen AWS since I have an edu account there from Secure System Development Course.

Things to be installed:

- `aws`, `aws cli`

```sh
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

- `terraform`

```sh
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

Terraform version

```sh
projacktor@projacktorLaptop ~/P/e/D/l/terraform (lab4)> terraform -v
Terraform v1.14.5
on linux_amd64
+ provider registry.terraform.io/hashicorp/aws v5.100.0
```

What do I've created:

- `t3.micro` instance of AWS EC2
- region `us-east-1`
- IP: `18.207.162.7`
  
SSH connection:
```sh
ssh -i ./labsuser.pem -o IdentitiesOnly=yes ubuntu@18.207.162.7
Welcome to Ubuntu 24.04.3 LTS (GNU/Linux 6.14.0-1018-aws x86_64)

<...>

ubuntu@ip-172-31-46-161:~$ 
```

Here terminal output of terraform execution:
```sh
terraform apply
data.aws_ami.ubuntu: Reading...
data.aws_ami.ubuntu: Read complete after 2s [id=ami-0136735c2bb5cf5bf]

Terraform used the selected providers to generate the following execution plan. Resource
actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_instance.devops-lab will be created
  + resource "aws_instance" "devops-lab" {
      + ami                                  = "ami-0136735c2bb5cf5bf"
      + arn                                  = (known after apply)
      + associate_public_ip_address          = (known after apply)
      + availability_zone                    = (known after apply)
      + cpu_core_count                       = (known after apply)
      + cpu_threads_per_core                 = (known after apply)
      + disable_api_stop                     = (known after apply)
      + disable_api_termination              = (known after apply)
      + ebs_optimized                        = (known after apply)
      + enable_primary_ipv6                  = (known after apply)
      + get_password_data                    = false
      + host_id                              = (known after apply)
      + host_resource_group_arn              = (known after apply)
      + iam_instance_profile                 = (known after apply)
      + id                                   = (known after apply)
      + instance_initiated_shutdown_behavior = (known after apply)
      + instance_lifecycle                   = (known after apply)
      + instance_state                       = (known after apply)
      + instance_type                        = "t3.micro"
      + ipv6_address_count                   = (known after apply)
      + ipv6_addresses                       = (known after apply)
      + key_name                             = "vockey"
      + monitoring                           = (known after apply)
      + outpost_arn                          = (known after apply)
      + password_data                        = (known after apply)
      + placement_group                      = (known after apply)
      + placement_partition_number           = (known after apply)
      + primary_network_interface_id         = (known after apply)
      + private_dns                          = (known after apply)
      + private_ip                           = (known after apply)
      + public_dns                           = (known after apply)
      + public_ip                            = (known after apply)
      + secondary_private_ips                = (known after apply)
      + security_groups                      = (known after apply)
      + source_dest_check                    = true
      + spot_instance_request_id             = (known after apply)
      + subnet_id                            = (known after apply)
      + tags                                 = {
          + "Name" = "DevOps-Lab"
        }
      + tags_all                             = {
          + "Name" = "DevOps-Lab"
        }
      + tenancy                              = (known after apply)
      + user_data                            = (known after apply)
      + user_data_base64                     = (known after apply)
      + user_data_replace_on_change          = false
      + vpc_security_group_ids               = (known after apply)

      + capacity_reservation_specification (known after apply)

      + cpu_options (known after apply)

      + ebs_block_device (known after apply)

      + enclave_options (known after apply)

      + ephemeral_block_device (known after apply)

      + instance_market_options (known after apply)

      + maintenance_options (known after apply)

      + metadata_options (known after apply)

      + network_interface (known after apply)

      + private_dns_name_options (known after apply)

      + root_block_device {
          + delete_on_termination = true
          + device_name           = (known after apply)
          + encrypted             = (known after apply)
          + iops                  = (known after apply)
          + kms_key_id            = (known after apply)
          + tags_all              = (known after apply)
          + throughput            = (known after apply)
          + volume_id             = (known after apply)
          + volume_size           = 16
          + volume_type           = "gp3"
        }
    }

  # aws_security_group.devops-firewall will be created
  + resource "aws_security_group" "devops-firewall" {
      + arn                    = (known after apply)
      + description            = "Allow SSH, HTTP/S traffic"
      + egress                 = [
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + from_port        = 0
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "-1"
              + security_groups  = []
              + self             = false
              + to_port          = 0
                # (1 unchanged attribute hidden)
            },
        ]
      + id                     = (known after apply)
      + ingress                = [
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + description      = "deploy_port-1"
              + from_port        = 5000
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 5000
            },
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + description      = "deploy_port-2"
              + from_port        = 5001
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 5001
            },
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + description      = "http"
              + from_port        = 80
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 80
            },
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + description      = "https"
              + from_port        = 443
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 443
            },
          + {
              + cidr_blocks      = [
                  + "0.0.0.0/0",
                ]
              + description      = "ssh"
              + from_port        = 22
              + ipv6_cidr_blocks = []
              + prefix_list_ids  = []
              + protocol         = "tcp"
              + security_groups  = []
              + self             = false
              + to_port          = 22
            },
        ]
      + name                   = "devops-firewall"
      + name_prefix            = (known after apply)
      + owner_id               = (known after apply)
      + revoke_rules_on_delete = false
      + tags_all               = (known after apply)
      + vpc_id                 = (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + instance_public_ip = (known after apply)

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

aws_security_group.devops-firewall: Creating...
aws_security_group.devops-firewall: Creation complete after 9s [id=sg-032a78a13d3392720]
aws_instance.devops-lab: Creating...
aws_instance.devops-lab: Still creating... [00m10s elapsed]
aws_instance.devops-lab: Creation complete after 16s [id=i-03e3abf8e8340e97b]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

instance_public_ip = "18.207.162.7"

 terraform plan
data.aws_ami.ubuntu: Reading...
aws_security_group.devops-firewall: Refreshing state... [id=sg-032a78a13d3392720]
data.aws_ami.ubuntu: Read complete after 2s [id=ami-0136735c2bb5cf5bf]
aws_instance.devops-lab: Refreshing state... [id=i-03e3abf8e8340e97b]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no
differences, so no changes are needed.
```

## Task 2 Pulumni

Terraform destroy:

```sh
terraform destroy
data.aws_ami.ubuntu: Reading...
aws_security_group.devops-firewall: Refreshing state... [id=sg-032a78a13d3392720]
data.aws_ami.ubuntu: Read complete after 2s [id=ami-0136735c2bb5cf5bf]
aws_instance.devops-lab: Refreshing state... [id=i-03e3abf8e8340e97b]

Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # aws_instance.devops-lab will be destroyed
  - resource "aws_instance" "devops-lab" {
      - ami                                  = "ami-0136735c2bb5cf5bf" -> null
      - arn                                  = "arn:aws:ec2:us-east-1:777556071455:instance/i-03e3abf8e8340e97b" -> null
      - associate_public_ip_address          = true -> null
      - availability_zone                    = "us-east-1d" -> null
      - cpu_core_count                       = 1 -> null
      - cpu_threads_per_core                 = 2 -> null
      - disable_api_stop                     = false -> null
      - disable_api_termination              = false -> null
      - ebs_optimized                        = false -> null
      - get_password_data                    = false -> null
      - hibernation                          = false -> null
      - id                                   = "i-03e3abf8e8340e97b" -> null
      - instance_initiated_shutdown_behavior = "stop" -> null
      - instance_state                       = "running" -> null
      - instance_type                        = "t3.micro" -> null
      - ipv6_address_count                   = 0 -> null
      - ipv6_addresses                       = [] -> null
      - key_name                             = "vockey" -> null
      - monitoring                           = false -> null
      - placement_partition_number           = 0 -> null
      - primary_network_interface_id         = "eni-04289a7c0ad2730ab" -> null
      - private_dns                          = "ip-172-31-46-161.ec2.internal" -> null
      - private_ip                           = "172.31.46.161" -> null
      - public_dns                           = "ec2-18-207-162-7.compute-1.amazonaws.com" -> null
      - public_ip                            = "18.207.162.7" -> null
      - secondary_private_ips                = [] -> null
      - security_groups                      = [
          - "devops-firewall",
        ] -> null
      - source_dest_check                    = true -> null
      - subnet_id                            = "subnet-067bbf4630181b6cb" -> null
      - tags                                 = {
          - "Name" = "DevOps-Lab"
        } -> null
      - tags_all                             = {
          - "Name" = "DevOps-Lab"
        } -> null
      - tenancy                              = "default" -> null
      - user_data_replace_on_change          = false -> null
      - vpc_security_group_ids               = [
          - "sg-032a78a13d3392720",
        ] -> null
        # (7 unchanged attributes hidden)

      - capacity_reservation_specification {
          - capacity_reservation_preference = "open" -> null
        }

      - cpu_options {
          - core_count       = 1 -> null
          - threads_per_core = 2 -> null
            # (1 unchanged attribute hidden)
        }

      - credit_specification {
          - cpu_credits = "unlimited" -> null
        }

      - enclave_options {
          - enabled = false -> null
        }

      - maintenance_options {
          - auto_recovery = "default" -> null
        }

      - metadata_options {
          - http_endpoint               = "enabled" -> null
          - http_protocol_ipv6          = "disabled" -> null
          - http_put_response_hop_limit = 2 -> null
          - http_tokens                 = "required" -> null
          - instance_metadata_tags      = "disabled" -> null
        }

      - private_dns_name_options {
          - enable_resource_name_dns_a_record    = false -> null
          - enable_resource_name_dns_aaaa_record = false -> null
          - hostname_type                        = "ip-name" -> null
        }

      - root_block_device {
          - delete_on_termination = true -> null
          - device_name           = "/dev/sda1" -> null
          - encrypted             = false -> null
          - iops                  = 3000 -> null
          - tags                  = {} -> null
          - tags_all              = {} -> null
          - throughput            = 125 -> null
          - volume_id             = "vol-0bfe84df20ace40a7" -> null
          - volume_size           = 16 -> null
          - volume_type           = "gp3" -> null
            # (1 unchanged attribute hidden)
        }
    }

  # aws_security_group.devops-firewall will be destroyed
  - resource "aws_security_group" "devops-firewall" {
      - arn                    = "arn:aws:ec2:us-east-1:777556071455:security-group/sg-032a78a13d3392720" -> null
      - description            = "Allow SSH, HTTP/S traffic" -> null
      - egress                 = [
          - {
              - cidr_blocks      = [
                  - "0.0.0.0/0",
                ]
              - from_port        = 0
              - ipv6_cidr_blocks = []
              - prefix_list_ids  = []
              - protocol         = "-1"
              - security_groups  = []
              - self             = false
              - to_port          = 0
                # (1 unchanged attribute hidden)
            },
        ] -> null
      - id                     = "sg-032a78a13d3392720" -> null
      - ingress                = [
          - {
              - cidr_blocks      = [
                  - "0.0.0.0/0",
                ]
              - description      = "deploy_port-1"
              - from_port        = 5000
              - ipv6_cidr_blocks = []
              - prefix_list_ids  = []
              - protocol         = "tcp"
              - security_groups  = []
              - self             = false
              - to_port          = 5000
            },
          - {
              - cidr_blocks      = [
                  - "0.0.0.0/0",
                ]
              - description      = "deploy_port-2"
              - from_port        = 5001
              - ipv6_cidr_blocks = []
              - prefix_list_ids  = []
              - protocol         = "tcp"
              - security_groups  = []
              - self             = false
              - to_port          = 5001
            },
          - {
              - cidr_blocks      = [
                  - "0.0.0.0/0",
                ]
              - description      = "http"
              - from_port        = 80
              - ipv6_cidr_blocks = []
              - prefix_list_ids  = []
              - protocol         = "tcp"
              - security_groups  = []
              - self             = false
              - to_port          = 80
            },
          - {
              - cidr_blocks      = [
                  - "0.0.0.0/0",
                ]
              - description      = "https"
              - from_port        = 443
              - ipv6_cidr_blocks = []
              - prefix_list_ids  = []
              - protocol         = "tcp"
              - security_groups  = []
              - self             = false
              - to_port          = 443
            },
          - {
              - cidr_blocks      = [
                  - "0.0.0.0/0",
                ]
              - description      = "ssh"
              - from_port        = 22
              - ipv6_cidr_blocks = []
              - prefix_list_ids  = []
              - protocol         = "tcp"
              - security_groups  = []
              - self             = false
              - to_port          = 22
            },
        ] -> null
      - name                   = "devops-firewall" -> null
      - owner_id               = "777556071455" -> null
      - revoke_rules_on_delete = false -> null
      - tags                   = {} -> null
      - tags_all               = {} -> null
      - vpc_id                 = "vpc-0101278bad9d21a53" -> null
        # (1 unchanged attribute hidden)
    }

Plan: 0 to add, 0 to change, 2 to destroy.

Changes to Outputs:
  - instance_public_ip = "18.207.162.7" -> null

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

aws_instance.devops-lab: Destroying... [id=i-03e3abf8e8340e97b]
aws_instance.devops-lab: Still destroying... [id=i-03e3abf8e8340e97b, 00m10s elapsed]
aws_instance.devops-lab: Still destroying... [id=i-03e3abf8e8340e97b, 00m20s elapsed]
aws_instance.devops-lab: Still destroying... [id=i-03e3abf8e8340e97b, 00m30s elapsed]
aws_instance.devops-lab: Still destroying... [id=i-03e3abf8e8340e97b, 00m40s elapsed]
aws_instance.devops-lab: Still destroying... [id=i-03e3abf8e8340e97b, 00m50s elapsed]
aws_instance.devops-lab: Still destroying... [id=i-03e3abf8e8340e97b, 01m00s elapsed]
aws_instance.devops-lab: Still destroying... [id=i-03e3abf8e8340e97b, 01m10s elapsed]
aws_instance.devops-lab: Destruction complete after 1m14s
aws_security_group.devops-firewall: Destroying... [id=sg-032a78a13d3392720]
aws_security_group.devops-firewall: Destruction complete after 2s

Destroy complete! Resources: 2 destroyed.
```

Pulumni installation

```sh
curl -fsSL https://get.pulumi.com | sh
fish_add_path ~/.pulumi/bin
pulumi version
v3.221.0
```

[Pulumi getting started guide](https://www.pulumi.com/docs/iac/get-started/aws/create-project/)

Deployment (after some troubleshooting)

```sh
projacktor@projacktorLaptop ~/P/e/D/l/pulumi (lab4) [SIGINT]> pulumi preview
Previewing update (projacktor/dev)

View in Browser (Ctrl+O): https://app.pulumi.com/projacktor/devops-lab/dev/previews/88b6308a-a62d-4a90-97ec-a0e60443e845

     Type                 Name            Plan        Info
     pulumi:pulumi:Stack  devops-lab-dev              
 +-  └─ aws:ec2:Instance  devops-lab      replace     [diff: ~ami,rootBlockDevice

Resources:
    +-1 to replace
    3 unchanged

projacktor@projacktorLaptop ~/P/e/D/l/pulumi (lab4)> pulumi up
Previewing update (projacktor/dev)

View in Browser (Ctrl+O): https://app.pulumi.com/projacktor/devops-lab/dev/previews/96a545b7-ab69-45d3-8eb6-5474fb388874

     Type                 Name            Plan        Info
     pulumi:pulumi:Stack  devops-lab-dev              
 +-  └─ aws:ec2:Instance  devops-lab      replace     [diff: ~ami,rootBlockDevice

Resources:
    +-1 to replace
    3 unchanged

Do you want to perform this update? yes
Updating (projacktor/dev)

View in Browser (Ctrl+O): https://app.pulumi.com/projacktor/devops-lab/dev/updates/4

     Type                 Name            Status             Info
     pulumi:pulumi:Stack  devops-lab-dev                     
 +-  └─ aws:ec2:Instance  devops-lab      replaced (35s)     [diff: ~ami,rootBloc

Outputs:
  ~ instancePublicIp: "107.20.95.190" => "23.20.145.103"

Resources:
    +-1 replaced
    3 unchanged

Duration: 1m0s

projacktor@projacktorLaptop ~/P/e/D/l/pulumi (lab4)> ssh -i ../terraform/labsuser.
pem -o IdentitiesOnly=yes ubuntu@23.20.145.103
The authenticity of host '23.20.145.103 (23.20.145.103)' can't be established.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '23.20.145.103' (ED25519) to the list of known hosts.
Welcome to Ubuntu 24.04.3 LTS (GNU/Linux 6.14.0-1018-aws x86_64)

<...>

ubuntu@ip-172-31-39-55:~$ 
```

I created the same instance with Pulumi but of course got new IP.

### Comparison

IMO, using Terraform is easier by several reasons:

- declarative style requires less code written
- variables managment more intuitive and almost the same as `.env` maintaince
- it works much faster

However Pulumi has also its pros:
- No need to know HCL language, more harmonic in projects with popular PL.
- Has good troubleshooting support on its site (with AI assistant), well-written documentation

I would prefer terraform because of its speed of deploying and managment if I'd be DevOps in a team. If I'd be a DevOps and coder at the same time, maybe pulumi suites better since switching from one language to another is hard.