job "promtail" {
  datacenters = ["dc1"]
  type = "system"

  group "promtail-group" {
    task "promtail" {
      driver = "docker"

      config {
        image = "grafana/promtail:2.9.4"
        args  = ["-config.file=/etc/promtail/promtail.yaml"]
        volumes = [
          "/var/log:/var/log",
          "alloc/promtail:/etc/promtail"
        ]
      }

      template {
        data = <<EOF
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki.service.consul:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*.log
EOF
        destination = "local/promtail/promtail.yaml"
      }

      resources {
        cpu    = 200
        memory = 256
      }
    }
  }
}
