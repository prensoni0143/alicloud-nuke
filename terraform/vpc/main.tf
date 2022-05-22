provider "random" {

}

provider "alicloud" {
  region = "cn-qingdao"
  alias  = "qd"
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

