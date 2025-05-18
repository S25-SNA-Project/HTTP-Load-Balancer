job "backend" {
  datacenters = ["dc1"]
  type = "service"

  group "backend-group" {
    count = 3

    constraint {
      attribute = "${meta.role}"
      operator = "="
      value = "backend"
    }

    task "backend" {
      driver = "docker"

      config {
        image = "wkwtfigo/backend-service:latest"
        ports = ["http"]
        volumes = [
          "/var/log/app-redirect-balancer:/app/.logs"
        ]
      }

      resources {
        cpu    = 500
        memory = 256
      }

      # service {
      #   name = "backend"
      #   port = "http"
      #   tags = ["backend"]
      # }
    }

    network {
      port "http" {
        static = 8080
      }
    }
  }
}
