job "loki" {
  datacenters = ["dc1"]
  type = "service"

  group "loki-group" {
    count = 1

    task "loki" {
      driver = "docker"

      config {
        image = "grafana/loki:2.9.4"
        args = [
          "-config.file=/etc/loki/loki-config.yaml"
        ]
        volumes = [
          "local/loki:/etc/loki"
        ]
        ports = ["http"]
      }

      template {
        data = <<EOF
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 3m
  max_chunk_age: 1h

schema_config:
  configs:
    - from: 2024-01-01
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /tmp/loki/index
    cache_location: /tmp/loki/boltdb-cache
    shared_store: filesystem
  filesystem:
    directory: /tmp/loki/chunks

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: true
  retention_period: 336h
EOF
        destination = "local/loki/loki-config.yaml"
      }

      resources {
        cpu    = 300
        memory = 512
      }

      # service {
      #   name = "loki"
      #   port = "http"
      # }
    }

    network {
      port "http" {
        static = 3100
      }
    }

    volume "local" {
      type      = "host"
      read_only = false
      source    = "local"
    }
  }
}
