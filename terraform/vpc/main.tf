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
  region = "cn-qingdao"
  alias  = "qd"
}

provider "alicloud" {
  region = "cn-zhangjiakou"
  alias  = "zjk"
}

resource "random_string" "rg" {
  length  = 8
  upper   = false
  special = false
}

resource "alicloud_resource_manager_resource_group" "this" {
  resource_group_name = "rg-${resource.random_string.rg.id}"
  display_name        = "rg-${resource.random_string.rg.id}"
}

module "vpc_qd" {
  source  = "alibaba/vpc/alicloud"
  version = "v1.10.0"

  providers = {
    alicloud = alicloud.qd
  }

  create            = true
  vpc_name          = "nuke-vpc-qd-01"
  vpc_cidr          = "172.16.0.0/16"
  resource_group_id = alicloud_resource_manager_resource_group.this.id

  availability_zones = ["cn-qingdao-b", "cn-qingdao-c"]
  vswitch_cidrs      = ["172.16.0.0/18", "172.16.64.0/18"]

  vpc_tags = {
    Owner       = "nuker"
    Environment = "dev"
  }
}

module "vpc_zjk" {
  source  = "alibaba/vpc/alicloud"
  version = "v1.10.0"

  providers = {
    alicloud = alicloud.zjk
  }

  create            = true
  vpc_name          = "nuke-vpc-zjk-01"
  vpc_cidr          = "172.17.0.0/16"
  resource_group_id = alicloud_resource_manager_resource_group.this.id

  availability_zones = ["cn-zhangjiakou-a", "cn-zhangjiakou-b", "cn-zhangjiakou-c", "cn-zhangjiakou-a", "cn-zhangjiakou-b", "cn-zhangjiakou-c", "cn-zhangjiakou-a", "cn-zhangjiakou-b", "cn-zhangjiakou-c", "cn-zhangjiakou-a", "cn-zhangjiakou-b", "cn-zhangjiakou-c", "cn-zhangjiakou-b", "cn-zhangjiakou-c"]
  vswitch_cidrs      = ["172.17.0.0/20", "172.17.16.0/20", "172.17.32.0/20", "172.17.48.0/20", "172.17.64.0/20", "172.17.80.0/20", "172.17.96.0/20", "172.17.112.0/20", "172.17.128.0/20", "172.17.144.0/20", "172.17.160.0/20", "172.17.176.0/20", "172.17.192.0/19", "172.17.224.0/19"]

  vpc_tags = {
    Owner       = "nuker"
    Environment = "dev"
  }
}

resource "alicloud_security_group" "group-zjk" {
  provider = alicloud.zjk
  name     = "sg-nuke-zjk-01"
  vpc_id   = module.vpc_zjk.this_vpc_id
}


resource "alicloud_security_group" "group-qd" {
  provider = alicloud.qd
  name     = "sg-nuke-qd-01"
  vpc_id   = module.vpc_qd.this_vpc_id
}

# output "rg_id" {
#   value = alicloud_resource_manager_resource_group.this
# }

output "vpc_id" {
  value = module.vpc_qd.this_vpc_id
}
