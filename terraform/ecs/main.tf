terraform {
  required_providers {
    alicloud = {
      source  = "hashicorp/alicloud"
      version = "1.168.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.2.0"
    }
  }
}

provider "alicloud" {
  region = "us-east-1"
}

resource "random_string" "this" {
  length  = 8
  upper   = false
  special = false
}

module "vpc" {
  source  = "alibaba/vpc/alicloud"
  version = "v1.10.0"

  create   = true
  vpc_name = "vpc-nuke-us-east-01"
  vpc_cidr = "172.16.0.0/16"

  availability_zones = ["us-east-1a", "us-east-1b"]
  vswitch_cidrs      = ["172.16.0.0/18", "172.16.64.0/18"]

  vpc_tags = {
    Owner       = "nuker"
    Environment = "dev"
  }
}

resource "alicloud_security_group" "group" {
  name        = "tf_test_foo"
  description = "foo"
  vpc_id      = module.vpc.this_vpc_id
}

resource "alicloud_instance" "instance" {
  availability_zone          = "us-east-1a"
  security_groups            = alicloud_security_group.group.*.id
  instance_type              = "ecs.g6.large"
  system_disk_category       = "cloud_efficiency"
  system_disk_name           = "test_foo_system_disk_name"
  system_disk_description    = "test_foo_system_disk_description"
  image_id                   = "ubuntu_18_04_64_20G_alibase_20190624.vhd"
  instance_name              = "test_foo"
  vswitch_id                 = module.vpc.this_vswitch_ids[0]
  internet_max_bandwidth_out = 2
  data_disks {
    name        = "disk2-xagasr"
    size        = 20
    category    = "cloud_efficiency"
    description = "disk2-xagasr"
    encrypted   = true
  }
}

data "alicloud_ecs_disks" "ecs_data" {
  disk_name = "disk2-xagasr"
}

resource "alicloud_ecs_snapshot" "default" {
  category       = "standard"
  description    = "Test For Terraform"
  disk_id        = data.alicloud_ecs_disks.ecs_data.ids[0]
  retention_days = "20"
  snapshot_name  = "tf-test"
  tags = {
    Created = "TF"
    For     = "Acceptance-test"
  }
}

output "disk_name" {
  value = alicloud_instance.instance.data_disks[0].name
}

output "disk_id" {
  value = data.alicloud_ecs_disks.ecs_data.ids[0]
}