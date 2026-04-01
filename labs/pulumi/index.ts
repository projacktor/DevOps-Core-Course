import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const config = new pulumi.Config();
const instanceType = config.get("instanceType") || "t3.micro";
const keyName = config.get("keyName") || "vockey";
const volumeSize = config.getNumber("volumeSize") || 8;
const instanceName = config.get("instanceName") || "DevOps-Lab";

const amiId = "ami-0136735c2bb5cf5bf";

// Создаем провайдер с отключенными проверками, чтобы обойти ограничения учебной среды
const awsProvider = new aws.Provider("aws-provider", {
  region: "us-east-1",
  skipCredentialsValidation: true,
  skipRequestingAccountId: true,
  skipMetadataApiCheck: true,
  skipRegionValidation: true,
});

const group = new aws.ec2.SecurityGroup(
  "devops-firewall",
  {
    name: "devops-firewall",
    description: "Allow SSH, HTTP/S traffic",
    ingress: [
      {
        description: "ssh",
        fromPort: 22,
        toPort: 22,
        protocol: "tcp",
        cidrBlocks: ["0.0.0.0/0"],
      },
      {
        description: "http",
        fromPort: 80,
        toPort: 80,
        protocol: "tcp",
        cidrBlocks: ["0.0.0.0/0"],
      },
      {
        description: "https",
        fromPort: 443,
        toPort: 443,
        protocol: "tcp",
        cidrBlocks: ["0.0.0.0/0"],
      },
      {
        description: "deploy_port-1",
        fromPort: 5000,
        toPort: 5000,
        protocol: "tcp",
        cidrBlocks: ["0.0.0.0/0"],
      },
      {
        description: "deploy_port-2",
        fromPort: 5001,
        toPort: 5001,
        protocol: "tcp",
        cidrBlocks: ["0.0.0.0/0"],
      },
    ],
    egress: [
      { fromPort: 0, toPort: 0, protocol: "-1", cidrBlocks: ["0.0.0.0/0"] },
    ],
  },
  { provider: awsProvider },
);

const server = new aws.ec2.Instance(
  "devops-lab",
  {
    ami: amiId,
    instanceType: instanceType,
    keyName: keyName,
    vpcSecurityGroupIds: [group.id],

    rootBlockDevice: {
      volumeSize: volumeSize,
      volumeType: "gp3",
      deleteOnTermination: true,
    },

    tags: {
      Name: instanceName,
    },
  },
  { provider: awsProvider },
);

export const instancePublicIp = server.publicIp;
