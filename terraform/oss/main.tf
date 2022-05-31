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
  alias  = "us-east-1"
}

provider "alicloud" {
  region = "cn-qingdao"
  alias  = "cn-qingdao"
}

resource "random_string" "this" {
  length  = 8
  upper   = false
  special = false
}


resource "alicloud_oss_bucket" "bucket-us-east-1" {
  bucket = "bucket-us-east-${resource.random_string.this.id}"
  acl    = "private"

  provider = alicloud.us-east-1

  server_side_encryption_rule {
    sse_algorithm = "AES256"
  }
}

resource "alicloud_oss_bucket" "bucket-cn-qingdao" {
  bucket = "bucket-cn-qingdao-${resource.random_string.this.id}"
  acl    = "private"

  provider = alicloud.cn-qingdao

  server_side_encryption_rule {
    sse_algorithm = "AES256"
  }
}


output "bucket-us-east-1" {
  value = alicloud_oss_bucket.bucket-us-east-1.id
}

output "bucket-cn-qingdao" {
  value = alicloud_oss_bucket.bucket-cn-qingdao.id
}
