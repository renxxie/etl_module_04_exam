terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

variable "yc_token" { type = string }
variable "cloud_id" { type = string }
variable "folder_id" { type = string }

provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = "ru-central1-a"
}

locals {
  folder_id   = var.folder_id
  bucket_name = "dvlgerasimenko-etl-bucket"

  source_endpoint_id = ""
  target_endpoint_id = ""
  transfer_enabled   = 0

  network_name        = "network"
  subnet_name         = "subnet-a"
  security_group_name = "security-group"
  ydb_database_name   = "ydb-database"
  sa_name             = "sa-for-transfer"
  transfer_name       = "ydb-to-object-storage-transfer"
}

resource "yandex_vpc_network" "network" {
  name        = local.network_name
}

resource "yandex_vpc_subnet" "subnet-a" {
  name           = local.subnet_name
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["10.1.0.0/16"]
}

resource "yandex_vpc_security_group" "security-group" {
  name        = local.security_group_name
  network_id  = yandex_vpc_network.network.id

  ingress {
    protocol       = "TCP"
    port           = 2135
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol       = "ANY"
    v4_cidr_blocks = ["0.0.0.0/0"]
    from_port      = 0
    to_port        = 65535
  }
}

resource "yandex_iam_service_account" "sa-for-transfer" {
  folder_id   = local.folder_id
  name        = local.sa_name
}

resource "yandex_ydb_database_serverless" "ydb-database" {
  name        = local.ydb_database_name
  location_id = "ru-central1"
}

resource "yandex_resourcemanager_folder_iam_member" "storage-editor" {
  folder_id = local.folder_id
  role      = "storage.editor"
  member    = "serviceAccount:${yandex_iam_service_account.sa-for-transfer.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "ydb-editor" {
  folder_id = local.folder_id
  role      = "ydb.editor"
  member    = "serviceAccount:${yandex_iam_service_account.sa-for-transfer.id}"
}

resource "yandex_iam_service_account_static_access_key" "sa-static-key" {
  service_account_id = yandex_iam_service_account.sa-for-transfer.id
}

resource "yandex_storage_bucket" "obj-storage-bucket" {
  access_key = yandex_iam_service_account_static_access_key.sa-static-key.access_key
  secret_key = yandex_iam_service_account_static_access_key.sa-static-key.secret_key
  bucket     = local.bucket_name
}

resource "yandex_datatransfer_transfer" "ydb-to-object-storage-transfer" {
  count       = local.transfer_enabled
  name        = local.transfer_name
  source_id   = local.source_endpoint_id
  target_id   = local.target_endpoint_id
  type        = "SNAPSHOT_ONLY"
}
