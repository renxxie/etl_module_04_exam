variable "kafka_enabled" {
  type    = bool
  default = false
}

resource "yandex_mdb_kafka_cluster" "kafka-cluster" {
  count       = var.kafka_enabled ? 1 : 0
  name        = "etl-kafka-cluster"
  environment = "PRODUCTION"
  folder_id   = var.folder_id

  network_id = yandex_vpc_network.network.id

  kafka {
    resources {
      resource_preset_id = "s2.small"
      disk_type_id      = "network-ssd"
      disk_size         = 32
    }

    hosts = [
      { zone = "ru-central1-a", subnet_id = yandex_vpc_subnet.subnet-a.id },
      { zone = "ru-central1-b", subnet_id = yandex_vpc_subnet.subnet-a.id }
    ]

    kafka_config {
      compression_type = "GZIP"
      log_retention_hours = 72
    }
  }

  zones = ["ru-central1-a", "ru-central1-b"]
}

resource "yandex_mdb_kafka_topic" "loan-applications" {
  count    = var.kafka_enabled ? 1 : 0
  cluster_id   = yandex_mdb_kafka_cluster.kafka-cluster[0].id
  name         = "loan_applications"
  partitions   = 3
  replication_factor = 2

  topic_config {
    cleanup_policy = "DELETE"
    retention_ms   = 43200000
  }
}

output "kafka_cluster_id" {
  value = var.kafka_enabled ? yandex_mdb_kafka_cluster.kafka-cluster[0].id : null
}

output "kafka_brokers" {
  value = var.kafka_enabled ? yandex_mdb_kafka_cluster.kafka-cluster[0].hosts[0].name : null
}
