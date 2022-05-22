provider "random" {

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

  availability_zones = ["cn-zhangjiakou-a", "cn-zhangjiakou-b", "cn-zhangjiakou-c"]
  vswitch_cidrs      = ["172.17.0.0/19", "172.17.32.0/20", "172.17.48.0/20"]

  vpc_tags = {
    Owner       = "nuker"
    Environment = "dev"
  }
}

# output "rg_id" {
#   value = alicloud_resource_manager_resource_group.this
# }

output "vpc_id" {
  value = module.vpc_qd.this_vpc_id
}
